---
name: flow-e-test
description: "Tahap E — Pembuktian Fork Pin per Lintasan (moneyflow v2.1): fork di domain Lintasan (dua domain bila rantai lintas-domain) + relay pesan via impersonasi pengirim sah; pustaka FlowFixtures per domain (helper transaksi normal + helper relay); dua metrik plafon C10-v2 per domain (tanpa penjumlahan antar-domain/varian tanpa uji); batch maks 3 per Lintasan; kartu lintas-Lintasan → MENUNGGU-RANGKAI bila Lintasan tujuan belum C; cakupan varian (representatif DIEKSEKUSI, anggota lain berlaku-turunan CODE-REVIEW-ONLY sampai diuji); kontrol positif, rerun forge gas IDENTIK, rantai (a)+(b)+(c) utuh (C11), tiga verdict terpisah. Dipakai saat menguji lead, atau saat user menyebut tahap E, uji, proof, fork."
---

# Skill flow-e-test — Tahap E (Uji test)

Tahap E = **membuktikan atau membantah** mekanisme di fork live + **mengukur P&L**.

Unit kerja = satu **Lintasan** (`STR-nn.Lk`); sasaran = kartu `QUEUED` Lintasan itu. Lintasan berikutnya dalam Stream yang sama memakai ulang fork + `FlowFixtures` yang sudah dibangun.
Skill ini memuat aturan dan format sampai Tahap E selesai. `methodology/aturan-alur-first.md` (seksi D — Tahap E + C1–C11) hanya rujukan sengketa.

## Gerbang masuk (tanpa ini, PoC TERBLOKIR)

1. **B8 Live-Match Lintasan lulus per domain segmen** (dilakukan di awal Tahap D). Belum live-match → Lintasan `TUNDA-LIVE` di `B05`, nol waktu eksekusi, jangan tulis PoC.
2. **Kartu lead ada** dengan rantai (a)+(b)+(c) dan klaim finansial (dari Tahap D).
3. **Gate D C10-v2 lulus** di Tahap D (permissionless + reachable + B8 + rumus plafon >= $1).
4. **Nol `LP-x` pengendali nilai `UNVERIFIED`** pada rantai kartu. Kartu `TUNDA-VERIFIKASI` **tidak boleh** ditarik ke batch.

## Langkah 1 — Fork live (C1, mengikat)

- **Mode default: `FORK_LIVE_PIN`** — fork pada blok pin, lalu panggil **alamat deployed**. ABI mengikuti versi live; kalau ABI live berbeda dari HEAD, sesuaikan PoC ke ABI live.
- `FORK_DEPLOYED_HEAD` adalah **pengecualian**, hanya dipakai dalam dua kasus: (a) membuktikan `PRE_LIVE_SCOPE`; (b) uji silang untuk `FIXED_IN_HEAD`.
- Fork dibangun ke **kondisi live**: kontrak ter-deploy + state live pada **blok yang dipin**.
- **PoC HEAD saja tidak cukup** bila live ≠ HEAD.

### Paket reproduksi (wajib dilampirkan per temuan)

Pengembang asli harus bisa langsung menjalankannya:
- chain, `fork_block`, kebutuhan RPC archive;
- alamat-alamat yang disentuh;
- perintah forge lengkap (`forge test --fork-url $RPC --fork-block-number <pin> --match-test <nama> -vvvv`);
- log `[PASS]`;
- `caller_role: permissionless`;
- `vm_store_used: false`, tanpa `deal` ke kontrak protokol;
- `ceiling_usd` beserta sumber angkanya;
- untuk rantai **lintas-domain**: semua domain + `fork_block` masing-masing + urutan perintah + baris `pengirim disimulasikan`;
- kontrak penerima kendali milik penguji (bila uji `CY-x`), dengan path berkas.

### Prosedur `FIXED_IN_HEAD` (dua log wajib)

- Log 1: PoC `[PASS]` di `FORK_LIVE_PIN`.
- Log 2: PoC yang sama **gagal** pada `FORK_DEPLOYED_HEAD`.
- Sertakan rujukan commit perbaikan, dicari dengan `git log -S "<potongan kode>" --oneline`.
- Kalau perbaikannya tidak bisa ditunjuk ke commit tertentu, tulis `FIXED_IN_HEAD_UNATTRIBUTED`. Wadahnya tetap `08`.
- Mekanisme penentu **wajib diuji ulang di fork live** bila fork-testable. Bila **tidak** fork-testable, catat keterbatasannya **eksplisit** (jangan diam-diam).
- Pengecualian: proyek TESTNET/DEVNET — "live" = lingkungan itu sendiri.

### Fork per domain (mode `MULTI-DOMAIN`, mengikat)

