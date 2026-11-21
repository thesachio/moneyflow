---
name: flow-autopilot
description: Autopilot / deep-run PROYEK PENUH (moneyflow v2.1). Jalankan seluruh wadah Stream — C00 pra-stream, lalu per Stream: rolling per Lintasan C -> B8 -> D (dua gelombang) -> E, lalu penutupan wadah (F antar-Lintasan -> G triage -> F antar-Stream), lalu sapuan akhir (F antar-varian + B9) — dari posisi kursor sampai sapuan akhir atas satu perintah berdiri, tanpa tap antar langkah; /stop mencabut otorisasi seketika. Memuat 7 iron law, mesin status tiga lapis (Lapis Proyek + Lapis Wadah Stream + Lapis Lintasan), Lintasan Context Capsule, dan pra-cek deterministik tools/verify_flow.py. Dipakai saat user memerintah full-autopilot, autopilot, deep-run, jalankan penuh, atau satu perintah berdiri untuk seluruh proyek.
---

# Skill flow-autopilot — Orkestrator Full-Autopilot Proyek (Stream-First, moneyflow v2.0)

Mesin otonom metode flow money first v2.0. Tugas: menjalankan **SELURUH proyek** — semua `Stream` (`STR-xx`), seluruh koridor aliran nilai — dari posisi kursor sampai sapuan akhir, atas **satu perintah berdiri**, tanpa menunggu tap antar langkah.

**Berhenti hanya bila:** semua Stream selesai (QUEUED == 0 **dan** ACTIVE == 0 di semua Stream; nol `EP+VM` pada klaster `CORE-FLOW` berstatus `BELUM_MASUK_STREAM`) **atau** `/stop` datang.

**Ini BUKAN autopilot satu Stream.** Satu Stream adalah unit kerja; proyek adalah cakupannya. Skill ini mengatur pemilihan Stream aktif, pembentukan Stream baru dari sisa ledger, dan penutupan proyek. Klaster hanyalah **papan kontrol indeks** Tahap B — unit eksekusi tetap Stream vertikal ujung-ke-ujung.

**Skill ini tidak memakai gate Segitiga** — tidak ada STAGE-0/A–F, tidak ada `verify_segitiga.py`, tidak ada wilayah R_i. Kursor dan gerbangnya milik metode ini; pra-cek deterministik memakai `python3 tools/verify_flow.py`.

## 1. Cakupan (Stream-First)

- **Semua Stream, semua klaster**, urut **pintu masuk pertama kali** (B2a Lapis 1 — entrypoint paling awal yang dilalui pengguna, bukan EV), sampai tidak ada Stream yang belum selesai.
- **Selesaikan satu wadah Stream sebelum pindah.** Di dalam wadah, kerjakan Lintasan satu per satu (urut arah aliran `Ingress → Egress`). Dilarang menyentuh Stream berikut sebelum syarat **"Stream tercakup"** (`flow-g-verdict`) terpenuhi.
- **Satu sesi / satu delegasi = satu Lintasan.** Dilarang mendelegasikan seluruh Stream sekaligus.
- **Resume, bukan mulai ulang.** Stream yang Tahap D-nya selesai tapi E sebagian → lanjutkan dari kartu tersisa. Kursor mencatat Stream aktif + tahap + batch.
- **Ekspansi dinamis wajib, tanpa Stream sapu sisa (B22):** seluruh `STR-xx` awal selesai tetapi ledger masih menyisa — wajib kelompokkan ulang sisa menurut `Ingress → Egress` dan keluarga varian/transport menjadi Stream/Lintasan baru (lihat `STEP DYNAMIC-STREAM-SPAWN`).
- **Stream selesai penuh tidak diulang.** Stream yang tidak live-match → `TUNDA-LIVE` (nol waktu eksekusi) dan dilewati.

## 2. Tujuh Iron Law (tidak boleh dilanggar)

1. **Zero-trust terhadap ingatan chat.** Di awal setiap transisi tahap, baca ulang dari disk: berkas aturan kanonik + `B05-LEDGER-SISA.md` + `B06-REGISTRY-INVARIANT.md` + daftar Stream (`B04`) + berkas Stream yang sedang jalan. **Output chat bukan acuan.**
2. **Verify-before-transition.** Jangan ubah kursor ke tahap berikut sebelum gate tahap itu lulus:
   - **B13** scope lock
   - **B0 Profil Topologi** (mode konsisten dengan hitungan)
   - **B8 Live-Match Lintasan** per domain segmen (cara kerja: alur + cek desain kode + `cast code`/view di blok pin dulu; log tx = verifikator terakhir)
   - **Gate D finansial** (C10-v2 — plafon live 0 **tidak** membuat DORMAN)
   - **verifikasi parent** atas bukti penentu di E
   - **penutupan wadah**: F antar-Lintasan dievaluasi + nol `MENUNGGU-RANGKAI` sebelum G
   - **aturan verdict** di G (C10-v2 + C11)

   Gate gagal → perbaiki di berkas kerja saat itu juga, jalankan ulang gate.
