#!/usr/bin/env python3
"""verify_flow.py — pemeriksa deterministik gerbang metode moneyflow v2.0 (Flow Money First).

Pustaka bawaan Python 3 saja (argparse, json, pathlib, re, sys) — tanpa dependensi eksternal.
Kode keluar: 0 = LULUS, 1 = GAGAL (daftar pelanggaran dicetak ke stdout/stderr).

Sub-perintah:
  check-staging <file> [--repo DIR]   staging subagent sebelum merge ke berkas kanonik
  check-b <audit_dir> [--repo DIR]    artefak Tahap B (B01..B07 + sensus statis JSONL)
  check-c <file> [--repo DIR]         inventaris Tahap C (C00 atau per-Stream)
  check-d <audit_dir> --stream ID [--repo DIR]   gelombang + kartu lead per Stream
  check-e <file> [--repo DIR]         berkas bukti batch Tahap E
  check-final <audit_dir> [--repo DIR]  gerbang penutupan proyek
"""

import argparse
import json
import re
from pathlib import Path
from sys import exit as sysexit

# ---------------------------------------------------------------------------
# 1. Deteksi token kompresi malas
# ---------------------------------------------------------------------------

# Pola berjaga-jaga (di luar pola spesifikasi; dipakai oleh check-staging): variasi
# singular/plural "and so on" / "rest of". Sub-perintah lain memakai pola atas.
_TOKEN_LAZY_WIDE = re.compile(
    r"(\.\.\.)|(…)|(\bdll\.?\b)|(\bdst\.?\b)|(\bdsb\.?\b)|(\betc\.?\b)"
    r"|(\band so on\b)|(\brest of logic\b)|(\brest of code\b)|(\brest of the\b)",
    re.IGNORECASE,
)

# Pola spesifikasi tepat untuk check-c / check-d / check-e / check-final
# (case-insensitive; match utuh kata / simbol):
#   ... , … , dll. / dll , dst. / dst , dsb. / dsb , etc. / etc ,
#   "and so on", "rest of logic", "rest of code"
# dengan abaikan URL http:// / https:// dan hash heksadesimal panjang (>=32) tanpa elipsis.
_TOKEN_LAZY_SPEC = re.compile(
    r"(\.{3,}|…|\bdll\.?\b|\bdst\.?\b|\bdsb\.?\b|\betc\.?\b|\band so on\b|\brest of logic\b|\brest of code\b)",
    re.IGNORECASE,
)

_URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
_LONG_HEX_RE = re.compile(r"\b[0-9a-fA-F]{32,}\b")


def _strip_ignorable(text):
    """Hapus URL dan hash panjang sebelum pencocokan token malas."""
    text = _URL_RE.sub(" ", text)
    text = _LONG_HEX_RE.sub(" ", text)
    return text


def scan_lazy_tokens(text):
    """Pola spesifikasi. Return (jumlah_pelanggaran, [ringkasan token])."""
    cleaned = _strip_ignorable(text)
    return len(_TOKEN_LAZY_SPEC.findall(cleaned)), _summary(_TOKEN_LAZY_SPEC, cleaned)


def scan_lazy_tokens_wide(text):
    """Pola berjaga-jaga (check-staging): + 'rest of the'."""
    cleaned = _strip_ignorable(text)
    return len(_TOKEN_LAZY_WIDE.findall(cleaned)), _summary(_TOKEN_LAZY_WIDE, cleaned)


def _summary(rx, text):
    out = []
    for m in rx.finditer(text):
        s = max(0, m.start() - 30)
        ctx = text[s:m.end() + 30].replace("\n", " ")
        out.append(f"token='{m.group(0)}' konteks='…{ctx}…'")
    return out


# ---------------------------------------------------------------------------
# 2. Validasi jangkar kode  path/to/File.ext:Lxx-Lyy  |  path/to/File.ext:Lxx
# ---------------------------------------------------------------------------

_ANCHOR_RE = re.compile(
    r"(?P<path>[\w./\-]+\.[A-Za-z0-9]{1,8}):L(?P<start>\d+)(?:-L(?P<end>\d+))?"
)

