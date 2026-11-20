---
name: flow-b-map
description: Tahap B — Mapping (moneyflow v2.1). B0 Profil Topologi (mode TUNGGAL / TUNGGAL-BERINSTANS / MULTI-DOMAIN), scope lock B13, sensus statis 100% (B1/B6-v2 — AST sebagai alat lokalisasi, verdict dari baca badan, 8 konvensi B14), sensus live ringan B7 per domain, B04-STREAMS-AND-CLUSTERS (klaster 4 tipe + katalog Stream/Lintasan + Katalog Ingress IN-x + Twin-Path + Flow Family), B05 ledger 3 populasi, B06 registry kosong, B07 State-Bridges (enum Sync_Status + window). Dipakai saat memetakan scope proyek, sensus, topologi, atau saat user menyebut tahap B, mapping, sensus, scope.
---

# Skill flow-b-map — Tahap B (Mapping) — moneyflow v2.1

Tahap B = tahu scope menyeluruh di awal (topologi + sensus utuh + peta alur), **tanpa buruan**.
Skill ini memuat langkah sampai Tahap B selesai. `methodology/aturan-alur-first.md` hanya rujukan sengketa tafsir.

**Prinsip universal:** rule sama untuk semua proyek. Yang berubah antar-proyek hanya **mode topologi** (Langkah 0), dan mode hanya mengubah *bentuk pemecahan* Stream/Lintasan, bukan kedalaman atau gerbang.

## Uji pemisah

Tahap B mengerjakan **hanya** yang butuh pandangan seluruh protokol dan **tidak bisa direkonstruksi** tahap berikut tanpa baca ulang seluruh protokol. Butuh konteks satu Lintasan saja → kerjakan di giliran Lintasan itu (C/D/E).

## Keluaran (sekali, untuk seluruh protokol) — 8 berkas kanonik

| Artefak | Isi |
| --- | --- |
| `B00-TOPOLOGY.md` | **BARU v2.1** — domain eksekusi, varian kode, varian konfigurasi + kelas aset, mode, Matriks Domain (bila MULTI-DOMAIN). Template: `templates/B00-TOPOLOGY.md` |
| `B01-SCOPE.md` | daftar scope + scope lock (B13) + tabel tiga arah aset ↔ alamat ↔ berkas |
| `B02-CENSUS-STATIC.md` + `scripts/out/b02-census.jsonl` + `scripts/out/ast-*.json` | sensus statis 100% + rekonsiliasi AST |
| `B03-CENSUS-LIVE.md` | inventaris alamat live per domain + B7 ringan per domain representatif |
| `B04-STREAMS-AND-CLUSTERS.md` | klaster 4 tipe + katalog Stream & Lintasan awal + **Katalog Ingress `IN-x`** + urutan B2a + Flow Family + Twin-Path |
| `B05-LEDGER-SISA.md` | ledger **3 populasi**: EP+VM, EP+SM, IN-x |
| `B06-REGISTRY-INVARIANT.md` | struktur + penomoran, **isi kosong** |
| `B07-STATE-BRIDGES.md` | kerangka: `Bridge_ID \| Storage_Var_&_Contract \| Writer_Lintasan_&_Guarantee \| Reader_Lintasan_&_Assumption \| Window_&_Trigger \| Sync_Status` |

Urutan langkah: **1 (B13) → 0 (B0) → 2 (B02) → 3 (B03) → 5 (B04) → 6 (B05) → 7 (B06/B07)**. Langkah 4 (B8) berjalan di Tahap D per Lintasan; dicatat di sini sebagai rujukan.

---

## Langkah 1 — B13 Scope lock (gerbang masuk)

Empat syarat, semuanya benar sebelum satu baris sensus ditulis:

1. **Daftar berkas cocok persis** inventaris kanonik — `diff` kosong.
1. **Commit terverifikasi** — `git rev-parse HEAD`; `git status --porcelain` nol baris.
1. **Direktori sumber bersih** — tidak ada artefak build yang menyamar sebagai sumber (`contracts/`, `src/`, `programs/`, `sources/` sesuai bahasa).
1. **Pemetaan tiga arah aset program ↔ alamat ↔ berkas** — tabel di `B01-SCOPE.md`: `| Aset program | Domain | Alamat | Kontrak | Berkas repo | Status |`. Status: `COCOK` / `ASET_TANPA_BERKAS` (eskalasi ke user sebelum sensus) / `BERKAS_DI_LUAR_PROGRAM` / `OUT_OF_SCOPE_PROGRAM` (keduanya tetap disensus; Stream yang seluruh koridornya hanya berisi berkas berstatus ini dikerjakan paling akhir). `program_assets: TIDAK ADA` → `TIDAK BERLAKU`.

Drift di luar scope **dicatat, tidak dihitung** (`scripts/out/scope-all.txt` vs daftar yang diproses).

## Langkah 0 — B0 Profil Topologi (setelah B13, sebelum sensus selesai dipakai)

Isi `B00-TOPOLOGY.md` dengan tiga hitungan mekanis (AST/grep boleh; parent memverifikasi):

1. **Domain eksekusi `DOM-x`** — tiap chain/rollup/runtime dengan state sendiri yang menjalankan kode scope. Sumber: `deployments/` (atau setara), INTEL, berkas konfigurasi deploy. Catat per domain: chainId/cluster, kontrak inti + alamat, blok pin domain (diisi Langkah 3).
1. **Varian kode `VK-x`** — dari AST: kontrak yang meng-override fungsi kontrak inti (`override`, pewarisan per domain, prefiks/sufiks domain `Arbitrum_*`, `*_SpokePool`, `Tron_*`), atau dua versi hidup berdampingan. Catat fungsi yang di-override per varian (bahan Tabel Selisih Tahap C).
1. **Varian konfigurasi `VC-x`** — instance kode sama dengan parameter berbeda (market, vault, pool, strategi, route), dan **kelas aset** yang diterima: `NATIVE`, `WRAPPED_NATIVE`, `ERC20_STD`, `FEE_ON_TRANSFER`, `REBASING`, `HOOK_TOKEN` (777/1363/ber-callback), `DECIMALS≠18`, `NON_EVM_ASSET`. Ragu bahwa kelas tertentu diterima → catat sebagai `MUNGKIN` (bukan dihapus).

**Penentuan mode (mekanis):**

| Mode | Syarat | Bentuk pemecahan di Tahap C |
| --- | --- | --- |
| `TUNGGAL` | 1 domain DAN `VK` ≤ 1 DAN `VC` ≤ 3 | Lintasan = Stream; pecah per fase (masuk / akuntansi / keluar) bila lewat anggaran |
| `TUNGGAL-BERINSTANS` | 1 domain DAN (`VK` > 1 ATAU `VC` > 3) | Stream × anggota representatif + Tabel Selisih untuk anggota lain |
| `MULTI-DOMAIN` | > 1 domain | Stream pengguna × domain representatif + Stream lintas-domain per keluarga transport + Tabel Selisih per keluarga |

Mode boleh dinaikkan dengan alasan tercatat; tidak boleh diturunkan di bawah hasil hitungan.

**Khusus `MULTI-DOMAIN` — Matriks Domain** (satu baris per `DOM-x`): `Domain | Kontrak inti | Autentikasi pesan masuk (fungsi:baris) | Transport keluar | Transport masuk | Kelas aset dirutekan | Keluarga | Representatif? | Status (LIVE/DEAD-CONFIG/UNVERIFIED — diisi Langkah 3)`. **Keluarga** = domain dengan autentikasi + transport yang sama (mis. OP-stack). Satu representatif per keluarga.

**Contoh bentuk (universal):**
- Lending single-chain dengan 12 market → `TUNGGAL-BERINSTANS`; Stream "supply→borrow→repay→withdraw" dibedah di 1–2 market representatif per kelas aset; market lain di Tabel Selisih (oracle, LTV, cap, IRM).
- DEX single-chain satu jenis pool, 2 token class → `TUNGGAL`.
- Bridge 15 chain → `MULTI-DOMAIN`; Lintasan per keluarga transport.
- Program Solana + kontrak EVM → `MULTI-DOMAIN` (dua runtime).

## Langkah 2 — B02 Sensus statis 100% (B1 + B6-v2 + B14)

### Apa yang dihitung (B1)

