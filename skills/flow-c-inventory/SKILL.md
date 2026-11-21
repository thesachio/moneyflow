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

## Keluaran

| Berkas | Isi |
| --- | --- |
| `C00-SHARED-PRIMITIVES.md` | inventaris deskriptif seluruh unit `SHARED-PRIMITIVE` (sekali, sebelum Lintasan pertama) + titik serah kendali per primitif (`C00-Uxx/CY`) |
| `C<NN>-<STR>-<Lk>-INVENTORY.md` | inventaris Lintasan (9 bagian di bawah) |

## Langkah 0 — Tetapkan batas Lintasan (sebelum menulis segmen)

1. Ambil usulan Lintasan dari `B04`. Lakukan **perluasan warisan/implementasi** (B14.6/B14.7) dan **penguraian dispatcher `unknown`** (B14.4) untuk entrypoint Lintasan.
1. Ikuti aliran nilai `Ingress → Accounting → Egress` secara vertikal; tandai pemicu batas (Langkah 1) di sepanjang jalan.
1. Hitung anggaran:

| Unit | Batas bawah | Batas atas |
| --- | --- | --- |
| Segmen | ≥ 1 pemicu batas | ≤ 4 fungsi dibaca langsung |
| Lintasan | ≥ 1 perpindahan nilai + ≥ 1 batas kepercayaan | 4–8 segmen; ≤ 12 fungsi dibaca langsung (rujukan C00 tidak dihitung); 1 keluarga varian |

1. Lewat batas atas → **pecah sebelum menulis**: per fase (masuk / akuntansi / keluar) atau per sisi domain (kirim / terima). Di bawah batas bawah → gabung dengan Lintasan tetangga dalam Stream yang sama. Catat keputusan pecah/gabung di Bagian 1 + koreksi `B04`.
1. Lintasan menyentuh > 1 anggota varian (`VK`/`VC`/`DOM` dari B00) → pilih **satu representatif** per keluarga untuk dibedah; anggota lain masuk Bagian 7 (Tabel Selisih). Representatif = anggota dengan nilai live terbesar bila terbaca, selain itu anggota dengan override terbanyak.

**Catatan kewajaran (mengikat):** angka anggaran adalah **rentang wajar, bukan ambang kaku**. Sedikit di luar rentang masih sah bila ada baris `KEPUTUSAN_ANGGARAN: <alasan>` di Bagian 1 (dicek `check-c`). Yang dilarang: menumpuk banyak pemicu batas dalam satu segmen tanpa alasan, atau memecah sampai satu Lintasan kehilangan alur nilai utuh.

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

## Format wajib: 9 bagian per `C<NN>-<STR>-<Lk>-INVENTORY.md`

Murni deskriptif — apa kata kode. Nol invariant, nol klaim bug, nol PoC.

### Bagian 1 — Identitas Lintasan

- `Lintasan_ID` (`STR-nn.Lk`) + Stream induk + Flow Family + Twin-Path Group.
- Mode topologi (dari B00) + domain eksekusi tiap segmen + anggota representatif yang dibedah.
- Pintu masuk utama (`File:Lxx-Lyy`).
- Daftar EP+VM, EP+SM, `IN-x` yang tercakup (dengan nama + nomor ledger), termasuk lintas-klaster.
- **Hitungan anggaran:** jumlah segmen (tanpa `S0`), jumlah fungsi dibaca langsung, jumlah rujukan C00.
- Keputusan pecah/gabung Lintasan + `KEPUTUSAN_ANGGARAN: <alasan>` bila di luar rentang.

### Bagian 2 — Segmen (`S0` opsional, `S1..Sn`)

Tiap segmen = potongan alur yang **bisa diamati** di batas unit:

| Kolom | Isi |
| --- | --- |
| ID | `S0` (Ingress tidak resmi, bila ada), `S1`…`Sn` |
| Nama segmen | ringkas, 1 baris |
| Pemicu batas | `a` / `b` / `c` / `d` / `e` (boleh lebih dari satu) |
| Domain | `DOM-x` tempat segmen berjalan |
| Fungsi & Jangkar Eksak | `Path/File.ext:Lxx-Lyy`, satu baris per fungsi |
| Batas masuk | apa yang menandai segmen mulai (event, perubahan state, pesan, waktu) |
| Batas keluar & efek saldo/state | apa yang menandai segmen selesai + efeknya |
| Aktor pemicu | `USER` / `ACTOR` (keeper/relayer/bot) / `ADMIN` / `EXTERNAL` / otomatis |
| `CY-x` di segmen ini | daftar ID (detail di Bagian 3); kosong bila tidak ada |

**`S0` — Ingress tidak resmi (B17).** Untuk tiap `IN-x` kelas `PASSIVE`/`ACCRUAL`/`CALLBACK` (dan `ACTOR` yang tidak lewat entrypoint pengguna) yang efeknya **dibaca** Lintasan ini, tulis `S0` deskriptif: kelas + ID `IN-x` pengikat, siapa bisa memicu, apakah ada batas/whitelist, variabel yang naik, di mana akuntansi membacanya (fungsi:baris, mis. `_sync` membaca `balanceOf(address(this))`, akrual membaca `block.timestamp`), apakah akuntansi membedakan sumber. Tandai `IN-x` → `TERIKAT_DI_<STR>.<Lk>` di `B05`.
`S0` **tidak** dihitung dalam rumus handoff Bagian 4: ia tidak bersambung lewat pemanggilan langsung, melainkan lewat saldo/state yang dibaca segmen lain (tulis segmen pembacanya di kolom "Batas keluar").

Keluaran `S(k)` wajib **nyambung ke masukan `S(k+1)`**. Bila tidak bersambung lewat pemanggilan langsung, itu kandidat **State-Bridge** (`HB-x`, Bagian 6) — bukan handoff langsung.

### Bagian 3 — Titik Serah Kendali (`CY-x`) (B18)

Satu baris per titik di dalam segmen tempat eksekusi berpindah ke kode yang tidak dikendalikan fungsi itu: `call`/`delegatecall`/`staticcall` eksternal, transfer native (`call{value}`/`transfer`/`send`/`sendValue`), transfer token yang bisa memanggil hook (`safeTransfer*` 721/1155, ERC-777, ERC-1363, token ber-callback), panggilan ke oracle/router/messenger/`EXTERNAL-BOUNDARY`, callback ke `msg.sender`, `try/catch`.

| Kolom | Isi |
| --- | --- |
| CY_ID | `CY-1`, `CY-2`, … |
| Segmen | `STR-nn.Lk.Sj` |
| Jangkar | `File:Lxx` |
| Jenis | `EXT_CALL` / `DELEGATECALL` / `NATIVE_SEND` / `TOKEN_HOOK` / `ORACLE_READ` / `CALLBACK` / `TRY_CATCH` |
| Penerima kendali dikendalikan oleh | `CALLER-INPUT` / `ADMIN-CONFIG` / `IMMUTABLE` / `EXTERNAL` |
| Storage ditulis SEBELUM | variabel + `File:Baris` |
| Storage ditulis SESUDAH | variabel + `File:Baris` (kosong = pola CEI terpenuhi secara deskriptif) |
| Storage dibaca SESUDAH | variabel + `File:Baris` |
| Guard aktif | `nonReentrant` / lock khusus / `none` — **modifier yang menulis state wajib disebut namanya + efeknya**, bukan hanya "lock khusus". Contoh wajib: `validateInternalCalls — menulis callValidated selama delegatecall, membuka semua onlyAdmin`. Daftar modifier penulis state ada di `B05` §11b; bila Lintasan menyentuhnya dan kolom hanya ditulis `lock khusus`, Lintasan itu belum selesai |
| Efek bila revert | `PROPAGASI` / `DITELAN` (try/catch, low-level call tanpa require) / `DEFER` (dicatat utang) |

Aturan:
- `CY-x` **tidak** otomatis memecah segmen (lihat pemicu c).
- Sumber kandidat: daftar `external_calls` AST untuk fungsi koridor (**wajib dipakai**); tiap kandidat dikonfirmasi dari badan. Kandidat yang ternyata tidak berlaku ditulis `DIBUANG: <alasan>`.
- Panggilan di primitif C00 cukup dirujuk `C00-Uxx/CY-y`, tidak diulang.