3. **Satu wadah Stream, sampai tercakup; satu Lintasan per sesi.**
4. **Kuras antrean dengan rolling batch maks 3 ACTIVE di E.** Tarik maks 3 kartu QUEUED teratas **Lintasan aktif** sesuai ketajaman struktural → buktikan di E → ulangi sampai QUEUED == 0 **dan** ACTIVE == 0 **per Lintasan** → Lintasan berikut dalam wadah → **penutupan wadah** (F antar-Lintasan → G) → Stream berikut.
5. **Larangan mutlak token kompresi malas.** Pola token lengkap dijalankan otomatis lewat `python3 tools/verify_flow.py` (sub-perintah `check-staging`, `check-c`, `check-d`, `check-e`, `check-final`) — token mencakup elipsis (titik-tiga dan karakter satu-kode), singkatan daftar Indonesia tiga huruf berhenti-titik atau tanpa tanda (pola baku di `tools/verify_flow.py`), singkatan Latin untuk daftar, frasa Inggris pengganti penghitungan, dan frasa pengganti penjelasan bagian tersisa di berkas audit mana pun. Setiap klaim wajib punya jangkar verbatim `Path/File.ext:Lxx-Lyy`, dan batas fungsi diperiksa via `grep -n` (**satu baris yang ada ≠ jangkar yang benar**).
6. **Write-ahead checkpoint di ledger.** Perbarui kursor (Stream aktif, tahap aktif, batch aktif, QUEUED/ACTIVE count) **SEBELUM** memulai tahap dan **SEGERA** setelah gate tahap itu lulus.
7. **`/stop` mencabut otorisasi seketika.** Hentikan subagent, tulis nol berkas, jangan promosi, jangan jalankan close-region. Lanjut hanya atas perintah eksplisit baru yang menyebut Stream/batch-nya.

## 3. Lantai bawah — yang tidak boleh dipangkas

Baca kode, ukur live, verifikasi parent atas bukti penentu.

**Yang TIDAK dipangkas deep-run:** dua gelombang · bukti fork blok pin + P&L dua metrik plafon · `B05` + `B07` + sapuan akhir · `/stop` kapan saja.

**Yang BOLEH dihemat:** satu instance fork blok pin per rantai dipakai ulang (pustaka `FlowFixtures` kumulatif) · `deploy_parity` sekali + cache per rantai · satu harness dua mode (pin + HEAD untuk regresi) · triase fork-testability di awal · pipeline (bukan paralel buta) · cek mesin otomatis `verify_flow.py` · pre-check murah sebelum gate.

## 4. Persiapan / Resume

1. **Belum ada berkas kerja kanonik** → buat dari `templates/` + `methodology/` (INTEL `A01`, `B01`–`B07`, ledger sisa, registry invariant), lalu jalankan `flow-a-intel` dan `flow-b-map` sampai Tahap B selesai. **Autopilot tidak memburu sebelum scope dikunci dan Tahap B selesai.**
2. **Baca posisi kursor** dari `B05-LEDGER-SISA.md` + daftar Stream `B04`: Stream aktif, tahap aktif, batch aktif, QUEUED/ACTIVE count. Lompat langsung ke STEP yang sesuai — jangan mulai dari awal.
3. Stream dan klaster yang selesai penuh **tidak diulang**.

## 5. Mesin Status — dua lapis (Stream-First)

### Lapis Proyek

**STEP PROJECT — pilih pekerjaan berikut.**
Pastikan Tahap A (`INTEL.md`, `A01`, `A02`) dan Tahap B (`B01`–`B07`, termasuk `B04-STREAMS-AND-CLUSTERS.md` dan `B07-STATE-BRIDGES.md`) sudah lulus gate sebelum memburu. Baca `B05` + daftar Stream `B04`. Cari Stream pertama yang belum tuntas (urut B2a Lapis 1). Tidak ada sisa → cek ekspansi dinamis → **STEP FINAL-SWEEP**.

**STEP C00-PRIMITIVES — Langkah Wajib Pra-Stream.**
Bila `C00-SHARED-PRIMITIVES.md` **belum ada**: jalankan satu putaran inventaris atas seluruh unit bertipe `SHARED-PRIMITIVE` di `B04` (jaminan pembulatan, skala desimal, invarian 1:1/share conversion, peran, event), verifikasi dengan `python3 tools/verify_flow.py check-c audit/C00-SHARED-PRIMITIVES.md`, lalu checkpoint di `B05-LEDGER-SISA.md`.

