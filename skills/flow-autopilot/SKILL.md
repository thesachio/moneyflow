---
name: flow-autopilot
description: Autopilot / deep-run PROYEK PENUH. Jalankan SEMUA alur proyek — semua klaster, semua jalur — dari posisi kursor sampai sapuan akhir atas satu perintah berdiri, tanpa tap antar langkah; /stop mencabut otorisasi seketika. Memuat 7 iron law, mesin status dua lapis, protokol delegasi, dan syarat penutupan proyek. Dipakai saat user memerintah full-autopilot, autopilot, deep-run, jalankan penuh, atau satu perintah berdiri untuk seluruh proyek.
---

# Skill flow-autopilot — Mesin Orkestrator Full-Autopilot Proyek

Mesin otonom metode flow money first. Tugas: menjalankan **SELURUH proyek** — semua klaster, semua jalur — dari posisi kursor sampai sapuan akhir, atas **satu perintah berdiri**, tanpa menunggu tap antar langkah.

**Berhenti hanya bila:** semua jalur selesai (QUEUED == 0 **dan** ACTIVE == 0 di semua klaster) **atau** `/stop` datang.

**Ini BUKAN autopilot satu jalur.** Satu jalur adalah unit kerja; proyek adalah cakupannya. Skill ini mengatur pergantian jalur/klaster, pembuatan daftar alur, dan penutupan proyek.

**Skill ini tidak memakai gate Segitiga** — tidak ada STAGE-0/A–F, tidak ada `verify_segitiga.py`, tidak ada wilayah R_i. Kursor dan gerbangnya milik metode ini.

## 1. Cakupan

- **Semua klaster, semua jalur**, urut **pintu masuk pertama kali** (B2a — entrypoint paling awal yang dilalui pengguna, bukan EV), sampai tidak ada jalur yang belum selesai.
- **Selesaikan satu jalur sebelum pindah jalur; selesaikan satu klaster sebelum pindah klaster.** Dilarang menyentuh berkas jalur/klaster berikut selama yang aktif masih punya QUEUED > 0 atau ACTIVE > 0.
- **Resume, bukan mulai ulang.** Klaster yang Tahap D selesai tapi E sebagian → lanjutkan dari kartu tersisa. Kursor mencatat klaster + jalur + tahap + batch.
- **Klaster tanpa daftar alur** → buat daftarnya dulu (enumerasi + entrypoint pertama tiap alur, dari `B02` + `B04`) sebelum deep-run.
- **Jalur selesai penuh tidak diulang.** Jalur yang tidak live-match → `TUNDA-LIVE` (nol waktu eksekusi) dan dilewati.

## 2. Tujuh Iron Law (tidak boleh dilanggar)

1. **Zero-trust terhadap ingatan chat.** Di awal setiap transisi tahap, baca ulang dari disk: berkas aturan kanonik + ledger sisa + registry invariant + daftar jalur (`D00`) + berkas jalur yang sedang jalan. **Output chat bukan acuan.**
2. **Verify-before-transition.** Jangan ubah kursor ke tahap berikut sebelum gate tahap itu lulus:
   - **B13** scope lock
   - **B8** live-match (cara kerja: alur + cek desain kode dulu; log tx = verifikator terakhir)
   - **gate finansial D** (C10 — plafon live 0 **tidak** membuat DORMAN)
   - **verifikasi parent** atas bukti penentu di E
   - **aturan verdict** di G (C10 + C11)

   Gate gagal → perbaiki di berkas kerja saat itu juga, jalankan ulang gate.
