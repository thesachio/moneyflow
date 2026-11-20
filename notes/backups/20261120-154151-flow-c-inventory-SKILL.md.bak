---
name: flow-c-inventory
description: Tahap C — Stream-Slice Inventory per Lintasan (moneyflow v2.1). C00-SHARED-PRIMITIVES sekali di awal + C<NN>-<STR>-<Lk>-INVENTORY per Lintasan dengan Aturan Koridor (Corridor-Bound Cross-Cluster). Segmen dibatasi 5 pemicu B19 + anggaran Segmen/Lintasan; format 9 bagian — identitas, segmen (termasuk Ingress S0), Titik Serah Kendali CY-x, handoff, simpul, State-Bridge (enum + window), Tabel Selisih Varian, Lembar Parameter Live per domain (UNVERIFIED), rekonsiliasi ledger. Murni deskriptif — tanpa invariant, buruan, PoC. Dipakai saat memetakan Stream/Lintasan, atau saat user menyebut tahap C, pemetaan mendalam, inventaris alur.
---

# Skill flow-c-inventory — Tahap C (Stream-Slice Inventory per Lintasan) — moneyflow v2.1

Tahap C membangun **yang riil/teramati** per Lintasan: segmen + titik serah kendali + kontrak handoff **deskriptif** (apa kata kode, bukan apa yang seharusnya) + selisih varian + parameter yang dibaca koridor.

Hierarki unit (B19): **Stream** (siklus hidup nilai, indeks cakupan) ⊃ **Lintasan** (unit kerja satu sesi C→D→E) ⊃ **Segmen** (unit buruan) ⊃ fungsi (unit sensus).
Mode topologi dari `B00-TOPOLOGY.md` menentukan bentuk Lintasan; format dan gerbang di skill ini sama untuk semua mode.

## Dua mode kerja

**Pra-Stream (`C00-SHARED-PRIMITIVES.md`) — sekali, sebelum Lintasan pertama.** Petakan seluruh unit `SHARED-PRIMITIVE` dari `B04`. Per primitif (deskriptif): lokasi `File:Lxx-Lyy`; fungsi konversi/akuntansi (wrap/unwrap, mint/redeem, share↔aset); arah pembulatan + desimal; state/saldo yang ditulis; event; **titik serah kendali di dalam primitif** (mis. `safeTransfer` ke token ber-hook, `call{value}`) — supaya Lintasan konsumen cukup merujuk `C00-Uxx/CY`, tidak mengulang.

**Utama (`C<NN>-<STR>-<Lk>-INVENTORY.md`) — satu Lintasan per putaran/sesi**, urutan `B2a` dari `B04`/`B05`.

## Langkah 0 — Tetapkan batas Lintasan (sebelum menulis segmen)

1. Ambil usulan Lintasan dari `B04`. Lakukan **perluasan warisan/implementasi** (B14.6/B14.7) dan **penguraian dispatcher `unknown`** (B14.4) untuk entrypoint Lintasan.
2. Ikuti aliran nilai `Ingress → Accounting → Egress` secara vertikal; tandai pemicu batas (Langkah 1) di sepanjang jalan.
3. Hitung anggaran:

| Unit | Batas bawah | Batas atas |
| --- | --- | --- |
| Segmen | ≥ 1 pemicu batas | ≤ 4 fungsi dibaca langsung |
| Lintasan | ≥ 1 perpindahan nilai + ≥ 1 batas kepercayaan | 4–8 segmen; ≤ 12 fungsi dibaca langsung (rujukan C00 tidak dihitung); 1 keluarga varian |

4. Lewat batas atas → **pecah sebelum menulis**: per fase (masuk / akuntansi / keluar) atau per sisi domain (kirim / terima). Di bawah batas bawah → gabung dengan Lintasan tetangga dalam Stream yang sama. Catat keputusan pecah/gabung di Bagian 1 + koreksi `B04`.
5. Lintasan menyentuh > 1 anggota varian (`VK`/`VC`/`DOM` dari B00) → pilih **satu representatif** per keluarga untuk dibedah; anggota lain masuk Bagian 7 (Tabel Selisih). Representatif = anggota dengan nilai live terbesar bila terbaca, selain itu anggota dengan override terbanyak.