_CODE_DEF_RE = re.compile(r"^\s*(function|contract|library|interface|abstract contract|mod|fn|pub fn|def|class|impl)\b")


def scan_code_anchors(text):
    return list(_ANCHOR_RE.finditer(text))


def validate_anchor(m, repo, violations, where):
    path = m.group("path")
    start = int(m.group("start"))
    end = int(m.group("end")) if m.group("end") else start
    tag = f"{where}: jangkar {m.group(0)}"
    if start > end:
        violations.append(f"{tag}: start ({start}) > end ({end})")
        return
    if repo is None:
        return
    srcp = Path(repo) / path
    if not srcp.is_file():
        # tolerir jangkar yang menunjuk artefak audit/metode repo kerja itu sendiri
        if Path(path).is_file():
            srcp = Path(path)
        else:
            violations.append(f"{tag}: berkas sumber tidak ada di --repo ({path})")
            return
    try:
        lines = srcp.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        violations.append(f"{tag}: tidak bisa dibaca ({exc})")
        return
    if end > len(lines):
        violations.append(
            f"{tag}: baris {end} melebihi jumlah baris {path} ({len(lines)})"
        )
        return
    seg = lines[start - 1 : end]
    if not any(_CODE_DEF_RE.match(l) for l in seg):
        nonblank = [l for l in seg if l.strip()]
        if not nonblank:
            violations.append(f"{tag}: rentang baris kosong murni")
        elif len(seg) == 1 and not _CODE_DEF_RE.match(seg[0]):
            # jangkar satu baris diizinkan walau bukan baris pembuka
            # definisi — cukup harus tak kosong.
            pass


# ---------------------------------------------------------------------------
# 3. Util pembaca berkas
# ---------------------------------------------------------------------------

