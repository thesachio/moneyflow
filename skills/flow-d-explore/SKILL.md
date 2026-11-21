---
name: flow-d-explore
description: "Tahap D — Eksplorasi per-Lintasan (moneyflow v2.1); sasaran = segmen dan titik sambungnya. Dua gelombang: Gelombang 1 bebas/buta dengan 5 Lensa (Konservasi, Handoff & State-Bridge, Selisih Varian, Serah Kendali CY-x, Ingress tak resmi S0) + SYMPTOM-TAGS; Gelombang 2 Symptom-Triggered Lazy Skill Router (maks 2-4 plugin). Kartu lead + invariant tiga lapis (INV-S/H/HB/CY/IN/J/F/V), Gate D C10-v2 statis dengan TUNDA-VERIFIKASI untuk LP UNVERIFIED, disposisi wajib (kartu / G / NIHIL_KANDIDAT) — bukan kuota kartu. Label DIANALISIS wajib (C11). Dipakai saat memburu Lintasan, atau saat user menyebut tahap D, eksplorasi, gelombang, kartu lead."
---

# Skill flow-d-explore — Tahap D (Eksplorasi)

Tahap D = buruan **per Lintasan** (moneyflow v2.1). Unit round = **satu Lintasan (`STR-nn.Lk`)**; sasaran di dalamnya = segmen dan titik sambungnya (handoff, `CY-x`, Fork/Join, `S0`, baris `BEDA`). Dua gelombang (bebas/buta → lazy skill augmentation).
Skill ini memuat aturan dan format sampai Tahap D selesai. `methodology/aturan-alur-first.md` (seksi D — Tahap D, B12, C10, C11) hanya rujukan sengketa.

## Prasyarat & Gerbang Awal B8 (tanpa ini D tidak mulai)

- Unit kerja Tahap D = **satu Lintasan (`STR-nn.Lk`)** berdasarkan `C<NN>-<STR>-<Lk>-INVENTORY.md` + `C00-SHARED-PRIMITIVES.md` + baris terkait di `B07-STATE-BRIDGES.md`.
- Registry invariant (`B06`) sudah punya struktur penomoran.
- **B8 Live-Match Lintasan** dijalankan sebelum Gelombang 1 dimulai: cek cepat atas kontrak pada koridor Lintasan aktif **di domain tempat tiap segmen berjalan** (kolom `Domain` Bagian 2) — **utamakan desain kode + `cast code`/view di blok pin domain itu**; DILARANG memindai log sejarah panjang (pindai log = verifikator terakhir, Tahap G/sapuan akhir). Bila kontrak target belum live-match: masukkan Lintasan ke `TUNDA-LIVE` di `B05-LEDGER-SISA.md` dan **hentikan putaran Lintasan tersebut** (nol waktu eksekusi). **Lintasan lain dalam Stream yang sama tetap jalan.**
- **B8 mengisi Lembar Parameter Live** (`C<NN>-<STR>-<Lk>-INVENTORY.md` **Bagian 8**): untuk tiap `LP-x`, baca nilai di **domain kolom `Domain` pada blok pin domain itu** (`cast call`; getter revert → `cast storage` dengan slot dari Bagian 8), isi kolom `Nilai @ blok pin` dan `Status Cabang` (`LIVE` / `DEAD-CONFIG` / `UNVERIFIED`). Ini pembacaan state blok pin, bukan pindai log — tetap dalam batas B8. Perubahan pada berkas C ini adalah pengisian kolom yang memang disediakan untuk B8, bukan revisi inventaris.
- **B8 mengisi `Live_Balance@pin`** untuk `Value_Holder` yang disentuh Lintasan aktif di `B04` — **per domain** (saldo per token pada blok pin domain masing-masing). Nilai ini menjadi masukan `Observed Live Ceiling` (C10-v2) di Tahap E. Lintasan berstatus `SINK_BELUM_JELAS` tidak boleh memulai Gelombang 1.

## Mode Eksekusi Tahap D: AUTO vs PAIR (Co-Audit)

Tahap D mendukung **dua mode eksekusi**. Pemilihan mode hanya dilakukan oleh user:

- **`MODE: AUTO`** (default — dipakai `flow-autopilot` dan bila user tidak meminta partisipasi interaktif): agen menyelesaikan Gelombang 1, Gelombang 2, Kartu Lead, dan Invariant untuk satu Stream secara penuh seperti aturan standar di bawah — tanpa berhenti menunggu input manusia.
- **`MODE: PAIR`** (Co-Audit — **hanya aktif bila user secara eksplisit meminta**: menyebut `pair`, `bareng`, `co-audit`, `interaktif`, atau `pandu per fungsi`; perintah autopilot proyek penuh TIDAK mengaktifkan PAIR): peneliti manusia berpartisipasi membaca kode fungsi demi fungsi bersama agen utama. Aturan rinci:

