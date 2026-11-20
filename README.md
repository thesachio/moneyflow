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
| B | Mapping | `B00-TOPOLOGY` (DOM-x/VK-x/VC-x → mode + Matriks Domain) lalu `B01`–`B07` (termasuk katalog `IN-x` di `B04` Bagian 2b): incl. `B04-STREAMS-AND-CLUSTERS` & `B07-STATE-BRIDGES` | Tanpa invariant, tanpa pemetaan mendalam, tanpa buruan/PoC/verdict |
| C | Stream-Slice Inventory | `C00-SHARED-PRIMITIVES` (sekali di awal) + `C<NN>-<STREAM_ID>-INVENTORY` per Stream (memuat Lintasan `STR-nn.Lk`, Tabel Selisih Varian, `CY-x`, Ingress `S0`) | Deskriptif saja; menembus batas klaster sepanjang koridor aliran nilai (`Corridor-Bound Cross-Cluster`); 5 pemicu batas segmen (B19) |
| D | Eksplorasi | `D<NN>-<STREAM_ID>-WAVE1-BLIND`, `-WAVE2-QUEUED`, `-LEAD-CARDS` + invariant (`INV-Sx/Hx/HBx/Jx/Fx`) | Gelombang 1 bebas katalog (3 Lensa Fisika Nilai + Twin-Path Diff) lalu Gelombang 2 Symptom-Triggered Lazy Skill Loading (2-4 plugin relevan); tanpa PoC |
| E | Pembuktian fork | `E<NN>-<STREAM_ID>-BATCH<M>-PROOF` + pustaka `FlowFixtures` kumulatif | Fork blok pin; rantai utuh (a)+(b)+(c); batch maks 3; standar C10-v2 (Permissionless + Observed Live Ceiling / Proven Potential Ceiling >= $1) |
| F | Komposisi Inkremental (bersyarat) | `F<NN>-<COMPOSITION_ID>` + pembaruan `Sync_Status` di `B07` | Dua pemicu: inkremental seusai E per Stream (menyentuh State-Bridge/brankas bersama) + sapuan akhir multi-stream; Lemma 4 Syarat tanpa fork ulang |
| G | Verdict | Verdict 06/07/08/09 per kandidat + distribusi akhir | Triage per-Stream + rekapitulasi akhir; tiga verdict terpisah |

Rolling **vertikal per Stream ujung-ke-ujung**: `C -> B8 -> D -> E -> F inkremental -> G triage` — satu Stream utuh dikerjakan sebelum Stream berikutnya; sapuan akhir `B9` + rekapitulasi di penutupan proyek. Pra-cek deterministik: `python3 tools/verify_flow.py` (check-staging / check-b / check-c / check-d / check-e / check-final).

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
| `tools/verify_flow.py` | Pemeriksa gerbang deterministik (exit 0 lulus / 1 gagal): check-staging, check-b, check-c, check-d, check-e, check-final |
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
