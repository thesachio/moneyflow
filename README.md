# moneyflow — Metode Flow Money First

Mesin/metode audit keamanan smart contract yang mempartisi pekerjaan berdasarkan **aliran uang**, bukan wadah berkas.
Unit kerja = satu aliran uang ujung-ke-ujung; tiap aliran diukur nilai live-nya sejak awal, diburu per segmen dan
handoff, lalu dibuktikan di fork live dengan P&L terukur.

Repo ini **bukan** proyek audit: tidak memuat kode kontrak target dan tidak memuat temuan. Dipakai dengan cara
**disalin ke folder kerja audit baru**, lalu dijalankan tahap demi tahap.

---

## 1. Tahap A–G

| Tahap | Nama | Keluaran | Batas |
| :--- | :--- | :--- | :--- |
| A | INTEL | `INTEL.md` (brief 9 butir), `A01-INTEL.md`, `A02-INTEL-discovery.md` | Brief saja; **tanpa cek onchain**, tanpa verifikasi teknis (A2) |
| B | Mapping | `B00-TOPOLOGY`, `B01-SCOPE`, `B02-CENSUS-STATIC` + **`scripts/out/b02-census.jsonl`** (18 field) + `scripts/out/ast-*.json`, `B03-CENSUS-LIVE` (**kolom `domain` wajib**), `B04-STREAMS-AND-CLUSTERS` (klaster 4 tipe + katalog Stream/Lintasan + **Katalog Ingress `IN-x`** Bagian 2b — 6 kelas), `B05-LEDGER-SISA` (3 populasi), `B06-REGISTRY-INVARIANT` (kosong di B), `B07-STATE-BRIDGES` | Tanpa invariant, tanpa pemetaan mendalam, tanpa buruan/PoC/verdict; AST boleh untuk lokalisasi (B6-v2) |
| C | Stream-Slice Inventory (rolling per-Lintasan) | `C00-SHARED-PRIMITIVES` (sekali), `C<NN>-<STR>-<Lk>-INVENTORY` | Deskriptif saja; koridor (`Corridor-Bound Cross-Cluster`); segmen menurut 5 pemicu B19; `CY-x`, Ingress `S0`, Tabel Selisih, LP-x per domain |
| D | Eksplorasi | Kartu lead + invariant (`INV-Sx/Hx/HBx/Jx/Fx` + `INV-CYx` serah kendali + `INV-INx` ingress tak resmi + `INV-Vx` selisih varian) | Per-Lintasan; dua gelombang; lima lensa; disposisi wajib (kartu / `G` berjangkar / `NIHIL_KANDIDAT` per segmen) — bukan kuota; kandidat bergantung `LP-x` `UNVERIFIED` → `TUNDA-VERIFIKASI`; mode `AUTO`/`PAIR` tetap |
| E | Pembuktian fork | `E<NN>-<STR>-<Lk>-BATCH<M>-PROOF` + pustaka `FlowFixtures` kumulatif | Fork blok pin per domain Lintasan; rantai utuh (a)+(b)+(c); batch maks 3; standar C10-v2 |
| F | Komposisi Tiga Lapis | `F<NN>-<ID>` + pembaruan `Sync_Status` (enum v2.1) di `B07` | (1) antar-Lintasan saat penutupan wadah — wajib dievaluasi, menutup `MENUNGGU-RANGKAI`; (2) antar-Stream inkremental; (3) antar-varian + siklus di sapuan akhir. Lemma 4 Syarat tanpa fork ulang |
| G | Verdict | Verdict 06/07/08/09 per kandidat + distribusi akhir | Triage per wadah Stream setelah semua Lintasan selesai E + F antar-Lintasan; syarat "Stream tercakup"; rekap proyek di penutupan; tiga verdict terpisah |

Rolling **vertikal per Lintasan**: `C -> B8 -> D -> E` per Lintasan; penutupan wadah `F antar-Lintasan -> G triage -> F antar-Stream`; satu Lintasan per sesi; semua Lintasan satu Stream tuntas sebelum Stream berikutnya; sapuan akhir `B9` (enumerasi AST independen) + rekapitulasi di penutupan. Pra-cek: `python3 tools/verify_flow.py` (check-staging / **check-b0** / check-b / check-c / check-d / **check-stream** / check-e / check-final).

