---
name: flow-autopilot
description: Autopilot / deep-run PROYEK PENUH Stream-First (moneyflow v2.0). Jalankan seluruh Stream ujung-ke-ujung — C00 pra-stream, lalu rolling per Stream C -> B8 -> D (dua gelombang) -> E -> F inkremental -> G triage — dari posisi kursor sampai sapuan akhir atas satu perintah berdiri, tanpa tap antar langkah; /stop mencabut otorisasi seketika. Memuat 7 iron law, mesin status dua lapis (Lapis Proyek + Lapis Stream), Stream Context Capsule, dan pra-cek deterministik tools/verify_flow.py. Dipakai saat user memerintah full-autopilot, autopilot, deep-run, jalankan penuh, atau satu perintah berdiri untuk seluruh proyek.
---

# Skill flow-autopilot — Orkestrator Full-Autopilot Proyek (Stream-First, moneyflow v2.0)

Mesin otonom metode flow money first v2.0. Tugas: menjalankan **SELURUH proyek** — semua `Stream` (`STR-xx`), seluruh koridor aliran nilai — dari posisi kursor sampai sapuan akhir, atas **satu perintah berdiri**, tanpa menunggu tap antar langkah.

**Berhenti hanya bila:** semua Stream selesai (QUEUED == 0 **dan** ACTIVE == 0 di semua Stream; nol `EP+VM` pada klaster `CORE-FLOW` berstatus `BELUM_MASUK_STREAM`) **atau** `/stop` datang.

**Ini BUKAN autopilot satu Stream.** Satu Stream adalah unit kerja; proyek adalah cakupannya. Skill ini mengatur pemilihan Stream aktif, pembentukan Stream baru dari sisa ledger, dan penutupan proyek. Klaster hanyalah **papan kontrol indeks** Tahap B — unit eksekusi tetap Stream vertikal ujung-ke-ujung.

**Skill ini tidak memakai gate Segitiga** — tidak ada STAGE-0/A–F, tidak ada `verify_segitiga.py`, tidak ada wilayah R_i. Kursor dan gerbangnya milik metode ini; pra-cek deterministik memakai `python3 tools/verify_flow.py`.

## 1. Cakupan (Stream-First)

- **Semua Stream, semua klaster**, urut **pintu masuk pertama kali** (B2a Lapis 1 — entrypoint paling awal yang dilalui pengguna, bukan EV), sampai tidak ada Stream yang belum selesai.
- **Selesaikan satu Stream hulu-ke-hilir sebelum pindah.** Dilarang menyentuh Stream berikut selama Stream aktif masih punya QUEUED > 0 atau ACTIVE > 0.
- **Resume, bukan mulai ulang.** Stream yang Tahap D-nya selesai tapi E sebagian → lanjutkan dari kartu tersisa. Kursor mencatat Stream aktif + tahap + batch.
- **Ekspansi dinamis wajib:** seluruh `STR-xx` awal selesai tetapi ledger masih menyisa — wajib bentuk Stream baru (lihat `STEP DYNAMIC-STREAM-SPAWN`).
- **Stream selesai penuh tidak diulang.** Stream yang tidak live-match → `TUNDA-LIVE` (nol waktu eksekusi) dan dilewati.

## 2. Tujuh Iron Law (tidak boleh dilanggar)

1. **Zero-trust terhadap ingatan chat.** Di awal setiap transisi tahap, baca ulang dari disk: berkas aturan kanonik + `B05-LEDGER-SISA.md` + `B06-REGISTRY-INVARIANT.md` + daftar Stream (`B04`) + berkas Stream yang sedang jalan. **Output chat bukan acuan.**
2. **Verify-before-transition.** Jangan ubah kursor ke tahap berikut sebelum gate tahap itu lulus:
   - **B13** scope lock
   - **B8 Live-Match Stream** (cara kerja: alur + cek desain kode + `cast code`/view di blok pin dulu; log tx = verifikator terakhir)
   - **Gate D finansial** (C10-v2 — plafon live 0 **tidak** membuat DORMAN)
   - **verifikasi parent** atas bukti penentu di E
   - **aturan verdict** di G (C10-v2 + C11)

   Gate gagal → perbaiki di berkas kerja saat itu juga, jalankan ulang gate.
