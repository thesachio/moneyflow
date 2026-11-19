---
name: flow-b-map
description: Tahap B — Mapping. Sensus statis 100% peristiwa pemindah nilai (B1/B6, 7 konvensi B14 lengkap, tanpa AST), sensus live ringan B7 wajib, B04-STREAMS-AND-CLUSTERS (klaster 4 tipe + katalog Stream + Twin-Path) + B07-STATE-BRIDGES, cek live-match B8 + TUNDA-LIVE, ledger sisa (B10), handoff dari batas unit (B11), scope lock (B13). Skill ini memuat aturan yang dibutuhkan sampai Tahap B selesai. Dipakai saat memetakan scope proyek, sensus, atau saat user menyebut tahap B, mapping, sensus, scope.
---

# Skill flow-b-map — Tahap B (Mapping)

Tahap B = tahu scope menyeluruh di awal (sensus utuh + peta alur), **tanpa buruan**.
Skill ini memuat aturan yang dibutuhkan untuk menjalankan Tahap B sampai selesai. `methodology/aturan-alur-first.md` (B1–B16) hanya rujukan bila ada sengketa tafsir — jangan buka methodology untuk mencari langkah; langkahnya ada di sini.

## Uji pemisah (pakai ini untuk memutuskan "ini pekerjaan B atau bukan")

Tahap B mengerjakan **hanya** yang butuh pandangan seluruh protokol dan **tidak bisa direkonstruksi** tahap berikut tanpa baca ulang seluruh protokol.
Butuh konteks satu klaster/Stream saja → bukan Tahap B; kerjakan di giliran Stream itu (C/D/E).

## Keluaran (sekali, untuk seluruh protokol)

7 berkas kanonik, semua wajib ada:

| Artefak | Isi |
| :--- | :--- |
| `B01-SCOPE.md` | daftar scope + scope lock (B13) |
| `B02-CENSUS-STATIC.md` + `scripts/out/*.jsonl` | sensus statis 100% (satu baris JSON per fungsi) |
| `B03-CENSUS-LIVE.md` | inventaris alamat live (daftar) + sensus live ringan B7 — **wajib ≤5 menit untuk MAINNET/TESTNET**; hanya ditandai `REPO-ONLY` bila stage Tahap A adalah `PRE-DEPLOY / REPO-ONLY` |
| `B04-STREAMS-AND-CLUSTERS.md` (menggantikan nama lama `B04-CLUSTERS.md`) | indeks klaster universal 4 tipe + katalog awal Stream + urutan B2a + Twin-Path Group + relasi handoff kasar |
| `B05-LEDGER-SISA.md` | ledger sisa seed (B10) |
| `B06-REGISTRY-INVARIANT.md` | struktur + penomoran, **isi kosong** (diisi Tahap D) |
| `B07-STATE-BRIDGES.md` (**BARU — moneyflow v2.0**) | kerangka tabel jembatan state lintas-Stream; diinisialisasi dengan header kolom baku: `Bridge_ID | Storage_Var_&_Contract | Writer_Stream_&_Guarantee | Reader_Stream_&_Assumption | Sync_Status` |

## Langkah 1 — B13 Scope lock (gerbang masuk; sebelum sensus)

Empat syarat, semuanya harus benar sebelum satu baris sensus ditulis:

1. **Daftar berkas cocok persis** inventaris kanonik — `diff` kosong antara daftar yang dipakai sensus dan daftar scope yang dikunci.
2. **Commit terverifikasi** — `git rev-parse HEAD` pada repo target, dan `git status --porcelain` bersih (nol baris).
3. **`contracts/` bersih** — tidak ada berkas build/artefak yang menyamar sebagai sumber.
4. **Pemetaan tiga arah aset program ↔ alamat ↔ berkas** — dari `program_assets` di `INTEL.md` + berkas `deployments/` (atau setara) di repo target, buat tabel di `B01-SCOPE.md`:
   `| Aset program | Chain | Alamat | Kontrak | Berkas repo (Path/File.ext) | Status |`
   Status: `COCOK` / `ASET_TANPA_BERKAS` (alamat in-scope, sumbernya tidak ada di repo/commit pin) / `BERKAS_DI_LUAR_PROGRAM` (berkas ada di repo, tidak termasuk aset program) / `OUT_OF_SCOPE_PROGRAM` (masuk daftar pengecualian program).
   Aturan: baris `ASET_TANPA_BERKAS` = eskalasi ke user sebelum sensus. Baris `BERKAS_DI_LUAR_PROGRAM` dan `OUT_OF_SCOPE_PROGRAM` tetap disensus (cakupan statis 100% tidak berubah), tapi Stream yang seluruh koridornya hanya berisi berkas berstatus itu dicatat di `B04` dan dikerjakan paling akhir. Bila `program_assets: TIDAK ADA`, syarat ke-4 dicatat `TIDAK BERLAKU (program tanpa daftar aset)`.

