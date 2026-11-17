---
name: flow-e-test
description: Tahap E — Uji test. PoC fork-live + P&L terukur per kandidat, batch maks 3, kontrol positif, parent menjalankan ulang forge dan mencocokkan gas, rantai (a)+(b)+(c) diuji utuh (C11), tiga verdict terpisah. Skill ini memuat aturan dan format sampai Tahap E selesai. Dipakai saat menguji lead, atau saat user menyebut tahap E, uji, proof, fork.
---

# Skill flow-e-test — Tahap E (Uji test)

Tahap E = **membuktikan atau membantah** mekanisme di fork live + **mengukur P&L**.
Skill ini memuat aturan dan format sampai Tahap E selesai. `methodology/aturan-alur-first.md` (seksi D — Tahap E + C1–C11) hanya rujukan sengketa.

## Gerbang masuk (tanpa ini, PoC TERBLOKIR)

1. **B8 live-match klaster lulus.** Belum live-match → `TUNDA-LIVE`, nol waktu eksekusi, jangan tulis PoC.
2. **Kartu lead ada** dengan rantai (a)+(b)+(c) dan klaim finansial (dari Tahap D).
3. **Gate C10 lulus** di Tahap D (mekanisme + plafon terukur + pemicu terjangkau).

## Langkah 1 — Fork live (C1, mengikat)

- Fork dibangun ke **kondisi live**: kontrak ter-deploy + state live pada **blok yang dipin**.
- **PoC HEAD saja tidak cukup** bila live ≠ HEAD.
- Mekanisme penentu **wajib diuji ulang di fork live** bila fork-testable. Bila **tidak** fork-testable, catat keterbatasannya **eksplisit** (jangan diam-diam).
- Pengecualian: proyek TESTNET/DEVNET — "live" = lingkungan itu sendiri.

### Sumber RPC (mengikat)

- **ALCHEMY utama**: `rpc-env.sh <rantai>` memilih key alchemy per-rantai dari `.env` / `.env.rpc.secret` lebih dulu.
- **Fallback public RPC** (publicnode dsb. di `.env.rpc`) hanya bila: rantai tidak punya key alchemy, ATAU alchemy gagal/limit.
- Free-tier alchemy ETH: `eth_getLogs` rentangnya dibatasi → **chunking wajib**.

### Aturan hemat yang diizinkan

- Satu fork per wilayah, dipakai ulang.
- `deploy_parity` sekali + cache.
- Satu harness dua mode (HEAD + fork).
- Triase fork-testability di awal.
- Bila satu tes penentu sudah bisa mengonfirmasi, jangan jalankan pindai sejarah panjang dulu.

## Langkah 2 — Batch maks 3 kartu

Tiap batch **maksimal 3 kartu**. Untuk tiap kartu wajib ada:

| Komponen | Isi |
| :--- | :--- |
| PoC | tes forge yang menjalankan rantai (a)+(b)+(c) utuh |
| Kontrol | kontrol **positif** (jalur sama menghasilkan bukan-nol) + kontrol negatif bila relevan |
| P&L | modal masuk, uang keluar, selisih — dalam satuan token dan USD bila ada harga |
| Mode kegagalan | apa yang terjadi bila prasyarat tidak terpenuhi |

**Brief memakai bahasa verifikasi invariant, bukan bahasa serangan.**

## Langkah 3 — Verifikasi parent atas bukti penentu (lantai bawah)

Tidak boleh dipangkas. Parent:

1. **Menjalankan ulang semua tes forge sendiri** dan mencocokkan **gas** — harus **IDENTIK**. Gas beda = tes tidak reproducible = bukti belum sah.
2. Memeriksa jangkar dari **kode bernomor**: batas fungsi via `grep -n`. **Satu baris yang ada ≠ jangkar yang benar** — periksa fungsinya, bukan hanya nomor barisnya.
3. Bila ada rantai koreksi: **tiap langkah berikut wajib memeriksa ulang jangkar yang dikoreksi**. Rantai koreksi bukan bukti.