### Bagian 4 — Kontrak Handoff (`H1..`) (B11)

Dienumerasi **ketat dari batas unit**: satu handoff per sambungan langsung antar-segmen. `N` segmen (tanpa `S0`) → **`N − 1`** handoff, ditambah **`Σ(m − 1)`** untuk tiap Join `Jx` yang menerima `m` cabang masukan. Jangan dilabeli tangan.

| Kolom | Isi |
| --- | --- |
| ID | `H1`… |
| Produsen (Segmen + Fungsi:Baris) | segmen + fungsi + baris yang menulis |
| Konsumen (Segmen + Fungsi:Baris) | segmen + fungsi + baris yang membaca |
| Field/Nilai Diteruskan | **nama + tipe + satuan/desimal** (mis. `uint128 amount`, 18 desimal) |
| Pengendali Field | per field: `CALLER-INPUT` / `ADMIN-CONFIG` / `DERIVED(<sumber>)` / `EXTERNAL-ORACLE` |
| Jaminan Faktual Produsen di Kode | apa yang produsen pastikan — **apa adanya di kode** |
| Asumsi Faktual Konsumen di Kode | apa yang konsumen anggap benar — **apa adanya di kode** |
| Lintas-domain? | `TIDAK` / `YA: <DOM asal> → <DOM tujuan>, autentikasi <fungsi:baris>` |
| Status | `TERTUTUP` / `TERBUKA_EKSTERNAL` |

Definisi `Pengendali Field` (deskriptif, dari kode):

- `CALLER-INPUT` — langsung dari parameter/calldata/`msg.value`/token yang dipilih pemanggil permissionless.
- `ADMIN-CONFIG` — dari storage yang hanya bisa ditulis peran istimewa (owner/admin/governance/role).
- `DERIVED(<sumber>)` — hasil hitung dari field lain; sebut sumbernya, mis. `DERIVED(amount, feeBps)`. Bila salah satu sumber `CALLER-INPUT`, tulis eksplisit.
- `EXTERNAL-ORACLE` — dari kontrak eksternal (oracle, pool, messenger) di luar kendali kode scope.

Satu field boleh punya > 1 pengendali (mis. `DERIVED(CALLER-INPUT amount, ADMIN-CONFIG feeBps)`); tulis semuanya.

Handoff `TERBUKA_EKSTERNAL` = konsumen di luar kode scope (`EXTERNAL-BOUNDARY` di `B04`). Tetap **dienumerasi**, tidak dihapus, tidak ditutup sepihak. Handoff lintas-domain (pemicu e) tetap satu baris `H-x`; bila ada jeda state di antaranya, juga dicatat sebagai `HB-x`.

### Bagian 5 — Simpul (`Fx` Fork / `Jx` Join)

Unit mandiri **berprioritas tinggi** — bukan catatan kaki segmen.

- **Fork `Fx`:** rumus pembagian aliran + potongan biaya **sebagaimana tertulis di kode** (nanti diuji: keluaran total = masukan − fee).
- **Join `Jx`:** penanda state anti-konsumsi-ganda **sebagaimana tertulis di kode** (nanti diuji: konsumsi tepat sekali) + baris `Masukan: S<a>, S<b>, …` (dipakai rumus handoff).

### Bagian 6 — State-Bridge (`HB-x`) & Referensi C00

- Baris `HB-x` yang disentuh, **sinkron dengan `B07`**: `Bridge_ID | Storage_Var_&_Contract | Writer_Lintasan_&_Guarantee | Reader_Lintasan_&_Assumption | Window_&_Trigger | Sync_Status`.
- `Window_&_Trigger`: jeda/tenggat (liveness, delay, epoch, deadline, `MAX_AGE`) + siapa yang boleh memicu pembaca (`USER`/`ACTOR`/`ADMIN`/`EXTERNAL`).
- `Sync_Status` (enum): `SEED` / `WRITER_MAPPED` / `READER_MAPPED` / `SINKRON` / `DESINKRON:<OBS-id>` / `TERBUKA_EKSTERNAL`.
- Daftar item `C00` yang dipakai (termasuk `C00-Uxx/CY-y` yang dirujuk).