Drift di luar scope **dicatat, tidak dihitung**. Bukti: simpan daftar scope (`scripts/out/scope-all.txt`) lalu bandingkan dengan daftar yang benar-benar diproses sensus.

## Langkah 2 — B02 Sensus statis 100% (B1 + B6 + B14)

### Apa yang dihitung (B1)

Sensus = **100% peristiwa pemindah nilai**, bukan hanya fungsi:

- entrypoint (fungsi yang bisa dipanggil dari luar)
- transfer langsung / donasi / force-feed
- pergerakan level-sistem (`selfdestruct`, `coinbase`, precompile)
- multicall / dispatch dinamis **transitif** (ikuti ke target/implementasi)
- proxy → implementation
- callback / hook
- transfer native/SPL ke PDA (non-EVM)
- langkah off-chain — **dilabeli asumsi**, bukan dihitung sebagai fungsi

**Fungsi = unit sensus (kelengkapan). Segmen = unit buruan (partisi).**

### B14-v2 — 4 nilai sah `value_moves` (revisi ketat 19 Nov 2026)

| Nilai | Kriteria |
| :--- | :--- |
| `yes` | memindahkan aset/token/native langsung ATAU mengubah saldo/share/klaim finansial langsung |
| `state_mutator` | `entrypoint: true`, tidak memindahkan aset langsung, bukan khusus admin terverifikasi, TETAPI menulis storage — `initialize`/setup, allowance/operator/recipient/delegasi, indeks/snapshot/timestamp/twap/sync/poke, siklus hidup posisi (merge/split/lock), pembuatan pool/rute publik, pembatalan/penguncian antrean |
| `unknown` | dispatcher target/calldata arbitrer, proxy fallback dinamis, penerusan eksternal belum pasti — diselesaikan transitif di inventaris alur |
| `no` | HANYA: (i) `view`/`pure`/getter yang sama sekali tidak menulis storage; (ii) `receive` berbadan kosong; (iii) fungsi konfigurasi terkunci rapat modifier peran istimewa murni (`onlyOwner`/`onlyAdmin`/`onlyGovernance`/`onlyTimelock`) tanpa jalur pemicu publik — WAJIB `notes` = `PRIVILEGED_ONLY: <nama_modifier>`; (iv) fungsi yang hanya menulis storage non-ekonomi — WAJIB `notes` = `COSMETIC_NON_ECONOMIC: <storage yang ditulis>` (lihat definisi di bawah) |

- Fungsi `initialize` TIDAK BOLEH `PRIVILEGED_ONLY` kecuali terbukti dikunci (konstruktor/`disableInitializers`) dan terverifikasi pada objek live di B8.
- Getter non-view yang menulis state (`sync`/`poke`/`exchangeRate` yang menyemar state) = `state_mutator`, BUKAN `no`.
- **`COSMETIC_NON_ECONOMIC:`** hanya sah bila storage yang ditulis **tidak dibaca** oleh fungsi mana pun yang memindahkan nilai, menghitung saldo/share/rate/fee/batas, memeriksa izin/peran, atau menentukan alamat tujuan. Contoh sah: metadata URI/nama tampilan, penanda UI, penghitung statistik yang tidak dibaca jalur nilai. `notes` wajib menyebut storage yang ditulis + bukti "tidak dibaca jalur nilai" (grep pembaca variabel itu). Ragu → `state_mutator`, bukan `no`.
- **Dua populasi yang mengikat cakupan: `EP+VM(yes)` DAN `EP+SM(state_mutator)`** — bukan EP total.
- Pemverifikasi otomatis (`tools/verify_flow.py check-b`) MENOLAK baris `entrypoint: true` + mutability non-view/pure + `value_moves: "no"` yang tidak membawa tag `PRIVILEGED_ONLY:` / `COSMETIC_NON_ECONOMIC:` / bukan `receive` kosong.

### Cara membaca (B6 — mengikat)

