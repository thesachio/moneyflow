---
name: flow-c-inventory
description: "Tahap C — Stream-Slice Inventory (moneyflow v2.0). Dua mode terstruktur: C00-SHARED-PRIMITIVES (sekali di awal) + C<NN>-<STREAM_ID>-INVENTORY per Stream ujung-ke-ujung dengan Aturan Koridor Stream (Corridor-Bound Cross-Cluster), format segmen/handoff/simpul/State-Bridge/Lembar Parameter Live lengkap, murni deskriptif — tanpa invariant, tanpa buruan, tanpa PoC. Dipakai saat memetakan Stream/klaster, atau saat user menyebut tahap C, pemetaan mendalam, inventaris alur."
---

# Skill flow-c-inventory — Tahap C (Stream-Slice Inventory)

Tahap C membangun **yang riil/teramati** per Stream: inventaris alur + segmentasi + kontrak handoff **deskriptif** (apa kata kode, bukan apa yang seharusnya) + daftar parameter yang dibaca koridor. Klaster = papan kontrol indeks Tahap B; **Stream = unit kerja** — satu aliran nilai ujung-ke-ujung (`Ingress` → `State/Share Accounting` → `Egress`), moneyflow v2.0.
Skill ini memuat format dan aturan sampai Tahap C selesai.
## Dua mode terstruktur

**Mode Pra-Stream (`C00-SHARED-PRIMITIVES.md`) — dijalankan SEKALI sebelum `STR-01` dimulai.** Petakan seluruh unit bertipe `SHARED-PRIMITIVE` dari `B04-STREAMS-AND-CLUSTERS.md`. Untuk tiap primitif catat **secara deskriptif**: lokasi `Path/File.ext:Lxx-Lyy`; fungsi konversi/akuntansi (mis. wrap/unwrap, mint/redeem, share↔aset); arah pembulatan dan satuan desimal; perubahan state/saldo yang ditulisnya; event yang diemisikan. Inventaris ini **dirujuk semua Stream** — tidak diulang per Stream.

**Mode Utama (`C<NN>-<STREAM_ID>-INVENTORY.md`) — dijalankan satu Stream ujung-ke-ujung per putaran**, mengikuti urutan `B2a` dari `B04` / `B05`.
 `methodology/aturan-alur-first.md` (seksi D — Tahap C) hanya rujukan sengketa.

## Aturan Koridor Stream (`Corridor-Bound Cross-Cluster`)

- Kerja **satu Stream (`STR-nn`) saja per putaran**. Bukan dua, bukan "sekalian".
- Urutan kerja = **pintu masuk pertama kali** (B2a, diputus 17 Nov 2026; B2a-v2 moneyflow v2.0): entrypoint paling awal yang dilalui pengguna dikerjakan lebih dulu, bukan EV live. Kalau user memerintah urutan lain, catat alasannya di `B04-STREAMS-AND-CLUSTERS.md`.
- Mulai dari entrypoint Stream aktif: lakukan **langkah perluasan warisan/implementasi** (konvensi B14.6 & B14.7) dan **penguraian dispatcher `unknown`** (B14.4) bila entrypoint melewatinya.
- Ikuti aliran uang/nilai dari `Ingress` → `Accounting/Transform` → `Egress` **secara vertikal** sampai aliran nilai pada transaksi/siklus tersebut tuntas.
- **WAJIB TEMBUS KLASTER SEPANJANG KORIDOR:** bila Segmen `S(k)` memanggil kontrak di klaster `CORE-FLOW` lain sebagai bagian langsung dari aliran nilai itu, **baca badan fungsi target tersebut dan jadikan `S(k+1)`** di berkas `C<NN>-<STREAM_ID>-INVENTORY.md` ini juga; tandai EP+VM tersebut selesai dipetakan di `B05-LEDGER-SISA.md` (`TERPETAKAN_DI_<STREAM_ID>`).
- **LARANGAN MELEBAR HORIZONTAL:** dilarang membaca atau menginventarisasi fungsi lain di kontrak/klaster seberang yang **tidak dipanggil** dan **tidak dilalui** oleh koridor Stream aktif.
- **JEMBATAN ASINKRON (`State-Bridge`):** bila aliran nilai berhenti di penyimpanan state (mis. pengguna mencatat deposit/request/stake ke variabel storage `V`, sementara pencairan/eksekusi/distribusi dilakukan di transaksi terpisah oleh pengguna/keeper/aktor lain pada Stream berbeda) — **hentikan segmen di penulisan `V`**, lalu **wajib daftarkan/perbarui baris `HB-x` di `B07-STATE-BRIDGES.md`**: tulis variabel `V`, lokasi kode penulis, dan jaminan faktual penulis dari kode. Sebaliknya, bila Stream aktif adalah **pembaca** variabel `V` yang sudah ada di `B07`, lengkapi kolom pembaca dan asumsi faktual pembacanya di `B07`.
- Pada Tahap D, koridor ini membuka hak **`1-hop peek`**: membaca tepat fungsi pembaca/penulis pasangan `HB-x` agar kecocokan jaminan penulis vs asumsi pembaca diuji saat konteks masih panas.