Sensus = **100% peristiwa pemindah nilai**:

- entrypoint (fungsi yang bisa dipanggil dari luar) → baris fungsi;
- multicall / dispatch dinamis **transitif**; proxy → implementation; callback / hook → baris fungsi;
- **peristiwa bukan-fungsi** — transfer langsung/donasi, force-feed/`selfdestruct`, akrual/rebase, airdrop pihak ketiga, transfer native/SPL ke PDA → **bukan diabaikan**: dicatat sebagai kandidat **Ingress `IN-x`** (Langkah 5 Bagian 2b);
- langkah off-chain — dilabeli asumsi.

**Fungsi = unit sensus (kelengkapan). Segmen = unit buruan (partisi).**

### B6-v2 — cara membaca (mengikat)

- **AST/parser diizinkan sebagai alat** (solc `--ast-compact-json`, Slither `function-summary` / `entry-points` / `vars-and-auth` / `call-graph`, Aderyn, tree-sitter untuk Rust/Move/Cairo). Pakai untuk: melokalisasi fungsi + atribut, daftar warisan/override (bahan B0 `VK-x`), daftar panggilan eksternal/delegatecall/transfer native (bahan Tahap C `CY-x`), storage ditulis/dibaca per fungsi, deteksi `receive`/`fallback`/`selfdestruct`/`balanceOf(address(this))`/`address(this).balance` (bahan `IN-x`). Simpan output ke `scripts/out/ast-*.json`.
- **Verdict `value_moves`, tag `PRIVILEGED_ONLY:`/`COSMETIC_NON_ECONOMIC:`, dan kelas Ingress diisi SETELAH badan fungsi dibaca penuh.** Kolom `ast_hint` boleh berisi saran AST; kolom `value_moves` tidak boleh disalin dari saran.
- **Rekonsiliasi wajib** di `B02-CENSUS-STATIC.md`: per berkas, `jumlah fungsi AST` vs `jumlah baris sensus`; tiap selisih dijelaskan per nama (deklarasi interface, warisan B14.6, fungsi yang dihasilkan kompiler). Selisih tak terjelaskan = sensus belum lulus.
- Baca bertingkat (classifier yang **menggantikan** baca badan) tetap **ditolak**.
- Biaya acuan: ~14–23 menit untuk ~200 berkas / ~1.200 baris (pilot Across, tanpa AST). Dengan AST untuk lokalisasi, waktu lokalisasi turun; **waktu baca badan tidak boleh dipotong**.

### B14-v2 — 4 nilai sah `value_moves`

| Nilai | Kriteria |
| --- | --- |
| `yes` | memindahkan aset/token/native langsung ATAU mengubah saldo/share/klaim finansial langsung |
| `state_mutator` | `entrypoint: true`, tidak memindahkan aset langsung, bukan khusus admin terverifikasi, TETAPI menulis storage — `initialize`/setup, allowance/operator/recipient/delegasi, indeks/snapshot/timestamp/twap/sync/poke, siklus hidup posisi (merge/split/lock), pembuatan pool/rute publik, pembatalan/penguncian antrean |
| `unknown` | dispatcher target/calldata arbitrer, proxy fallback dinamis, penerusan eksternal belum pasti — diselesaikan transitif di Tahap C |
| `no` | HANYA: (i) `view`/`pure`/getter yang tidak menulis storage; (ii) `receive` berbadan kosong; (iii) konfigurasi terkunci modifier peran istimewa murni tanpa jalur pemicu publik — `notes` = `PRIVILEGED_ONLY: <modifier>`; (iv) hanya menulis storage non-ekonomi — `notes` = `COSMETIC_NON_ECONOMIC: <storage> \| pembaca: <hasil AST/grep pembaca>` |

- `initialize` TIDAK BOLEH `PRIVILEGED_ONLY` kecuali terbukti dikunci (konstruktor/`disableInitializers`) dan terverifikasi live di B8.
- Getter non-view yang menulis state (`sync`/`poke`/`exchangeRate` yang menyemar state) = `state_mutator`.
- `COSMETIC_NON_ECONOMIC` sah hanya bila storage-nya **tidak dibaca** fungsi mana pun yang memindahkan nilai, menghitung saldo/share/rate/fee/batas, memeriksa izin/peran, atau menentukan alamat tujuan. Pembaca dibuktikan dengan AST (daftar pembaca variabel). Ragu → `state_mutator`.
- `receive` kosong pada kontrak yang memakai `address(this).balance` dalam akuntansi tetap `no`, tetapi **wajib** dibuatkan `IN-x` kelas `PASSIVE`.