### Bagian 7 — Tabel Selisih Varian (B20)

Wajib bila Lintasan menyentuh > 1 anggota `VK`/`VC`/`DOM`. Satu anggota representatif dibedah penuh di Bagian 2–6; anggota lain satu baris per anggota:

| Anggota | Fungsi override (jangkar) | Autentikasi | Jalur native/wrapped | Transport/route | Kelas aset diterima | Parameter live beda (LP-x) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| (representatif) | — dibedah penuh di Bagian 2–6 — | | | | | | `REPRESENTATIF` |
| anggota-2 | `File:Lxx-Lyy` | alias / messenger / `crossChainSender` / oracle | unwrap / tidak | | `NATIVE` / `WRAPPED_NATIVE` / `ERC20_STD` / `FEE_ON_TRANSFER` / `REBASING` / `HOOK_TOKEN` / `DECIMALS≠18` / `NON_EVM_ASSET` | `LP-x` | `SAMA` / `BEDA:<kolom>` |

Aturan:
- Kolom diisi dari baca titik override + AST daftar override (B00 `VK-x`).
- `BEDA` di kolom yang menyentuh **nilai** atau **autentikasi** → **wajib** menjadi kartu di Tahap D (Twin-Path Differential otomatis).
- Kelas aset (B00 `VC-x`) dihitung sebagai anggota varian bila jalur kodenya berbeda.
- Status `TIDAK-DIBACA` dilarang pada anggota yang akan dipakai PoC.
- Hanya satu anggota → tulis `TIDAK_BERLAKU: anggota tunggal` (jangan hapus bagiannya).

### Bagian 8 — Lembar Parameter Live (`LP-x`) per domain (B21)

Setiap variabel storage dan nilai eksternal yang dibaca fungsi koridor dan memengaruhi aliran nilai: penjaga (`require`/`if`), rumus, rate, fee, cap, flag pause, whitelist/allowlist, alamat tujuan/adapter, sumber oracle. Tahap C mengisi kolom kode; kolom nilai live diisi di **B8 Live-Match Lintasan** (awal Tahap D).

| Kolom | Diisi di | Isi |
| --- | --- | --- |
| ID | C | `LP-1`… |
| Variabel & Jangkar Baca | C | nama + `Path/File.ext:Lxx-Lyy` |
| Kontrak | C | pemilik storage (alamat live diisi di B8) |
| **Domain** | C | `DOM-x` tempat segmen pembaca berjalan — nilai **wajib dibaca di sini** |
| Slot storage | C | dari layout AST (dipakai bila getter revert) |
| Pengendali | C | `ADMIN-CONFIG` / `DERIVED(<sumber>)` / `EXTERNAL-ORACLE` / `CALLER-INPUT` |
| Penulis di Kode | C | fungsi + jangkar + peran yang bisa memanggilnya |
| Cabang yang Bergantung | C | `S2`, `H3`, `F1`, `CY-2`… |
| Nilai @ blok pin domain | B8 | `cast call` / `cast storage`; `DIISI_B8` di Tahap C |
| Status Cabang | B8 | `LIVE` / `DEAD-CONFIG` / `UNVERIFIED`; `DIISI_B8` di Tahap C |

Arti `Status Cabang`:

- `LIVE` — nilai live membuat cabang bisa dilalui transaksi normal.
- `DEAD-CONFIG` — nilai live membuat cabang tidak bisa dilalui (mis. `paused == true`, `cap == 0`, token tidak di-whitelist, adapter `address(0)`).
- `UNVERIFIED` — getter dan slot sama-sama gagal dibaca di domain yang benar. **BUKAN `LIVE`.** LP-x pengendali nilai berstatus ini → Lintasan tidak lolos Gate D. Status `TIDAK-TERBACA` dicabut (v2.1).

Aturan Bagian 8:

- **Bukan filter.** Cabang `DEAD-CONFIG` tetap ada di Bagian 2–7; Bagian 8 hanya menandai.
- `CALLER-INPUT` dicatat agar D/E tahu field mana yang bebas diisi (termasuk nilai ekstrem); `ADMIN-CONFIG` agar D/E memakai nilai live, bukan nilai karangan.
- Satu variabel dibaca di beberapa tempat → satu baris dengan semua jangkar.
- Nol penilaian bahaya, nol invariant.

### Bagian 9 — Rekonsiliasi Ledger

| Kolom | Isi |
| --- | --- |
| Jenis | `EP+VM` / `EP+SM` / `IN-x` |
| Nama | `File:Baris` + `contract.function` atau `IN-x` (bukan hanya jumlah) |
| Status baru | `TERPETAKAN_DI_<STR>.<Lk>` (EP+VM/EP+SM) / `TERIKAT_DI_<STR>.<Lk>` (IN-x) |
| Catatan | bila ditunda / `UNVERIFIED` / `TUNDA-LIVE`, sebut alasannya |

Aturan:
- Sisa per populasi dihitung ulang **berbasis nama** dari `B05` + tabel ini (B10 v2.1), bukan pengurangan angka berjalan. Selisih dengan trail lama dicatat eksplisit.
- Fungsi di luar seed yang ditemukan di koridor (mis. setter admin yang belum dibariskan) → daftar terpisah untuk parent.
- Bila katalog awal habis dan sisa > 0 → bentuk Lintasan baru menurut Ingress→Egress, **bukan** Lintasan penampung (B22).

## Yang TIDAK dilakukan di Tahap C

1. Menulis invariant — itu Tahap D (B12). Invariant = klaim tentang apa yang _seharusnya_ berlaku, bukan fakta teramati. Penomoran `INV-` dan klaim `TERBUKTI` dilarang di Tahap C.
1. Buruan saat memetakan.
1. PoC / verifikasi / verdict.
1. Menutup handoff yang konsumennya di luar kode tanpa keputusan user.
1. Menilai Lintasan/Stream ("bersih", "berbahaya") — itu Tahap G.
1. Filter di dalam Lintasan — Bagian 8 menandai, bukan menyaring.
1. Melebar horizontal.
1. Mengisi kolom `Nilai @ blok pin` / `Status Cabang` (itu B8 awal Tahap D).
1. **(v2.1)** Membedah penuh semua anggota varian — satu representatif per keluarga; sisanya Tabel Selisih.
1. **(v2.1)** Membuat segmen tanpa pemicu batas, menumpuk banyak pemicu dalam satu segmen tanpa alasan, atau Lintasan di luar anggaran tanpa `KEPUTUSAN_ANGGARAN`.
1. **(v2.1)** Menulis `S0` tanpa menyebut kelas + ID `IN-x` pengikatnya.

## Definition of done Tahap C

**Pra-Stream (sekali):**
- `C00-SHARED-PRIMITIVES.md` lengkap: semua `SHARED-PRIMITIVE` dari `B04` — lokasi, konversi/akuntansi, pembulatan + desimal, state/saldo, event, titik serah kendali per primitif (`C00-Uxx/CY`).

**Per Lintasan (`C<NN>-<STR>-<Lk>-INVENTORY.md`):**
- Bagian 1: identitas + mode + domain + representatif + EP/IN tercakup + hitungan anggaran dalam rentang (atau `KEPUTUSAN_ANGGARAN`)
- Bagian 2: tiap segmen punya pemicu batas a–e + domain + batas masuk/keluar + bersambung (atau berakhir di `HB-x`); `S0` untuk tiap `IN-x` PASSIVE/ACCRUAL/CALLBACK yang dibaca
- Bagian 3: tiap kandidat `external_calls` AST di fungsi koridor = baris `CY-x` (10 kolom) atau `DIBUANG: <alasan>`
- Bagian 4: jumlah handoff sesuai rumus (`N−1 + Σ(m−1)`, N tanpa `S0`); field nama+tipe+satuan + pengendali per field + jaminan + asumsi + lintas-domain + status
- Bagian 5: tiap `Fx` rumus + fee; tiap `Jx` penanda anti-ganda + baris `Masukan:`
- Bagian 6: `HB-x` sinkron `B07` dengan `Window_&_Trigger` + `Sync_Status` enum; item C00 terdaftar
- Bagian 7: Tabel Selisih lengkap atau `TIDAK_BERLAKU: anggota tunggal`
- Bagian 8: semua LP-x punya Domain + slot; nilai `DIISI_B8`
- Bagian 9: rekonsiliasi berbasis nama
- koridor: fungsi lintas-klaster di garis aliran masuk sebagai `S(k+1)`; nol pelebaran horizontal
- nol invariant, nol buruan, nol PoC
- `B05` diperbarui (nama); `B07` diperbarui bila menyentuh jembatan; `B04` dikoreksi bila Lintasan dipecah/digabung
- `python3 tools/verify_flow.py check-c <berkas> --repo <repo>` → **LULUS**