- **Baca manual penuh**: semua fungsi di semua berkas dibaca dan dapat verdict.
- **TIDAK pakai AST.** Penghitung AST pernah dibangun dan divalidasi di pilot, lalu **ditolak** — jangan bangun ulang.
- **Baca bertingkat DITOLAK** untuk sensus statis (classifier + baca sebagian). Kedalaman sensus statis tidak diambil risiko.
- Skrip penghitung mekanis **boleh** dipakai untuk *melokalisasi* (file, function, line, end_line, visibility) dan sebagai daftar periksa — **tetapi verdict `value_moves` tidak boleh diisi skrip**. Verdict diisi setelah badan fungsi dibaca.
- Biaya jujur satu putaran: **~14–23 menit** untuk ~200 berkas / ~1.200 baris (pilot). Skala proporsional untuk repo lebih besar; **jangan potong kedalaman**.

### 7 konvensi sensus (B14 — universal, dipakai apa adanya)

| # | Konvensi | Konsekuensi baris |
| :-: | :--- | :--- |
| 1 | **Getter publik = entrypoint (ya).** Entrypoint = bisa dipanggil dari luar (literal, mekanis); filter nilai lewat `value_moves`. | getter → `entrypoint: true` |
| 2 | **`receive` badan kosong = `value_moves: no`.** Menerima saja bukan memindahkan. Nilai dinilai dari **badan**: ada perpindahan lanjutan (transfer keluar / perubahan saldo pihak lain) → `yes`; hanya menerima → `no`; tidak bisa dipastikan → `unknown`. | `receive` kosong → `no` |
| 3 | **Fungsi payable yang memanggil sistem eksternal yang diketahui** (misal: relayMessage adapter → messenger bridge, liveness toggle, fee splitter) = `value_moves: yes`. Tahap alur **WAJIB** verifikasi penerusan value per adapter dari badan — bila ternyata tidak meneruskan, turunkan menurut B14-v2: **`state_mutator`** bila fungsi masih menulis storage, **`no`** hanya bila memenuhi salah satu kriteria `no` di tabel B14-v2. | `yes` sementara, wajib dikonfirmasi |
| 4 | **Dispatcher dengan target/calldata arbitrer** (Multicall3 `aggregate*`, `deployAndExecute`, `directWithdraw`, metarouter generik) = `value_moves: unknown`. Diselesaikan **transitif di inventaris alur** (ikuti ke implementasi/target), bukan di sensus. | `unknown` + catat target |
| 5 | **Getter auto-generated DIBARISKAN** (konsisten dengan butir 1): semua getter publik punya baris sendiri. | satu baris per getter |
| 6 | **Entrypoint warisan TIDAK dibariskan** — satu baris per **definisi**, di berkas pendefinisi. Tahap alur **WAJIB** punya langkah perluasan permukaan lewat implementasi/warisan sebelum segmentasi. | jangan duplikasi baris warisan |
| 7 | **Atribut berkas direct/proxy dicatat dua lapis**: permukaan milik-sendiri + permukaan warisan. Inventaris alur memakai lapis **warisan** untuk permukaan deployed, lapis **milik-sendiri** untuk lokasi kode. | dua kolom, bukan satu |

### Field wajib per baris JSON

```
file, contract, function, line, end_line, visibility, mutability,
payable, entrypoint, value_moves, mechanisms, events_emitted,
external_calls, notes
```

- `entrypoint`: `true` bila public/external (termasuk getter, `receive`, `fallback`).
- `value_moves`: `yes` / `state_mutator` / `no` / `unknown` — **hanya** menurut B14-v2.
- `mechanisms`: mekanisme yang terlihat di badan (transfer, mint, burn, delegatecall, assembly, selfdestruct).
- `notes`: alasan verdict bila tidak obvious; **wajib** untuk `unknown`; **wajib format `PRIVILEGED_ONLY: <modifier>`** untuk fungsi admin yang dilabeli `no`; **wajib** menyebut storage yang ditulis untuk `state_mutator`.

**EP+VM** (entrypoint DAN `value_moves: yes`) DAN **EP+SM** (entrypoint DAN `value_moves: state_mutator`) = angka yang **mengikat** untuk inventaris alur. Bukan EP total.

### Kontrol positif (wajib, bukan opsional)

Pilih **9 fungsi yang sudah diketahui pasti memindah nilai** (fungsi transfer/withdraw/swap/deposit utama), lalu buktikan tiap satunya **ada** di sensus dengan baris yang benar dan `value_moves: yes`.
Hasil wajib **9/9**. Kurang satu = sensus buta, ulangi bagian itu.