### 8 konvensi sensus (B14)

| # | Konvensi | Konsekuensi baris |
| --- | --- | --- |
| 1 | Getter publik = entrypoint | `entrypoint: true` |
| 2 | `receive` badan kosong = `no`; ada perpindahan lanjutan → `yes`; tak pasti → `unknown` | dinilai dari badan |
| 3 | Payable yang memanggil sistem eksternal yang diketahui = `yes` sementara; Tahap C wajib verifikasi penerusan value; bila tidak meneruskan → `state_mutator` atau `no` sesuai B14-v2 | `yes` sementara |
| 4 | Dispatcher target/calldata arbitrer = `unknown` + catat target | diselesaikan Tahap C |
| 5 | Getter auto-generated dibariskan | satu baris per getter |
| 6 | Entrypoint warisan TIDAK dibariskan (satu baris per definisi); Tahap C wajib perluasan warisan sebelum segmentasi | tanpa duplikasi |
| 7 | Berkas direct/proxy dicatat dua lapis: milik-sendiri + warisan | dua kolom |
| 8 | **(v2.1)** Modifier peran non-standar (`onlyHubPool`, `onlyRole(X)`, `onlySelf`, `onlyFromCrossDomainAdmin`, dan setara) **bukan** `PRIVILEGED_ONLY` otomatis. Sah hanya bila pemegang peran terbukti aktor istimewa. Bila pemegang adalah kontrak yang bisa dipicu publik → `state_mutator`/`yes` | `notes` sebut pemegang peran |

### Field wajib per baris JSON

```
file, contract, function, line, end_line, visibility, mutability,
payable, modifiers, entrypoint, value_moves, mechanisms, events_emitted,
external_calls, storage_writes, ast_hint, domain_variant, notes
```

- `modifiers`, `external_calls`, `storage_writes`, `ast_hint` boleh diisi dari AST (diverifikasi saat baca badan).
- `domain_variant`: kosong untuk kontrak inti; `VK-x` bila berkas varian (dari B0).
- `notes`: wajib untuk `unknown`, `state_mutator` (storage yang ditulis), semua `no` pada entrypoint non-view (tag).

**EP+VM** (entrypoint + `yes`) dan **EP+SM** (entrypoint + `state_mutator`) = angka yang mengikat. Bukan EP total.

### Kontrol positif & nol mekanis

- Pilih **9 fungsi** yang pasti memindah nilai; buktikan tiap satu **ada** dengan `value_moves: yes`. Wajib **9/9**.
- Untuk `MULTI-DOMAIN`/`BERINSTANS`: minimal **2 dari 9** berasal dari berkas varian (`VK-x`) — membuktikan sensus tidak buta varian.
- Hitungan mekanis yang menghasilkan **0** untuk sesuatu yang seharusnya ada = wajib dipecahkan.

### Yang TIDAK dilakukan saat sensus

- Baca mendalam memahami logika (mengklasifikasi, bukan memahami) — mendalam di Tahap C.
- Menyelesaikan semua `unknown`.
- Rerun sensus penuh sebagai syarat (enumerasi kedua = sapuan B9 dengan AST independen).

## Langkah 3 — B03 Sensus live ringan (B7)

Wajib untuk MAINNET/TESTNET; `REPO-ONLY` hanya bila stage Tahap A = `PRE-DEPLOY / REPO-ONLY`.