- **Fork dua domain (v2.1):** Lintasan `MULTI-DOMAIN` menguji di fork domain sumber **DAN** domain tujuan bila handoff lintas-domain berada di rantai (a)+(b)+(c). Pengiriman pesan disimulasikan dengan **impersonasi pengirim sah** sesuai autentikasi domain (alias L1→L2, `crossChainSender`, messenger), dan dicatat di `E-PROOF`.
- **Fork mengikuti chain tempat kontrak koridor kartu berada.** Bila rantai (a)+(b)+(c) kartu menyentuh kontrak di lebih dari satu chain (mis. deposit di Polygon → fill di Base), jalankan fork untuk setiap chain yang menyentuh garis aliran dan uji di fork yang sesuai — multi-chain fork (dua anvil instance / satu tes per fork) diizinkan dan wajib dicatat di `E-PROOF`.
- **Kartu yang menyentuh perilaku per-varian/per-domain WAJIB diuji di fork domain varian tersebut**, bukan di domain utama. Daftar override yang relevan diambil dari `B00` (`VK-x`) dan Tabel Selisih Lintasan; daftar contoh spesifik proyek ditulis di `audit/notes/`, bukan di skill.
- **Dasar pengetahuan per-chain = implementasi yang sudah dibaca di Tahap B/C** (sensus 100% varian + inventaris koridor). Fork Tahap E mengonfirmasi **eksekusi** behavior itu; fork bukan sumber pertama pengetahuan behavior.
- Bila fork chain tertentu tidak tersedia (RPC publik menolak archive dan sejenisnya), catat transport eksplisit di `E-PROOF` (C3) dan turunkan label bukti sesuai tangga (mis. `CODE-REVIEW-ONLY` untuk behavior khusus chain itu) — jangan klaim fork yang tidak dijalankan.

- **Relay pesan antar-domain dibuat sebagai helper fixture:** (1) eksekusi sisi kirim di fork domain asal, ambil payload dari event/log transaksi itu; (2) di fork domain tujuan, **impersonasi pengirim sah** sesuai autentikasi domain (alias, `crossChainSender`, messenger, relayer) lalu kirim payload yang sama. Tulis baris `pengirim disimulasikan: <alamat> via <mekanisme autentikasi>` di `E-PROOF`. **Payload buatan tangan** yang tidak berasal dari sisi kirim nyata = `CODE-REVIEW-ONLY` untuk mata rantai itu.

### Sumber RPC (mengikat)

- **ALCHEMY utama**: `rpc-env.sh <rantai>` memilih key alchemy per-rantai dari `.env` / `.env.rpc.secret` lebih dulu.
- **Fallback public RPC** (endpoint publik di `.env.rpc`) hanya bila: rantai tidak punya key alchemy, ATAU alchemy gagal/limit.
- Free-tier alchemy ETH: `eth_getLogs` rentangnya dibatasi → **chunking wajib**.

### Aturan hemat yang diizinkan

- Satu fork per wilayah, dipakai ulang.
- `deploy_parity` sekali + cache.
- Satu harness dua mode (HEAD + fork).
- Triase fork-testability di awal.
- Bila satu tes penentu sudah bisa mengonfirmasi, jangan jalankan pindai sejarah panjang dulu.

## Langkah 2 — Penarikan batch maks 3 kartu per Lintasan

Tarik **maksimal 3 kartu teratas** dari `QUEUED` **Lintasan aktif** sesuai urutan ketajaman struktural (`INV-Jx`/`Fx`/`Vx` > `INV-Hx`/`HBx`/`CYx`/`INx` > `INV-Sx` lokal S1→Sn) — ulangi sampai `QUEUED == 0` dan `ACTIVE == 0` **untuk Lintasan itu** (anti-kuota: tak ada target jumlah; kartu habis = Lintasan selesai diuji). Untuk tiap kartu wajib ada:

| Komponen | Isi |
| :--- | :--- |
| PoC | tes forge yang menjalankan rantai (a)+(b)+(c) utuh |
| Kontrol | kontrol **positif** (jalur sama menghasilkan bukan-nol) + kontrol negatif bila relevan |
| P&L | modal masuk, uang keluar, selisih — dalam satuan token dan USD bila ada harga |
| Mode kegagalan | apa yang terjadi bila prasyarat tidak terpenuhi |

### Kartu yang rantainya melewati batas Lintasan

Kartu dengan kolom **Lintasan rambatan** terisi:

- **Lintasan tujuan sudah lulus Tahap C** → uji rantai (a)+(b)+(c) utuh sampai kerugian; prasyarat sisi tujuan dibangun lewat `FlowFixtures`, perilaku sisi tujuan dibaca dari kontrak handoff/`HB-x` yang tercatat.
- **Lintasan tujuan belum lulus Tahap C** → buktikan sampai **batas Lintasan** (keluaran yang melanggar jaminan handoff), label `DIEKSEKUSI` untuk bagian itu, lalu status kartu **`MENUNGGU-RANGKAI`** di `B05` dengan rujukan Lintasan tujuan. Kartu ini diselesaikan Tahap F pemicu 1 saat Stream ditutup. **Dilarang** menulis verdict `TERBUKTI` untuk kartu `MENUNGGU-RANGKAI`.

### Cakupan varian (representatif vs anggota)

- Kartu dibuktikan di anggota **representatif** → label `DIEKSEKUSI` **untuk anggota itu saja**.
- Anggota berstatus `SAMA` di Tabel Selisih → **berlaku-turunan**, label `CODE-REVIEW-ONLY` sampai diuji di fork domain anggota itu.
- Anggota berstatus `BEDA:<kolom>` → **tidak boleh diklaim terdampak** tanpa uji tersendiri.
- Uji tambahan per anggota hanya dijalankan bila **mengubah keputusan verdict** (eligibility per domain, atau severity karena plafon).

### Cumulative Normal-Path Fixtures (FlowFixtures) — wajib

Direktori `poc/FlowFixtures` (atau setara bahasa target):

- Gunakan kembali **satu instance fork blok pin per domain** (blok pin domain dari `B00`) — dipakai ulang oleh semua Lintasan dalam Stream dan Stream berikutnya; jangan spin-up fork baru per kartu.
- Simpan **fungsi pembantu transaksi normal pengguna** dari setiap Lintasan yang diuji (mis. penyetoran normal, pertukaran normal, pembukaan posisi normal) ke **berkas fixture bersama** agar Lintasan hilir membangun prasyarat state 100% melalui rangkaian panggilan transaksi resmi pengguna.
- Simpan juga **helper relay pesan** (lihat *Fork per domain*) per keluarga transport/autentikasi, agar Lintasan lain di keluarga yang sama tidak membangun ulang.
- Uji **Ingress `PASSIVE` (`S0`)**: donasi / transfer langsung dilakukan dengan **transfer nyata** dari akun penguji; `deal` hanya boleh ke EOA penguji, **tidak pernah** ke saldo kontrak protokol.
- Uji **`CY-x`**: kontrak penerima kendali (callback/hook) milik penguji **diizinkan** karena permissionless; kodenya ditaruh di `poc/<STR>-<Lk>/` dan dicantumkan di paket reproduksi.
- **DILARANG** memalsukan slot storage protokol (`vm.store`) **atau** `deal` langsung ke saldo kontrak protokol.

**Brief memakai bahasa verifikasi invariant, bukan bahasa serangan.**

## Dua Mode Pengukuran Plafon (C10-v2)

**Mode 1 (`Observed Live Ceiling`):** bila kontrak pada blok pin sudah menyimpan saldo/likuiditas `> 0`, jalankan rantai (a)+(b)+(c) langsung terhadap state blok pin dan catat nilai kerugian aktual dalam satuan aset & USD.