**STEP STREAM-PICK — pemilihan Stream Aktif (urutan `B2a-PostAudit`).**
Ambil `Stream` pertama yang berstatus `PENDING` atau belum tuntas menurut urutan dua tier `B2a-PostAudit`: **bila metadata audit tersedia dan ada Stream ber-tag `[DELTA]`/`[SCAR]`/`[SEAM]`** — kerjakan dulu seluruh **Tier 1 (Hot Streams First)** (urutan antar-sesamanya tetap B2a), dengan **`Prerequisite C-Only Pass`** untuk Stream hulu `[COLD-AUDITED]` yang dibutuhkan state-nya (hanya Tahap C + 1 transaksi normal di `FlowFixtures`, tanpa D/E); setelah Tier 1 tuntas `C -> D -> E -> G`, lanjutkan **Tier 2** menyapu `D -> E -> G` seluruh Stream `[COLD-AUDITED]` tersisa. Bila metadata audit tidak tersedia → urutan murni B2a dari awal. Cakupan 100% tetap mutlak (tier = pengurutan prioritas, bukan pemangkasan scope). Stream aktif diambil dari `B04-STREAMS-AND-CLUSTERS.md` + `B05-LEDGER-SISA.md` → masuk **STEP STREAM-R**.

**STEP DYNAMIC-STREAM-SPAWN — jaring cakupan dinamis.**
Apabila seluruh `STR-xx` awal telah **tercakup** tetapi `B05` masih menyisakan `EP+VM` / `EP+SM` / `IN-x` `CORE-FLOW` belum tercakup (**dihitung per nama**): orkestrator **WAJIB** (1) mengelompokkan sisa menurut `Ingress → Egress`, keluarga varian (`B00`), dan keluarga transport; (2) mendaftarkan setiap kelompok sebagai **Stream/Lintasan baru** di `B04` dengan label yang sesuai isinya; (3) menjalankannya seperti wadah Stream biasa. **Dilarang** membentuk satu Stream penampung berisi "semua sisa" (B22) — `check-b` **B-22** menolak. `EP+SM` berdiri sendiri tetap boleh menjadi unit pemeriksaan sendiri. Baru setelah sisa **ketiga populasi** tepat **0** → **STEP FINAL-SWEEP**.

**STEP FINAL-SWEEP — sapuan akhir proyek.**
**Tahap F pemicu 3** (antar-varian: replay lintas-domain, cakupan temuan representatif; + siklus 3+ Stream / loop umpan-balik nilai), **sapuan akhir enumerasi AST independen per nama (`B9`)**, dan `python3 tools/verify_flow.py check-final audit/` untuk memastikan cakupan `EP+VM`, `EP+SM`, dan `IN-x` **100% per nama**, nol antrean menggantung, dan konsistensi angka distribusi `06/07/08/09`. Patuhi `HOLD` (`C5`). Selesai → **COMPLETED** + ringkasan akhir ke user (distribusi + temuan 09 + sisa 07 beserta pemicunya).

### Lapis Wadah Stream (STEP STREAM-R)

Ambil daftar **Lintasan** Stream aktif dari `B04` (urut arah aliran). Untuk tiap Lintasan → **Lapis Lintasan** (`STEP C-LINTASAN` … `STEP E-BATCH`).

Semua Lintasan selesai E → **`STEP F-ANTAR-LINTASAN`**: evaluasi `flow-f-compose` **pemicu 1**; tutup semua `MENUNGGU-RANGKAI` atau catat `TIDAK MENYALA` per batas Lintasan.

**`STEP G-STREAM`**: jalankan `check-stream`, lalu triage wadah (`flow-g-verdict`), cek syarat **"Stream tercakup"**.

**`STEP F-ANTAR-STREAM`**: evaluasi `flow-f-compose` **pemicu 2** terhadap Stream yang sudah ditutup; bila menemukan rantai gabungan → buka kembali Stream lama **sebatas rantai itu**.

Kembali ke **STEP PROJECT**.

### Lapis Lintasan (satu Lintasan per sesi, tanpa putus konteks)