- **`TUNGGAL` / `TUNGGAL-BERINSTANS`:** anggaran **≤ 5 menit**. `getCode` 1–3 alamat inti di blok referensi + satu view murah. Tetapkan blok pin.
- **`MULTI-DOMAIN`:** anggaran **≤ 5 menit per keluarga domain** (bukan per domain). Untuk domain utama + **satu representatif per keluarga**: `getCode` kontrak inti + satu view murah + penetapan **blok pin per domain**. Isi kolom `Status` Matriks Domain. Domain non-representatif: `UNVERIFIED` sampai B8 Lintasan yang menyentuhnya.
- Routing on-chain (mis. tabel adapter/route per domain di kontrak hub) **boleh** dibaca di sini bila satu panggilan view mengembalikan seluruh tabel; bila per-entri, tunda ke B8.
- RPC gagal (timeout/403/429) → jangan tunggu, pindah ke representatif lain di keluarga sama; semua gagal → catat apa yang dicoba, verifikasi pindah ke B8.
- **TIDAK termasuk B7:** jejak event, hitung log, verifikasi seluruh inventaris alamat.

## Langkah 4 — B8 Live-Match Lintasan (rujukan; dijalankan di awal Tahap D)

- Dijalankan **di awal Tahap D tiap Lintasan, wajib lulus sebelum Gate D**. Tanpa B8, PoC Lintasan itu **TERBLOKIR**.
- Dibaca **per domain eksekusi segmen** (B21): tiap `LP-x` di domain tempat segmen pembacanya berjalan, pada blok pin domain itu.
- Getter revert → baca slot (`cast storage`, layout dari AST). Tetap tak terbaca → `UNVERIFIED` (bukan `LIVE`).
- Tidak live-match → `TUNDA-LIVE` (tercatat di ledger, nol waktu eksekusi, ditinjau di sapuan akhir).
- Cara kerja mengikat: utamakan alur + cek desain kode; pindai log = verifikator terakhir (Tahap G/sapuan akhir). Pengecualian sampel: 3–5 tx terbaru per entrypoint Lintasan aktif, ≤ 5 menit per Lintasan, hanya untuk contoh `CALLER-INPUT`.
- Definisi live-match L1–L4 mengikuti `AGENTS.md` §3.

## Langkah 5 — B04-STREAMS-AND-CLUSTERS.md (4 bagian)

### Bagian 1 — Indeks Klaster Universal

Kelompokkan **EP+VM** dan **EP+SM** ke 4 tipe peran tanpa bias nama proyek:

| Tipe | Definisi |
| --- | --- |
| `CORE-FLOW` | alur nilai utama pengguna/protokol |
| `SHARED-PRIMITIVE` | token internal, pustaka math/share/pembulatan, brankas akuntansi bersama, kontrol akses dasar — dipetakan ke `C00-SHARED-PRIMITIVES.md` di awal Tahap C |
| `EXTERNAL-BOUNDARY` | target eksternal di luar kode scope — dicatat sebagai handoff terbuka |
| `NON-PROD-SKIP` | mock, fixture uji, skrip usang — dicatat, dilewati utuh |

Mock/adapter uji (mis. `Mock_*`) wajib `NON-PROD-SKIP` dan **tidak** boleh dihitung ke Stream mana pun.

### Bagian 2 — Katalog Awal Stream & Lintasan

- Definisikan `STR-nn` dari **Ingress → Egress** siklus hidup nilai (bukan dari klaster, bukan dari sisa ledger).
- Tiap Stream wajib punya: `Value_Holder` (+ alamat per domain), `Sink` (`USER` / `FEE_RECIPIENT` / `BRIDGE_OUT:<domain>` / `HB-x → <STR-yy>`), `Live_Balance@pin` = `DIISI_B8`. `Sink` tak bisa ditentukan → `SINK_BELUM_JELAS`, wajib selesai di Tahap C sebelum D.
- **Lintasan awal `STR-nn.Lk`** — usulan kasar pemecahan per mode B0 (dikoreksi di Tahap C saat anggaran B19 dihitung):
  - `TUNGGAL`: 1 Lintasan per Stream, atau per fase bila Stream jelas besar.
  - `TUNGGAL-BERINSTANS`: 1 Lintasan per keluarga varian/kelas aset yang mengubah alur (bukan per instance).
  - `MULTI-DOMAIN`: Lintasan per keluarga domain untuk Stream yang berperilaku beda per domain; Stream lintas-domain (transport hub→domain, domain→hub) dipecah per keluarga transport.