3. **Satu jalur, satu klaster, sampai selesai.**
4. **Kuras antrean dengan rolling batch maks 3 ACTIVE di E.** Tarik maks 3 kartu QUEUED yang menyentuh entrypoint paling awal → buktikan di E → adili di G → ulangi sampai QUEUED == 0 **dan** ACTIVE == 0, per jalur, lalu jalur berikut.
5. **Larangan mutlak token kompresi malas.** Jangan pernah menulis `...`, `dll.`, `dst.`, `etc.`, `and so on`, `rest of logic`, `rest of code` di berkas audit mana pun. Setiap klaim wajib punya jangkar verbatim `Path/File.ext:Lxx-Lyy`, dan batas fungsi diperiksa via `grep -n` (**satu baris yang ada ≠ jangkar yang benar**).
6. **Write-ahead checkpoint di ledger.** Perbarui kursor (klaster aktif, jalur aktif, tahap aktif, batch aktif, QUEUED/ACTIVE count) **SEBELUM** memulai tahap dan **SEGERA** setelah gate tahap itu lulus.
7. **`/stop` mencabut otorisasi seketika.** Hentikan subagent, tulis nol berkas, jangan promosi, jangan jalankan close-region. Lanjut hanya atas perintah eksplisit baru yang menyebut wilayah/batch-nya.

## 3. Lantai bawah — yang tidak boleh dipangkas

Baca kode, ukur live, verifikasi parent atas bukti penentu.

**Yang TIDAK dipangkas deep-run:** dua gelombang · bukti fork-live + P&L · ledger + sapuan akhir · `/stop` kapan saja.

**Yang BOLEH dihemat:** satu fork per wilayah dipakai ulang · `deploy_parity` sekali + cache · satu harness dua mode · triase fork-testability di awal · pipeline (bukan paralel buta) · cek mesin otomatis · pre-check murah sebelum gate.

## 4. Persiapan / Resume

1. **Belum ada berkas kerja kanonik** → buat dari `templates/` + `methodology/` (INTEL `A01`, `B01`–`B06`, ledger sisa, registry invariant), lalu jalankan `flow-a-intel` dan `flow-b-map` sampai Tahap B selesai. **Autopilot tidak memburu sebelum scope dikunci.**
2. **Baca posisi kursor** dari ledger sisa + semua `D00`: klaster aktif, jalur aktif, tahap aktif, batch aktif, QUEUED/ACTIVE count. Lompat langsung ke STEP yang sesuai — jangan mulai dari awal.
3. Jalur dan klaster yang selesai penuh **tidak diulang**.

## 5. Mesin Status — dua lapis

### Lapis proyek

**STEP PROJECT — pilih pekerjaan berikut.**
Baca ledger sisa + semua `D00`. Cari klaster/jalur pertama yang belum selesai (urut pintu masuk pertama kali, B2a). Tidak ada → **STEP FINAL-SWEEP**. Tentukan posisi kursor:

| Kondisi | Langkah |
| :--- | :--- |
| belum punya daftar alur | STEP PATH-BUILD |
| daftar alur ada, D belum jalan | STEP PATH-RUN dari B8 |
| D selesai, E sebagian | STEP PATH-RUN dari E-BATCH (kartu tersisa saja) |
| E selesai, verdict belum | STEP PATH-RUN dari G |

**STEP PATH-BUILD — daftar alur klaster.**
Enumerasi alur klaster (dari `B02` + `B04`) + entrypoint pertama tiap alur → tulis `D00-<KLASTER>-PATHS.md` → urut pintu masuk pertama kali → checkpoint → STEP PATH-RUN jalur pertama.

**STEP CLUSTER-CLOSE — tutup klaster.**
Semua jalur klaster selesai (QUEUED == 0 **dan** ACTIVE == 0 di tiap jalur) → perbarui ledger + `D00` → checkpoint → STEP PROJECT untuk klaster berikut.

**STEP FINAL-SWEEP — sapuan akhir proyek.**
Enumerasi independen kedua (rerun sensus manual) dibanding ledger akhir; handoff terbuka + `TUNDA-LIVE` ditinjau; distribusi akhir dihitung di seluruh protokol. Selesai → **COMPLETED** + ringkasan akhir ke user (distribusi 06/07/08/09 + temuan 09 + sisa 07 beserta pemicunya).

### Lapis jalur (STEP PATH-RUN — deep-run satu jalur)

**STEP B8 — cek live-match jalur.**
Jalankan B8 untuk jalur itu (sensus kaki + cek live pin, pakai ulang cache trunk).
LULUS → gelombang 1. **TIDAK LIVE-MATCH** → `TUNDA-LIVE` (catat di ledger, nol waktu eksekusi) → kembali ke STEP PROJECT.