### PAIR — Gelombang 1 (Tanpa Katalog)

- DILARANG mendelegasikan pembacaan ke subagent tertutup di belakang layar lalu hanya menyodorkan berkas jadi. Agen utama memandu user berjalan **satu Segmen + Handoff keluarnya (`Sk` + `Hk`) per giliran percakapan** sepanjang `S1 -> Sn`, mengikuti **Urutan perhatian Gelombang 1** di bawah
- Pada setiap pemberhentian fungsi, agen WAJIB menyajikan 5 komponen berurutan di chat:
  1. **Kode Asli Bernomor (`Path/File.ext:Lxx-Lyy`)** — blok kode sumber fungsi pada segmen `Sk` secara utuh (tanpa pemotongan barisan kode) agar user membaca kode asli.
  2. **Aliran Nilai & Mutasi State Lokal** — ringkasan faktual apa yang masuk, variabel storage apa yang berubah, dan nilai/field apa yang dikirim ke `Hk` atau `State-Bridge (HB-x)` — sebutkan `Pengendali Field` (Bagian 4) dan `Status Cabang` (`LP-x`, Bagian 8) yang relevan.
  3. **Titik Sensitif Kode Ini (Code Sensitivity Hotspots)** — nomor baris eksak yang wajib diwaspadai beserta alasannya dari kacamata fisika nilai (urutan baca-tulis-panggilan eksternal, arah pembulatan/pembagian, pengakuan nilai masuk `RAW_PARAM` vs `BALANCE_DELTA`, parameter tujuan/kontrak yang dikendalikan pemanggil, asimetri terhadap Twin-Path, atau kondisi `revert`/loop pengunci dana).
  4. **Panduan Invariant & Cara Cek (Candidate Invariant & Mental Check)** — (a) syarat sehat/invariant apa yang harus terjaga pada segmen/handoff ini agar nilai tidak bocor atau terkunci; (b) pertanyaan uji bagaimana mematahkannya lewat input permissionless. Status tetap kandidat analisis; penomoran `INV-` resmi dikunci di akhir D.
  5. **Draf Observasi (`OBS` / `G` / `Q`) & Kontrol Giliran User** — tampilkan pengamatan awal agen lalu berhenti menunggu input user:
     - `lanjut` -> pindah ke segmen `S(k+1)` berikutnya;
     - `cek: <pertanyaan>` -> bedah baris kode terkait atau lakukan `1-hop peek` untuk menjawab pertanyaan user sebelum pindah segmen;
     - `obs: <catatan user>` -> catat temuan/kecurigaan user sebagai `OBS` berlabel `[USER-INSIGHT]` yang wajib dikawal hingga disposisi akhir (dilarang digugurkan tanpa bukti kode penjaga eksak atau uji fork);
     - `auto` -> beralih ke `MODE: AUTO` untuk menyelesaikan sisa segmen pada gelombang/stream aktif secara langsung.

### PAIR — Gelombang 2 (Lazy Skill Augmentation & Perumusan Kartu)

1. Tampilkan rekap `OBS`, `Q` (termasuk `[USER-INSIGHT]`), dan `SYMPTOM-TAGS`, lalu sebutkan 2-4 plugin katalog yang dimuat oleh *Lazy Skill Router*.
2. Terjemahkan poin pemeriksaan dari ke-2 s.d. ke-4 plugin tersebut langsung menunjuk nomor baris kode `S1..Sn` yang baru saja dibaca bersama (bukan kutipan teori abstrak).
3. Diskusikan dan kunci bersama user daftar Invariant resmi (`INV-Sx / Hx / HBx / Jx / Fx` ke `B06-REGISTRY-INVARIANT.md`) dan Kartu Lead rantai `(a)+(b)+(c)` sebelum menulis berkas kanonik `D<NN>-<STR>-<Lk>-WAVE1-BLIND.md`, `WAVE2-QUEUED.md`, dan `LEAD-CARDS.md`.

### Aturan keras yang tetap berlaku penuh di PAIR