### Nol mekanis wajib dipecahkan

Hitungan mekanis yang menghasilkan **0** untuk sesuatu yang seharusnya ada = **wajib dipecahkan** (cari nama sebenarnya, cek regex, cek warisan), **bukan diterima** sebagai "memang tidak ada".

### Yang TIDAK dilakukan saat sensus

- Baca mendalam untuk memahami logika tiap fungsi — sensus **mengklasifikasi**, bukan memahami. Baca mendalam hanya untuk fungsi EP+VM + di Tahap C.
- Menyelesaikan semua `unknown` — `unknown` **dicatat sebagai unknown**, diselesaikan di Tahap C saat konteks alurnya ada.
- Rerun sensus penuh sebagai syarat.

## Langkah 3 — B03 Sensus live ringan (B7 — WAJIB untuk MAINNET/TESTNET; hanya dilewati bila stage = `PRE-DEPLOY / REPO-ONLY`)

Anggaran **maks 5 menit** untuk seluruh B7. Isi:

1. `getCode` **1–3 alamat inti** pada **blok referensi**.
2. Bila ada kode: **satu** panggilan view murah (`owner()`, `liveness()`, `totalSupply()`).

Aturan rantai:

- Rantai utama = rantai tempat kontrak inti ter-deploy (menurut INTEL + `deployments/`). Bila INTEL tidak eksplisit: rantai dengan alamat deployment inti terbanyak.
- Rantai utama gagal (RPC mati / tidak ada kode / tidak ada blok referensi) → **rantai utama kedua** (deployment inti terbanyak berikutnya).
- Satu rantai tidak merespons (timeout/403/429) → **jangan tunggu, langsung pindah**.
- Keduanya gagal → B7 selesai **dengan catatan** (apa yang dicoba + hasil); verifikasi pindah ke B8.

**TIDAK termasuk B7:** jejak event, hitung log, verifikasi seluruh inventaris alamat, cek rantai lain — itu B8 per-Stream.

**Blok referensi ditetapkan di sini** (A5) dan dicatat sebagai koreksi eksplisit bila berbeda dari dugaan Tahap A.

## Langkah 4 — B8 Cek live-match per Stream + TUNDA-LIVE

B8 **diulang di awal fase uji tiap Stream**, sebelum PoC ditulis. Tanpa B8, PoC Stream itu **TERBLOKIR**.

Tidak live-match → wadah **TUNDA-LIVE**:

- tercatat di ledger sisa (**tetap terhitung**, bukan hilang)
- **nol waktu eksekusi** (tanpa PoC, tanpa fork)
- dibuka lagi hanya bila deployment live muncul atau user memerintah cek ulang
- ditinjau ulang di sapuan akhir

**Cara kerja B8 (mengikat):**

1. **Utamakan alur.** Tahu mekanisme jalan atau tidak dari: baca kode + `cast`/cek live + uji fork di Tahap E. **Bukan** dari memindai log tx orang lain.
2. **Pindai log = verifikator terakhir.** Hanya untuk Tahap G / sapuan akhir. Preseden buruk: satu B8 memakan ~8,5 jam memindai event per rantai — jangan diulang.
3. **Cek desain kode dulu** untuk memutuskan "nilai ini 0 atau bukan": apakah kode **men-set 0** atau **bisa memuat**? Nilai yang di-set dari parameter input tanpa `require`/validasi = **bisa memuat non-zero by design**; live 0 berasal dari off-chain, bukan batasan kode.

## Langkah 5 — B04-STREAMS-AND-CLUSTERS.md (3 bagian)

**Bagian 1 — Indeks Klaster Universal.** Kelompokkan kontrak/fungsi **EP+VM(yes) dan EP+SM(state_mutator)** (B14-v2) ke dalam 4 tipe peran universal tanpa bias nama proyek:

| Tipe | Definisi |
| :--- | :--- |
| `CORE-FLOW` | kelompok alur nilai utama pengguna/protokol |
| `SHARED-PRIMITIVE` | token internal, pustaka matematika/share/pembulatan, brankas akuntansi bersama, kontrol akses dasar — **wajib dipetakan lebih dulu ke `C00-SHARED-PRIMITIVES.md` di awal Tahap C** |
| `EXTERNAL-BOUNDARY` | target eksternal di luar kode scope |
| `NON-PROD-SKIP` | mock, fixture pengujian, skrip usang — **dicatat lalu dilewati utuh, nol waktu eksekusi** |

**Bagian 2 — Katalog Awal Stream & Urutan Kerja `B2a`.**