**STEP D-WAVE1 — gelombang 1 buta.**
Koordinator + 2 worker, **kode saja, buta** — tanpa katalog, tanpa badan fungsi klaster lain.
Keluaran: `OBS` / `G` / `R` / `Q`, semua berlabel **DIANALISIS**.
Verifikasi parent → checkpoint.

**STEP D-WAVE2 — gelombang 2 berpengetahuan.**
Koordinator + 2 worker: katalog + cek live, pindai baru **≤10k blok**, tanpa forge.
Keluaran: QUEUED (urut pintu masuk) + DORMAN (hanya bila gagal C10) + disposisi `Q`/RADAR.
Verifikasi parent → checkpoint.

**STEP D-LEAD-CARDS — kartu lead + invariant.**
Koordinator sendiri: kartu 1:1 dari QUEUED (rantai (a)+(b)+(c) per C11) + invariant baru ke registry (**wajib sumber**: field handoff atau docs/NatSpec).
Gate C10: lead lanjut ke E bila kerugian bisa dibuktikan (mekanisme di fork/test + plafon terukur + pemicu terjangkau tanpa peran istimewa/state eksotis). **Plafon live 0 TIDAK membuat DORMAN.** DORMAN hanya bila gagal C10, dengan syarat buka-ulang.
Verifikasi parent (subjek kartu identik kata-per-kata) → checkpoint.

**STEP E-BATCH — uji test (loop, maks 3 per batch).**
Koordinator + 3 worker, fork blok pin. Tiap batch **maks 3 kartu**. Parent **menjalankan ulang semua forge** dan mencocokkan gas (**harus IDENTIK**) sebelum batch dinyatakan selesai.
Ulangi sampai QUEUED == 0 **dan** ACTIVE == 0 untuk jalur itu.
Kartu yang spawn-nya ditolak kebijakan keamanan **TIDAK** diulang/diparafrase/diputar — parkir, invariant-nya tetap dirumuskan.

**STEP F — komposisi (bersyarat).**
Hanya bila **penting dan urgent** DAN lead **multi-segmen**. Uji F **tanpa fork/PoC ulang** — pakai data terbaru (`flow-f-compose`). Lead satu segmen **lewati** F.

**STEP G — verdict jalur.**
Adili tiap kartu: 06/07/08/09, **tiga verdict terpisah**, severity dari **plafon teramati** (`flow-g-verdict`). Perbarui ledger + `D00`. Kembali ke STEP PROJECT.

## 6. Protokol Delegasi ke Subagent

1. **Parent memegang kendali eksklusif** atas berkas kanonik + ledger + registry. Parent satu-satunya penulis berkas kanonik.
2. Sebelum mendelegasikan, parent menyusun **brief berdiri sendiri** — membawa semua konteks yang dibutuhkan.
3. Subagent menulis **HANYA** ke `notes/staging-<jalur>-<tahap>-<item>.md`, diawali blok `## STAGING MANIFEST` **maks 16 baris**.
4. Parent memeriksa staging (bebas token kompresi, berjangkar verbatim), menggabungkannya ke berkas kanonik, lalu **menjalankan gate tahap terkait**.
5. Brief Tahap E memakai **bahasa verifikasi invariant**, bukan bahasa serangan.

## 7. Syarat penutupan proyek (COMPLETED)

Semua ini benar sebelum menyatakan selesai:

- [ ] semua klaster: QUEUED == 0 **dan** ACTIVE == 0 di tiap jalur
- [ ] ledger sisa kosong atau hanya berisi `TUNDA-LIVE` + DORMAN dengan syarat buka-ulang
- [ ] sapuan akhir dijalankan (enumerasi independen kedua)
- [ ] distribusi akhir konsisten dengan isi wadah
- [ ] nol submisi / kontak program (HOLD dipatuhi)
- [ ] ringkasan akhir disajikan ke user: distribusi + temuan 09 + sisa 07 beserta pemicunya