- Dilarang membuka katalog pada Gelombang 1; dilarang memberi vonis `TERBUKTI` di Tahap D (semua tetap `DIANALISIS` sampai diuji di Tahap E); hasil akhir berkas `D<NN>-<STR>-<Lk>-*` tetap wajib lulus `python3 tools/verify_flow.py check-d`.
- `[USER-INSIGHT]` adalah observasi berstatus sama dengan `OBS` agen — wajib terdisposisi di Gelombang 2, tidak boleh hilang saat transisi mode.

## Gelombang 1 — Eksplorasi Bebas Murni (Tanpa Katalog)

Bekal: inventaris Lintasan aktif (`C<NN>-<STR>-<Lk>-INVENTORY.md`, termasuk **Bagian 8** yang sudah diisi B8, **Bagian 3** `CY-x`, **Bagian 7** Tabel Selisih), baris `B00-TOPOLOGY.md` untuk domain Lintasan, `C00-SHARED-PRIMITIVES.md`, baris `B07-STATE-BRIDGES.md` yang bersinggungan, premis parent.

**Urutan perhatian Gelombang 1 (bukan filter):**

1. handoff/`HB-x` dengan field `CALLER-INPUT` (atau `DERIVED` dari `CALLER-INPUT`) yang `Asumsi Faktual Konsumen`-nya **tidak dijamin** oleh `Jaminan Faktual Produsen`;
1. `CY-x` (Bagian 3) dengan penerima kendali `CALLER-INPUT` atau `EXTERNAL` yang punya `Storage ditulis SESUDAH` atau `Storage dibaca SESUDAH` **tidak kosong**;
1. baris `BEDA` Tabel Selisih (Bagian 7) di kolom **Autentikasi / Jalur native-wrapped / Transport / Kelas aset**, dan `S0` (Ingress tak resmi) yang dibaca akuntansi;
1. simpul `Fx`/`Jx` pada cabang `LIVE`;
1. sisa segmen pada cabang `LIVE`;
1. cabang `DEAD-CONFIG` — tetap dibaca dan dicatat, tapi kandidat yang **hanya** menyala di cabang ini diarahkan ke `DORMAN` di Gate D.

Urutan ini menentukan **mana yang dikerjakan lebih dulu**, bukan mana yang boleh dilewati. Seluruh segmen, handoff, dan simpul tetap wajib dibaca dan didisposisi.

**LARANGAN MUTLAK:**

- membuka berkas `_ROUTER.md` mana pun atau berkas plugin (`M-*`, `AF-*`, `DOM-*`, `POV-*`, `CHAIN-*`)
- memakai laporan audit lama sebagai sumber hipotesis
- (dihapus dari versi lama) larangan membaca fungsi lintas-klaster **apabila fungsi itu berada di dalam koridor Lintasan aktif** — Aturan Koridor tetap mengikat: dilarang melebar horizontal ke luar garis aliran.

Ikuti kode sepanjang `S1 -> H1 -> S2 -> Sn` berikut rentetan handoffnya dengan **Lima Lensa Fisika Nilai**:

**Lensa 1 (Konservasi Simpul & Akuntansi):** lacak setiap satuan nilai dari `Ingress` hingga `Egress`. Uji apakah pada setiap percabangan (`Fx`) berlaku `total_keluaran + fee == masukan`, dan pada setiap penggabungan/klaim (`Jx`) penanda state mengunci konsumsi tepat satu kali — tanpa celah klaim ulang, pencetakan hak berlebih, atau saldo mengendap permanen.

**Lensa 2 (Adu Kontrak Handoff & State-Bridge):** adu kolom `Jaminan Faktual Produsen` melawan `Asumsi Faktual Konsumen` pada setiap `H1..Hn-1`, dengan memperhatikan kolom `Pengendali Field`: asumsi konsumen atas field `CALLER-INPUT` yang tidak dijamin produsen adalah prioritas pertama. Bila Stream menyentuh `State-Bridge (HB-x)` di `B07-STATE-BRIDGES.md`, **`1-hop peek`** diizinkan (baca tepat satu lapis fungsi pasangan penulis/pembaca di stream seberang) agar ketidaksinkronan skala desimal, urutan pembaruan state, atau nilai basi langsung tertangkap selagi konteks panas.

**Lensa 3 (Selisih Varian & Twin-Path):** sumber utama = **Tabel Selisih Bagian 7 Lintasan aktif** — untuk tiap baris `BEDA`, sandingkan perilaku anggota itu dengan representatif yang dibedah di Bagian 2–6 (tidak perlu menunggu anggota punya inventaris sendiri). Sumber tambahan = pasangan `Twin-Path Group` di `B04` yang sudah punya inventaris `C`: sandingkan tabel Handoff, Simpul, urutan pembaruan state, dan arah pembulatan Lintasan aktif terhadap Lintasan kembarnya; catat setiap asimetri yang tidak dijelaskan oleh perbedaan rumus dasar.