- Definisikan daftar `Stream` (`STR-01`, `STR-02`, dan seterusnya sesuai jumlah Stream) berdasarkan titik masuk nilai/aksi pengguna pada `CORE-FLOW`.
- Urutkan daftar Stream memakai `B2a` (entrypoint paling awal yang dilalui pengguna dalam siklus hidup protokol, diikuti alur berikutnya secara kausal); EV live boleh dicatat sebagai data, **bukan penentu urutan**. Catat urutan + alasannya di `B04`.
- **Penandaan 3 tag pasca-audit (`B2a-PostAudit`, revisi 19 Nov 2026 — hanya bila metadata audit tersedia dari Tahap A):** di `B01-SCOPE.md` dan `B04`, tandai mekanis per berkas/Stream:
  - `[DELTA]` — berkas/fungsi yang ditambah/dimodifikasi pada `git diff <latest_audited_commit>..<pinned_commit>`;
  - `[SCAR]` — fungsi berjejak commit perbaikan (`fix`/`mitigation`/`audit`/pengetatan guard) di riwayat git;
  - `[SEAM]` — handoff/`HB-x` yang mempertemukan kontrak ter-audit dengan tidak-ter-audit atau cakupan audit terpisah.
  Bila metadata tidak tersedia → semua Stream `[COLD-AUDITED]`-netral dan urutan tetap `B2a` murni.
- **Urutan eksekusi dua tier (`B2a-PostAudit`)**: bila ada Stream ber-tag `[DELTA]`/`[SCAR]`/`[SEAM]` — Tier 1 (Hot Streams First) dikerjakan lebih dulu (urutan antar-sesamanya tetap `B2a`), dengan `Prerequisite C-Only Pass` untuk Stream hulu dingin yang dibutuhkan state-nya (hanya Tahap C + 1 transaksi normal di `FlowFixtures`), lalu Tier 2 menyapu `D -> E -> G` semua Stream `[COLD-AUDITED]` sampai sisa `0`. Cakupan 100% tetap mutlak — tier adalah pengurutan prioritas, bukan pemangkasan scope.
- Tandai pasangan/kelompok **Jalur Kembar (`Twin-Path Group`)** bila proyek punya dua Stream atau lebih yang menjalankan fungsi ekonomi setara lewat varian mekanisme/kontrak berbeda (misal: dua jenis pool, dua jalur router, penarikan instan vs antrean) — agar di Tahap D otomatis memicu pemeriksaan *Twin-Path Differential*. Bila salah satu sisi kembar membawa tag `[SCAR]`/`[DELTA]`, tandai eksplisit di grup — memicu Deep-Check pasangan di Tahap D.

**Bagian 3 — Aturan Handoff di Tahap B.** Handoff detail (`H1..Hn-1`) dan Simpul (`Fx/Jx`) **dihitung per Stream di Tahap C, BUKAN dirinci penuh semua di Tahap B** (agar Tahap B tetap cepat dan tidak melanggar larangan inventaris mendalam di depan). Di `B04` cukup catat **relasi kasar antar-klaster** bila terlihat dari sensus.

## Langkah 6 — B05 Ledger sisa (seed)

Seed memuat **DUA populasi yang mengikat (B14-v2)**:

- seluruh baris `EP+VM(yes)` berstatus `BELUM_MASUK_STREAM`;
- seluruh baris `EP+SM(state_mutator)` berstatus `BELUM_TERCAKUP` bila belum masuk koridor Stream dan belum terdaftar sebagai penulis di `B07-STATE-BRIDGES.md`; `EP+SM` yang berdiri sendiri (mis. `initialize` publik) wajib dibuatkan unit pemeriksaan sendiri;
- daftar `STR-01..STR-k` berstatus `PENDING`;
- tabel `HANDOFF_TERBUKA`;
- tabel pantau `TUNDA-LIVE` dan `DORMAN`.

**Aturan penyusutan (moneyflow v2.0):** setiap kali satu `Stream` dipetakan di Tahap C — termasuk fungsi lintas-klaster yang ikut tersapu dalam koridor Stream tersebut — semua `EP+VM` dan `EP+SM` yang dilalui langsung berubah status menjadi `TERPETAKAN_DI_<STREAM_ID>`. Bila saat seluruh `STR` awal habis masih ada `EP+VM(yes)` **atau** `EP+SM(state_mutator)` pada `CORE-FLOW` berstatus belum tercakup, **wajib dibuatkan `Stream` baru** (atau unit pemeriksaan untuk `EP+SM` berdiri sendiri) sampai sisa kedua populasi di `CORE-FLOW` tepat `0`.