**Catatan kewajaran (mengikat):** angka anggaran di atas adalah **rentang wajar, bukan ambang kaku**. Sedikit di atas/di bawah masih sah selama ada alasan tercatat di Bagian 1. Yang dilarang: menumpuk banyak pemicu batas dalam satu segmen tanpa alasan, atau memecah sampai satu Lintasan kehilangan alur nilai utuh.

## Langkah 1 — 5 pemicu batas segmen (B19)

Segmen baru dimulai **hanya** pada:

- **(a)** perpindahan aset/token/native masuk atau keluar `Value_Holder`;
- **(b)** penulisan variabel akuntansi (saldo, share, supply, reserve, debt, index, rate, klaim) yang ada di C00/LP-x;
- **(c)** serah kendali ke **domain kepercayaan berbeda** — kontrak eksternal, `EXTERNAL-BOUNDARY`, delegatecall/call ke target yang dipilih admin atau caller. Serah kendali ke kode in-scope dengan kepercayaan sama **tidak** memecah segmen, cukup dicatat `CY-x`;
- **(d)** batas transaksi/aktor/waktu → segmen berhenti di penulisan storage, dicatat `HB-x`;
- **(e)** perpindahan domain eksekusi (chain/runtime) → handoff lintas-domain.

Bukan pemicu: helper `pure`/`view`, panggilan primitif C00 (dirujuk), modifier, emit event.
Konsekuensi: dua agen yang memetakan Lintasan sama akan menghasilkan batas segmen yang sama — perbedaan jumlah segmen = tanda salah satu melanggar pemicu.

## Aturan Koridor (`Corridor-Bound Cross-Cluster`)

- **Satu Lintasan per putaran.** Bukan dua, bukan "sekalian".
- **WAJIB TEMBUS KLASTER SEPANJANG KORIDOR:** bila `S(k)` memanggil kontrak di klaster `CORE-FLOW` lain sebagai bagian langsung dari aliran nilai, baca badan target dan jadikan `S(k+1)` di berkas ini; tandai di `B05` → `TERPETAKAN_DI_<STR>.<Lk>` (dengan nama).
- **LARANGAN MELEBAR HORIZONTAL:** dilarang menginventarisasi fungsi lain di kontrak/klaster seberang yang tidak dipanggil dan tidak dilalui koridor.
- **JEMBATAN ASINKRON:** aliran berhenti di storage `V` karena jeda tx/waktu/aktor → hentikan segmen di penulisan `V`, daftarkan/perbarui `HB-x` di `B07` (penulis + jaminan; atau pembaca + asumsi bila Lintasan ini pembaca).
- Tahap D memperoleh hak **`1-hop peek`** pada pasangan `HB-x`.
- Urutan kerja = **pintu masuk pertama kali** (B2a). Bila user memerintah urutan lain, catat alasannya di `B04`.

## Keluaran

| Berkas | Isi |
| --- | --- |
| `C00-SHARED-PRIMITIVES.md` | inventaris deskriptif seluruh unit `SHARED-PRIMITIVE` (sekali di awal Tahap C, sebelum Lintasan pertama) + titik serah kendali per primitif (`C00-Uxx/CY`) |
| `C<NN>-<STR>-<Lk>-INVENTORY.md` | inventaris Lintasan (9 bagian di bawah) |

## Format wajib: 9 bagian per `C<NN>-<STR>-<Lk>-INVENTORY.md`

Murni deskriptif — apa kata kode. Nol invariant, nol klaim bug, nol PoC.

### Bagian 1 — Identitas Lintasan

- `Lintasan_ID` (`STR-nn.Lk`) + Stream induk + Flow Family + Twin-Path Group.
- Mode topologi (dari B00) + domain eksekusi tiap segmen + anggota representatif yang dibedah.
- Pintu masuk utama (`File:Lxx-Lyy`).
- Daftar EP+VM, EP+SM, `IN-x` yang tercakup (dengan nama + nomor ledger), termasuk lintas-klaster.
- Keputusan pecah/gabung Lintasan (Langkah 0 butir 4) + alasannya bila melewati anggaran.

### Bagian 2 — Segmen (`S0..Sn`)