## Langkah 4 — C11: uji rantai, bukan satu fungsi

**TERBUKTI** = ada **cukup jalur pendek yang saling bergantung** dari pelanggaran invariant sampai kerugian terukur, diverifikasi lewat **alur-alur terkait**.

- Tes yang berhenti di **satu fungsi pendek** lalu menyimpulkan = masih **HIPOTESIS**.
- Kartu E menguji **(a)+(b)+(c) sebagai SATU rantai** — bukan tiga tes terpisah yang masing-masing lulus.
- Bila salah satu mata rantai tidak bisa diuji, hasilnya **TIDAK KONKLUSIF**, bukan TERBUKTI.

## Langkah 5 — Verdict invariant + tiga verdict

### Verdict invariant (tulis ke registry `B06`)

`TERBANTAH` / `TERBUKTI` / `TIDAK KONKLUSIF`.

### Tiga verdict terpisah per finding

| Verdict | Isi |
| :--- | :--- |
| mekanisme | jalan atau tidak, di fork, dengan bukti |
| eligibility bounty | masuk scope atau tidak |
| dampak | berapa, untuk siapa, dalam kondisi apa |

Aturan severity:

- Severity dari **plafon TERAMATI**, bukan dari kapabilitas mekanisme.
- Klaim insidensi wajib **analisis same-transaction**.
- **Plafon per-eksekusi tidak dikalikan** tanpa bukti pengulangan.

## C10 — definisi kerugian (mengikat)

Kerugian = yang **BISA DIBUKTIKAN** merugikan:

1. mekanisme jalan di fork/test atas **kode + state nyata**;
2. **plafon terukur**;
3. pemicu **terjangkau lewat jalur operasi normal** — tanpa peran istimewa, tanpa state eksotis.

**TIDAK HARUS LIVE.** P&L live 0 tidak membuat lead DORMAN atau gugur.
Ambang: potensi kerugian **≥ $1 = bukan debu** (kandidat sah, disimpan). Hanya **< $1** yang gugur DUST.

## Disiplin bukti (mengikat)

- **Label jelas**: `DIEKSEKUSI` vs `DIANALISIS` vs `CODE-REVIEW-ONLY`. **Jangan** sajikan penalaran sebagai serangan yang dieksekusi.
- **verify_zero_and_scan**: setiap **nol = mencurigakan**. Simpan output lengkap termasuk error; wajib **kontrol positif bukan-nol lewat jalur yang sama**; pindai besar dibuktikan sensus (rentang + chunk + cakupan) atau **dilabeli SAMPEL persis**; langkah yang belum dijalankan = **langkah terbuka**, bukan rejection/finding.
- **Cabut klaim yang gugur sampai ke dokumennya** — bukan dibiarkan menggantung.
- **Penolakan safety classifier TIDAK boleh diulang, diparafrase, atau diputar lewat jalur lain.** Pivot saja.

## Keluaran

- `E<nn>-<JALUR>-BATCH<n>-PROOF.md` — PoC + kontrol + P&L + tiga verdict + label bukti.
- `poc/e<nn>-batch<n>/` — berkas tes forge + log eksekusi lengkap (gas tercatat).

## Definition of done Tahap E (per batch)

- [ ] fork dibangun di blok pin; live ≠ HEAD tercatat
- [ ] maks 3 kartu per batch
- [ ] tiap kartu: PoC + kontrol positif + P&L terukur + mode kegagalan
- [ ] parent rerun forge; gas **IDENTIK**
- [ ] jangkar diperiksa via `grep -n` (fungsi, bukan baris)
- [ ] rantai (a)+(b)+(c) diuji utuh (C11); yang berhenti di satu fungsi = TIDAK KONKLUSIF
- [ ] tiga verdict terpisah; severity dari plafon teramati
- [ ] semua klaim berlabel DIEKSEKUSI / DIANALISIS / CODE-REVIEW-ONLY
- [ ] nol klaim tanpa log; nol log tanpa perintah