### Bagian 10 — Kesiapan Eksplorasi (`SIAP-D`) — **gerbang masuk Tahap D**

Prinsip **kelengkapan bertambah**: B ⊂ C ⊂ D. Sebelum Tahap D menyentuh Lintasan ini, **semua** yang
terkait Lintasan harus sudah teridentifikasi di C. Bagian ini adalah daftar periksa yang **dihitung**,
bukan dinarasikan.

| # | Objek | Wajib terisi | Status |
| :-: | :--- | :--- | :--- |
| 1 | **Aset** | setiap token/native yang menyentuh `Value_Holder` Lintasan ini: alamat per domain + **kelas aset** (`NATIVE` / `WRAPPED_NATIVE` / `ERC20_STD` / `FEE_ON_TRANSFER` / `REBASING` / `HOOK_TOKEN` / `DECIMALS≠18` / `NON_EVM_ASSET`) + fungsi:baris tempat ia masuk/keluar | `LENGKAP` \| `BELUM: <nama>` |
| 2 | **Data / storage** | setiap variabel storage yang **ditulis** dan **dibaca** di koridor, dengan `File:Baris` + `HB-x` bila menyeberang Lintasan | `LENGKAP` \| `BELUM: <nama>` |
| 3 | **Entrypoint** | setiap `EP+VM`/`EP+SM` yang dialokasikan ke Lintasan ini di `B05` muncul di kolom `Fungsi & Jangkar Eksak` minimal satu segmen — **atau** ditulis `DI_LUAR_KORIDOR: <fungsi> — <alasan + jangkar>` | `LENGKAP` \| `BELUM: <nama>` |
| 4 | **Parameter live** | setiap `LP-x` Bagian 8 punya `Nilai @ blok pin` + `Status Cabang` (`LIVE` / `DEAD-CONFIG` / `UNVERIFIED`) | `LENGKAP` \| `BELUM: <nama>` |
| 5 | **Serah kendali & ingress** | jumlah `CY-x` Bagian 3 dan `S0` Bagian 2 cocok dengan daftar di Bagian 9, masing-masing punya `Guard aktif` | `LENGKAP` \| `BELUM: <nama>` |
| 6 | **Bahan invariant** | daftar `INV-` yang akan diuji Lintasan ini (rujuk `B06`), atau `NIHIL_KANDIDAT: <alasan>` | `LENGKAP` \| `BELUM: <nama>` |

**Aturan gerbang:**

1. Baris berstatus `BELUM: …` **memblokir** Tahap D untuk Lintasan ini. `check-c` menolak berkas yang
   masih memuat `BELUM:` pada Bagian 10.
2. Baris 3 diuji **mekanis**: gabungan fungsi di kolom `Fungsi & Jangkar Eksak` seluruh segmen harus
   memuat setiap fungsi yang dilabeli `TERPETAKAN_DI_<STR>.<Lk>` di `B05`. Selisih = segmen bolong.
3. Baris 1 dan 2 **tidak boleh** disalin dari `B00`/`B07` sebagai prosa — wajib `File:Baris` Lintasan ini.
4. Bila objek memang tidak ada di Lintasan ini, tulis `TIDAK_ADA: <alasan>` — bukan dikosongkan.