Tiap segmen = potongan alur yang **bisa diamati** di batas unit. Untuk tiap segmen tulis:

| Kolom | Isi |
| --- | --- |
| ID | `S0`, `S1`, `S2`, dan seterusnya hingga `Sn` |
| Nama segmen | ringkas, 1 baris |
| Fungsi & Jangkar Eksak | `Path/File.ext:Lxx-Lyy` — satu baris per fungsi yang terlibat |
| Batas masuk | apa yang menandai segmen mulai (event, perubahan state, pesan, waktu) |
| Batas keluar & efek saldo/state | apa yang menandai segmen selesai + efeknya ke saldo/state |
| Aktor pemicu | siapa yang bisa memicu (`USER` / `ACTOR` / `ADMIN` / `EXTERNAL` / otomatis) |
| Pemicu batas | pemicu B19 yang memulai segmen ini: **(a)** aset masuk/keluar `Value_Holder` / **(b)** tulis variabel akuntansi / **(c)** serah kendali domain kepercayaan beda / **(d)** batas transaksi-aktor-waktu (`HB-x`) / **(e)** pindah domain eksekusi |
| `CY-x` di segmen | ID titik serah kendali yang jatuh di segmen ini (kosong bila tidak ada) |
| Domain | `DOM-x` tempat segmen dieksekusi |

**Ingress `S0` (B17).** Ingress kelas `PASSIVE`/`ACCRUAL` (dan `ACTOR` yang tidak lewat entrypoint pengguna) muncul sebagai **segmen masuk tidak resmi `S0`** di inventaris Lintasan pembacanya — deskriptif: siapa bisa memicu, berapa batasnya, bagaimana akuntansi menyerapnya (mis. `_sync` membaca `balanceOf(address(this))`, akrual fee per detik membaca `block.timestamp`). `S0` dihitung sebagai segmen dalam rumus handoff Bagian 4.

Keluaran `S(k)` wajib **nyambung ke masukan `S(k+1)`**. Bila tidak bersambung lewat pemanggilan langsung, itu kandidat **State-Bridge** (`HB-x`, Bagian 6) — bukan handoff langsung.

### Bagian 3 — Titik Serah Kendali (`CY-x`)

Tiap titik di dalam segmen tempat eksekusi berpindah ke kode yang tidak dikendalikan fungsi itu: `call`/`delegatecall`/`staticcall` eksternal, transfer native (`call{value}`/`transfer`/`send`/`sendValue`), transfer token ber-hook (ERC-721/1155/777/1363), panggilan ke `EXTERNAL-BOUNDARY`/oracle/router, callback ke `msg.sender`, `try/catch`.

| Kolom | Isi |
| --- | --- |
| `CY_ID` | `CY-1`, `CY-2`, dan seterusnya |
| Segmen | `STR-01.L1.S3` |
| Jangkar | `File:Lxx-Lyy` |
| Jenis | `call` / `delegatecall` / `staticcall` / native-transfer / token-hook / try-catch |
| Penerima kendali | `CALLER-INPUT` / `ADMIN-CONFIG` / `IMMUTABLE` / `EXTERNAL` |
| Storage ditulis SEBELUM | variabel + `File:Baris` |
| Storage ditulis SESUDAH | variabel + `File:Baris` |
| Storage dibaca SESUDAH | variabel + `File:Baris` |
| Guard aktif | `nonReentrant` / `lock` / `none` |
| Efek bila revert | `propagasi` / `ditelan` / `defer` |

Aturan: `CY-x` **tidak** otomatis memecah segmen (lihat B19 pemicu c). AST wajib dipakai untuk enumerasi kandidat; tiap kandidat dikonfirmasi dari badan fungsi. Titik serah kendali yang sudah diinventarisasi di `C00` cukup dirujuk (`C00-Uxx/CY`), tidak diulang.

### Bagian 4 — Kontrak Handoff (`H1..Hn-1`)

Dienumerasi **ketat dari batas unit**: satu handoff per sambungan langsung antar-segmen. Rantai linear atau bercabang tanpa penggabungan ulang: `N` segmen → **tepat `N-1` handoff**. Bila ada Join `Jx` yang menerima `m` cabang masukan dari segmen berbeda di Lintasan ini: jumlah handoff = `N - 1 + Σ(m - 1)` atas semua `Jx` tersebut. Jangan dilabeli tangan.