| STEP | Ubahan |
| :--- | :--- |
| `C-STREAM` → **`STEP C-LINTASAN`** | petakan inventaris Lintasan. **Tambah:** bila anggaran B19 terlewati tanpa `KEPUTUSAN_ANGGARAN` → pecah Lintasan, koreksi `B04`, ulangi. |
| `B8-STREAM` → **`STEP B8-LINTASAN`** | verifikasi live-match Lintasan (L1–L4) **per domain segmen**. `live-match-<STREAM>.md` → `live-match-<STR>-<Lk>.md`; gagal → Lintasan `TUNDA-LIVE`, lanjut Lintasan berikut dalam wadah. |
| `D-WAVE1` | **Tiga Lensa** Fisika Nilai → **Lima Lensa** (konservasi, handoff & State-Bridge, selisih varian, serah kendali `CY-x`, Ingress `S0`); *Twin-Path Diff* bila … → **Tabel Selisih Lintasan + Twin-Path**. |
| `D-CARDS` | invariant → `INV-S`/`H`/`HB`/`CY`/`IN`/`J`/`F`/`V`; **tambah:** kandidat bergantung `LP` `UNVERIFIED` → `TUNDA-VERIFIKASI`; disposisi (kartu / `G` / `NIHIL_KANDIDAT`) **wajib, bukan kuota**; `--stream <STR>` → `--lintasan <STR>.<Lk>`. |
| `E-BATCH` | uji di satu fork blok pin → uji di **fork domain Lintasan** (dua domain + helper relay bila lintas-domain); **tambah:** kartu lintas-Lintasan yang tujuannya belum C → `MENUNGGU-RANGKAI`; `untuk Stream itu` → `untuk Lintasan itu`. |
| `F-INCREMENTAL`, `G-STREAM` | **HAPUS** dari lapis ini (sudah pindah ke **Lapis Wadah**). |

## 6. Protokol Delegasi & Stream Context Capsule

1. **Parent memegang kendali eksklusif** atas berkas kanonik + `B05` + `B06` + `B07`. Parent satu-satunya penulis berkas kanonik.
2. **Lintasan Context Capsule — daftar periksa isi paket konteks subagent** (satu delegasi = satu Lintasan; input selalu ramping dan tajam; brief wajib mandiri, bersih dari riwayat chat):
   - [ ] path proyek + paradigma rantai + invarian inti Lintasan aktif;
   - [ ] artefak yang terikat Lintasan aktif: `C<NN>-<STR>-<Lk>-INVENTORY.md` + `C00-SHARED-PRIMITIVES.md` + baris relevan `B07-STATE-BRIDGES.md` + baris `B00` domain Lintasan;
   - [ ] maks 1 ringkasan handoff batas dari Lintasan tetangga (hulu/hilir) dalam wadah yang sama, bila rantai melewati batas;
   - [ ] maks 1 tabel Twin-Path (jika pasangan kembar ada);
   - [ ] maks 2–4 plugin di Wave 2 (pilih dari Lazy Skill Router sesuai `SYMPTOM-TAGS`);
   - [ ] format keluaran tahap + label wajib (DIANALISIS/DIEKSEKUSI);
   - [ ] DILARANG membawa riwayat chat, ledger penuh, atau katalog plugin borongan.
3. Subagent menulis **HANYA** ke `notes/staging-<fase>-<stream>-<tahap>-<item>.md`, diawali blok `## STAGING MANIFEST` **maks 16 baris**.
4. **Wajib pemeriksaan otomatis sebelum merge:** parent menjalankan `python3 tools/verify_flow.py check-staging <berkas_staging> --repo <projek-target>`; hanya staging yang LULUS boleh digabungkan ke berkas kanonik, lalu parent menjalankan gate tahap terkait.
5. Brief Tahap E memakai **bahasa verifikasi invariant**, bukan bahasa serangan.

## 7. Syarat penutupan proyek (COMPLETED)

Semua ini benar sebelum menyatakan selesai:

- [ ] semua **wadah Stream tercakup** (syarat di `flow-g-verdict`); nol `MENUNGGU-RANGKAI`
- [ ] nol `EP+VM` / `EP+SM` / `IN-x` `CORE-FLOW` belum tercakup di `B05`, **dihitung per nama** (ekspansi dinamis tanpa Stream sapu sisa sudah dikerjakan)
- [ ] `check-final` `verify_flow.py` LULUS (cek `06`/`07`/`G01` tuntas)
- [ ] ledger sisa kosong atau hanya berisi `TUNDA-LIVE` + DORMAN + `TUNDA-VERIFIKASI` dengan syarat buka-ulang
- [ ] sapuan akhir dijalankan: **F pemicu 3** (antar-varian + siklus) + **`B9`** enumerasi AST independen per nama
- [ ] distribusi akhir konsisten dengan isi wadah
- [ ] nol submisi / kontak program (HOLD dipatuhi)
- [ ] ringkasan akhir disajikan ke user: distribusi + temuan 09 + sisa 07 beserta pemicunya