- **Larangan Stream sapu sisa (B22):** Stream tidak boleh didefinisikan sebagai "semua yang tersisa". Label wajib sesuai isi; Stream berlabel admin tidak boleh berisi EP+VM permissionless.
- Urutan `B2a` (pintu masuk pertama yang dilalui pengguna; EV dicatat sebagai data, bukan penentu) + `B2a-PostAudit` bila metadata audit ada (`[DELTA]`/`[SCAR]`/`[SEAM]` → Tier 1; `Prerequisite C-Only Pass`; Tier 2 sampai sisa 0).
- **Flow Family** (`FAM-xx`): Stream satu siklus hidup lewat beberapa tx, tersambung `Sink: HB-x → STR-yy`; dikerjakan berurutan tanpa disela.
- **Twin-Path Group** (`TPG-xx`): Stream/Lintasan dengan fungsi ekonomi setara lewat varian berbeda. Di `BERINSTANS`/`MULTI-DOMAIN`, keluarga varian dari B0 otomatis menjadi TPG.

### Bagian 2b — Katalog Ingress `IN-x` (B17, BARU v2.1)

Satu baris per cara nilai/klaim bisa bertambah di sebuah `Value_Holder`:

| Kelas | Contoh | Deteksi (AST + baca) |
| --- | --- | --- |
| `USER` | deposit, swap, mint | EP+VM |
| `ACTOR` | keeper, relayer, liquidator, harvester, bot publik | EP+VM/EP+SM dengan pemicu non-pengguna |
| `CALLBACK` | messenger bridge, `lzCompose`, `on*Received`, flash-loan callback, oracle push, handler pesan | entrypoint yang dipanggil kontrak eksternal |
| `PASSIVE` | transfer ERC-20 langsung, donasi, `selfdestruct`/force-feed, `receive` kosong, airdrop pihak ketiga | `balanceOf(address(this))` / `address(this).balance` dibaca di jalur nilai |
| `ACCRUAL` | yield/rebase, bunga per waktu, smear fee | rumus membaca `block.timestamp` atau saldo token rebasing |
| `ADMIN` | top-up, rescue, haircut | fungsi `PRIVILEGED_ONLY` yang mengubah saldo/klaim |

Kolom: `IN_ID | Kelas | Value_Holder | Pintu (fungsi:baris atau "transfer langsung") | Pembaca akuntansi (fungsi:baris) | Lintasan pengikat (usulan) | Status`.

**Wajib minimal satu baris `PASSIVE` per `Value_Holder`** yang membaca saldonya sendiri dalam akuntansi; bila tidak ada pembaca saldo sendiri, tulis `PASSIVE: TIDAK_BERDAMPAK — <bukti AST: tidak ada pembacaan balanceOf(this)>`.

### Bagian 3 — Relasi kasar

Handoff detail (`H1..Hn-1`), simpul, `CY-x` dihitung per Lintasan di Tahap C. Di `B04` cukup relasi kasar antar-klaster dan antar-domain.

## Langkah 6 — B05 Ledger sisa (seed) — 3 populasi

- seluruh `EP+VM(yes)` → `BELUM_MASUK_STREAM`;
- seluruh `EP+SM(state_mutator)` → `BELUM_TERCAKUP` (belum masuk koridor / belum terdaftar penulis di `B07`); `EP+SM` berdiri sendiri (mis. `initialize` publik) → unit pemeriksaan sendiri;
- seluruh `IN-x` → `BELUM_TERIKAT`;
- daftar `STR-nn` dan `STR-nn.Lk` → `PENDING`;
- tabel `HANDOFF_TERBUKA`, `TUNDA-LIVE`, `DORMAN`, `UNVERIFIED`.

**Aturan penyusutan:** tiap Lintasan selesai Tahap C → semua EP+VM/EP+SM yang dilalui → `TERPETAKAN_DI_<STR>.<Lk>`; IN-x yang diikat → `TERIKAT_DI_<STR>.<Lk>`. **Tulis nama, bukan hanya jumlah.**
**Rekonsiliasi berbasis nama (v2.1):** sisa dihitung ulang dari daftar nama yang belum berstatus `TERPETAKAN_`/`TERIKAT_`, bukan dari pengurangan angka berjalan. Bila katalog awal habis dan sisa > 0 → bentuk Stream/Lintasan baru menurut Ingress→Egress (B22), bukan Stream sapu sisa.
B10: ledger diperbarui sesudah tiap round; round selesai hanya bila sisa menyusut; target buruan harus ada di sensus.