**Lensa 4 (Serah Kendali — `CY-x`):** untuk tiap baris Bagian 3, tanyakan: bila penerima kendali menjalankan kode apa pun yang dia mau (masuk ulang, memanggil fungsi publik lain, revert sengaja), apakah state yang ditulis atau dibaca **sesudah** titik itu bisa menjadi tidak konsisten dengan yang ditulis **sebelum**? Perhatikan `Guard aktif == none`, `Efek bila revert == DITELAN`, dan **read-only reentrancy** (fungsi view yang dibaca pihak lain saat state setengah jadi).

**Lensa 5 (Ingress tak resmi — `S0`):** untuk tiap `S0`, tanyakan: apakah akuntansi **membedakan** nilai masuk resmi dari donasi / force-feed / akrual / callback? Bisakah pihak permissionless menggeser rasio, share pertama, batas, atau saldo pembanding lewat Ingress itu?

### Deep-Check — Tiga Uji Kritis Wajib (Gelombang 1 & 2; berlaku di `MODE: AUTO` maupun memandu peneliti di `MODE: PAIR`)

Dilarang sekadar merangkum ulang tabel Tahap C. Pada setiap Stream, Gelombang 1 **wajib** menjalankan tiga uji kritis berikut dan mencatat hasilnya sebagai `OBS`/`G`/`Q`:

1. **Deep-Check Handoff & State-Bridge:**
   - Uji silang batas ekstrem input (`0`, `1 wei`, batas maksimum tipe, dan ketidaksamaan desimal token seperti `6` vs `18`) antara `Jaminan Faktual Produsen` dan `Asumsi Faktual Konsumen` pada setiap `Hk` dan `HB-x`. Nilai ekstrem dipakai untuk field `CALLER-INPUT`; untuk field `ADMIN-CONFIG` pakai nilai `Nilai @ blok pin` dari Bagian 8.
   - Uji *State Interleaving*: periksa daftar `EP+SM (state_mutator)` di sensus/`B07` dan jawab eksplisit apakah ada fungsi mutator publik atau pengiriman aset langsung yang dapat diselipkan di antara sisi Produsen dan sisi Konsumen — khususnya pada tag `[SEAM]` dan callback.
   - Uji handoff **lintas-domain** (kolom `Lintas-domain?` = `YA`): siapa yang diterima sebagai pengirim sah di domain tujuan (fungsi autentikasi), apakah pesan yang sama bisa diterima **dua kali** atau **di domain lain** (anti-replay), dan apakah urutan/jendela waktu pesan bisa **dibalik**.
2. **Deep-Check Simpul Fork/Join:**
   - Pada setiap `Fx`, tulis persamaan pembagian integer aktual dari kode dan uji apakah pembulatan dapat membuat `jumlah_keluaran > masukan` (menguras saldo pengguna terakhir / insolvensi) atau mengendapkan nilai secara permanen.
   - Pada setiap `Jx`, uji apakah penanda klaim dapat dikelabui lewat pemindahan kepemilikan posisi (`transfer`), penggabungan (`merge`), pemecahan (`split`), atau siklus klaim-setor di blok yang sama.
3. **Deep-Check Twin-Path & Patch-Scar:**
   - Pada setiap pasangan `Twin-Path Group` (terutama bila salah satu sisi ber-tag `[SCAR]` atau `[DELTA]`), buat daftar selisih baris eksak pada penjaga (`require`/`if`), urutan pembaruan state terhadap panggilan eksternal, dan arah pembulatan; uji apakah tambalan di satu jalur lupa diterapkan di jalur kembarnya atau justru memicu penguncian dana baru (*freeze*).

Keluaran wajib Gelombang 1 — `D<NN>-<STR>-<Lk>-WAVE1-BLIND.md`, seluruhnya berlabel `DIANALISIS`:

| Label | Arti |
| :--- | :--- |
| `OBS` | observasi anomali kode bernomor `Path/File.ext:Lxx-Lyy` (fakta kode, belum jalur) |
| `G` | jalur yang terbukti tertutup oleh penjaga kode eksak `Path/File.ext:Lxx-Lyy` |
| `Q` | pertanyaan mekanis tajam / celah asumsi yang harus dipastikan di Gelombang 2 |
| `SYMPTOM-TAGS` | daftar tag gejala faktual yang ditemukan di kode Lintasan aktif untuk memicu pemuatan malas di Gelombang 2 |