| Kolom | Isi |
| --- | --- |
| ID | `H1`, `H2`, dan seterusnya hingga `Hn-1` |
| Produsen (Segmen + Fungsi:Baris) | segmen + fungsi + baris yang menulis |
| Konsumen (Segmen + Fungsi:Baris) | segmen + fungsi + baris yang membaca |
| Field/Nilai Diteruskan | **nama + tipe + satuan/desimal** (mis. `uint128 amount`, 18 desimal) |
| Pengendali Field | per field: `CALLER-INPUT` / `ADMIN-CONFIG` / `DERIVED(<sumber>)` / `EXTERNAL-ORACLE` — siapa yang menentukan nilainya **menurut kode** |
| Jaminan Faktual Produsen di Kode | apa yang produsen pastikan (mis. "amount sudah dikurangi fee") — **apa adanya di kode** |
| Asumsi Faktual Konsumen di Kode | apa yang konsumen anggap benar (mis. "amount <= saldo kontrak") — **apa adanya di kode** |
| Status | `TERTUTUP` / `TERBUKA_EKSTERNAL` |

Definisi `Pengendali Field` (deskriptif, dari kode):

- `CALLER-INPUT` — nilai berasal langsung dari parameter/calldata/`msg.value`/token yang dipilih pemanggil permissionless.
- `ADMIN-CONFIG` — nilai dibaca dari storage yang hanya bisa ditulis peran istimewa (owner/admin/governance/role).
- `DERIVED(<sumber>)` — hasil hitung dari field lain; sebut sumbernya, mis. `DERIVED(amount, feeBps)`. Bila salah satu sumber `CALLER-INPUT`, tulis eksplisit.
- `EXTERNAL-ORACLE` — dibaca dari kontrak eksternal (oracle, pool, messenger) yang tidak dikendalikan kode scope.

Satu field bisa punya lebih dari satu pengendali (mis. `DERIVED(CALLER-INPUT amount, ADMIN-CONFIG feeBps)`); tulis semuanya, jangan dipilih salah satu.

Handoff `TERBUKA_EKSTERNAL` = konsumennya di luar kode scope (mis. messenger eksternal, `EXTERNAL-BOUNDARY` di `B04`). Tetap **dienumerasi**, jangan dihapus, jangan ditutup sepihak.

Handoff lintas-domain (pemicu **e**) tetap satu baris `H-x`; domain asal/tujuan disebut di kolom Produsen/Konsumen dan dicatat sebagai `HB-x` bila ada jeda state.

### Bagian 5 — Simpul (`Fx` Fork / `Jx` Join)

Unit mandiri **berprioritas tinggi** — bukan catatan kaki segmen.

- **Fork (`Fx`)** = percabangan aliran: catat **rumus pembagian aliran & potongan biaya sebagaimana tertulis di kode** (nanti diuji: keluaran total = masukan − fee).
- **Join (`Jx`)** = penggabungan/klaim: catat **penanda state yang mencegah konsumsi ganda sebagaimana tertulis di kode** (nanti diuji: konsumsi tepat sekali — tidak dobel, tidak hilang). Tulis juga baris `Masukan: S<a>, S<b>, ...` (segmen-segmen yang bertemu di Join ini) — dipakai untuk menghitung jumlah handoff.

### Bagian 6 — State-Bridge (`HB-x`) & Referensi Primitif (`C00`)

- Daftar **jembatan storage asinkron** yang disentuh Lintasan ini — **sinkron dengan `B07-STATE-BRIDGES.md`** (baris `HB-x` yang sama; kolom baku: `Bridge_ID | Storage_Var_&_Contract | Writer_Lintasan_&_Guarantee | Reader_Lintasan_&_Assumption | Window_&_Trigger | Sync_Status`).
- `Window_&_Trigger`: jeda/tenggat yang mengatur kapan pembaca boleh jalan (liveness, delay, epoch, deadline) + siapa yang boleh memicu pembaca (`USER`/`ACTOR`/`ADMIN`/`EXTERNAL`).
- `Sync_Status` (enum baku): `SEED` → `WRITER_MAPPED` / `READER_MAPPED` → `SINKRON` | `DESINKRON:<OBS-id>` | `TERBUKA_EKSTERNAL`.
- Daftar item `C00-SHARED-PRIMITIVES.md` yang dipakai segmen-segmen Lintasan ini (termasuk `C00-Uxx/CY` yang dirujuk, bukan diulang).