## Keluaran

| Berkas | Isi |
| :--- | :--- |
| `C00-SHARED-PRIMITIVES.md` | inventaris deskriptif seluruh unit `SHARED-PRIMITIVE` (sekali di awal Tahap C, sebelum Stream pertama) |
| `C<NN>-<STREAM_ID>-INVENTORY.md` | inventaris Stream itu (identitas + segmen + handoff + simpul + State-Bridge + referensi C00 + Lembar Parameter Live) |

## Format wajib: 6 bagian per `C<NN>-<STREAM_ID>-INVENTORY.md` (murni deskriptif - apa kata kode, nol invariant, nol klaim bug, nol PoC)

### Bagian 1 - Identitas Stream & Cakupan EP+VM

- `Stream_ID` (`STR-nn`);
- pintu masuk utama (`Path/File.ext:Lxx-Lyy`);
- daftar seluruh `EP+VM` (termasuk lintas-klaster) yang tercakup Stream ini;
- rujukan `Twin-Path Group` bila ada di `B04`.

### Bagian 2 - Segmen (S1..Sn)

Tiap segmen = potongan alur yang **bisa diamati** di handoff. Untuk tiap segmen tulis:

| Kolom | Isi |
| :--- | :--- |
| ID | `S1`, `S2`, dan seterusnya hingga `Sn` |
| Nama segmen | ringkas, 1 baris |
| Fungsi & Jangkar Eksak | `Path/File.ext:Lxx-Lyy` - satu baris per fungsi yang terlibat |
| Batas masuk | apa yang menandai segmen mulai (event, perubahan state, pesan, waktu) |
| Batas keluar & efek saldo/state | apa yang menandai segmen selesai + efeknya ke saldo/state |
| Aktor pemicu | siapa yang bisa memicu (user / keeper / relayer / admin / otomatis) |

Keluaran `S(k)` wajib **nyambung ke masukan `S(k+1)`**. Bila tidak bersambung lewat pemanggilan langsung, itu kandidat **State-Bridge** (`HB-x`, Bagian 5) - bukan handoff langsung.

### Bagian 3 - Kontrak Handoff (`H1..Hn-1`) (B11)

Dienumerasi **ketat dari batas unit**: satu handoff per sambungan langsung antar-segmen. Rantai linear atau bercabang tanpa penggabungan ulang: `N` segmen -> **tepat `N-1` handoff**. Bila ada Join `Jx` yang menerima `m` cabang masukan dari segmen berbeda di Stream ini: jumlah handoff = `N - 1 + Σ(m - 1)` atas semua `Jx` tersebut. Jangan dilabeli tangan.

| Kolom | Isi |
| :--- | :--- |
| ID | `H1`, `H2`, dan seterusnya hingga `Hn-1` |
| Produsen (Segmen + Fungsi:Baris) | segmen + fungsi + baris yang menulis |
| Konsumen (Segmen + Fungsi:Baris) | segmen + fungsi + baris yang membaca |
| Field/Nilai Diteruskan | **nama + tipe + satuan/desimal** (mis. `uint128 amount`, 18 desimal) |
| Pengendali Field | per field: `CALLER-INPUT` / `ADMIN-CONFIG` / `DERIVED(<sumber>)` / `EXTERNAL-ORACLE` — siapa yang menentukan nilainya **menurut kode** |
| Jaminan Faktual Produsen di Kode | apa yang produsen pastikan (mis. "amount sudah dikurangi fee") - **apa adanya di kode** |
| Asumsi Faktual Konsumen di Kode | apa yang konsumen anggap benar (mis. "amount <= saldo kontrak") - **apa adanya di kode** |
| Status | `TERTUTUP` / `TERBUKA_EKSTERNAL` |

Definisi `Pengendali Field` (deskriptif, dari kode):