3. **Satu Stream, sampai selesai.**
4. **Kuras antrean dengan rolling batch maks 3 ACTIVE di E.** Tarik maks 3 kartu QUEUED teratas sesuai ketajaman struktural B2a-v2 Lapis 2 → buktikan di E → adili di G → ulangi sampai QUEUED == 0 **dan** ACTIVE == 0, per Stream, lalu Stream berikut.
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

**STEP STREAM-PICK — pemilihan Stream Aktif.**
Ambil `Stream` (`STR-xx`) pertama yang berstatus `PENDING` atau belum tuntas berdasarkan urutan pintu masuk pengguna paling awal (B2a Lapis 1) → masuk **STEP STREAM-R**.

**STEP DYNAMIC-STREAM-SPAWN — jaring cakupan dinamis.**
Apabila seluruh `STR-xx` awal telah selesai tetapi di `B05-LEDGER-SISA.md` masih ditemukan baris `EP+VM` bertipe `CORE-FLOW` berstatus `BELUM_MASUK_STREAM`: orkestrator **WAJIB** membentuk `STR` baru dari entrypoint tersisa paling awal, mendaftarkannya di `B04`, dan menjalankannya sampai sisa `EP+VM` pada `CORE-FLOW` tepat **0**. Baru setelah itu boleh ke **STEP FINAL-SWEEP**.

**STEP FINAL-SWEEP — sapuan akhir proyek.**
Komposisi multi-stream akhir (bila ada siklus 3+ stream atau loop umpan-balik nilai), sapuan akhir enumerasi independen kedua (`B9`), dan `python3 tools/verify_flow.py check-final audit/` untuk memastikan cakupan `EP+VM` 100%, nol antrean menggantung, dan konsistensi angka distribusi `06/07/08/09`. Patuhi `HOLD` (`C5`). Selesai → **COMPLETED** + ringkasan akhir ke user (distribusi + temuan 09 + sisa 07 beserta pemicunya).

### Lapis Stream (STEP STREAM-R — satu Stream utuh hulu-ke-hilir tanpa putus konteks)

**STEP C-STREAM — petakan inventaris Stream.**
Petakan `C<NN>-<STREAM_ID>-INVENTORY.md` menembus batas klaster sepanjang koridor aliran dana aktif (`Corridor-Bound Cross-Cluster` — boleh `1-hop peek` pada `State-Bridge`), perbarui `B05-LEDGER-SISA.md` dan `B07-STATE-BRIDGES.md`, lalu jalankan `python3 tools/verify_flow.py check-c audit/C<NN>-<STREAM_ID>-INVENTORY.md`. Verifikasi parent → checkpoint.

**STEP B8-STREAM — verifikasi live-match Stream.**
Verifikasi `deploy_parity` / kode live kontrak pada koridor Stream di blok pin (pakai ulang cache per rantai). Tidak live-match → tandai `TUNDA-LIVE` di `B05`, nol waktu eksekusi, kembali ke **STEP PROJECT**.

**STEP D-WAVE1 — eksplorasi bebas murni.**
Delegasikan dengan **`Stream Context Capsule`** murni tanpa katalog: **Tiga Lensa Fisika Nilai** + `1-hop peek` pada `B07` + *Twin-Path Diff* bila pasangan kembar sudah punya berkas `C`. Keluaran `D<NN>-<STREAM_ID>-WAVE1-BLIND.md`: `OBS`, `G`, `Q`, `SYMPTOM-TAGS` (semua berlabel `DIANALISIS`). Verifikasi parent → checkpoint.

**STEP D-WAVE2 — lazy skill augmentation.**
Koordinator memilih **maksimal 2 sampai 4 plugin katalog** berdasarkan `SYMPTOM-TAGS` (+ maks 1 `CHAIN-*` dan 1 `DOM-*` bila relevan) sesuai tabel *Lazy Skill Router* di `flow-d-explore`. Disposisi seluruh `OBS` dan `Q` sampai habis tanpa kuota. Verifikasi parent → checkpoint.

**STEP D-CARDS — kartu lead + invariant + Gate D.**
Koordinator merumuskan `D<NN>-<STREAM_ID>-LEAD-CARDS.md` (rantai `(a)+(b)+(c)` per C11) + mengisi `B06-REGISTRY-INVARIANT.md` (`INV-Sx` / `INV-Hx` / `INV-HBx` / `INV-Jx` / `INV-Fx`, bersumber) + menyaring lewat **Gate D** (C10-v2: *permissionless* + *reachable state* + lulus B8 + rumus plafon potensial >= $1) + mengurutkan `QUEUED` berdasarkan bobot struktural (`Simpul/Komposisi > Handoff/State-Bridge > Segmen Lokal`). Jalankan `python3 tools/verify_flow.py check-d audit/ --stream <STREAM_ID>`. Verifikasi parent → checkpoint.