Tiap `OBS` dan `Q` mencantumkan `LP-x` yang relevan beserta `Status Cabang`-nya bila observasi bergantung pada parameter.

## Gelombang 2 — Symptom-Triggered Lazy Skill Augmentation

Silang empat hal:

1. **Inversi handoff / State-Bridge** — patahkan jaminan produsen / asumsi konsumen dari `C<NN>`; lengkapi sisi pembaca `HB-x` di `B07`.
2. **Konservasi** — keluaran total vs masukan di tiap simpul fork/join.
3. **Jejak event live** — enumerasi independen, bukan cara kerja utama (pindai log = verifikator terakhir).
4. **Plugin malas berdasarkan gejala** — LIHAT TABEL DI BAWAH.

**LARANGAN MUAT BORONGAN:** dilarang memuat seluruh katalog 52 plugin. Koordinator/pekerja hanya boleh memuat **maksimal 2 sampai 4 berkas plugin spesifik** yang cocok dengan `SYMPTOM-TAGS` dari Gelombang 1 (ditambah maksimal 1 berkas `CHAIN-*` sesuai arsitektur rantai target dan maksimal 1 berkas `DOM-*` sesuai domain protokol bila relevan).

### Lazy Skill Router (tabel pemetaan gejala -> plugin)

Lokasi nyata berkas plugin (rujuk path berikut saat memuat):
- `<AF-*>` : `methodology/attack-forms/`
- `<CHAIN-*>` : `references/chains/`
- `<M-*>` : `references/methods/`
- `<POV-*>` : `references/pov/`
- `<DOM-*>` : `methodology/domains/`

| Gejala di kode (dari `SYMPTOM-TAGS`) | Plugin yang dimuat |
| :--- | :--- |
| pembagian integer, konversi share/asset, pembulatan biaya, pemecahan transaksi | `AF-02-precision-slicing-dust-splitting.md`, `POV-MATH-02-inverse-rounding-fee-truncation.md`, `M-007-metamorphic-split-vs-bulk-asymmetry.md`, `CHAIN-rounding-amplification-drain.md` |
| pool/vault baru, saldo awal nol, donasi langsung, manipulasi batas pertama/terakhir, Ingress `PASSIVE` `S0` (`balanceOf(this)` dibaca akuntansi) | `AF-01-flash-liquidity-donation-inflation.md`, `AF-03-boundary-zero-first-last-manipulation.md` |
| indeks akrual, snapshot distribusi, pencatatan utang/imbal hasil lintas waktu | `POV-MATH-01-accrual-index-desync.md`, `M-006-stale-snapshot-aliasing.md`, `CHAIN-shared-state-desync.md` |
| panggilan eksternal di tengah fungsi, callback/hook, subcall, multicall, `CY-x` tanpa guard dengan tulis-sesudah | `AF-04-reentrancy-callback-cpi-interleaving.md`, `POV-CALL-01-state-desync-control-handoff.md`, `POV-CALL-02-subcall-state-divergence.md`, `POV-EVM-01-multicall-context-reuse.md`, `M-008-caller-callee-seam.md`, `CHAIN-reentrancy-valuation.md` |
| pemisahan dua transaksi (`request -> execute`), antrean publik, relayer/keeper, urutan state bersama | `AF-05-shared-state-ordering-sandwich.md`, `AF-09-asymmetric-griefing-queue-bricking.md`, `AF-10-offchain-relayer-desync-arbitrage.md`, `M-009-suspended-lifecycle-state.md`, `POV-relayer-mev.md` |
| pembacaan harga/valuasi, likuidasi, batas jaminan | `AF-06-oracle-price-liquidation-cascade.md`, `POV-DEFI-01-self-liquidation-bad-debt.md`, `POV-DEFI-02-valuation-source-execution-sink.md`, `CHAIN-flash-oracle-liquidation.md` |
| tanda tangan, bukti Merkle, otorisasi objek/kapabilitas, status pasca-upgrade | `AF-07-account-object-capability-spoofing.md`, `AF-08-signature-proof-replay-malleability.md`, `M-010-live-residual-state-post-upgrade-drift.md`, `CHAIN-offchain-sign-onchain-mutate.md` |
| pesan lintas-domain, autentikasi messenger/alias, bukti light-client, relay L1→L2/L2→L1 | `AF-07-account-object-capability-spoofing.md`, `AF-08-signature-proof-replay-malleability.md`, `AF-10-offchain-relayer-desync-arbitrage.md`, `M-008-caller-callee-seam.md` |
| **Stream ber-tag `[SCAR]` (patch scar — Post-Audit Hot-Zone)** | **wajib sertakan `M-004-patch-scar-view-write-asymmetry.md`** |
| **Stream ber-tag `[SEAM]` (cross-audit scope seam — Post-Audit Hot-Zone)** | **wajib sertakan `M-008-caller-callee-seam.md`** |