def _read(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace"), None
    except OSError as exc:
        return None, str(exc)


# ---------------------------------------------------------------------------
# 4. Sub-perintah
# ---------------------------------------------------------------------------

def cmd_check_staging(args):
    """check-staging <file> [--repo DIR]"""
    v = []
    text, err = _read(args.file)
    if err:
        print(f"GAGAL check-staging: {err}")
        return 1
    lines = text.splitlines()
    if not lines or not lines[0].startswith("## STAGING MANIFEST"):
        v.append("baris pertama wajib dimulai '## STAGING MANIFEST'")
    else:
        n = 0
        for l in lines[1:]:
            if l.startswith("## "):
                break
            n += 1
        if n > 16:
            v.append(f"blok manifes pembuka {n} baris (batas 16) sebelum heading berikutnya")

    n_lazy, details = scan_lazy_tokens_wide(text)
    for d in details:
        v.append(f"token kompresi malas [{d}]")

    for m in scan_code_anchors(text):
        validate_anchor(m, args.repo, v, "staging")

    return _report("check-staging", args.file, v)


def cmd_check_b(args):
    """check-b <audit_dir> [--repo DIR]"""
    v = []
    ad = Path(args.audit_dir)
    if not ad.is_dir():
        print(f"GAGAL check-b: direktori {ad} tidak ada")
        return 1

    required = [
        "B01-SCOPE.md",
        "B02-CENSUS-STATIC.md",
        "B03-CENSUS-LIVE.md",
        "B04-STREAMS-AND-CLUSTERS.md",
        "B05-LEDGER-SISA.md",
        "B06-REGISTRY-INVARIANT.md",
        "B07-STATE-BRIDGES.md",
    ]
    for name in required:
        if not (ad / name).is_file():
            v.append(f"artefak Tahap B hilang: {name}")

    # ---- sensus statis JSONL (14 kunci spesifikasi flow-b-map)
    JSONL_FIELDS = [
        "file", "contract", "function", "line", "end_line", "visibility",
        "mutability", "payable", "entrypoint", "value_moves", "mechanisms",
        "events_emitted", "external_calls", "notes",
    ]
    jsonl_files = sorted(ad.glob("*.jsonl"))
    out_dir = ad / "scripts" / "out"
    if out_dir.is_dir():
        jsonl_files += sorted(out_dir.glob("*.jsonl"))
    if not jsonl_files:
        v.append("tidak ada berkas *.jsonl sensus statis di audit_dir (cari juga scripts/out/)")
    for jf in jsonl_files:
        for i, raw in enumerate(jf.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError as exc:
                v.append(f"{jf.name}:{i}: JSON tidak valid ({exc})")
                continue
            if not isinstance(row, dict):
                v.append(f"{jf.name}:{i}: baris bukan objek JSON")
                continue
            missing = [f for f in JSONL_FIELDS if f not in row]
            if missing:
                v.append(f"{jf.name}:{i}: field wajib hilang {missing}")
                continue
            if row.get("value_moves") not in ("yes", "state_mutator", "no", "unknown"):
                v.append(f"{jf.name}:{i}: value_moves='{row.get('value_moves')}' (harus yes|state_mutator|no|unknown — B14-v2)")
                continue
            if row["value_moves"] == "unknown" and not str(row.get("notes", "")).strip():
                v.append(f"{jf.name}:{i}: value_moves='unknown' tanpa notes")
            if row["value_moves"] == "state_mutator" and row.get("entrypoint") is not True:
                v.append(f"{jf.name}:{i}: value_moves='state_mutator' hanya sah untuk entrypoint:true (B14-v2)")
            if row["value_moves"] == "state_mutator" and not str(row.get("notes", "")).strip():
                v.append(f"{jf.name}:{i}: value_moves='state_mutator' tanpa notes (wajib sebut storage yang ditulis)")
            # --- B14-v2 strict rule: larangan label 'no' pada entrypoint yang bisa menulis state
            if (row["value_moves"] == "no" and row.get("entrypoint") is True
                    and str(row.get("mutability", "")).lower() not in ("view", "pure")):
                fname_lc = str(row.get("function", "")).lower()
                notes = str(row.get("notes", ""))
                is_empty_receive = fname_lc == "receive"
                has_tag = ("PRIVILEGED_ONLY:" in notes) or ("COSMETIC_NON_ECONOMIC:" in notes)
                if not (is_empty_receive or has_tag):
                    v.append(
                        f"{jf.name}:{i}: B14-v2 pelanggaran — entrypoint:true + mutability="
                        f"'{row.get('mutability')}' (bisa menulis state) + value_moves='no' "
                        f"tanpa tag PRIVILEGED_ONLY:/COSMETIC_NON_ECONOMIC: dan bukan receive kosong "
                        f"(fungsi='{row.get('function')}')"
                    )

    # ---- artefak B bebas token malas
    for name in required:
        p = ad / name
        if p.is_file():
            n_lazy, details = scan_lazy_tokens(p.read_text(encoding="utf-8", errors="replace"))
            for d in details:
                v.append(f"{name}: token kompresi malas [{d}]")

    return _report("check-b", str(ad), v)


def cmd_check_c(args):
    """check-c <file> [--repo DIR]"""
    v = []
    text, err = _read(args.file)
    if err:
        print(f"GAGAL check-c: {err}")
        return 1

    n_lazy, details = scan_lazy_tokens(text)
    for d in details:
        v.append(f"token kompresi malas [{d}]")

    for m in scan_code_anchors(text):
        validate_anchor(m, args.repo, v, "check-c")

    fname = Path(args.file).name
    is_stream = re.match(r"^C\d{2,}-.*-INVENTORY\.md$", fname) and not fname.startswith("C00-")
    if is_stream:
        # --- hitung segmen S1..Sn unik yang DIDEFINISIKAN (bukan disebut)
        seg_defs = set(re.findall(r"^\s*\|?\s*(?:\*\*)?(S\d{1,2})(?:\*\*)?\s*(?:\||:|- )", text, re.M))
        n = len(seg_defs)
        # --- handoff H1..H(n-1) unik yang DIDEFINISIKAN
        hnd_defs = set(re.findall(r"^\s*\|?\s*(?:\*\*)?(H\d{1,2})(?:\*\*)?\s*(?:\||:|- )", text, re.M))
        if n >= 2:
            need = set(f"H{i}" for i in range(1, n))
            missing = sorted(need - hnd_defs)
            if missing:
                v.append(f"{n} segmen didefinisikan tetapi handoff kurang: butuh {len(need)}, "
                         f"yang belum terdefinisi: {', '.join(missing)}")
        # --- larangan klaim prematur
        for m2 in re.finditer(r"\bTERBUKTI\b", text):
            s = max(0, m2.start() - 30)
            v.append(f"klaim prematur 'TERBUKTI' di berkas Tahap C: konteks='…{text[s:m2.end()+30]}…'")
        for m2 in re.finditer(r"\bINV-", text):
            s = max(0, m2.start() - 30)
            v.append(f"penomoran invariant dilarang di Tahap C: konteks='…{text[s:m2.end()+30]}…'")

    return _report("check-c", args.file, v)


def cmd_check_d(args):
    """check-d <audit_dir> --stream ID [--repo DIR]"""
    v = []
    ad = Path(args.audit_dir)
    if not ad.is_dir():
        print(f"GAGAL check-d: direktori {ad} tidak ada")
        return 1
    sid = args.stream
    reg = ad / "B06-REGISTRY-INVARIANT.md"
    regtext = reg.read_text(encoding="utf-8", errors="replace") if reg.is_file() else None
    if regtext is None:
        v.append("B06-REGISTRY-INVARIANT.md tidak ada; rujukan INV- kartu tidak bisa diverifikasi")

    # pola nama eksak: D<NN>-<STREAM_ID>-WAVE1-BLIND.md / -WAVE2-QUEUED.md / -LEAD-CARDS.md
    groups = (
        ("Gelombang 1", f"D*-{sid}-WAVE1-BLIND.md", False),
        ("Gelombang 2", f"D*-{sid}-WAVE2-QUEUED.md", False),
        ("Lead Cards", f"D*-{sid}-LEAD-CARDS.md", True),
    )
    card_files = []
    for lab, pat, allow_terbukti in groups:
        found = sorted(ad.glob(pat), key=lambda x: x.name)
        if not found:
            v.append(f"berkas {lab} milik Stream {sid} tidak ditemukan (pola: {pat})")
            continue
        if lab == "Lead Cards":
            card_files = found
        for p in found:
            text = p.read_text(encoding="utf-8", errors="replace")
            n_lazy, details = scan_lazy_tokens(text)
            for d in details:
                v.append(f"{p.name}: token kompresi malas [{d}]")
            for m in scan_code_anchors(text):
                validate_anchor(m, args.repo, v, p.name)
            if not allow_terbukti and re.search(r"\bTERBUKTI\b", text):
                _once(v, f"{p.name}: Gelombang 1/2 TIDAK memberi verdict TERBUKTI (C11)")

    for cards in card_files:
        body = cards.read_text(encoding="utf-8", errors="replace")
        chunks = _split_entries(body)
        if not chunks:
            v.append(f"{cards.name}: tidak ada kartu (heading '## ')")
        for cid, chunk in chunks:
            miss = [k for k in ("a", "b", "c") if not re.search(rf"\(\s*{k}\s*\)", chunk)]
            if miss:
                v.append(f"{cards.name} kartu '{cid}': komponen rantai hilang "
                         f"{', '.join('(' + m + ')' for m in miss)}")
            if re.search(r"\bINV-(?:S|H|HB|J|F)x\b", chunk):
                v.append(f"{cards.name} kartu '{cid}': masih memakai placeholder INV-?x, bukan ID nyata")
            invs = set(re.findall(r"\bINV-[A-Za-z]*-?\d+\b", chunk))
            if not invs:
                v.append(f"{cards.name} kartu '{cid}': tanpa rujukan ID invariant INV- bernomor")
                continue
            if regtext is not None:
                for inv in sorted(invs):
                    if not re.search(rf"\b{re.escape(inv)}\b", regtext):
                        v.append(f"{cards.name} kartu '{cid}': invariant {inv} "
                                 f"tidak tercatat di B06-REGISTRY-INVARIANT.md")
    return _report("check-d", f"{ad} [stream {sid}]", v)


def cmd_check_e(args):
    """check-e <file> [--repo DIR]"""
    v = []
    text, err = _read(args.file)
    if err:
        print(f"GAGAL check-e: {err}")
        return 1

    n_lazy, details = scan_lazy_tokens(text)
    for d in details:
        v.append(f"token kompresi malas [{d}]")

    for m in scan_code_anchors(text):
        validate_anchor(m, args.repo, v, "check-e")

    if not any(lab in text for lab in ("DIEKSEKUSI", "DIANALISIS", "CODE-REVIEW-ONLY")):
        v.append("tidak ada label bukti eksplisit (DIEKSEKUSI / DIANALISIS / CODE-REVIEW-ONLY)")

    if ("Observed Live Ceiling" not in text) and ("Proven Potential Ceiling" not in text):
        v.append("tidak memuat metrik plafon (Observed Live Ceiling atau Proven Potential Ceiling)")

    if not re.search(r"\bgas\b", text, re.IGNORECASE):
        v.append("tidak mencatat nilai gas eksekusi")

    return _report("check-e", args.file, v)


def cmd_check_final(args):
    """check-final <audit_dir> [--repo DIR]"""
    v = []
    ad = Path(args.audit_dir)
    if not ad.is_dir():
        print(f"GAGAL check-final: direktori {ad} tidak ada")
        return 1

    # ---- B05: nol CORE-FLOW BELUM_MASUK_STREAM (EP+VM(yes)) DAN nol EP+SM(state_mutator) tersisa; nol QUEUED>0 / ACTIVE>0
    b05 = ad / "B05-LEDGER-SISA.md"
    if not b05.is_file():
        v.append("B05-LEDGER-SISA.md tidak ada; keberadaan wajib bagi cakupan 100%")
    else:
        text = b05.read_text(encoding="utf-8", errors="replace")
        for i, l in enumerate(text.splitlines(), 1):
            if "BELUM_MASUK_STREAM" in l and "CORE-FLOW" in l:
                v.append(f"B05:{i}: EP+VM(yes) CORE-FLOW tersisa BELUM_MASUK_STREAM: {l.strip()[:100]}")
        # --- B14-v2: nol sisa populasi EP+SM(state_mutator) pada CORE-FLOW
        for i, l in enumerate(text.splitlines(), 1):
            has_sm = ("EP+SM" in l) or ("state_mutator" in l)
            uncovered = ("BELUM_TERCAKUP" in l) or ("BELUM_MASUK_STREAM" in l)
            if has_sm and uncovered and ("CORE-FLOW" in l or "state_mutator" in l):
                v.append(f"B05:{i}: EP+SM(state_mutator) CORE-FLOW tersisa belum tercakup: {l.strip()[:100]}")
        for i, l in enumerate(text.splitlines(), 1):
            mq = re.search(r"QUEUED\s*(?:==|=|:)\s*(\d+)", l)
            ma = re.search(r"ACTIVE\s*(?:==|=|:)\s*(\d+)", l)
            if mq and int(mq.group(1)) > 0:
                v.append(f"B05:{i}: QUEUED = {mq.group(1)} > 0 pada Stream: {l.strip()[:80]}")
            if ma and int(ma.group(1)) > 0:
                v.append(f"B05:{i}: ACTIVE = {ma.group(1)} > 0 pada Stream: {l.strip()[:80]}")
        n_lazy, details = scan_lazy_tokens(text)
        for d in details:
            v.append(f"B05: token kompresi malas [{d}]")

    # ---- G01
    g01 = ad / "G01-VERDICT.md"
    if not g01.is_file():
        v.append("G01-VERDICT.md tidak ada")
    else:
        gtext = g01.read_text(encoding="utf-8", errors="replace")
        n_lazy, details = scan_lazy_tokens(gtext)
        for d in details:
            v.append(f"G01-VERDICT.md: token kompresi malas [{d}]")

    # ---- 06: REJECTED_POC_FAILS / NEGATIVE_EV / DUST wajib BUKTI_SIMULASI
    f06 = ad / "06-refuted-invalid.md"
    if f06.is_file():
        body = f06.read_text(encoding="utf-8", errors="replace")
        for eid, chunk in _split_entries(body):
            if any(lab in chunk for lab in
                   ("REJECTED_POC_FAILS", "REJECTED_NEGATIVE_EV", "REJECTED_DUST")):
                if "BUKTI_SIMULASI:" not in chunk:
                    v.append(f"06 '{eid}': penolakan POC_FAILS/NEGATIVE_EV/DUST tanpa blok BUKTI_SIMULASI: "
                             f"(anti PAPER_REFUTATION_DETECTED)")

    # ---- 07: wajib Disposition: + PERCOBAAN:
    f07 = ad / "07-needs-next-step.md"
    if f07.is_file():
        body = f07.read_text(encoding="utf-8", errors="replace")
        for eid, chunk in _split_entries(body):
            if "Disposition:" not in chunk:
                v.append(f"07 '{eid}': tanpa 'Disposition:' (anti LAZY_BAILOUT_DETECTED)")
            if "PERCOBAAN:" not in chunk:
                v.append(f"07 '{eid}': tanpa blok 'PERCOBAAN:' (anti LAZY_BAILOUT_DETECTED)")

    return _report("check-final", str(ad), v)


# ---------------------------------------------------------------------------
# 5. Utilistik pelaporan
# ---------------------------------------------------------------------------

def _once(v, msg):
    if msg not in v:
        v.append(msg)


def _split_entries(text):
    """ciutkan teks jadi [(judul, blok)] per heading '## '."""
    chunks = []
    cur_title, buf = None, []
    for l in text.splitlines():
        if l.startswith("## "):
            if cur_title is not None:
                chunks.append((cur_title, "\n".join(buf)))
            cur_title, buf = l.strip("# ").strip(), []
        elif cur_title is not None:
            buf.append(l)
    if cur_title is not None:
        chunks.append((cur_title, "\n".join(buf)))
    return chunks


def _report(cmd, subject, violations):
    if violations:
        print(f"GAGAL {cmd} [{subject}] — {len(violations)} pelanggaran:")
        for x in violations:
            print(f"  - {x}")
        return 1
    print(f"LULUS {cmd} [{subject}]")
    return 0


# ---------------------------------------------------------------------------
# 6. CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        prog="verify_flow.py",
        description="Pemeriksa deterministik gerbang metode moneyflow v2.0 (exit 0 = LULUS, 1 = GAGAL).",
    )
    ap.add_argument("--repo", help="direktori repo target untuk validasi jangkar (opsional); "
                                   "terbawa ke sub-perintah yang mendukung")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("check-staging", help="staging subagent sebelum merge")
    p.add_argument("file")
    p.add_argument("--repo")
    p.set_defaults(func=cmd_check_staging)

    p = sub.add_parser("check-b", help="artefak Tahap B + sensus statis JSONL")
    p.add_argument("audit_dir")
    p.add_argument("--repo")
    p.set_defaults(func=cmd_check_b)

    p = sub.add_parser("check-c", help="inventaris Tahap C (C00 atau per-Stream)")
    p.add_argument("file")
    p.add_argument("--repo")
    p.set_defaults(func=cmd_check_c)

    p = sub.add_parser("check-d", help="gelombang + kartu lead per Stream")
    p.add_argument("audit_dir")
    p.add_argument("--stream", required=True)
    p.add_argument("--repo")
    p.set_defaults(func=cmd_check_d)

    p = sub.add_parser("check-e", help="berkas bukti batch Tahap E")
    p.add_argument("file")
    p.add_argument("--repo")
    p.set_defaults(func=cmd_check_e)

    p = sub.add_parser("check-final", help="gerbang penutupan proyek (0-sisa + G01 + 06/07)")
    p.add_argument("audit_dir")
    p.add_argument("--repo")
    p.set_defaults(func=cmd_check_final)

    args = ap.parse_args()
    sysexit(args.func(args))


if __name__ == "__main__":
    main()