**Mode 2 (`Proven Potential Ceiling`):** bila kontrak pada blok pin memiliki saldo/aktivitas `== 0` tetapi terbuka bagi operasi pengguna normal, langkah pertama PoC wajib mensimulasikan transaksi pengguna korban (`victim`) secara wajar lewat **entrypoint resmi** pada fork blok pin (*Victim Seeding* rasional sesuai Pernyataan #3 dan #4 `verify/VERDICT.md`), diikuti transaksi akun penguji tanpa hak istimewa (**pemanggil permissionless**) yang mengeksekusi rantai (a)+(b)+(c); lalu ukur selisih P&L bersih — wajib **>= $1**.

**Plafon per domain (v2.1):** `Observed Live Ceiling` memakai `Live_Balance@pin` `Value_Holder` **di domain tempat uji dijalankan**. Plafon **tidak dijumlahkan** antar-domain atau antar-anggota varian kecuali tiap domain/anggota diuji sendiri dan hasilnya dicatat terpisah. Ringkasan lintas-domain ditulis sebagai **daftar per domain**, bukan satu angka total.

## Langkah 3 — Verifikasi parent atas bukti penentu (lantai bawah)

Tidak boleh dipangkas. Parent:

1. **Menjalankan ulang semua tes forge sendiri** dan mencocokkan **gas** — harus **IDENTIK**. Gas beda = tes tidak reproducible = bukti belum sah.
2. Memeriksa jangkar dari **kode bernomor**: batas fungsi via `grep -n`. **Satu baris yang ada ≠ jangkar yang benar** — periksa fungsinya, bukan hanya nomor barisnya.
3. Bila ada rantai koreksi: **tiap langkah berikut wajib memeriksa ulang jangkar yang dikoreksi**. Rantai koreksi bukan bukti.
4. Pemeriksaan batas fungsi lewat **`grep -n`** dijalankan parent (fungsi, bukan baris).

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
3. pemicu **terjangkau oleh siapa pun (permissionless)** — tanpa peran istimewa. "Keanehan" susunan transaksi **BUKAN** alasan gugur; yang menggugurkan hanya ketergantungan pada kunci admin/governance/oracle tepercaya atau state mustahil dicapai permissionless.

**TIDAK HARUS LIVE.** P&L live 0 tidak membuat lead DORMAN atau gugur.
Ambang: potensi kerugian **≥ $1 = bukan debu** (kandidat sah, disimpan). Hanya **< $1** yang gugur DUST.

## Disiplin bukti (mengikat)

- **Label jelas**: `DIEKSEKUSI` vs `DIANALISIS` vs `CODE-REVIEW-ONLY`. **Jangan** sajikan penalaran sebagai serangan yang dieksekusi.
- **verify_zero_and_scan**: setiap **nol = mencurigakan**. Simpan output lengkap termasuk error; wajib **kontrol positif bukan-nol lewat jalur yang sama**; pindai besar dibuktikan sensus (rentang + chunk + cakupan) atau **dilabeli SAMPEL persis**; langkah yang belum dijalankan = **langkah terbuka**, bukan rejection/finding.
- **Cabut klaim yang gugur sampai ke dokumennya** — bukan dibiarkan menggantung.
- **Penolakan safety classifier TIDAK boleh diulang, diparafrase, atau diputar lewat jalur lain.** Pivot saja.

## Keluaran

- `E<NN>-<STR>-<Lk>-BATCH<M>-PROOF.md` — PoC + kontrol + P&L (kedua metrik plafon dicatat: mana yang dipakai dan angkanya) + tiga verdict + label bukti.
- `poc/<STR>-<Lk>/` — berkas tes forge + log eksekusi lengkap (gas tercatat) + kontrak penerima kendali penguji (bila ada); helper transaksi normal + **helper relay** ditambahkan ke `poc/FlowFixtures/<domain>/`.
- **Pembaruan `B05`:** status kartu (`TERUJI` / `MENUNGGU-RANGKAI`) + kursor Lintasan.

## Definition of done Tahap E (per batch per Lintasan)

- [ ] fork dibangun di blok pin; live != HEAD tercatat; fixture dibangun via `Cumulative Normal-Path Fixtures` (victim seeding lewat entrypoint resmi, nol `vm.store`/`deal` ke saldo kontrak protokol)
- [ ] penarikan batch mengikuti urutan ketajaman struktural B2a-v2; berhenti saat `QUEUED == 0` dan `ACTIVE == 0`
- [ ] maks 3 kartu per batch
- [ ] fork di **domain Lintasan** (dua domain bila rantai lintas-domain), relay lewat helper dengan pengirim sah tercatat
- [ ] nol kartu bergantung `LP-x` `UNVERIFIED` di batch
- [ ] kartu lintas-Lintasan: diuji utuh, atau `MENUNGGU-RANGKAI` dengan rujukan Lintasan tujuan (tanpa verdict `TERBUKTI`)
- [ ] label cakupan varian: representatif `DIEKSEKUSI`; anggota `SAMA` berlaku-turunan `CODE-REVIEW-ONLY`; anggota `BEDA` tidak diklaim tanpa uji
- [ ] plafon dicatat **per domain**; nol penjumlahan antar-domain/varian tanpa uji masing-masing
- [ ] tiap kartu: PoC + kontrol positif + P&L terukur + mode kegagalan
- [ ] kedua metrik plafon C10-v2 diterapkan: `Observed Live Ceiling` (saldo > 0, langsung ke state blok pin) atau `Proven Potential Ceiling` (saldo == 0 tapi terbuka, victim seeding + pemanggil permissionless, P&L bersih >= $1)
- [ ] parent rerun forge; gas **IDENTIK**
- [ ] jangkar diperiksa via `grep -n` (fungsi, bukan baris)
- [ ] rantai (a)+(b)+(c) diuji utuh (C11); yang berhenti di satu fungsi = TIDAK KONKLUSIF
- [ ] tiga verdict terpisah; severity dari plafon teramati
- [ ] semua klaim berlabel DIEKSEKUSI / DIANALISIS / CODE-REVIEW-ONLY
- [ ] nol klaim tanpa log; nol log tanpa perintah