**Anti-anchoring tetap mutlak:** bila anomali dari Gelombang 1 tidak cocok dengan plugin mana pun, beri label `[NOVEL / NO-CATALOG]`; **dilarang keras menggugurkan kandidat karena tidak ada di katalog**. Temuan di luar katalog = kandidat plugin baru.

Keluaran Gelombang 2 — `D<NN>-<STR>-<Lk>-WAVE2-QUEUED.md`: kandidat `QUEUED` (terurut ketajaman struktural, lihat di bawah) + `DORMAN` (hanya bila gagal Gate D C10-v2, dengan syarat buka-ulang konkret) + disposisi `Q`/SYMPTOM-TAGS.

### Urutan QUEUED menuju Tahap E (B2a-v2 Lapis 2 — ketajaman struktural)

Urutkan kartu di dalam Lintasan aktif menurut ketajaman struktural:

1. **`INV-Jx` / `INV-Fx` / `INV-Vx`** — kegagalan konservasi simpul fork/join, komposisi multi-segmen, atau selisih varian yang menyentuh nilai/autentikasi;
2. **`INV-Hx` / `INV-HBx` / `INV-CYx` / `INV-INx`** — patahan kontrak handoff, ketidaksinkronan `State-Bridge`, ketidakkonsistenan saat serah kendali, atau Ingress tak resmi yang tidak dibedakan akuntansi;
3. **`INV-Sx`** — anomali lokal satu segmen, urut `S1 -> Sn`.

Urutan **antar-Lintasan** di dalam satu Stream mengikuti arah aliran (`Ingress → Egress`); urutan **antar-Stream** tetap B2a (pintu masuk pertama kali). EV live tidak dipakai sebagai penentu urutan; boleh dicatat sebagai data pendukung.

> Catatan jujur: label `P1–P5` yang dipakai di beberapa berkas adalah kosakata warisan katalog dan **tidak punya definisi di methodology repo ini**. Jangan mengarang definisinya. Kalau user meminta label prioritas, minta definisinya lebih dulu.

## Kartu lead (C11) + Invariant Tiga Lapis + State-Bridge (B12)

### Kartu lead (1:1 dari QUEUED)

Tiap kartu **wajib punya klaim finansial sendiri** — bukan "ini mencurigakan", tapi "kalau ini pecah, X unit nilai berpindah dari A ke B".

**C11 mengikat bentuk kartu:** kartu merumuskan rantai **(a)+(b)+(c)** sebagai **satu rantai** yang akan diuji utuh di Tahap E:

- (a) pelanggaran invariant pada `File:Lxx-Lyy`;
- (b) jalur rambatan antar-fungsi/segmen menuju perubahan hak/saldo;
- (c) rumus plafon kerugian finansial >= $1 (angka, bukan perkiraan).

Kartu yang hanya berhenti di (a) = **HIPOTESIS**, bukan kandidat uji.

Tiap kartu juga mencantumkan **daftar `LP-x` yang dipakai rantainya** beserta `Nilai @ blok pin` dan `Status Cabang`-nya — ini bahan seed `FlowFixtures` di Tahap E.

Dua kolom wajib tambahan (v2.1):

- **Lintasan rambatan** — Lintasan tempat (b)/(c) terjadi bila **berbeda** dari Lintasan pelanggaran (a). Kartu ditulis di Lintasan tempat pelanggaran terjadi; `1-hop peek` ke Lintasan tetangga diizinkan **sebatas fungsi yang dilalui rantai**.
- **Anggota varian berlaku** — daftar anggota (dari Tabel Selisih Bagian 7) yang diduga terdampak: `REPRESENTATIF` saja, atau tambah anggota berstatus `SAMA` / `BEDA:<kolom>`. **Bukan klaim**; diuji atau dilabeli di Tahap E.

### Invariant tiga lapis