### Bagian 7 — Tabel Selisih Varian (B20)

Wajib bila Lintasan menyentuh > 1 anggota keluarga (`VK`/`VC`/`DOM`). Satu anggota **representatif** dibedah penuh (Bagian 1–6); anggota lain dicatat di sini, satu baris per anggota:

| Anggota | Fungsi override (jangkar) | Autentikasi | Jalur native/wrapped | Transport/route | Kelas aset diterima | Parameter live beda (LP-x) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | `File:Lxx-Lyy` | alias / messenger / `crossChainSender` / oracle | unwrap / tidak | | `NATIVE` / `WRAPPED_NATIVE` / `ERC20_STD` / `FOT` / `REBASING` / `HOOK_TOKEN` / `DECIMALS!=18` / `NON_EVM_ASSET` | `LP-x` | `SAMA` / `BEDA:<kolom>` |

Aturan: baris `BEDA` yang menyentuh **nilai** atau **autentikasi** = wajib jadi kartu di Tahap D (Twin-Path Differential otomatis). Status `TIDAK-DIBACA` dilarang pada anggota yang dipakai PoC. Bila hanya satu anggota → tulis `SELISIH: N/A (satu anggota)` (bukan dihapus).

### Bagian 8 — Lembar Parameter Live (`LP-x`) per domain

Daftar **setiap variabel storage dan nilai eksternal yang dibaca** fungsi di koridor Lintasan aktif dan memengaruhi aliran nilai: penjaga (`require`/`if`), rumus, rate, fee, cap, flag pause, whitelist/allowlist, alamat tujuan/adapter, sumber oracle. Murni deskriptif — Tahap C mengisi kolom kode; kolom nilai live diisi di **B8 Live-Match Lintasan** (awal Tahap D).

| Kolom | Diisi di | Isi |
| --- | --- | --- |
| ID | C | `LP-1`, `LP-2`, dan seterusnya |
| Variabel & Jangkar Baca | C | nama variabel + `Path/File.ext:Lxx-Lyy` tempat dibaca di koridor |
| Kontrak | C | kontrak pemilik storage (alamat live diisi di B8) |
| Domain | C | `DOM-x` tempat segmen pembaca dieksekusi (B21 — LP-x dibaca di domain itu, blok pin domain itu) |
| Pengendali | C | `ADMIN-CONFIG` / `DERIVED(<sumber>)` / `EXTERNAL-ORACLE` / `CALLER-INPUT` (definisi sama dengan Bagian 4) |
| Penulis di Kode | C | fungsi + `Path/File.ext:Lxx-Lyy` yang menulis variabel ini, + peran yang bisa memanggilnya |
| Cabang yang Bergantung | C | segmen/handoff/simpul yang perilakunya berubah karena nilai ini (`S2`, `H3`, `F1`) |
| Nilai @ blok pin | B8 | hasil `cast call` / `cast storage` pada blok pin domain itu; tulis `DIISI_B8` di Tahap C |
| Status Cabang | B8 | `LIVE` / `DEAD-CONFIG` / `UNVERIFIED`; tulis `DIISI_B8` di Tahap C |

Arti `Status Cabang`:

- `LIVE` — nilai live membuat cabang itu bisa dilalui transaksi normal.
- `DEAD-CONFIG` — nilai live membuat cabang tidak bisa dilalui (mis. `paused == true`, `feeBps == 0` untuk cabang fee, token tidak di-whitelist, `cap == 0`, adapter `address(0)`).
- `UNVERIFIED` — nilai tidak bisa dibaca andal di blok pin domain itu (RPC/arsip gagal, getter revert). **BUKAN `LIVE`**: Lintasan dengan `LP-x` pengendali nilai berstatus ini tidak lolos Gate D sampai terbaca. Status `TIDAK-TERBACA` dicabut (v2.1).