**STEP E-BATCH — pembuktian fork blok pin (loop, maks 3 per batch).**
Tarik maks 3 kartu teratas per batch, uji di satu fork blok pin menggunakan pustaka kumulatif `FlowFixtures`, ukur `Observed Live Ceiling` atau `Proven Potential Ceiling` (*rational victim seeding*), wajib kontrol positif, dan parent menjalankan ulang seluruh tes forge hingga **gas IDENTIK**. Jalankan `python3 tools/verify_flow.py check-e audit/E<NN>-<STREAM_ID>-BATCH<M>-PROOF.md`. Ulangi sampai `QUEUED == 0` **dan** `ACTIVE == 0` untuk Stream itu.

**STEP F-INCREMENTAL — komposisi inkremental.**
Bila Stream aktif menyentuh baris `B07-STATE-BRIDGES.md` yang sisi pasangannya sudah terpetakan, atau berbagi kolam dana dengan Stream sebelumnya, **jalankan** evaluasi komposisi inkremental saat itu juga (`flow-f-compose`) — jangan menunda ke akhir proyek.

**STEP G-STREAM — triage per-Stream.**
Adili seluruh kartu Stream aktif ke wadah `06 / 07 / 08 / 09` dengan tiga verdict terpisah (`flow-g-verdict`), perbarui kursor `B05-LEDGER-SISA.md`, lalu kembali ke **STEP PROJECT**.

## 6. Protokol Delegasi & Stream Context Capsule

1. **Parent memegang kendali eksklusif** atas berkas kanonik + `B05` + `B06` + `B07`. Parent satu-satunya penulis berkas kanonik.
2. **Stream Context Capsule — daftar periksa isi paket konteks subagent** (input selalu ramping dan tajam; brief wajib mandiri, bersih dari riwayat chat):
   - [ ] path proyek + paradigma rantai + invarian inti Stream aktif;
   - [ ] artefak yang terikat Stream aktif: `C<NN>-<STREAM_ID>-INVENTORY.md` + `C00-SHARED-PRIMITIVES.md` + baris relevan `B07-STATE-BRIDGES.md`;
   - [ ] maks 1 tabel Twin-Path (jika pasangan kembar ada);
   - [ ] maks 2–4 plugin di Wave 2 (pilih dari Lazy Skill Router sesuai `SYMPTOM-TAGS`);
   - [ ] format keluaran tahap + label wajib (DIANALISIS/DIEKSEKUSI);
   - [ ] DILARANG membawa riwayat chat, ledger penuh, atau katalog plugin borongan.
3. Subagent menulis **HANYA** ke `notes/staging-<fase>-<stream>-<tahap>-<item>.md`, diawali blok `## STAGING MANIFEST` **maks 16 baris**.
4. **Wajib pemeriksaan otomatis sebelum merge:** parent menjalankan `python3 tools/verify_flow.py check-staging <berkas_staging> --repo <projek-target>`; hanya staging yang LULUS boleh digabungkan ke berkas kanonik, lalu parent menjalankan gate tahap terkait.
5. Brief Tahap E memakai **bahasa verifikasi invariant**, bukan bahasa serangan.

## 7. Syarat penutupan proyek (COMPLETED)

Semua ini benar sebelum menyatakan selesai:

- [ ] semua Stream: QUEUED == 0 **dan** ACTIVE == 0
- [ ] nol baris `EP+VM` `CORE-FLOW` berstatus `BELUM_MASUK_STREAM` di `B05` (ekspansi dinamis sudah dikerjakan)
- [ ] `check-final` `verify_flow.py` LULUS (cek `06`/`07`/`G01` tuntas)
- [ ] ledger sisa kosong atau hanya berisi `TUNDA-LIVE` + DORMAN dengan syarat buka-ulang
- [ ] sapuan akhir dijalankan (komposisi multi-stream bila ada siklus + enumerasi independen kedua `B9`)
- [ ] distribusi akhir konsisten dengan isi wadah
- [ ] nol submisi / kontak program (HOLD dipatuhi)
- [ ] ringkasan akhir disajikan ke user: distribusi + temuan 09 + sisa 07 beserta pemicunya