| Lapis | ID | Cakupan |
| :--- | :--- | :--- |
| L1 | `INV-Sx` | di dalam segmen |
| L2 | `INV-Hx`, `INV-Jx`, `INV-HBx`, `INV-CYx`, `INV-INx` | di handoff, di simpul, di State-Bridge, di titik serah kendali, dan di Ingress tak resmi |
| L2/L3 | `INV-Vx` | keseragaman perilaku antar-anggota varian (dari Tabel Selisih) |
| L3 | `INV-Fx` | ujung-ke-ujung / komposisi |

**Subtipe `INV-HBx` (State-Bridge):** mendampingi `INV-Hx` dan `INV-Jx` pada Lapis L2; mencatat invarian sinkronisasi atas variabel storage yang ditulis satu Lintasan dan dibaca Lintasan lain secara asinkron (dari `B07-STATE-BRIDGES.md`, kolom `Writer_Lintasan_&_Guarantee` vs `Reader_Lintasan_&_Assumption`, plus `Window_&_Trigger`). Satu penomoran global di `B06-REGISTRY-INVARIANT.md`.

Aturan wajib per invariant:

- **Wajib mencantumkan sumbernya**: field kontrak handoff, atau baris `docs`/NatSpec. **Bukan** perasaan agen.
- **Wajib punya akibat finansial bila pecah** — invariant tanpa akibat finansial bukan invariant, itu catatan.
- Cek **testability** dicatat saat perumusan: fork apa, data live apa (rujuk `LP-x`); dilabeli bila tidak bisa diuji.
- Registry invariant **satu penomoran global** (`B06`), diisi mulai Tahap D. Kartu wajib merujuk ID bernomor (mis. `INV-H3`), bukan placeholder `INV-Hx`.

## Gate D (C10-v2, statis) — gerbang masuk Tahap E

**Gate D diuji statis di akhir Gelombang 2, SEBELUM PoC Tahap E; eksekusi fork adalah verifikasi Gate E di Tahap E.** Kandidat masuk `QUEUED` menuju Tahap E bila secara desain kode + bacaan state blok pin terbukti:

1. pemicu **permissionless** (atau *unprivileged state poisoning* yang dieksekusi rutin oleh keeper normal);
2. state prasyarat **reachable** lewat transaksi operasi normal — tanpa `vm.store`/role admin;
3. lulus **B8 live-match (L1–L4)**. Jalur `FORK_DEPLOYED_HEAD` hanya boleh dipakai bila B8 membuktikan kontrak/fungsi koridor BELUM ter-deploy (`cast code` = 0x, atau fungsinya tidak ada di sumber deployed). Bukti itu wajib dilampirkan;
4. rumus plafon potensial terukur **>= $1**.

**Konsekuensi penting:** plafon live 0 **TIDAK** membuat lead DORMAN — nilai 0 di live hanya berarti pemicunya belum terjadi.

`DORMAN` **hanya** untuk fitur live yang sedang dikunci saklar konfigurasi admin aktif (`paused`, `cap == 0` admin), wajib disertai **syarat buka-ulang konkret** (mis. "buka bila saklar X diangkat", "buka bila parameter Y diubah").

- Kandidat yang hanya bisa dipicu lewat cabang `DEAD-CONFIG` di Bagian 8 = `DORMAN`, dengan syarat buka-ulang menunjuk `LP-x` (mis. "buka bila `LP-3 feeBps` > 0"). Kandidat pada cabang `LIVE` dinilai normal. Kandidat yang **rantainya bergantung** pada `LP-x` pengendali nilai berstatus `UNVERIFIED` → status **`TUNDA-VERIFIKASI`** (bukan `QUEUED`, bukan `DORMAN`), dicatat di `B05` beserta `LP-x` penghambatnya; status **otomatis dibuka** menjadi kandidat Gate D begitu `LP-x` terbaca. **Kandidat lain di Lintasan yang sama tetap boleh `QUEUED`.**
- Nilai `ADMIN-CONFIG` yang dipakai dalam rumus plafon (c) wajib nilai dari Bagian 8 kolom `Nilai @ blok pin`, bukan asumsi.

## C11 — gelombang 1 dan 2 TIDAK memberi verdict TERBUKTI

Konsekuensi yang sering dilanggar:

- Gelombang 1/2 **tidak boleh** menyimpulkan `TERBUKTI`.
- Tiap observasi/jawaban dilabeli **`DIANALISIS`**.
- Wajib mencatat **alur terkait apa yang masih kurang** menuju kerugian terukur.
- `TERBUKTI` hanya boleh datang dari Tahap E yang menguji rantai (a)+(b)+(c) utuh.

## Aturan mengikat lain

