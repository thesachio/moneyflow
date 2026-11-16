# moneyflow v1.0 — Mesin Audit Adversarial Berbasis Aliran Uang (Flow Money First)

**Repo ini adalah MESIN/METODE, bukan proyek audit.** Tidak memuat kode kontrak target dan tidak memuat temuan. Dipakai dengan cara disalin ke folder kerja audit baru, lalu dijalankan tahap demi tahap.

Metode inti: **Flow Money First** — partisi berdasarkan aliran uang, bukan wadahnya (berkas). Unitnya satu aliran uang ujung-ke-ujung; tiap aliran diukur nilai live-nya sejak awal, diburu per segmen dan handoff, dan dibuktikan di fork live dengan P&L terukur.

Status: **pilot** (16 Nov 2026). Metode ini sedang diuji di audit Across dan belum diputuskan sebagai pengganti metode Segitiga. Aturan di sini adalah hasil revisi terbaru.

---

## 1. Siklus Eksekusi

```
A   INTEL        Brief 9 butir → pin (commit + blok referensi + stage)
B   Mapping      Sensus 100% + klaster + jahitan + ledger sisa + registry
   │
   ├── Untuk SETIAP alur (vertikal, rolling C → D → E):
   │     C   Pemetaan mendalam klaster — inventaris alur + segmentasi + kontrak handoff deskriptif
   │     D   Eksplorasi — gelombang 1 buta → gelombang 2 berpengetahuan → kartu lead + invariant
   │     E   Uji test — PoC fork-live + P&L terukur per kandidat (batch maks 3)
   │
   ├── F   Komposisi (USULAN) — hanya lead multi-segmen, PoC gabungan
   └── G   Verdict — 06 / 07 / 08 / 09 per kandidat + distribusi akhir
       + sapuan akhir (enumerasi independen kedua dibanding ledger akhir)
```

## 2. Berkas Konstitusi (mengikat)

| Berkas | Isi | Kapan dibaca |
| :--- | :--- | :--- |
| **`SOUL.md`** | identitas, 7 Hukum Kognitif Besi, lantai bawah, prioritas EV | setiap sesi, sebelum apa pun |
| **`AGENTS.md`** | konstitusi operasional: bootloader, tahap A–G, delegasi, gerbang, hemat | setiap sesi + tiap delegasi |
| **`methodology/aturan-alur-first.md`** | aturan kanonik (A1–A5, B1–B16, C1–C9, Tahap C–G, belum diputus) | sumber kebenaran metode |
| **`methodology/resume-aturan-preferensi-alur-first.md`** | ringkasan aturan + preferensi | acuan cepat |
| **`methodology/acuan-workflow-tahap-B.md`** | acuan kerja Tahap B | pekerja Tahap B |
| **`methodology/rancangan-hemat-fase-d.md`** | aturan hemat Fase D + prinsip efisiensi + lantai bawah | mulai Fase D |

## 3. Struktur

```
SOUL.md                     identitas + hukum kognitif + lantai bawah
AGENTS.md                   konstitusi operasional
methodology/
  aturan-alur-first.md      aturan kanonik (A1–A5, B1–B16, C1–C9)
  resume-aturan-preferensi-alur-first.md
  acuan-workflow-tahap-B.md acuan Tahap B
  rancangan-hemat-fase-d.md aturan hemat + efisiensi + floor
  attack-forms/             AF-01..AF-10 — kelas kerentanan (diwarisi theadvers)
  domains/                  DOM-* — 7 domain (diwarisi theadvers)
references/
  methods/                  M-001..M-010 — metode bedah universal (diwarisi)
  pov/                      POV-* — 15 sudut pandang aktor (diwarisi)
  chains/                   CHAIN-* — 10 plugin rantai (diwarisi)
templates/                  wadah kerja audit + standar laporan (diwarisi)
  STATE.md FACTS.md RADAR.md path-map.md
  04-code-guarded.md 05-raw-leads.md 06-refuted-invalid.md
  07-needs-next-step.md 08-valid-not-eligible.md 09-confirmed-findings.md
  INTEL.md POC-PACKAGE.md SEVERITY-RUBRIC.md SUBMISSION-EMAIL.md
  TECHNICAL-REPORT.md VERDICT.md case/
skills/                     README — skill Tahap A–G BELUM ditulis (lihat §6 AGENTS.md)
tools/
  deploy_parity.py          cek parity deployment live vs HEAD (diwarisi)
verify/                     skema verdict 06–09 + severity rubric (diwarisi)
projects/                   tempat proyek target (di-.gitignore, tidak ikut commit)
```

## 4. Asal

Dibangun dari 0 dengan RULE dan PREFERENSI terbaru metode alur-first. Yang tetap + data modular diambil dari `thesachio/theadvers` (branch `v2`, commit `2f31e1a`): katalog 52 plugin (AF 10 + DOM 7 + M 10 + POV 15 + CHAIN 10), templates, `tools/deploy_parity.py`, dan `verify/`. Yang TIDAK diambil: skill `sc-*` dan `verify_segitiga.py` (terikat STAGE-0 + A–F Segitiga — harus ditulis ulang untuk Tahap A–G), `methodology/METHODOLOGY-SEGITIGA.md` + `BOOTSTRAP.md` + `INJECTION-CONTRACT.md` (digantikan berkas aturan di `methodology/`), dan `notes/backups/` (arsip riwayat).

## 5. Lantai Bawah (tidak boleh dipangkas)

Baca kode, ukur live, verifikasi parent atas bukti penentu.