Aturan Bagian 8:

- **Bukan filter.** Cabang `DEAD-CONFIG` tetap ada di Bagian 2–7; Bagian 8 hanya menandai.
- Variabel `CALLER-INPUT` dicatat agar Tahap D/E tahu field mana yang **bebas diisi** (termasuk nilai ekstrem); variabel `ADMIN-CONFIG` dicatat agar Tahap D/E **memakai nilai live**, bukan nilai karangan.
- **Lokasi LP-x (B21):** tiap `LP-x` dibaca **di domain tempat segmen pembacanya dieksekusi**, pada blok pin domain itu. Getter yang revert → baca slot storage (`cast storage`) dari layout AST. Tetap tidak terbaca → `UNVERIFIED`.
- Bila satu variabel dibaca di beberapa tempat di koridor, cukup satu baris `LP-x` dengan semua jangkar baca disebut.
- Nol penilaian bahaya, nol invariant — tetap deskriptif.

### Bagian 9 — Rekonsiliasi Ledger

Deskriptif, tanpa penilaian: catat **nama** setiap baris ledger yang diselesaikan Lintasan ini.

| Kolom | Isi |
| --- | --- |
| Jenis | `EP+VM` / `EP+SM` / `IN-x` |
| Nama | `File:Baris` + `contract.function` (bukan hanya jumlah) |
| Status baru | `TERPETAKAN_DI_<STR>.<Lk>` (EP+VM/EP+SM) / `TERIKAT_DI_<STR>.<Lk>` (IN-x) |
| Catatan | bila ditunda / `UNVERIFIED` / `TUNDA-LIVE`, sebut alasannya |

Aturan: penyusutan ledger dihitung **berbasis nama** (B10 v2.1), bukan pengurangan angka berjalan. Bila setelah katalog awal habis masih ada sisa, bentuk Lintasan baru menurut Ingress→Egress — **bukan** Lintasan penampung (B22).

## Yang TIDAK dilakukan di Tahap C

1. Menulis invariant — itu Tahap D (B12). Invariant = klaim asumsi tentang apa yang *seharusnya* berlaku, bukan fakta teramati.
2. Buruan saat memetakan.
3. PoC / verifikasi / verdict.
4. Menutup handoff yang konsumennya di luar kode tanpa keputusan user.
5. Menilai Lintasan/Stream ("ini bersih", "ini berbahaya") — itu Tahap G.
6. Filter di dalam Lintasan (hanya mengambil data yang dibutuhkan alur live) — dinilai berisiko, tidak diadopsi. Filter yang aman hanya utuh per Lintasan. Bagian 8 menandai, bukan menyaring.
7. Melebar horizontal — membaca/menginventarisasi fungsi lain di kontrak/klaster seberang yang tidak dipanggil dan tidak dilalui koridor aktif.
8. Mengisi kolom `Nilai @ blok pin` / `Status Cabang` di Bagian 8 — itu B8 di awal Tahap D.
9. **(v2.1)** Menggabungkan banyak pemicu batas dalam satu segmen tanpa alasan tercatat.
10. **(v2.1)** Menulis `S0` sebagai segmen biasa tanpa menyebut kelas `IN-x` pengikatnya.

## Definition of done Tahap C

**Pra-Stream (sekali):**

- [ ] `C00-SHARED-PRIMITIVES.md` lengkap: seluruh unit `SHARED-PRIMITIVE` dari `B04` terpetakan — lokasi `File:Lxx-Lyy`, fungsi konversi/akuntansi, arah pembulatan + desimal, perubahan state/saldo, event, **titik serah kendali per primitif** (`C00-Uxx/CY`)

**Per-Lintasan (`C<NN>-<STR>-<Lk>-INVENTORY.md`):**