- **Bahasa brief: verifikasi invariant, bukan bahasa serangan.** Brief Tahap E memakai bahasa verifikasi.
- **Tugas agen dibatasi KORIDOR LINTASAN, bukan klaster** — wajib menembus batas klaster sepanjang koridor Lintasan aktif (Aturan Koridor, `Corridor-Bound Cross-Cluster`); dilarang melebar horizontal ke luar garis aliran nilai.
- **Deep-run per jalur**: satu perintah berdiri hulu→hilir sampai verdict per lead, tanpa tap antar langkah.
- **`/stop` mencabut otorisasi seketika** — hentikan subagent, tulis nol berkas.

## Keluaran

- `C<NN>-<STR>-<Lk>-INVENTORY.md` Bagian 8 — kolom `Nilai @ blok pin` + `Status Cabang` terisi oleh B8.
- `D<NN>-<STR>-<Lk>-WAVE1-BLIND.md` — OBS / G / Q / SYMPTOM-TAGS, semua berlabel `DIANALISIS`.
- `D<NN>-<STR>-<Lk>-WAVE2-QUEUED.md` — QUEUED terurut ketajaman struktural + DORMAN (dengan syarat buka-ulang) + disposisi OBS/Q.
- `D<NN>-<STR>-<Lk>-LEAD-CARDS.md` — kartu 1:1 dengan rantai (a)+(b)+(c) + klaim finansial >= $1 + daftar `LP-x` yang dipakai.
- Registry invariant (`B06-REGISTRY-INVARIANT.md`) terisi dengan sumber tiap invariant (termasuk `INV-HBx`).

## Definition of done Tahap D (per Lintasan)

- [ ] B8 Live-Match Lintasan lulus **per domain segmen** (atau Lintasan masuk `TUNDA-LIVE` di `B05`, nol waktu eksekusi)
- [ ] **Bagian 8** inventaris Lintasan terisi kolom nilai + status cabang oleh B8 **di domain yang benar**; nol `DIISI_B8` tersisa
- [ ] gelombang 1 dijalankan **tanpa** membuka katalog/_ROUTER/plugin/laporan audit lama, mengikuti Urutan perhatian Gelombang 1
- [ ] **Lima Lensa** dijalankan: konservasi simpul, adu handoff+State-Bridge (1-hop peek bila perlu), selisih varian (Tabel Selisih + Twin-Path), serah kendali `CY-x`, Ingress tak resmi `S0`
- [ ] gelombang 2 memuat maks 2-4 plugin via Lazy Skill Router; 1 CHAIN-\* dan 1 DOM-\* bila relevan
- [ ] tiap QUEUED punya kartu lead dengan rantai (a)+(b)+(c), rumus plafon >= $1, dan daftar `LP-x` yang dipakai
- [ ] tiap invariant punya sumber (field handoff/state-bridge atau docs/NatSpec) + akibat finansial + catatan fork-testability
- [ ] Gate D C10-v2 diuji untuk tiap kandidat; DORMAN hanya saklar admin aktif atau cabang `DEAD-CONFIG`, dengan syarat buka-ulang menunjuk `LP-x`
- [ ] seluruh OBS dan Q habis terdisposisi (QUEUED / DORMAN / G dengan jangkar penjaga kode eksak) — anti-kuota: tidak ada target jumlah
- [ ] **disposisi Lintasan:** ≥ 1 kartu, ATAU `NIHIL_KANDIDAT:` yang menyebut **tiap segmen** beserta jangkar penjaga atau alasan kode (bukan kalimat umum) — ini **disposisi, bukan kuota kartu**
- [ ] **disposisi Tabel Selisih:** tiap baris `BEDA` di kolom nilai/autentikasi punya kartu ATAU `G` dengan jangkar penjaga eksak yang menutup jalurnya di anggota itu
- [ ] **disposisi `CY-x`:** tiap `CY-x` dengan tulis-sesudah tidak kosong DAN guard `none` punya kartu ATAU `G` dengan alasan kode (mis. penerima `IMMUTABLE`, state sesudah tidak dipakai jalur nilai)
- [ ] kandidat bergantung `LP-x` `UNVERIFIED` tercatat **`TUNDA-VERIFIKASI`** di `B05`, bukan dibuang dan bukan `QUEUED`
- [ ] kartu yang rambatannya di Lintasan lain mengisi kolom **Lintasan rambatan**
- [ ] nol verdict `TERBUKTI` dari gelombang 1/2; semua berlabel `DIANALISIS`
- [ ] nol PoC (itu Tahap E)