- `CALLER-INPUT` — nilai berasal langsung dari parameter/calldata/`msg.value`/token yang dipilih pemanggil permissionless.
- `ADMIN-CONFIG` — nilai dibaca dari storage yang hanya bisa ditulis peran istimewa (owner/admin/governance/role).
- `DERIVED(<sumber>)` — hasil hitung dari field lain; sebut sumbernya, mis. `DERIVED(amount, feeBps)`. Bila salah satu sumber `CALLER-INPUT`, tulis eksplisit.
- `EXTERNAL-ORACLE` — dibaca dari kontrak eksternal (oracle, pool, messenger) yang tidak dikendalikan kode scope.

Satu field bisa punya lebih dari satu pengendali (mis. `DERIVED(CALLER-INPUT amount, ADMIN-CONFIG feeBps)`); tulis semuanya, jangan dipilih salah satu.

Handoff `TERBUKA_EKSTERNAL` = konsumennya di luar kode scope (mis. messenger eksternal, `EXTERNAL-BOUNDARY` di `B04`). Tetap **dienumerasi**, jangan dihapus, jangan ditutup sepihak.

### Bagian 4 - Simpul (`Fx` Fork / `Jx` Join)

Unit mandiri **berprioritas tinggi** - bukan catatan kaki segmen.

- **Fork (`Fx`)** = percabangan aliran: catat **rumus pembagian aliran & potongan biaya sebagaimana tertulis di kode** (nanti diuji: keluaran total = masukan - fee).
- **Join (`Jx`)** = penggabungan/klaim: catat **penanda state yang mencegah konsumsi ganda sebagaimana tertulis di kode** (nanti diuji: konsumsi tepat sekali - tidak dobel, tidak hilang). Tulis juga baris `Masukan: S<a>, S<b>, ...` (segmen-segmen yang bertemu di Join ini) — dipakai untuk menghitung jumlah handoff.

### Bagian 5 - Daftar State-Bridge (`HB-x`) & Referensi Primitif (`C00`)

- Daftar **jembatan storage asinkron** yang disentuh Stream ini - **sinkron dengan `B07-STATE-BRIDGES.md`** (baris `HB-x` yang sama; kolom baku: `Bridge_ID | Storage_Var_&_Contract | Writer_Stream_&_Guarantee | Reader_Stream_&_Assumption | Sync_Status`).
- Daftar item `C00-SHARED-PRIMITIVES.md` yang dipakai segmen-segmen Stream ini.

### Bagian 6 - Lembar Parameter Live (`LP-x`)

Daftar **setiap variabel storage dan nilai eksternal yang dibaca** fungsi di koridor Stream aktif dan memengaruhi aliran nilai: penjaga (`require`/`if`), rumus, rate, fee, cap, flag pause, whitelist/allowlist, alamat tujuan/adapter, sumber oracle. Murni deskriptif — Tahap C mengisi kolom kode; kolom nilai live diisi di **B8 Live-Match Stream** (awal Tahap D).

| Kolom | Diisi di | Isi |
| --- | --- | --- |
| ID | C | `LP-1`, `LP-2`, dan seterusnya |
| Variabel & Jangkar Baca | C | nama variabel + `Path/File.ext:Lxx-Lyy` tempat dibaca di koridor |
| Kontrak | C | kontrak pemilik storage (alamat live diisi di B8) |
| Pengendali | C | `ADMIN-CONFIG` / `DERIVED(<sumber>)` / `EXTERNAL-ORACLE` / `CALLER-INPUT` (definisi sama dengan Bagian 3) |
| Penulis di Kode | C | fungsi + `Path/File.ext:Lxx-Lyy` yang menulis variabel ini, + peran yang bisa memanggilnya |
| Cabang yang Bergantung | C | segmen/handoff/simpul yang perilakunya berubah karena nilai ini (`S2`, `H3`, `F1`) |
| Nilai @ blok pin | B8 | hasil `cast call` / `cast storage` pada blok pin; tulis `DIISI_B8` di Tahap C |
| Status Cabang | B8 | `LIVE` / `DEAD-CONFIG` / `TIDAK-TERBACA`; tulis `DIISI_B8` di Tahap C |

Arti `Status Cabang`:

- `LIVE` — nilai live membuat cabang itu bisa dilalui transaksi normal.
- `DEAD-CONFIG` — nilai live membuat cabang tidak bisa dilalui (mis. `paused == true`, `feeBps == 0` untuk cabang fee, token tidak di-whitelist, `cap == 0`, adapter `address(0)`).
- `TIDAK-TERBACA` — nilai tidak bisa dibaca andal di blok pin; diperlakukan sama dengan `LIVE` (bukan alasan menunda).