## Langkah 7 — B06 Registry invariant + B07 State-Bridges

- `B06`: struktur + penomoran global, **isi kosong**. Prefiks yang disiapkan: `INV-S`, `INV-H`, `INV-HB`, `INV-J`, `INV-F`, `INV-CY` (serah kendali), `INV-V` (selisih varian), `INV-IN` (Ingress).
- `B07`: header baku `Bridge_ID | Storage_Var_&_Contract | Writer_Lintasan_&_Guarantee | Reader_Lintasan_&_Assumption | Window_&_Trigger | Sync_Status`.
  - `Window_&_Trigger`: jeda/tenggat yang mengatur kapan pembaca boleh jalan (liveness, delay, epoch, deadline) + siapa yang boleh memicu pembaca (`USER`/`ACTOR`/`ADMIN`/`EXTERNAL`).
  - `Sync_Status` (enum): `SEED` → `WRITER_MAPPED` / `READER_MAPPED` → `SINKRON` | `DESINKRON:<OBS-id>` | `TERBUKA_EKSTERNAL`.

## Larangan Tahap B

1. Inventaris mendalam semua klaster/Lintasan sekaligus (termasuk Tabel Selisih penuh).
1. Menulis invariant.
1. Buruan saat memetakan.
1. Eksekusi/verifikasi saat memetakan (handoff di B deskriptif).
1. Sensus live penuh (semua domain, jejak event lengkap).
1. Baca mendalam semua fungsi saat sensus.
1. Menyelesaikan semua `unknown`.
1. Menilai Stream/klaster ("bersih/berbahaya").
1. Rerun sensus penuh sebagai syarat.
1. Memoles artefak.
1. Filter di dalam Stream/Lintasan saat inventory.
1. **(v2.1)** Mengisi `value_moves` dari output AST tanpa membaca badan.
1. **(v2.1)** Membentuk Stream sapu sisa.

## Penutupan graf + sapuan akhir (B9) — dicatat di sini, dieksekusi di akhir

Bukti kelengkapan datang dari: baca ulang per Lintasan; cek handoff + konservasi; jejak event live (verifikator akhir); cek penutupan graf.
**Penopang wajib (v2.1):** enumerasi **AST independen** (alat berbeda dari alat lokalisasi bila mungkin) dibandingkan **per nama** dengan ledger akhir, termasuk pembandingan `IN-x` (pembacaan saldo sendiri, `receive`, `selfdestruct`) dan kandidat `CY-x` (semua panggilan eksternal di fungsi koridor). Rerun sensus manual tetap sah sebagai alternatif. Regex yang sama tidak sah.

## Definition of done Tahap B

- `B00-TOPOLOGY.md`: DOM/VK/VC + kelas aset + mode (konsisten dengan hitungan) + Matriks Domain bila `MULTI-DOMAIN`
- `B01-SCOPE.md` + scope lock 4 syarat
- `B02-CENSUS-STATIC.md` + JSONL + rekonsiliasi AST (selisih 0 atau terjelaskan per nama); kontrol positif 9/9 (≥ 2 dari varian bila mode ≠ TUNGGAL); nol mekanis terpecahkan; nol baris `no` melanggar B14-v2
- `B03-CENSUS-LIVE.md`; B7 dalam anggaran; blok pin per domain representatif; kegagalan RPC tercatat
- `B04-STREAMS-AND-CLUSTERS.md`: klaster 4 tipe; Stream dari Ingress→Egress (tanpa sapu sisa) + Lintasan awal per mode; `Value_Holder`/`Sink`/`Live_Balance@pin`; Katalog Ingress `IN-x` (≥ 1 `PASSIVE` atau `TIDAK_BERDAMPAK` per Value_Holder); Flow Family; Twin-Path
- `B05-LEDGER-SISA.md` 3 populasi, nama per baris
- `B06` struktur kosong (prefiks v2.1); `B07` header baku + enum
- nol invariant; nol buruan; nol PoC

---