---

## 2. Sumber kebenaran

| Berkas | Isi |
| :--- | :--- |
| `methodology/aturan-alur-first.md` | **Aturan kanonik** A1–A5, B, C, D, E, F, G + preferensi C1–C11. Bila ada berkas lain yang berbeda, berkas ini yang berlaku. |
| `methodology/resume-aturan-preferensi-alur-first.md` | Ringkasan preferensi mengikat |
| `methodology/acuan-workflow-tahap-B.md` | Acuan kerja Tahap B |
| `methodology/rancangan-hemat-fase-d.md` | Aturan hemat Fase D + lantai bawah |
| `SOUL.md` | Identitas + hukum kognitif metode flow |
| `AGENTS.md` | Konstitusi operasional: tahap, delegasi, gerbang, preferensi, lantai bawah |
| `verify/VERDICT.md`, `verify/SEVERITY-RUBRIC.md` | Standar verdict + severity (dipakai Tahap G) + blok penyetaraan metode Flow Money First v2.0 |
| `tools/verify_flow.py` | Pemeriksa gerbang deterministik (exit 0 lulus / 1 gagal): check-staging, **check-b0**, check-b, check-c, check-d, **check-stream**, check-e, check-final |
| `templates/B00-TOPOLOGY.md` | Template profil topologi (B0) — hitungan `DOM-x`/`VK-x`/`VC-x`, Matriks Domain, Katalog `IN-x`, Tabel Selisih Varian, daftar Lintasan |
| `skills/flow-*` | Skill per tahap + autopilot |

---

## 3. Memulai proyek baru

```bash
# 1. Salin kerangka DARI REPO INI — bukan dari folder proyek lain
cp -a /path/ke/moneyflow/. /path/ke/workspace/projects/<proyek>/
mkdir -p /path/ke/workspace/projects/<proyek>/audit/notes

# 2. Pasang skill ke profil agen (sekali)
cp -a skills/flow-* ~/.hermes/profiles/<profil>/skills/

# 3. Buktikan kesetaraan sebelum menulis apa pun
git -C /path/ke/moneyflow ls-files | sort > /tmp/mf.txt
cd /path/ke/workspace/projects/<proyek> && git ls-files | grep -vE '^(audit/|target/)' | sort > /tmp/pr.txt
comm -23 /tmp/pr.txt /tmp/mf.txt   # harus kosong: tidak ada berkas asing
comm -13 /tmp/pr.txt /tmp/mf.txt   # harus kosong: tidak ada berkas metode yang hilang

# 4. Mulai Tahap A
#    baca AGENTS.md §0 → SOUL.md → methodology/aturan-alur-first.md
#    lalu jalankan skill flow-a-intel
```

Larangan scaffold: **jangan** menyalin kerangka dari folder proyek lain (mis. `projects/across*`) — folder proyek
bisa memakai metode berbeda, dan menyalinnya mencampur dua metode.

---

## 4. Wadah kerja proyek

| Wadah | Isi |
| :--- | :--- |
| `audit/` | Artefak tahap: `INTEL.md`, `A01`/`A02`, lalu `B0*`, `C*`, `D*`, `E*`, `F*`, `G*` |
| `audit/notes/` | Catatan kerja, ledger sisa, staging subagent, log alat |
| `target/` | Klon repo target (di-pin lewat commit, **tidak** di-vendor ke git) |

---

## 5. Legacy — Metode Segitiga v2.0

Metode Segitiga (STAGE-0 + A–F, `path-map.md`, `FACTS.md`, `RADAR.md`, `STATE.md`, wadah `04`–`09`,
`verify_segitiga.py`, skill `sc-*`) **bukan** metode aktif repo ini. Sisa berkasnya disimpan utuh di
`archive/segitiga-v2/` sebagai rujukan sejarah dan **tidak** dipakai untuk proyek baru.

`templates/` tetap dipakai metode flow (Tahap G memakai format `06`/`09` + laporan teknis + email; autopilot memakai
`INTEL.md`), jadi bukan residu.
