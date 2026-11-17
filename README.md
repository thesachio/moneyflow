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
| B | Mapping | `B01-SCOPE`, `B02-CENSUS-STATIC`, `B03-CENSUS-LIVE`, `B04-CLUSTERS`, `B05-LEDGER-SISA`, `B06-REGISTRY-INVARIANT` | Tanpa invariant, tanpa pemetaan mendalam, tanpa buruan/PoC/verdict |
| C | Pemetaan mendalam per klaster | `C<NN>-<KLASTER>-FLOW-INVENTORY` | Deskriptif saja; jahitan adalah batas |
| D | Eksplorasi | Kartu lead + invariant (`INV-Sx/Hx/Jx/Fx`) | Dua gelombang (buta → berpengetahuan + katalog); tanpa PoC |
| E | Uji test | PoC fork-live + P&L per kandidat | Fork blok pin; P&L terukur; batch maks 3 |
| F | Komposisi (bersyarat) | Lemma dari data terbaru | Hanya lead multi-segmen; tanpa fork/PoC ulang |
| G | Verdict | Verdict 06/07/08/09 per kandidat + distribusi akhir | Tiga verdict terpisah |

Rolling per klaster: `C → D → E`. Tahap F lintas-klaster + Tahap G di akhir.

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
| `verify/VERDICT.md`, `verify/SEVERITY-RUBRIC.md` | Standar verdict + severity (dipakai Tahap G) |
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

`templates/` masih memuat template era Segitiga yang tidak dirujuk oleh tahap A–G mana pun — kandidat pembersihan,
bukan bagian alur kerja aktif.