## Lampiran — warisan v2.0 yang TETAP BERLAKU (tidak tercakup teks A03)

Bagian ini dipertahankan agar penambahan lama tidak hilang saat A03 mengganti berkas. Isinya **mengikat**, setara bagian di atas.

### L1. B16 — TIDAK DIPAKAI (jangan bangun ulang)

Field `keluar` per fungsi EP+VM **tidak wajib**; daftar jahitan `SM-xx` lengkap **tidak wajib**. Urutan Stream = **pintu masuk pertama kali** (B2a), bukan EV. **Jangan bangun pass enumerasi jahitan terpisah.** Detail handoff per-Lintasan dihitung di Tahap C; jeda aliran pada variabel storage dicatat ke `B07-STATE-BRIDGES.md`.

### L2. Verifikasi gerbang (wajib dijalankan, bukan opsional)

```
python3 tools/verify_flow.py check-b0 <audit_dir>                  # B00-TOPOLOGY + IN-x + Matriks Domain
python3 tools/verify_flow.py check-b  <audit_dir> --repo <repo>    # artefak B + sensus JSONL
python3 tools/verify_flow.py check-staging <file>                  # staging subagent sebelum merge
```

Exit 0 = LULUS, 1 = GAGAL beserta daftar pelanggaran spesifik. `check-b` menolak baris `entrypoint: true` + mutability non-view/pure + `value_moves: "no"` tanpa tag `PRIVILEGED_ONLY:` / `COSMETIC_NON_ECONOMIC:` / bukan `receive` kosong. Proyek lama (format v2.0) ditandai `LEGACY-v2.0` di baris pertama `B04-STREAMS-AND-CLUSTERS.md` agar verifier menerima kedua format.

### L3. B8 — cek desain kode dulu (mengikat, 17 Nov 2026)

Untuk memutuskan "nilai ini 0 atau bukan": **cek desain kode lebih dulu** — apakah kode **men-set 0** atau **bisa memuat**? Nilai yang di-set dari parameter input tanpa `require`/validasi = **bisa memuat non-zero by design**; live 0 berasal dari off-chain, bukan batasan kode. Preseden buruk yang tidak boleh diulang: satu B8 memakan ~8,5 jam memindai event per rantai (BSC gagal total, Base gagal per chunk ~20 menit/chunk).

### L4. Blok referensi (A5)

Blok referensi/pin ditetapkan di Langkah 3 dan **dicatat sebagai koreksi eksplisit** bila berbeda dari dugaan Tahap A. Untuk `MULTI-DOMAIN`: satu blok pin per domain representatif; domain non-representatif mewarisi status `UNVERIFIED` sampai B8 Lintasan yang menyentuhnya.

### L5. B2a-PostAudit — rincian dua tier

Bila ada Stream ber-tag `[DELTA]`/`[SCAR]`/`[SEAM]`:
- **Tier 1 (Hot Streams First)** dikerjakan lebih dulu (urutan antar-sesamanya tetap `B2a`);
- **`Prerequisite C-Only Pass`** untuk Stream hulu dingin yang state-nya dibutuhkan: jalankan **hanya Tahap C + 1 transaksi normal di `FlowFixtures`** (tanpa D/E pada Stream dingin itu);
- **Tier 2** menyapu `D -> E -> G` semua Stream `[COLD-AUDITED]` sampai sisa `0`.

Cakupan 100% tetap mutlak — tier adalah pengurutan prioritas, **bukan** pemangkasan scope.

### L6. DoD tambahan

- [ ] nol baris `no` melanggar B14-v2 — dibuktikan lewat `check-b` (bukan dibaca manual saja)
- [ ] setiap baris ledger menyebut **nama** `(file, contract, function)` / `IN-x`, bukan hanya jumlah
- [ ] `B07` memakai enum `Sync_Status` A03 (`SEED`/`WRITER_MAPPED`/`READER_MAPPED`/`SINKRON`/`DESINKRON:<OBS-id>`/`TERBUKA_EKSTERNAL`) + kolom `Window_&_Trigger`
- [ ] `B04` Bagian 2b memuat **minimal satu baris `PASSIVE`** per `Value_Holder` (atau `PASSIVE: TIDAK_BERDAMPAK` + bukti AST)