- [ ] Bagian 1 Identitas: `Lintasan_ID` + Stream + Flow Family + Twin-Path + mode B0 + domain per segmen + anggota representatif + pintu masuk + daftar EP+VM/EP+SM/`IN-x` (nama + nomor ledger) + keputusan pecah/gabung
- [ ] Bagian 2 Segmen: semua segmen punya batas masuk/keluar + pemicu batas + domain; bersambung (`S(k)` → `S(k+1)` atau berakhir di `HB-x`); `S0` ada bila `PASSIVE`/`ACCRUAL` terikat
- [ ] Bagian 3 `CY-x`: tiap titik serah kendali punya 10 kolom (urutan tulis sebelum/sesudah + storage dibaca sesudah + guard + efek revert); kandidat AST dikonfirmasi dari badan
- [ ] Bagian 4 Handoff: jumlah sesuai rumus (`N-1`, ditambah `Σ(m-1)` bila ada Join bercabang-masuk); tiap handoff punya field (nama+tipe+satuan) + pengendali per field + jaminan produsen + asumsi konsumen + status
- [ ] Bagian 5 Simpul: tiap `Fx` punya rumus pembagian + potongan biaya; tiap `Jx` punya penanda anti-konsumsi-ganda + baris `Masukan:`
- [ ] Bagian 6 State-Bridge: semua `HB-x` sinkron dengan `B07` (enum `Sync_Status` + `Window_&_Trigger`); item `C00` yang dipakai terdaftar
- [ ] Bagian 7 Tabel Selisih: terisi bila > 1 anggota; baris `BEDA` nilai/autentikasi siap jadi kartu Tahap D; `SELISIH: N/A` bila satu anggota
- [ ] Bagian 8 `LP-x`: tiap variabel yang memengaruhi aliran nilai terdaftar + kolom `Domain`; nilai = `DIISI_B8`; nol `UNVERIFIED` pada Lintasan yang dipakai Gate D
- [ ] Bagian 9 Rekonsiliasi: nama per baris + status `TERPETAKAN_DI_<STR>.<Lk>` / `TERIKAT_DI_<STR>.<Lk>`
- [ ] koridor: fungsi lintas-klaster di garis aliran masuk sebagai `S(k+1)`; nol pelebaran horizontal
- [ ] nol invariant, nol buruan, nol PoC
- [ ] `python3 tools/verify_flow.py check-c <berkas> --repo <repo>` → **LULUS**

---

## Lampiran — warisan & catatan sumber

### S1. Catatan sumber A04

A04 yang diterima **terpotong** pada Bagian 1 (berhenti di "termasuk lintas-"). Bagian yang ada — frontmatter, intro, dua mode kerja, Langkah 0, Langkah 1, Aturan Koridor, judul "Format wajib: 9 bagian", dan Bagian 1 — diterapkan **verbatim**. Bagian 2–9, Larangan, dan DoD **direkonstruksi** mengikuti urutan yang dinyatakan di `description` A04 sendiri (identitas → segmen/`S0` → `CY-x` → handoff → simpul → State-Bridge → Tabel Selisih → `LP-x` → rekonsiliasi ledger), memakai bahan skill v2.1 sebelumnya yang sudah lolos `check-c`. Bila A04 lengkap tersedia, bagian rekonstruksi wajib ditimpa.

### S2. Butir lama yang dipertahankan (tidak ada di teks A04 yang diterima)

- **Rumus handoff** `N - 1 + Σ(m-1)` dan baris `Masukan: S.., S..` — dipakai `check-c` untuk memvalidasi jumlah handoff.
- **Definisi `Pengendali Field`** (`CALLER-INPUT`/`ADMIN-CONFIG`/`DERIVED(...)`/`EXTERNAL-ORACLE`) + aturan "satu field boleh punya >1 pengendali".
- **`TERTUTUP` / `TERBUKA_EKSTERNAL`** pada handoff + larangan menutup handoff eksternal sepihak.
- **Arti `Status Cabang`** (`LIVE`/`DEAD-CONFIG`/`UNVERIFIED`) + aturan "bukan filter".
- **Larangan klaim prematur** `TERBUKTI` dan penomoran `INV-` di Tahap C (dicek `check-c`).
- **`1-hop peek`** di Tahap D untuk pasangan `HB-x`.
- **Perluasan warisan/implementasi** (B14.6/B14.7) + **penguraian dispatcher `unknown`** (B14.4) di awal Lintasan.
- **Urutan B2a** (pintu masuk pertama kali) + kewajiban mencatat alasan bila user memerintah urutan lain.
- **Perintah verifikasi** `check-c` di DoD.