Aturan B10 tetap: ledger diperbarui **sesudah tiap round**; round selesai **hanya bila sisa menyusut**; round tanpa hasil baru = sinyal berhenti dan periksa. Target buruan **harus ada di sensus** — kalau tidak, di luar scope menurut konstruksi.

## Langkah 7 — B06 Registry invariant (struktur saja)

Buat struktur + penomoran global. **Isi kosong.** Invariant dirumuskan di Tahap D (B12), bukan di B atau C.

## Larangan Tahap B (11 butir)

1. Inventaris mendalam semua klaster sekaligus.
2. Menulis invariant.
3. Buruan saat memetakan.
4. Eksekusi/verifikasi saat memetakan (kontrak handoff di B bersifat **deskriptif** — apa kata kode).
5. Sensus live penuh (semua rantai, jejak event lengkap).
6. Baca mendalam semua fungsi saat sensus.
7. Menyelesaikan semua `unknown` saat sensus.
8. Menilai/menghakimi klaster atau Stream saat memetakan ("ini bersih/berbahaya") — itu Tahap G; peta harus netral.
9. Rerun sensus penuh sebagai syarat tetap.
10. Memoles artefak/laporan akhir — artefak B adalah berkas kerja (JSON, daftar, ledger).
11. **Filter di DALAM klaster/Stream saat inventory** (hanya data yang dibutuhkan alur live) — dinilai berisiko, tidak diadopsi. Filter yang aman hanya **utuh per Stream**.

## B16 — TIDAK DIPAKAI

Field `keluar` per fungsi EP+VM **tidak wajib**; daftar jahitan `SM-xx` lengkap **tidak wajib**. Urutan Stream = **pintu masuk pertama kali** (B2a), bukan EV. Jangan bangun pass enumerasi jahitan terpisah. Detail handoff per-Stream dihitung di Tahap C; jeda aliran pada variabel storage dicatat ke `B07-STATE-BRIDGES.md` (moneyflow v2.0).

## Penutupan graf + sapuan akhir (B9) — dicatat di sini, dieksekusi di akhir

Sensus di depan adalah **rencana + daftar periksa, bukan bukti kelengkapan**. Bukti datang dari 4 mekanisme di eksplorasi:

1. baca ulang mendalam per Stream (koridor alirannya);
2. cek handoff + konservasi (delta tak terjawab diselidiki);
3. jejak event live sebagai enumerasi independen;
4. cek penutupan graf.

**Penopang wajib:** sapuan akhir dengan **enumerasi independen kedua** dibanding ledger akhir. Cara yang diterima: **rerun sensus manual** (pilot: rerun menemukan 15 baris yang sensus pertama lewatkan). Bukan AST, bukan regex yang sama.

Batasan jujur: cek penutupan tidak bisa menemukan item yang tidak ada di daftarnya.

## Definition of done Tahap B

Semua ini ada dan bisa ditunjuk:

- [ ] `B01-SCOPE.md` + scope lock empat syarat lulus (termasuk tabel pemetaan tiga arah)
- [ ] `B02-CENSUS-STATIC.md` + JSONL; kontrol positif **9/9**; nol mekanis terpecahkan; EP+VM(yes) dan EP+SM(state_mutator) dihitung; nol baris `no` melanggar B14-v2 (dicek `check-b`)
- [ ] `B03-CENSUS-LIVE.md`; B7 ≤5 menit; blok referensi ditetapkan; kegagalan RPC tercatat
- [ ] `B04-STREAMS-AND-CLUSTERS.md`; klaster 4 tipe + katalog Stream terurut B2a + Twin-Path Group + relasi kasar antar-klaster
- [ ] `B05-LEDGER-SISA.md` seed lengkap (EP+VM `BELUM_MASUK_STREAM` + EP+SM `BELUM_TERCAKUP`, `STR` `PENDING`, `HANDOFF_TERBUKA`, `TUNDA-LIVE`, `DORMAN`)
- [ ] `B06-REGISTRY-INVARIANT.md` struktur kosong
- [ ] `B07-STATE-BRIDGES.md` kerangka + header kolom baku: `Bridge_ID | Storage_Var_&_Contract | Writer_Stream_&_Guarantee | Reader_Stream_&_Assumption | Sync_Status`
- [ ] nol invariant ditulis; nol buruan; nol PoC