Aturan Bagian 6:

- **Bukan filter.** Cabang `DEAD-CONFIG` tetap ada di Bagian 2–5; Bagian 6 hanya menandai. Larangan filter di dalam Stream tetap berlaku.
- Variabel `CALLER-INPUT` dicatat agar Tahap D/E tahu field mana yang **bebas diisi** (termasuk nilai ekstrem); variabel `ADMIN-CONFIG` dicatat agar Tahap D/E **memakai nilai live**, bukan nilai karangan.
- Bila satu variabel dibaca di beberapa tempat di koridor, cukup satu baris `LP-x` dengan semua jangkar baca disebut.
- Nol penilaian bahaya, nol invariant — tetap deskriptif.

## Yang TIDAK dilakukan di Tahap C

1. Menulis invariant — itu Tahap D (B12). Invariant = klaim asumsi tentang apa yang *seharusnya* berlaku, bukan fakta teramati.
2. Buruan saat memetakan.
3. PoC / verifikasi / verdict.
4. Menutup handoff yang konsumennya di luar kode tanpa keputusan user.
5. Menilai klaster/Stream ("ini bersih", "ini berbahaya") — itu Tahap G.
6. Filter di dalam Stream (hanya mengambil data yang dibutuhkan alur live) — dinilai berisiko, tidak diadopsi. Filter yang aman hanya utuh per Stream. Bagian 6 menandai, bukan menyaring.
7. Melebar horizontal — membaca/menginventarisasi fungsi lain di kontrak/klaster seberang yang tidak dipanggil dan tidak dilalui koridor Stream aktif. Menembus klaster HANYA sepanjang koridor (lihat Aturan Koridor Stream).

7. Mengisi kolom `Nilai @ blok pin` / `Status Cabang` di Bagian 6 — itu B8 di awal Tahap D.

## Definition of done Tahap C

**Pra-Stream (sekali):**

- [ ] `C00-SHARED-PRIMITIVES.md` lengkap: seluruh unit `SHARED-PRIMITIVE` dari `B04` terpetakan — lokasi `File:Lxx-Lyy`, fungsi konversi/akuntansi, arah pembulatan + desimal, perubahan state/saldo, event

**Per-Stream (`C<NN>-<STREAM_ID>-INVENTORY.md`):**

- [ ] Bagian 1 Identitas: `Stream_ID` + pintu masuk (`File:Lxx-Lyy`) + daftar EP+VM (termasuk lintas-klaster) + rujukan Twin-Path bila ada
- [ ] Bagian 2 Segmen: semua segmen punya batas masuk/keluar dan bersambung — keluaran `S(k)` nyambung ke masukan `S(k+1)` (atau berakhir di State-Bridge `HB-x`)
- [ ] Bagian 3 Handoff: jumlahnya sesuai rumus Bagian 3 (`N−1`, ditambah `Σ(m−1)` bila ada Join bercabang-masuk), tiap handoff punya field (nama+tipe+satuan) + `Pengendali Field` per field + jaminan produsen + asumsi konsumen + Status
- [ ] Bagian 4 Simpul: tiap `Fx` punya rumus pembagian + potongan biaya; tiap `Jx` punya penanda anti-konsumsi-ganda — apa adanya di kode
- [ ] Bagian 5: semua `HB-x` yang disentuh sinkron dengan `B07-STATE-BRIDGES.md` (pembaca/penulis + asumsi/jaminan terisi untuk sisi Stream aktif); item `C00` yang dipakai terdaftar
- [ ] Bagian 6 Lembar Parameter Live: tiap variabel storage/eksternal yang dibaca di koridor dan memengaruhi aliran nilai terdaftar sebagai `LP-x` dengan jangkar baca + pengendali + penulis + cabang yang bergantung; kolom nilai = `DIISI_B8`
- [ ] koridor: fungsi lintas-klaster di garis aliran sudah masuk sebagai `S(k+1)`; nol pelebaran horizontal
- [ ] nol invariant, nol buruan, nol PoC
- [ ] `B05-LEDGER-SISA.md` diperbarui: semua EP+VM koridor ini berstatus `TERPETAKAN_DI_<STREAM_ID>` (sisa menyusut)
- [ ] `B07-STATE-BRIDGES.md` diperbarui bila Stream menyentuh/membaca jembatan state
