# Aturan Alur-First — Tahap A (INTEL) dan Tahap B (Scope Mapping)

Status: aturan mengikat untuk metode alur-first. Metode kerja aktif sejak 22:33 WIB 16 Nov 2026 (diputus Kim: 'pakai paling mutakhir'; Segitiga menjadi rujukan/legacy). Disusun 15 Nov 2026. **Lapis Konstitusi moneyflow v2.0** (diputus 18 Nov
2026): arsitektur Stream-first (B2a-v2), klasifikasi klaster 4 tipe
generik (B4), artefak B07-STATE-BRIDGES + C00-SHARED-PRIMITIVES,
Aturan Koridor Stream, C10-v2, Gate D/E, B7 WAJIB, F inkremental,
C12 Stream Context Capsule
dari keputusan Kim + preferensi yang sudah mengikat. Sumber: draf
`usulan-alur-first.md` + `MEMORY.md` + berkas pilot
`~/workspace/theadvers/projects/across-flow-first/B01-SCOPE.md`.
Penerapan pertama: pilot Across.
Acuan workflow Tahap B (konsolidasi B1–B14 + definisi, untuk proyek
berikut): `acuan-workflow-tahap-B.md`.

Yang ada di sini hanya yang sudah diputus. Yang belum diputus tercatat di
bagian akhir sebagai usulan/belum diputus — bukan rule.

## A. INTEL

A1. INTEL = brief, bukan dokumen teknis. Isinya 9 butir: nama project
(singkat); deskripsi lingkup project (bridge/swap/LP dan lainnya, singkat);
deployment stage; Repo (alamat github atau setara); website (tempat user
akses dan interaksi UI aktif); docs (link); audit (singkat: siapa + link);
bugbounty (URL); brief severity (singkat bila ada).

A2. Pre-0 = daftar docs pendukung saja, BUKAN verifikasi teknis.

A3. Stage (MAINNET/TESTNET/DEVNET) = filter pertama yang menentukan Mode
Uji di D (FORK LIVE_MATCH). HEAD bisa lebih lama atau lebih baru dari
live — bukan patokan kebenaran. D fokus ke yang cocok LIVE_MATCH.

A4. Batas pencarian Tahap A (15 Nov 2026, perintah Kim): peran agen
Tahap A untuk proyek baru — mulai hanya dari nama proyek (+ tautan
yang user beri, bila ada). Tiap butir INTEL dicari lewat tangga
sumber berurutan, maks 3 cek per butir. Bila tangga habis tanpa hasil
→ TIDAK KETEMU (bukan bukti tidak ada). Tiga status hasil: DITEMUKAN
(dengan tautan), TIDAK ADA (sumber resmi menyatakan tidak ada),
TIDAK KETEMU (tangga habis, tidak terbukti ada/tidak). Tiap TIDAK
KETEMU wajib dicatat apa yang sudah dicoba (sumber + hasil). Dua
butir penahan beban: stage (butir 3) dan repo (butir 4) — bila salah
satunya TIDAK KETEMU, Tahap A berhenti dan eskalasi ke Kim (tidak
ditebak). Anggaran total penemuan maks 30 menit kerja agen; bila
habis, berhenti dengan hasil yang ada + TIDAK KETEMU untuk sisanya.
INTEL COMPLETE hanya bila semua butir DITEMUKAN (atau TIDAK ADA
dengan sumber yang menyatakan); bila ada TIDAK KETEMU → PARTIAL +
tabel Catatan Ketiadaan.

Tangga per butir (urutan cek):
- (1) Nama: dari user, tanpa pencarian. Bila ambigu, satu putaran
  klarifikasi; bila tetap ambigu, catat apa adanya.
- (2) Deskripsi lingkup: docs intro → README repo → deskripsi repo
  GitHub. Berhenti bila satu sumber menjelaskan lingkup dalam satu
  paragraf.
- (3) Stage: docs (apakah mainnet live?) → app UI (apakah hidup?) →
  repo (deployments/README). Stage di Tahap A = klaim docs/app/repo
  saja (A2: bukan verifikasi teknis); konfirmasi teknis di Tahap B
  (sensus live / deploy_parity). Bila tidak ada klaim → TIDAK KETEMU
  → eskalasi.
- (4) Repo: tautan di docs → GitHub search nama proyek → tautan di
  website. Hanya pilih bila jelas resmi (org cocok, ditaut dari
  docs); bila ada beberapa kandidat dan tidak jelas → TIDAK KETEMU
  (ambigu) + eskalasi. JANGAN menebak URL dari nama.
- (5) Website: tautan di docs → tautan di README repo → web search
  '<proyek> app'. Cek hidup murah: URL merespons (200/30x). Bila URL
  ketemu tapi tidak merespons → catat kodenya, bukan TIDAK KETEMU.
- (6) Docs: tautan di README → tautan di website → web search
  '<proyek> docs'. Sama: tidak merespons ≠ tidak ketemu.
- (7) Audit: halaman audit/security di docs → folder audits/ di repo
  → web search '<proyek> audit report' (1 pencarian, 3 hasil
  teratas). Bila tidak ketemu → TIDAK KETEMU + PARTIAL (tidak adanya
  di docs+repo bukan bukti tidak ada audit).
- (8) Bugbounty: halaman bug bounty di docs → SECURITY.md/README repo
  → web search '<proyek> bug bounty' (1 pencarian). Bila tidak
  ketemu → TIDAK KETEMU + PARTIAL.
- (9) Brief severity: diturunkan dari halaman bounty (butir 8). Bila
  bounty TIDAK KETEMU, severity ikut TIDAK KETEMU; tidak ada
  pencarian terpisah.

A5. INTEL dikunci dengan pin: commit + blok referensi (+ stage). INTEL
kanonik read-only selama audit — tidak disentuh. Bila D menemukan INTEL
salah, koreksi dicatat eksplisit dan terbuka, tidak diam-diam. Diputus 22:33 WIB 16 Nov 2026: (a) commit yang dipin di run dari-0 = HEAD saat penemuan; (b) blok referensi ditentukan di Tahap B (sensus live).

## B. Scope Mapping

B0. PROFIL TOPOLOGI (moneyflow v2.1, WAJIB — dijalankan setelah B13 scope
lock dan sebelum katalog Stream B04). Keluaran `B00-TOPOLOGY.md`. Tiga
hitungan mekanis (AST/grep boleh; hasil diverifikasi parent):

- **Domain eksekusi (`DOM-x`)**: tiap lingkungan yang menjalankan kode
  scope dengan state sendiri — chain/rollup/appchain, atau runtime
  non-EVM (Solana program, Move module). Sumber: `deployments/`, INTEL,
  konfigurasi routing on-chain (dibaca di B7).
- **Varian kode (`VK-x`)**: berkas/kontrak yang meng-override atau
  menurunkan kontrak inti per domain atau per versi (mis. `*_SpokePool`,
  `Tron_*`, V1 & V2 hidup berdampingan).
- **Varian konfigurasi (`VC-x`)**: instance dengan parameter berbeda dari
  kode yang sama (market, vault, pool, strategi) + **kelas aset** yang
  diterima, memakai token baku: `NATIVE`, `WRAPPED_NATIVE`, `ERC20_STD`,
  `FEE_ON_TRANSFER`, `REBASING`, `HOOK_TOKEN` (777/1363/ber-callback),
  `DECIMALS!=18`, `NON_EVM_ASSET`. Ragu bahwa kelas tertentu diterima ->
  catat `MUNGKIN` (bukan dihapus).

Mode ditentukan mekanis:

| Mode | Syarat | Bentuk pemecahan |
| --- | --- | --- |
| `TUNGGAL` | 1 domain DAN (`VK` <= 1 DAN `VC` <= 3) | Lintasan = Stream; dipecah per fase (masuk / akuntansi / keluar) bila melewati anggaran B19 |
| `TUNGGAL-BERINSTANS` | 1 domain DAN (`VK` > 1 ATAU `VC` > 3) | Stream x anggota representatif + Tabel Selisih Varian (B20) untuk anggota lain |
| `MULTI-DOMAIN` | > 1 domain | Stream pengguna x domain representatif + Stream lintas-domain per keluarga transport + Tabel Selisih Varian per keluarga |

Mode boleh dinaikkan (TUNGGAL -> BERINSTANS) atas alasan tercatat; tidak
boleh diturunkan di bawah hasil hitungan. Tidak ada varian -> Tabel
Selisih kosong dan langkah B20 selesai otomatis — rule sama, beban nol.

Untuk `MULTI-DOMAIN`, B00 wajib memuat **Matriks Domain**: per `DOM-x` ->
kontrak inti + alamat, cara autentikasi pesan masuk, transport
keluar/masuk, kelas aset yang dirutekan, status
`LIVE`/`DEAD-CONFIG`/`UNVERIFIED` (dibaca B7 di domain itu sendiri).
Domain representatif dipilih satu per keluarga transport/autentikasi;
sisanya masuk Tabel Selisih.

Aturan mengikat tambahan:
1. Profil + buktinya ditulis di `B00-TOPOLOGY.md` (template
   `templates/B00-TOPOLOGY.md`).
2. `B03-CENSUS-LIVE.md` WAJIB memuat kolom `domain` pada setiap alamat;
   tanpa itu profil belum sah.
3. Profil menentukan bentuk pemecahan, BUKAN isi rule — DILARANG membuat
   rule berbeda per mode.
4. Perubahan profil dicatat di `B00-TOPOLOGY.md` + `B05-LEDGER-SISA.md`
   (alasan + tanggal), lalu pemecahan yang sudah jadi diperiksa ulang.
5. Mode `TUNGGAL` tetap WAJIB mengisi `B00-TOPOLOGY.md` (satu baris bukti
   cukup) — menutup asumsi diam-diam "satu domain".

B1. Sensus = 100% peristiwa pemindah nilai (bukan fungsi saja):
entrypoint + transfer langsung/donasi/force-feed + pergerakan
level-sistem (selfdestruct/coinbase) + multicall/dispatch dinamis
transitif + proxy→implementation + callback/hook + transfer SOL/SPL ke
PDA + langkah off-chain (dilabeli asumsi). Fungsi = unit sensus
(kelengkapan); segmen = unit buruan (partisi).

**Cara pakai (v2.1):** tiap fungsi di tiap berkas scope dapat satu baris
JSON dengan verdict `value_moves` (`yes`/`state_mutator`/`no`/`unknown` —
B14-v2). Peristiwa bukan-fungsi (transfer langsung, donasi, force-feed,
`selfdestruct`, akrual/rebase, callback eksternal) **tidak lagi hanya
"permukaan berkas"**: masing-masing wajib dicatat sebagai baris
**Ingress `IN-x`** (B17) dan menjadi populasi ketiga yang mengikat
ledger.

**B1-v2 (moneyflow v2.1 — populasi INGRESS, MENGIKAT):** nilai yang
MASUK tanpa aksi pengguna WAJIB ikut disensus sebagai kelas tersendiri
(Katalog Ingress `IN-x`, B17), bukan disisipkan sebagai catatan kaki.
Sensus yang hanya memuat entrypoint + transfer yang dipicu pengguna
DINYATAKAN BELUM 100%.

B2. Scope menyeluruh diketahui di awal; pemetaan mendalam +
eksplorasi round per round **per Lintasan di dalam Stream** (B19),
diurutkan menurut B2a / B2a-v2 / B2a-PostAudit. [RIWAYAT: versi 15 Nov
2026 memakai "per klaster, diurutkan EV live" — diganti B2a 17 Nov 2026
dan B2a-v2 18 Nov 2026; kalimat lama tidak berlaku.] Urutan
EV live = default, bukan gerbang. **DIGANTI oleh B2a di bawah** untuk
penentuan urutan (17 Nov 2026); kalimat ini disimpan sebagai riwayat.
Bila EV tidak dipakai (data live
tidak ada — lihat B15 — atau Kim memerintah urutan lain), pakai
urutan lain yang dicatat alasannya (mis. hulu→hilir dari peta alur,
atau pilihan Kim). Cakupan tetap dijamin B9/B10; yang hilang hanya
prioritas uang-dulu.

B2a. URUTAN DEFAULT DIGANTI (diputus 17 Nov 2026, perintah Kim):
urutan kerja = **pintu masuk pertama kali** — entrypoint paling awal
yang dilalui pengguna — bukan EV live. EV live TIDAK dipakai sebagai
penentu urutan klaster, alur, maupun penarikan kartu di Tahap E;
EV boleh tetap dicatat sebagai data, tetapi bukan penentu urutan.
Cara menentukan: susun klaster/alur menurut urutan entrypoint pada
alur pengguna (pintu masuk pertama yang dijumpai → berikutnya →
seterusnya); klaster/alur yang entrypoint-nya lebih awal dikerjakan
lebih dulu. Alasan perubahan dicatat di B04-STREAMS-AND-CLUSTERS.md per proyek.
Konsekuensi: prioritas uang-dulu hilang (sama seperti B2); cakupan
tetap dijamin B9/B10, dan urutan tidak boleh dipakai menunda klaster
mana pun — semua klaster tetap wajib dikerjakan sampai selesai.

B2a-v2. URUTAN KERJA DUA LAPIS + ARSITEKTUR STREAM-FIRST (moneyflow
v2.0 — Lapis Konstitusi, diputus 18 Nov 2026, mengikat):
- Definisi baku: **Klaster** = pengelompokan indeks cakupan di Tahap B
  untuk papan kontrol kelengkapan — bukan pagar pembatas analisis.
  **Stream** = satu aliran nilai ujung-ke-ujung dari titik masuk nilai
  (`Ingress`), pemrosesan/pencatatan hak (`State/Share Accounting`),
  hingga titik keluar atau klaim nilai (`Egress`). Unit rolling
  `C → D → E` adalah **per-Stream**, bukan sapuan horizontal satu
  klaster penuh.
- **Lapis 1 (urutan antar-Stream):** tetap `B2a` — entrypoint pengguna
  paling awal yang belum diproses di `B05-LEDGER-SISA.md` dikerjakan
  lebih dulu.
- **Lapis 2 (urutan penarikan kartu di dalam satu Stream menuju Tahap
  E):** kartu `QUEUED` di dalam Stream aktif diurutkan menurut **bobot
  struktural**, bukan `S1 sebelum S2`: Prioritas 1 = kegagalan
  konservasi pada Simpul Fork/Join atau Komposisi Multi-Langkah
  (`INV-Jx`, `INV-Fx`); Prioritas 2 = ketidakcocokan Kontrak Handoff
  atau State-Bridge (`INV-Hx`, `INV-HBx`); Prioritas 3 = anomali lokal
  di dalam satu Segmen (`INV-Sx`), diurutkan `S1 → Sn`. Aturan
  anti-kuota tetap mutlak: seluruh kartu `QUEUED` pada Stream aktif
  wajib dikuras sampai `QUEUED == 0` dan `ACTIVE == 0` sebelum pindah
  ke Stream berikutnya.
- **Aturan Koridor Stream (`Corridor-Bound Cross-Cluster`)** —
  menggantikan larangan kaku "jangan baca badan fungsi klaster lain /
  jahitan adalah batas mati" di Tahap C dan Tahap D Gelombang 1: saat
  memetakan (C) dan mengeksplorasi (D) satu Stream aktif, bila segmen
  `S(k)` memanggil fungsi atau meneruskan aliran nilai langsung ke
  fungsi di klaster lain dalam satu rangkaian alur yang sama, agen
  WAJIB menembus batas klaster untuk memasukkan fungsi itu sebagai
  `S(k+1)` di dalam Stream aktif, dan langsung menandai EP+VM tersebut
  selesai dipetakan di `B05-LEDGER-SISA.md`. Agen DILARANG melebar
  horizontal ke fungsi lain di klaster seberang yang tidak berada di
  garis aliran nilai Stream aktif.
- **State-Bridge Handoff (`HB-x`):** bila aliran nilai berhenti
  sementara karena jeda transaksi/waktu/aktor lain pada suatu variabel
  storage, catat sebagai `HB-x` di `B07-STATE-BRIDGES.md`. Pada Tahap
  D, agen diizinkan `1-hop peek` (membaca tepat fungsi pembaca/penulis
  pasangannya) agar kecocokan jaminan penulis vs asumsi pembaca
  langsung diuji saat konteks masih panas.
- **B2a-PostAudit — Urutan Eksekusi Stream Dua Tier (revisi 19 Nov
  2026, mengikat; hanya aktif bila metadata audit tersedia):**
  - Di `B01-SCOPE.md` dan `B04-STREAMS-AND-CLUSTERS.md`, bila proyek
    punya riwayat audit sebelumnya dengan commit/cakupan yang diketahui
    (dari `audited_commit`/`audited_files_summary` Tahap A), jalankan
    penandaan mekanis 3 tag faktual per berkas/Stream:
    - `[DELTA]` (Post-Audit Commit Delta): berkas/fungsi pada scope
      aktif yang ditambah atau dimodifikasi pada
      `git diff <latest_audited_commit>..<pinned_commit>`;
    - `[SCAR]` (Patch Scar): fungsi berjejak commit perbaikan
      bug/mitigasi audit (`fix`, `mitigation`, `audit`, atau pengetatan
      guard spesifik) di riwayat git;
    - `[SEAM]` (Cross-Audit Scope Seam): kontrak handoff atau
      `State-Bridge (HB-x)` yang mempertemukan kontrak dari satu
      cakupan audit dengan kontrak yang tidak diaudit atau diaudit
      oleh laporan terpisah.
  - **Bila proyek belum pernah diaudit (atau metadata commit/scope
    audit tidak tersedia):** jalankan urutan `Stream` murni `B2a` dari
    awal hingga akhir — tanpa tier.
  - **Bila ada Stream ber-tag `[DELTA]`, `[SCAR]`, atau `[SEAM]`:**
    - **Tier 1 (Hot Streams First):** angkat seluruh Stream yang
      mengandung `[DELTA]`/`[SCAR]`/`[SEAM]` ke gelombang eksekusi
      pertama (diurutkan di antara sesamanya tetap memakai `B2a`).
    - **Aturan Prasyarat Hulu Cepat (`Prerequisite C-Only Pass`):**
      apabila sebuah Hot Stream Tier 1 membutuhkan state hulu atau
      mengonsumsi jaminan dari Stream hulu yang murni
      `[COLD-AUDITED]`, jalankan lebih dulu **hanya Tahap C
      (`C<NN>-INVENTORY.md`) + pembuatan 1 fungsi transaksi normal di
      `FlowFixtures`** untuk Stream hulu itu (tanpa Tahap D/E pada
      Stream dingin tersebut), sehingga Hot Stream langsung punya
      model domain hulu dan fondasi state fork yang sah.
    - **Tier 2 (Full Coverage Completion):** setelah seluruh Hot
      Stream Tier 1 selesai melewati `C -> D -> E -> G`, lanjutkan
      `D -> E -> G` pada seluruh Stream `[COLD-AUDITED]` tersisa
      hingga `B05-LEDGER-SISA.md` tetap mencapai cakupan mutlak
      100% (`0` sisa). Dilarang menghentikan proyek hanya setelah
      Tier 1 selesai — Tier 1 adalah pengurutan prioritas, bukan
      pemangkasan scope.
- **2 artefak standar baru:** (1) `B07-STATE-BRIDGES.md` — dibuat di
  Tahap B, diperbarui di C/D: tabel pencatat variabel storage yang
  ditulis satu Lintasan dan dibaca Lintasan lain secara asinkron (kolom:
  `Bridge_ID | Storage_Var_&_Contract | Writer_Lintasan_&_Guarantee | Reader_Lintasan_&_Assumption | Window_&_Trigger | Sync_Status`). Kolom
  `Sync_Status` WAJIB memakai enum baku (v2.1, A03): `SEED` ->
  `WRITER_MAPPED` / `READER_MAPPED` -> `SINKRON` (jaminan penulis ==
  asumsi pembaca) | `DESINKRON:<OBS-id>` (tidak cocok — wajib jadi
  kandidat invariant) | `TERBUKA_EKSTERNAL` (konsumen di luar kode
  scope). Kolom `Window_&_Trigger`
  memuat jendela waktu (ISO-8601) + pemicu yang membuat variabel itu
  ditulis/dibaca — menggantikan kolom `Waktu` v2.0. (2)
  `C00-SHARED-PRIMITIVES.md` — dijalankan SEKALI di awal Tahap C
  sebelum Stream pertama: inventaris deskriptif seluruh
  kontrak/library bertipe `SHARED-PRIMITIVE` (jaminan pembulatan,
  skala desimal, invarian 1:1 atau share conversion, peran, event).

B3. Yang TETAP UTUH: sensus (statis + live), daftar scope, inventaris
alamat live, cek penutupan graf akhir, registry invariant (satu penomoran —
diisi mulai Tahap D, lihat B12), aturan/gerbang.

B4. Yang BISA DIPECAH per Stream: inventaris alur + segmentasi,
kontrak handoff, penulisan invariant, uji invariant, komposisi,
verdict. Klasifikasi klaster — 4 tipe generik universal, berlaku
proyek apa pun (moneyflow v2.0; menghapus bias proyek tunggal): tiap
klaster di `B04-STREAMS-AND-CLUSTERS.md` diberi tepat satu tipe — `CORE-FLOW`
(klaster alur nilai utama pengguna/protokol), `SHARED-PRIMITIVE`
(kontrak/library dasar bersama: token internal, math/share library,
brankas akuntansi bersama, modul akses dasar), `EXTERNAL-BOUNDARY`
(integrasi/komponen di luar kode scope), `NON-PROD-SKIP` (mock, test
harness, script migrasi mati — dilewati utuh). Penanganan:
`SHARED-PRIMITIVE` diinventarisasi sekali di `C00-SHARED-PRIMITIVES.md`
dan dirujuk semua konsumen; `NON-PROD-SKIP` dilewati utuh dan dicatat
di ledger; `EXTERNAL-BOUNDARY` dicatat sebagai handoff terbuka
(boundary), bukan dihapus; `CORE-FLOW` menjadi sumber Stream yang
di-rolling C→D→E.

B5. Peta utuh, bukti just-in-time: mapping awal jalur dan relasi harus
menyeluruh (cakupan); kerja yang bisa dikerjakan di fase/klaster
spesifik TIDAK dijalankan di scope besar.

B6-v2. Sensus statis: **baca badan penuh, AST sebagai alat bantu**
(moneyflow v2.1; menggantikan larangan AST 15 Nov 2026).

- **Yang boleh dikerjakan AST/parser** (solc `--ast-compact-json`,
  Slither printer `function-summary` / `entry-points` / `vars-and-auth` /
  `call-graph`, Aderyn, tree-sitter untuk non-Solidity): melokalisasi
  fungsi (file, contract, function, line, end_line, visibility,
  mutability, payable, modifiers), daftar warisan + override (bahan
  B14.6/B14.7 & B0 `VK-x`), daftar panggilan eksternal + delegatecall +
  transfer native (bahan B18 `CY-x`), daftar storage yang ditulis/dibaca
  per fungsi (bahan B19 pemicu batas & B21 LP-x), deteksi
  `receive`/`fallback`/`selfdestruct`/`balanceOf(address(this))` (bahan
  B17 `IN-x`).
- **Yang TIDAK boleh diisi AST:** verdict `value_moves` (4 nilai B14-v2),
  tag `PRIVILEGED_ONLY:`/`COSMETIC_NON_ECONOMIC:`, kelas Ingress B17, dan
  seluruh kolom deskriptif Tahap C (jaminan produsen / asumsi konsumen).
  Semua itu diisi **setelah badan fungsi dibaca penuh**. Output AST =
  daftar periksa + saran, bukan keputusan.
- **Rekonsiliasi wajib:** jumlah fungsi dari AST vs jumlah baris sensus
  per berkas; selisih != 0 wajib dijelaskan per baris (mis. deklarasi
  interface, fungsi warisan B14.6). Selisih yang tidak dijelaskan = sensus
  belum lulus.
- Kontrol positif 9/9; untuk `MULTI-DOMAIN`/`TUNGGAL-BERINSTANS` minimal
  **2 dari 9** berasal dari berkas varian (`VK-x`) — membuktikan sensus
  tidak buta varian. Nol mekanis wajib dipecahkan, dan verifikasi parent
  tetap jalan (lantai bawah). B9 (usaha yang cukup) tetap TIDAK berlaku
  untuk kedalaman sensus statis.
- Verdict `value_moves` = **4 nilai** `yes | state_mutator | no | unknown`
  (B14-v2). Penyebutan "yes/no/unknown" di dokumen mana pun = riwayat v1.

**B6-v2 — AST DIIZINKAN (moneyflow v2.1, diputus 20 Nov 2026;
menggantikan larangan 15 Nov 2026 untuk keperluan LOKALISASI):** AST
boleh dipakai untuk (a) melokalisasi definisi fungsi/selector, (b)
membangun call-graph untuk transitif dispatcher/proxy, (c) mendeteksi
kandidat `CY-x` (B18), (d) enumerasi independen pada sapuan akhir B9.
Lantai bawah TIDAK berubah: **verdict `value_moves` tetap diisi setelah
badan fungsi dibaca utuh** oleh manusia/agen — AST tidak boleh
memberi verdict, tidak boleh menggantikan baca badan, dan hitungan AST
bukan bukti kelengkapan sensus. AST yang dipakai wajib dicatat
(tool+versi+perintah) di `B02-CENSUS-STATIC.md`.

B7. Cek rantai utama proyek, singkat dan ringan (diputus Kim 15 Nov
2026 — menggantikan 'cek ETH L1'): cek SATU rantai utama proyek
(rantai tempat kontrak inti ter-deploy, menurut INTEL + deployments/;
bila INTEL tidak menyebut eksplisit: rantai dengan alamat deployment
inti terbanyak). Bila rantai utama tidak bisa dicek (RPC tidak
terjangkau / tidak ada kode di alamat inti / tidak ada blok
referensi), cek rantai utama KEDUA (deployment inti terbanyak
berikutnya). Bila satu rantai tidak merespons (timeout/403/429),
jangan tunggu — langsung pindah ke rantai kedua. Bila keduanya
gagal: B7 selesai dengan catatan (apa yang dicoba + hasil),
verifikasi pindah ke B8. Tes ringan = (1) getCode alamat kontrak
inti (1–3 alamat) pada blok referensi; (2) bila ada kode, satu
panggilan view murah (mis. liveness()/owner()). TIDAK termasuk:
jejak event, hitung log, verifikasi seluruh inventaris alamat, cek
rantai lain — itu kerja B8 per klaster. Anggaran maks 5 menit untuk
seluruh B7 (target, belum terukur); bila habis, berhenti dengan
hasil yang ada + catatan. Status B7 (moneyflow v2.0, selaras B15):
B7 **WAJIB** untuk proyek MAINNET/TESTNET — ringan (≤5 menit: getCode
1–3 alamat inti + 1 view murah + penetapan blok pin referensi). Untuk
`MULTI-DOMAIN`: anggaran ≤5 menit **per keluarga domain** (bukan per
domain), dengan satu domain representatif per keluarga; domain
non-representatif berstatus `UNVERIFIED` sampai B8 Lintasan yang
menyentuhnya. Satu blok pin per domain representatif.
Dilewati HANYA bila proyek murni belum di-deploy (`repo-only`); bila
dilewati sah, sensus live di Tahap B tinggal inventaris alamat
klaim-repo (statis) + catatan verifikasi ditunda ke B8; kerja statis
tetap valid sebagai peta kode (menunggu di TUNDA-LIVE).

B8. B8 Live-Match Lintasan — dijalankan di awal Tahap D, wajib lulus sebelum Gate D, per domain eksekusi segmen (B21); sebelum PoC
ditulis. Yang tidak live-match masuk wadah TUNDA-LIVE: tercatat di
ledger sisa (tetap terhitung, bukan hilang); nol waktu eksekusi
(tanpa PoC, tanpa fork); dibuka lagi hanya bila deployment live muncul
atau Kim memerintah cek ulang; wadah ditinjau ulang di sapuan akhir.

Utamakan alur, log untuk verifikator terakhir (diputus 17 Nov 2026 08:26 WIB, perintah Kim, MENGIKAT untuk semua B8 berikut): tahu suatu mekanisme work atau tidak dari tes tool (baca kode + cast/cek live + uji fork di Tahap E), BUKAN dari mengandalkan log tx orang lain di blockchain. Pindai log itu pilihan terakhir yang mahal — hanya untuk verifikator akhir (Tahap G / sapuan akhir), bukan cara kerja B8. Pemicu: B8 P4 memakan ~8,5 jam memindai RelayedRootBundle per rantai (BSC gagal total lewat log, Base gagal per chunk ~20 menit/chunk); koordinator dialihkan 08:26 WIB — hentikan semua pindai log, selesaikan B8 dari alur + 5 rantai yang sudah terukur (ETH 63, OP 63, Polygon 63, Linea 58, BSC 63; slowRelayRoot non-zero 0 di semua).

Cek desain kode dulu (diputus 17 Nov 2026 ~08:33 WIB, perintah Kim, MENGIKAT): untuk tahu suatu nilai 0 atau bukan, cek dari desain kode apakah DISET 0 oleh kode atau MEMANG BISA MEMUAT — jangan simpulkan dari log. Contoh P4: slowRelayRoot = parameter input proposer di `proposeRootBundle` HubPool.sol:565, disimpan verbatim :579, diteruskan verbatim :685, TIDAK ada require/validasi atasnya — jadi BISA MEMUAT non-zero by design; live 0 berasal dari proposer/off-chain (0 RequestedSlowFill), bukan dari batasan kode.

B9. Scope mapping cukup usaha yang cukup — miss bisa terdeteksi di
eksplorasi lewat: (1) baca ulang mendalam per klaster; (2) cek handoff
+ konservasi (delta tak terjawab diselidiki); (3) jejak event live
sebagai enumerasi independen; (4) cek penutupan graf. Penopang wajib:
sapuan akhir dengan enumerasi independen kedua dibanding ledger
akhir. Cara yang diterima (moneyflow v2.1): **enumerasi AST independen**
(alat berbeda dari yang dipakai melokalisasi sensus bila memungkinkan,
mis. sensus pakai solc AST -> sapuan pakai Slither `entry-points`)
dibandingkan per nama `(file, contract, function)` dengan ledger akhir;
rerun sensus manual tetap sah sebagai alternatif. Regex yang sama dengan
sensus tetap tidak sah. Sapuan juga membandingkan katalog `IN-x` (B17)
dan `CY-x` (B18) terhadap daftar panggilan eksternal / `receive` /
`balanceOf(this)` dari AST. Sensus di
depan adalah rencana + daftar periksa, bukan bukti kelengkapan;
buktinya datang dari eksplorasi + sapuan akhir. Diputus 22:33 WIB 16 Nov 2026: rerun sensus manual DITERIMA sebagai enumerasi independen kedua (pilot: rerun menemukan 15 baris yang sensus pertama lewatkan). Cara parser independen tetap terbuka sebagai riset, bukan rule.

B10. Ledger "sisa" sesudah tiap round (entrypoint belum masuk alur,
handoff terbuka, klaster belum dikerjakan; **v2.1: ledger mengikat TIGA
populasi** — `EP+VM(yes)` berstatus `BELUM_MASUK_STREAM`,
`EP+SM(state_mutator)` berstatus `BELUM_TERCAKUP`, dan **`IN-x`
(Ingress B17) berstatus `BELUM_TERIKAT`**; ketiganya wajib habis di
`CORE-FLOW` sebelum penutupan). Round selesai hanya bila
sisa menyusut. Target buruan harus ada di sensus — kalau tidak, di
luar scope menurut konstruksi.
**B10-v2 (moneyflow v2.1):** penyusutan ledger dihitung dengan
**rekonsiliasi by-name** — setiap baris ledger ditandai nama unit
penutupnya (`STR-xx`/`LINT-xx`/unit `IN-x`), lalu hitung ulang dari
daftar nama; DILARANG menghitung sisa dengan pengurangan aritmetika
(`total − selesai`) karena baris ganda/typo tidak terdeteksi.
Kolom `waktu` (ISO-8601) wajib ada pada setiap baris ledger.

**Rekonsiliasi berbasis nama (v2.1):** sisa ledger dihitung ulang dari
daftar nama `(file, contract, function)` / `IN-x` yang belum berstatus
`TERPETAKAN_DI_<STR>.<Lk>` / `TERIKAT_DI_<STR>.<Lk>`, **bukan** dari pengurangan angka berjalan.
Setiap baris status `TERPETAKAN_DI_` wajib menyebut nama, bukan hanya
jumlah. (Pemicu: across_hermes C10 menemukan trail angka 45/20 vs
enumerasi nama 49/36.)

B11. Inventaris handoff dienumerasi dari batas unit (rantai linear N
unit → N−1 handoff), bukan dilabeli tangan. Simpul fork/join jadi unit
sendiri.

Batas unit (segmen) ditentukan oleh **5 pemicu batas B19**, bukan pilihan
bebas agen. Titik serah kendali di tengah segmen yang tidak memicu batas
tetap dicatat sebagai `CY-x` (B18).

B12. Invariant TIDAK dinyatakan di Tahap B atau Tahap C (direvisi
15 Nov 2026 atas perintah Kim — menggantikan 'invariant DINYATAKAN
dulu'; pemetaan mendalam pindah ke Tahap C, 15 Nov 2026, perintah Kim
'nomor baru saja'): Tahap B hanya membangun yang riil/teramati untuk
seluruh protokol — sensus, profil topologi (B0), klaster, katalog
Ingress (B17), daftar handoff kasar (B11). (B16 tidak dipakai.) Tahap C
membangun yang riil/teramati per Lintasan (B19) — inventaris alur,
segmentasi, kontrak handoff deskriptif (jaminan produsen + asumsi
konsumen sebagaimana teramati di kode: nama+tipe+satuan field).
Invariant adalah klaim asumsi agen tentang apa yang SEHARUSNYA
berlaku — bukan fakta teramati — jadi dirumuskan di Tahap D
(eksplorasi), bersama kartu leadnya, dan diuji di Tahap E. Setiap
invariant di Tahap D WAJIB mencantumkan sumbernya: field kontrak
handoff yang bersangkutan, atau baris docs/NatSpec — bukan perasaan
agen. Tiga lapis tetap: L1 dalam segmen (INV-Sx), L2 handoff + simpul
(INV-Hx, INV-Jx), L3 ujung-ke-ujung/komposisi (INV-Fx). Tiap invariant
wajib akibat finansial bila pecah. Cek testability dicatat saat
perumusan (fork apa, data live apa; dilabeli bila tidak bisa diuji).
Registry invariant tetap satu penomoran global (B3), diisi mulai Tahap D.
Prefiks yang disiapkan (v2.1): `INV-S` (segmen), `INV-H` (handoff),
`INV-HB` (state-bridge), `INV-J` (join), `INV-F` (komposisi),
`INV-CY` (serah kendali `CY-x`), `INV-V` (selisih varian `BEDA`),
`INV-IN` (Ingress `IN-x`).

B13. Scope lock sebelum sensus jalan: daftar berkas scope harus cocok
persis dengan inventaris kanonik (diff kosong), commit terverifikasi,
contracts/ bersih.

B14. Konvensi sensus statis (15 Nov 2026, diputus asisten atas
delegasi Kim — berlaku universal, bukan cuma Across; **DIREVISI
B14-v2 Strict Census 19 Nov 2026 perintah Kim: value_moves = 4 nilai
sah `yes | state_mutator | no | unknown`; larangan membuang fungsi
pengubah state berdampak finansial sebagai `no`**):
- Getter publik = entrypoint (ya). Entrypoint = bisa dipanggil dari
  luar (literal, mekanis); filter nilai lewat value_moves; yang
  mengikat alur tetap **EP+VM(yes) DAN EP+SM(state_mutator)**.
- **Definisi ketat value_moves (B14-v2):**
  - `yes`: fungsi memindahkan aset/token/native secara langsung ATAU
    mengubah saldo/share/klaim finansial langsung.
  - `state_mutator`: fungsi `entrypoint: true` yang TIDAK memindahkan
    aset secara langsung dan BUKAN khusus admin terverifikasi, TETAPI
    menulis ke storage — termasuk `initialize`/setup, perubahan
    allowance/operator/recipient/delegasi, pembaruan
    indeks/snapshot/timestamp/twap/sync/poke, perubahan siklus hidup
    posisi (merge/split/lock), pembuatan pool/rute publik,
    pembatalan/penguncian antrean.
  - `unknown`: dispatcher target/calldata arbitrer, proxy fallback
    dinamis, atau penerusan eksternal yang belum pasti; diselesaikan
    transitif di inventaris alur (ikuti ke implementasi/target).
  - `no`: HANYA untuk (i) fungsi `view`/`pure`/getter publik yang
    sama sekali tidak menulis storage; (ii) `receive` berbadan
    kosong pada kontrak yang tidak memakai `address(this).balance`
    dalam rumus akuntansinya; (iii) fungsi konfigurasi yang TERBUKTI
    di kode dikunci rapat modifier peran istimewa murni (`onlyOwner`,
    `onlyAdmin`, `onlyGovernance`, `onlyTimelock`) TANPA jalur
    pemicu publik — WAJIB mengisi `notes` dengan format
    `PRIVILEGED_ONLY: <nama_modifier_atau_guard>`.
  (iv) fungsi yang HANYA menulis storage non-ekonomi — WAJIB `notes` =
    `COSMETIC_NON_ECONOMIC: <storage yang ditulis> | pembaca: <hasil
    grep/AST pembaca>`. Sah hanya bila storage itu **tidak dibaca** oleh
    fungsi mana pun yang memindahkan nilai, menghitung
    saldo/share/rate/fee/batas, memeriksa izin/peran, atau menentukan
    alamat tujuan. Ragu -> `state_mutator`. (Selaras dengan
    `flow-b-map` + `check-b`; sebelumnya hanya ada di skill.)
    Fungsi `initialize` TIDAK BOLEH diberi `PRIVILEGED_ONLY` kecuali
    sudah dikunci konstruktor/`disableInitializers` dan terverifikasi
    pada objek live di B8.
- Receive badan kosong = value_moves no. Menerima saja bukan
  memindahkan; value_moves dinilai dari badan — ada perpindahan
  lanjutan (transfer keluar / perubahan saldo pihak lain) → yes;
  hanya menerima → no; tidak bisa dipastikan → unknown. Pengecualian
  B14-v2: bila kontrak memakai `address(this).balance` dalam rumus
  akuntansinya, `receive` kosong tetap tercatat no tetapi catat di
  `notes` bahwa donasi ETH mengubah basis akuntansi.
- Fungsi payable yang memanggil sistem eksternal yang diketahui
  (mis. relayMessage adapter → messenger bridge) = value_moves yes;
  tahap alur WAJIB verifikasi penerusan value per adapter dari badan
  — bila tidak meneruskan, turunkan ke `state_mutator` bila fungsi
  itu masih menulis storage, atau `no` bila murni view.
- Dispatcher dengan target/calldata arbitrer (Multicall3 aggregate*,
  deployAndExecute, directWithdraw dan sejenisnya) = value_moves unknown;
  diselesaikan transitif di inventaris alur (ikuti ke
  implementasi/target).
- Getter auto-generated DIBARISKAN (konsisten dengan butir pertama):
  semua getter publik dibariskan (entrypoint yes; value_moves `no`
  bila view murni tanpa efek samping, `state_mutator` bila menulis
  storage — getter non-view seperti `sync`/`poke`/`exchangeRate`
  yang menyemar state = state_mutator).
- Entrypoint warisan TIDAK dibariskan (satu baris per definisi, di
  berkas pendefinisi). Tahap alur WAJIB punya langkah perluasan
  permukaan lewat implementasi/warisan sebelum segmentasi.
- Atribut berkas direct/proxy dicatat dua lapis: permukaan
  milik-sendiri + permukaan warisan. Inventaris alur memakai lapis
  warisan untuk permukaan deployed, lapis milik-sendiri untuk lokasi
  kode.
- **Konvensi 8 (v2.1) — modifier peran non-standar:** `onlyHubPool`,
  `onlyRole(X)`, `onlySelf`, `onlyFromCrossDomainAdmin`, dan guard
  setara **bukan** `PRIVILEGED_ONLY` otomatis. Sah `PRIVILEGED_ONLY`
  hanya bila pemegang peran dibuktikan aktor istimewa
  (owner/admin/governance/timelock) dari kode + B7. Bila pemegang peran
  adalah kontrak lain yang bisa dipicu publik (mis. HubPool yang
  dieksekusi permissionless) -> `state_mutator` atau `yes`, dan masuk
  koridor Lintasan pemicunya.
- **Ikatan cakupan ledger (B14-v2):** sensus mengikat dua populasi —
  `EP+VM(yes)` dan `EP+SM(state_mutator)`. Semua `EP+VM(yes)` wajib
  masuk koridor `Stream` (`STR-xx`). Semua `EP+SM(state_mutator)`
  wajib masuk koridor Stream terkait ATAU terdaftar sebagai penulis
  di `B07-STATE-BRIDGES.md` dan diaudit berpasangan saat Stream
  pembaca storage-nya masuk Tahap C/D. `EP+SM` yang berdiri sendiri
  (mis. `initialize` publik) wajib dibuatkan unit pemeriksaan
  sendiri sampai sisa `BELUM_TERCAKUP` di `B05-LEDGER-SISA.md`
  tepat 0.

B15. Cek onchain: sensus live ringan B7 WAJIB di Tahap B; cek
onchain mendalam WAJIB di B8 (15 Nov 2026, direvisi atas perintah Kim
'perlu sensus live ringan' — menggantikan revisi 15:11 yang membuat B7
opsional): Tahap A TIDAK cek onchain (A2 — brief klaim saja). Tahap B
wajib B7 ringan — getCode 1–3 alamat inti di blok referensi + satu view
murah, rantai utama (fallback rantai utama kedua), anggaran 5 menit —
sebagai konfirmasi live bahwa klaim INTEL/deployment benar, sumber data
EV, dan sinyal live untuk identifikasi klaster. Sensus live PENUH
(semua rantai, jejak event lengkap) tetap OPSIONAL di Tahap B; cek
onchain mendalam WAJIB di B8: live-match per klaster sebelum PoC
ditulis; yang tidak live-match masuk TUNDA-LIVE; PoC klaster itu
TERBLOKIR sampai cek live-match ada. Pengecualian: proyek
TESTNET/DEVNET — "live" = lingkungan itu sendiri (A3).

B16. TIDAK DIPAKAI (diputus Kim 22:33 WIB 16 Nov 2026 — 'B16 tidak perlu'). Mekanisme di bawah ini TIDAK menjadi rule; dibiarkan sebagai arsip usulan [ARSIP RIWAYAT PILOT]: jahitan (handoff antar-klaster) dienumerasi UTUH di depan
(Tahap B mapping), dari graf alur — bukan ditemukan belakangan per
klaster. (1) Sensus mencatat, untuk tiap fungsi EP+VM, tepi
keluarnya: fungsi/kontrak apa yang dipanggil, token apa yang
dipindah, event apa yang diemisikan. (2) Klaster diidentifikasi DARI
graf itu, bukan dilabeli tangan dari nama kontrak: satu klaster =
satu tahap pipa alur; draf klaster dari nama kontrak hanya hipotesis
awal yang dikoreksi graf. (3) Daftar jahitan = semua tepi
antar-klaster, masing-masing dengan ID (SM-xx), klaster produsen,
klaster konsumen, bukti (baris sensus + baris kode), dan status.
Status di ledger sisa: dienumerasi → produsen terverifikasi →
konsumen terverifikasi → TERTUTUP; jahitan tertutup hanya bila kedua
sisi terverifikasi. Jejak event live (B7/B8) menambah jahitan
berbasis event (aktor off-chain yang menyambung klaster) dan
mengonfirmasi tepi statis mana yang benar-benar menyala live; tepi
statis yang tidak pernah live dicatat statis-saja, bukan dihapus.
Lead/PoC yang jalurnya melewati jahitan terbuka WAJIB melabeli
jahitan itu sebagai asumsi terbuka. Urutan klaster default =
hulu→hilir (topologis): klaster berjalan sesudah produsennya,
supaya jahitan masuknya sudah terverifikasi sisi produsen saat
klaster itu jalan; EV live memecah seri di antara klaster yang
sejajar. (Bila diputus, ini menggantikan default EV di B2: EV jadi
pemecah seri, bukan urutan utama.) Primitif bersama
(kontrak/library/token yang dipakai banyak klaster) = klaster
bersama sendiri, diinventarisasi sekali dan dirujuk semua konsumen;
bila belum diinventarisasi, konsumen mencatat jahitannya terbuka
dan mengutip interface primitif dari sensus sebagai asumsi. Cek
penutupan akhir (B9) memverifikasi semua jahitan TERTUTUP. Biaya:
sensus sedikit lebih dalam untuk fungsi EP+VM (waktu sensus perlu
diukur ulang — angka 13m36s rerun tidak memuat field 'keluar').

B17. Katalog Ingress (`IN-x`) — nilai masuk tanpa aksi pengguna langsung
(moneyflow v2.1, MENGIKAT). Tiap cara nilai/klaim bisa bertambah di
sebuah `Value_Holder` dicatat satu baris `IN-x` di `B04` Bagian 2b,
dengan **kelas**:

| Kelas | Contoh | Sumber deteksi |
| --- | --- | --- |
| `USER` | deposit, swap, mint via entrypoint | EP+VM |
| `ACTOR` | keeper/relayer/liquidator/harvester/bot publik memicu perpindahan | EP+VM/EP+SM dengan pemicu non-pengguna |
| `CALLBACK` | messenger bridge, `lzCompose`, `onERC721Received`, flash-loan callback, oracle push, `handleV3AcrossMessage` | entrypoint yang dipanggil kontrak eksternal |
| `PASSIVE` | transfer langsung ERC-20, donasi, `selfdestruct`/force-feed ETH, `receive` kosong, airdrop pihak ketiga | `balanceOf(address(this))` / `address(this).balance` dibaca di jalur nilai |
| `ACCRUAL` | yield/rebase token, bunga berbasis waktu, akrual fee per detik | rumus yang membaca `block.timestamp` atau saldo token rebasing |
| `ADMIN` | top-up/rescue/haircut oleh peran istimewa | fungsi `PRIVILEGED_ONLY` yang mengubah saldo |

Kolom wajib: `IN_ID | Kelas | Value_Holder | Pintu (fungsi:baris atau
"transfer langsung") | Pembaca akuntansi (fungsi:baris yang membaca
saldo/state yang naik) | Lintasan pengikat | Status`.
Aturan ikat: tiap `IN-x` wajib terikat ke **Lintasan yang membaca
efeknya** (bukan Lintasan penulisnya) — untuk `PASSIVE`/`ACCRUAL`
pengikatnya adalah Lintasan yang rumusnya membaca saldo/waktu itu.
`IN-x` kelas `ADMIN` boleh diikat ke Lintasan admin dan diprioritaskan
terakhir. Status: `BELUM_TERIKAT` -> `TERIKAT_DI_<LINTASAN>`.
`check-final` menolak sisa `BELUM_TERIKAT` pada `CORE-FLOW`.
**Wajib minimal satu baris `PASSIVE` per `Value_Holder`** yang membaca
saldonya sendiri dalam akuntansi; bila tidak ada pembaca saldo sendiri,
tulis `PASSIVE: TIDAK_BERDAMPAK` + bukti AST (tidak ada pembacaan
`balanceOf(this)` / `address(this).balance`).
Konsekuensi Tahap C: Ingress `PASSIVE`/`ACCRUAL` muncul sebagai **segmen
masuk tidak resmi** `S0` di inventaris Lintasan pembacanya (deskriptif:
siapa bisa memicu, berapa batasnya, bagaimana akuntansi menyerapnya).

B18. Titik Serah Kendali (`CY-x`) (moneyflow v2.1, MENGIKAT).
Tiap titik di dalam segmen tempat eksekusi berpindah ke kode yang tidak
dikendalikan fungsi itu dicatat satu baris `CY-x`: `call`/`delegatecall`/
`staticcall` eksternal, transfer native (`call{value}`, `transfer`,
`send`, `sendValue`), transfer token yang bisa memanggil hook
(`safeTransfer*` ERC-721/1155, ERC-777, ERC-1363, token ber-hook),
panggilan ke `EXTERNAL-BOUNDARY`/oracle/router, callback ke `msg.sender`,
`try/catch`.
Kolom wajib (deskriptif, tanpa penilaian): `CY_ID | Segmen | Jangkar |
Jenis | Penerima kendali (siapa yang bisa mengatur kodenya: CALLER-INPUT
/ ADMIN-CONFIG / IMMUTABLE / EXTERNAL) | Storage ditulis SEBELUM |
Storage ditulis SESUDAH | Storage dibaca SESUDAH | Guard aktif
(nonReentrant/lock/none) | Efek bila revert (propagasi / ditelan /
defer)`.
`CY-x` **tidak** otomatis memecah segmen (lihat B19 pemicu c). AST wajib
dipakai untuk enumerasi kandidat `CY-x` (daftar panggilan eksternal per
fungsi koridor); agen wajib mengonfirmasi tiap kandidat dari badan.

B19. Batas Segmen & Anggaran Unit (moneyflow v2.1, MENGIKAT).
Hierarki unit: **Stream** (siklus hidup nilai, indeks cakupan) >
**Lintasan** (unit kerja C->D->E satu sesi) > **Segmen** (unit buruan) >
fungsi (unit sensus).
Segmen baru dimulai HANYA pada salah satu **5 pemicu batas**:
(a) perpindahan aset/token/native keluar atau masuk `Value_Holder`;
(b) penulisan variabel akuntansi (saldo, share, supply, reserve, debt,
index, rate, klaim) yang terdaftar di C00/LP-x;
(c) serah kendali ke **domain kepercayaan berbeda** (kontrak eksternal,
`EXTERNAL-BOUNDARY`, delegatecall ke kode yang dipilih admin/caller) —
serah kendali ke kode in-scope dengan kepercayaan sama cukup `CY-x`;
(d) batas transaksi/aktor/waktu -> State-Bridge `HB-x` (segmen berhenti);
(e) perpindahan domain eksekusi (chain/runtime) -> handoff lintas-domain.
Bukan pemicu: helper internal `pure`/`view`, panggilan primitif yang sudah
di C00 (dirujuk, tidak diulang), modifier, event.
**Anggaran** (pedoman kewajaran, dicek `check-c` secara lunak):

| Unit | Batas bawah | Batas atas (wajar) | Bila jauh melewati |
| --- | --- | --- | --- |
| Segmen | >= 1 pemicu batas | sekitar 1-4 fungsi dibaca langsung | pecah di pemicu berikutnya |
| Lintasan | >= 1 perpindahan nilai + >= 1 batas kepercayaan | sekitar 4-8 segmen, sekitar <= 12 fungsi dibaca langsung (rujukan C00 tidak dihitung), 1 keluarga varian | pecah per fase (masuk/akuntansi/keluar) atau per sisi domain (kirim/terima) |
| Stream | >= 1 Lintasan | sekitar <= 6 Lintasan | pecah menjadi Stream baru dalam satu `Flow Family` |

Angka di tabel adalah **rentang wajar, bukan ambang kaku**: sedikit di
atas/di bawah masih sah selama ada alasan tercatat di inventaris
(mis. fungsi koridor panjang tak terpisahkan, atau varian yang menuntut
satu Lintasan utuh). Yang DILARANG adalah menggabungkan banyak pemicu
batas dalam satu segmen tanpa alasan, atau memecah sampai satu Lintasan
kehilangan alur nilai utuh.
Lintasan di bawah batas bawah digabung ke Lintasan tetangga dalam Stream
yang sama. **Satu sesi kerja / satu delegasi = satu Lintasan** (C12
Capsule berlaku per Lintasan).
Penamaan: `STR-nn` (Stream), `STR-nn.Lk` (Lintasan), `STR-nn.Lk.Sj`
(segmen). Berkas: `C<NN>-<STR>-<Lk>-INVENTORY.md`, `D<NN>-<STR>-<Lk>-*`,
`E<NN>-<STR>-<Lk>-BATCH<M>-PROOF`.

B20. Tabel Selisih Varian (moneyflow v2.1, MENGIKAT).
Untuk tiap Lintasan yang menyentuh `VK-x`/`VC-x`/`DOM-x` dengan > 1
anggota: satu anggota **representatif** dibedah penuh; anggota lain
dicatat di Tabel Selisih — satu baris per anggota, kolom: `Anggota |
Fungsi override (jangkar) | Autentikasi | Jalur native/wrapped |
Transport/route | Kelas aset diterima | Parameter live beda (LP-x) |
Status (SAMA / BEDA:<kolom>)`.
Representatif dipilih per keluarga (sama transport + sama autentikasi).
Baris `BEDA` yang menyentuh nilai atau autentikasi = **wajib** jadi kartu
di Tahap D (Twin-Path Differential otomatis). Ini menggantikan praktik
"varian dibaca pada titik override saja".

B21. Lokasi & status Parameter Live (moneyflow v2.1, MENGIKAT).
Tiap `LP-x` dibaca **di domain tempat segmen pembacanya dieksekusi**
(kolom baru `Domain`), pada blok pin domain itu (B00 mencatat blok pin
per domain). Getter yang revert -> baca slot storage (`cast storage`)
dari layout AST. Bila tetap tidak terbaca -> status **`UNVERIFIED`**
(bukan `LIVE`). Lintasan dengan `LP-x` pengendali nilai berstatus
`UNVERIFIED` tidak lolos Gate D. `TIDAK-TERBACA` sebagai status dicabut.

B22. Larangan Stream sapu sisa (moneyflow v2.1, MENGIKAT).
Dilarang membentuk Stream penampung yang isinya ditentukan oleh "sisa
ledger" (contoh terlarang: "KURAS FINAL"). Sisa ledger setelah katalog
awal habis wajib dikelompokkan ulang menurut **Ingress -> Egress** dan
**keluarga varian** menjadi Stream/Lintasan baru. Label Stream wajib
sesuai isinya: Stream berlabel admin tidak boleh berisi EP+VM
permissionless (dicek `check-c`).


## Tahap B — yang wajib selesai (15 Nov 2026, perintah Kim)
Uji pemisahnya: Tahap B wajib menyelesaikan semua yang dipakai tahap
berikut sebagai INPUT dan tidak bisa direkonstruksi tahap berikut
tanpa baca ulang seluruh protokol. Yang tidak memenuhi uji itu bukan
pekerjaan Tahap B.
Wajib selesai di Tahap B:
0. Profil Topologi B0 (`B00-TOPOLOGY.md`) — mode + Matriks Domain (bila
   MULTI-DOMAIN) + daftar `VK-x`/`VC-x`.
1. Daftar scope + scope lock (B13) — gerbang masuk sensus.
2. Sensus statis 100% peristiwa pemindah nilai (B1/B6) — fondasi cakupan. (Field 'keluar' tiap fungsi EP+VM TIDAK wajib — B16 tidak dipakai, diputus 22:33 WIB 16 Nov 2026.)
3. Inventaris alamat live — daftarnya saja (B3); verifikasi onchain
daftar itu = B7/B8.
4. Sensus live ringan B7 (B15) — konfirmasi live klaim INTEL, sumber
EV, sinyal live identifikasi klaster.
5. Identifikasi klaster + daftar handoff (B11) — partisi kerja +
klasifikasi 4 tipe per klaster (B4: CORE-FLOW / SHARED-PRIMITIVE /
EXTERNAL-BOUNDARY / NON-PROD-SKIP). (Daftar jahitan SM-xx lengkap
TIDAK wajib — B16 tidak dipakai, diputus 22:33 WIB 16 Nov 2026.)
6. Ledger sisa — seed (B10): semua entrypoint, klaster, jahitan,
handoff terbuka; diperbarui sesudah tiap round.
   - Katalog Ingress `IN-x` (B17) — seed di `B04` Bagian 2b; populasi
     ketiga di ledger.
7. Struktur registry invariant (B3) — penomoran + registry kosong;
diisi mulai Tahap D.
8. B07-STATE-BRIDGES — seed (moneyflow v2.0): tabel variabel storage
yang ditulis satu Lintasan dan dibaca Lintasan lain secara asinkron
(`Bridge_ID | Storage_Var_&_Contract | Writer_Lintasan_&_Guarantee | Reader_Lintasan_&_Assumption | Window_&_Trigger | Sync_Status`); diperbarui di C/D.
Bukan pekerjaan Tahap B (dikerjakan di tahap berikut): pemetaan
mendalam per klaster (Tahap C: inventaris alur + segmentasi + kontrak
handoff deskriptif), invariant (Tahap D), buruan (Tahap D), PoC + P&L
(Tahap E), komposisi (Tahap F), verdict (Tahap G), live-match mendalam
per klaster (B8, di giliran klaster), sensus live penuh (opsional), cek
penutupan graf akhir (B9 — dieksekusi di akhir audit; yang wajib ada di
Tahap B adalah bahannya: ledger sisa + daftar jahitan + sensus).

## Tahap B — yang TIDAK dilakukan (15 Nov 2026, perintah Kim: waktu
Tahap B harus efektif-efisien, jangan buang waktu ke yang seharusnya
dikerjakan spesifik di tahap berikut)
Uji pemisahnya: Tahap B hanya mengerjakan yang butuh pandangan
seluruh protokol; semua yang butuh konteks satu klaster saja
dikerjakan di giliran klaster itu (Tahap C/D/E).
Jangan dilakukan di Tahap B:
1. Inventaris mendalam semua klaster sekaligus (inventaris alur +
segmentasi + kontrak handoff penuh untuk semua klaster di depan) —
itu Tahap C per klaster, just-in-time. Alasan: 2–4 jam sebelum eksplorasi
apa pun; batas bisa bergeser sesudah klaster tetangga dibaca.
(v2.1: berlaku juga untuk Tabel Selisih — diisi per Lintasan di Tahap C,
bukan di B.)
2. Menulis invariant — itu Tahap D (B12). Alasan: asumsi yang ditulis
sebelum eksplorasi akan basi dan ditulis ulang.
3. Buruan (mencari celah) saat memetakan — itu Tahap D. Alasan:
memperlambat pemetaan; lead tanpa sumber (handoff belum ada); bias
peta ke yang 'menarik'.
4. Menguji/mengeksekusi saat memetakan, termasuk memverifikasi
kontrak handoff dengan eksekusi — itu Tahap E. Kontrak handoff di
Tahap B bersifat deskriptif (apa kata kode).
5. Sensus live penuh (semua rantai, jejak event lengkap, verifikasi
semua alamat) — itu B8 per klaster. Di Tahap B cukup B7 ringan
(≤5 menit). Alasan: sebagian besar hanya dibutuhkan saat giliran
klasternya; state live berubah; biaya transport besar (pilot: 53/101
pemeriksaan gagal transport).
6. Baca mendalam semua fungsi saat sensus — sensus mengklasifikasi
(value_moves/entrypoint), bukan memahami logika tiap fungsi. Baca
mendalam hanya untuk fungsi EP+VM (tepi keluar, B16) + inventaris
per klaster (Tahap C).
7. Menyelesaikan semua 'unknown' saat sensus — unknown dicatat
sebagai unknown, diselesaikan di Tahap C klaster yang bersangkutan saat
konteks alurnya ada. Alasan: sebagian besar unknown (deklarasi
interface, dispatcher arbitrer) baru bisa diputus dengan konteks alur.
8. Menilai/menghakimi klaster saat memetakan ('klaster ini
kelihatannya bersih/berbahaya') — itu Tahap G (verdict). Peta harus
netral; penilaian dini membiasakan eksplorasi.
9. Rerun sensus penuh sebagai syarat tetap — rerun pilot adalah
validasi/pengukuran, bukan syarat metode. Kendali mutu sensus =
verifikasi parent atas hitungan + kontrol positif (B6); enumerasi
kedua yang independen = sapuan akhir B9, bukan sensus ulang di
Tahap B.
10. Menulis laporan akhir / memoles artefak — artefak Tahap B adalah
berkas kerja (baris JSON, daftar, ledger), bukan laporan poles.
11. Filter di DALAM klaster saat inventory (hanya data yang dibutuhkan
alur live) — dinilai BERISIKO oleh Kim (15 Nov 2026 18:22 WIB), tidak
diadopsi; larangan ini ditulis ke berkas ini 22:33 WIB 16 Nov 2026
atas perintah Kim ('larangan ditulis'). Filter yang aman hanya utuh
per klaster/alur.
Untuk proyek baru, tepi keluar EP+VM dicatat DALAM pass sensus
(field 'keluar' di baris sensus) — bukan pass terpisah; pass
enumerasi jahitan yang terpisah hanya catch-up untuk pilot Across
yang sensusnya sudah jalan tanpa field itu. (Koreksi 22:33 WIB
16 Nov 2026: field 'keluar' TIDAK wajib — B16 tidak dipakai. Pass
enumerasi jahitan terpisah tetap hanya catch-up pilot Across.)
Yang dikerjakan di
Tahap B: lihat seksi 'Tahap B — yang wajib selesai'.

## C. Preferensi yang mengikat (berlaku selama metode dijalankan)

C1. Fork-live: pengujian mengikuti kondisi live nyata — fork dibangun ke
kondisi live (kontrak ter-deploy + state live pada blok yang di-pin),
kecuali user sudah menjelaskan di awal proyek masih testnet/devnet.
Mekanisme penentu wajib diuji ulang di fork live bila fork-testable;
bila tidak fork-testable, catat eksplisit. Sumber RPC (diputus Kim
17 Nov 2026, mengikat): ALCHEMY UTAMA — key per-rantai dari .env /
.env.rpc.secret dipakai lebih dulu lewat `rpc-env.sh <rantai>`;
fallback ke public RPC (publicnode dan lainnya di .env.rpc) hanya bila rantai
itu tidak punya key alchemy ATAU alchemy gagal/limit.

C2. Kejujuran bukti: label DIEKSEKUSI vs DIANALISIS vs
CODE-REVIEW-ONLY; klaim yang gugur dicabut sampai ke dokumennya;
koreksi disampaikan eksplisit.

C3. Verify_zero_and_scan: setiap nol = mencurigakan; simpan output
lengkap termasuk error; wajib kontrol positif bukan-nol lewat jalur
yang sama; pindai besar dibuktikan sensus (rentang + chunk + cakupan)
atau dilabeli SAMPEL persis; langkah belum dijalankan = langkah
terbuka, bukan rejection/finding; koreksi label di dokumen yang sama.

C4. Ambang $1 bukan ambang batas (direvisi 17 Nov 2026, perintah Kim:
dari $500 turun ke $1): apapun yang merugikan protokol /
sistem yang salah DISIMPAN sebagai kandidat berapapun kecilnya; floor
$1 hanya konteks eligibility. Tersimpan ≠ tersubmit.

C5. HOLD: nol submisi / kontak program tanpa persetujuan eksplisit per
kandidat; jangan buat draf laporan submisi tanpa instruksi eksplisit.

C6. Tiga verdict terpisah (mekanisme / eligibility / dampak); severity
dari plafon TERAMATI; insidensi wajib analisis same-tx; plafon
per-eksekusi tidak dikalikan tanpa bukti pengulangan.

C7. Bahasa: Indonesia ringan dan sederhana.

C8. Keep-hunting: tolak kesimpulan prematur "no vulnerability"; hasil
kecil berharga; tetapkan target lanjutan konkret, bukan menyatakan
permukaan bersih.

C9. /stop atau perintah berhenti eksplisit mencabut otorisasi round
seketika: hentikan subagent, tulis nol berkas, lanjutkan hanya atas
perintah eksplisit baru.

C10-v2. Permissionless & Reachable Potential Ceiling (moneyflow v2.0
— Lapis Konstitusi, diputus 18 Nov 2026; menyempurnakan C10 17 Nov
2026): kandidat sah naik dari Tahap D ke Tahap E dan layak masuk wadah
`09` bila terbukti di E, dengan KEEMPAT syarat terpenuhi:
(1) **Permissionless:** aksi pemicu dapat dijalankan akun publik biasa
tanpa peran istimewa (`owner`, `admin`, `governance`, `whitelisted
multisig`). Alur yang melibatkan bot/keeper/relayer publik yang
memproses input pengguna sesuai operasi normal protokol tetap dihitung
sah; "keanehan" susunan transaksi BUKAN alasan gugur.
(2) **Reachable Action & State:** seluruh prasyarat state dapat
dicapai lewat urutan transaksi operasi normal yang sah di atas kode +
state live blok pin — dilarang manipulasi slot storage paksa
(`vm.store`) yang mustahil dicapai lewat transisi kontrak.
(3) **Measurable Potential Ceiling ≥ $1:** dampak finansial merugikan
(kehilangan dana, pencetakan nilai tak berjaminan, penghapusan
kewajiban, atau penguncian dana permanen) terukur secara eksak ≥ $1;
hanya dampak < $1 yang gugur sebagai `DUST` (ke wadah `06`).
(4) **Dua mode pengukuran plafon di fork blok pin (untuk C6 & Tahap
E/G):** saldo/likuiditas live blok pin > 0 → ukur langsung sebagai
`Observed Live Ceiling`; saldo/likuiditas live blok pin == 0 TAPI
kontrak sudah live dan terbuka menerima aktivitas pengguna normal →
Tahap E WAJIB mensimulasikan transaksi penyetoran/aktivitas pengguna
korban secara sah lewat entrypoint normal lebih dulu di atas fork
blok pin, lalu mengeksekusi transaksi akun penguji terpisah tanpa hak
istimewa untuk mengukur `Proven Potential Ceiling` ≥ $1.
Gate dipisah agar bebas kontradiksi dengan larangan PoC di Tahap D:
- **Gate D (sebelum PoC):** verifikasi statis dari kode + bacaan state
  blok pin bahwa jalur pemicu permissionless, state prasyarat
  reachable tanpa peran admin, kontrak lulus B8 live-match, dan rumus
  plafon potensial ≥ $1 terdefinisi jelas.
- **Gate E (eksekusi PoC):** pembuktian mekanisme dan angka P&L
  aktual lewat Foundry/test harness di fork blok pin.
`DORMAN` (definisi tunggal, moneyflow v2.0): HANYA dipakai bila jalur
pada deployment live saat ini diblokir keras oleh saklar konfigurasi
admin aktif (`paused == true`, `cap == 0` yang dikunci admin, atau
modul belum didaftarkan di kontrak induk), dan wajib mencatat syarat
buka-ulang yang konkret. TIDAK HARUS LIVE: kejadian nyata / P&L live /
korban nyata BUKAN syarat; plafon live 0 dengan kontrak terbuka BUKAN
DORMAN — ukur `Proven Potential Ceiling`. Ini melanjutkan standar tiga
tingkat Kim 23 Okt 2026 (mekanisme jalan di lab = syarat perlu; pemicu
terjangkau operasi normal tanpa role istimewa/state eksotis; plafon
terukur; korban nyata tidak wajib).

C11. Standar bukti TERBUKTI — jalur pendek yang saling bergantung (diputus 17 Nov 2026,
perintah Kim 12:14 WIB): TERBUKTI = ada CUKUP jalur pendek yang saling bergantung
(1 atau beberapa) dari pelanggaran invariant sampai ke kerugian yang terukur;
kerugian diukur lewat verifikasi alur-alur TERKAIT, bukan simpulan di dalam satu
fungsi pendek — tes yang berhenti di satu fungsi pendek lalu menyimpulkan = masih
HIPOTESIS. Konsekuensi: (a) kartu E yang buktinya cuma satu fungsi pendek harus
dinilai ulang; (b) Gelombang 1/2 tidak memberi verdict TERBUKTI — tiap observasi/
jawaban dilabeli DIANALISIS + dicatat alur terkait apa yang masih kurang menuju
kerugian terukur; (c) kartu lead merumuskan rantai (a)+(b)+(c) sebagai satu rantai
yang harus diuji Tahap E, bukan hanya satu fungsi; (d) verdict 09/G memakai
standar ini bersama C10. Berlaku ke G02 juga (buka ulang P7) dan mulai P8.

C12. Stream Context Capsule (moneyflow v2.0, 18 Nov 2026, mengikat
untuk delegasi): brief delegasi subagent Tahap C/D/E hanya memuat
konteks terikat Stream aktif — `C00-SHARED-PRIMITIVES.md`,
`C<NN>-<STR>-<Lk>-INVENTORY.md` beserta potongan kode bernomor
`File:Lxx-Lyy` pada koridor stream, baris relevan dari
`B07-STATE-BRIDGES.md`, maksimal 1 ringkasan tabel Handoff/Simpul dari
stream kembar (*twin-path*) bila relevan, dan (khusus Tahap D
Gelombang 2) maksimal 2–4 berkas plugin katalog yang cocok dengan
gejala kode. Dilarang meneruskan riwayat percakapan panjang atau
berkas stream lain yang tidak bersinggungan. Lantai bawah tetap utuh:
baca kode manual penuh saat sensus, uji fork blok pin, kontrol positif
untuk setiap hasil nol, rerun forge oleh parent dengan kecocokan gas
identik, tiga verdict terpisah, bahasa brief berbasis verifikasi
invariant, aturan `HOLD` dan `/stop`.

## D. Tahap C–G — modular (15 Nov 2026, perintah Kim: pisah modular seperti versi triangle; pemetaan mendalam jadi Tahap C, 15 Nov 2026, perintah Kim 'nomor baru saja')

Pemetaan huruf (15 Nov 2026, perintah Kim 'ubah tahap jadi huruf saja'): Tahap A = INTEL (dulu Tahap 0), B = Mapping (dulu Tahap 1), C = Pemetaan mendalam per klaster (dulu Tahap 2), D = Eksplorasi (dulu Tahap 3), E = Uji test (dulu Tahap 4), F = Komposisi (dulu Tahap 5, USULAN), G = Verdict (dulu Tahap 6). Output tiap tahap: `<huruf><NN>-<NAMA>`, mis. B01-SCOPE, C01-FLOW-INVENTORY. Penomoran aturan (A1–A5, B0–B22, C1–C12) dan SM/INV tidak berubah — namespace terpisah.

- Tahap B — Mapping: sensus + klaster (4 tipe, B4) + daftar handoff + `B07-STATE-BRIDGES` + ledger sisa + registry (B1–B16). Tanpa invariant (B12), tanpa pemetaan mendalam, tanpa buruan/PoC/verdict.
- Tahap C — Stream-Slice Inventory (rolling per-Lintasan): `C00-SHARED-PRIMITIVES.md` sekali di awal Tahap C sebelum Stream pertama; inventaris per Lintasan (`C<NN>-<STR>-<Lk>-INVENTORY.md`) — **9 bagian baku (A04)**: identitas Lintasan, segmen (`S0..Sn`, B19), Titik Serah Kendali `CY-x` (B18), handoff (B11), simpul, State-Bridge (`HB-x`, B07), Tabel Selisih Varian (B20), Lembar Parameter Live per domain (B21), rekonsiliasi ledger; `C00` wajib mencatat titik serah kendali per primitif (`C00-Uxx/CY`). Segmen ditetapkan lewat **Langkah 0 anggaran** (Segmen ≤ ~4 fungsi, Lintasan 4–8 segmen / ≤ ~12 fungsi, 1 keluarga varian; rentang wajar, bukan ambang kaku) mengikuti Aturan Koridor Stream (`Corridor-Bound Cross-Cluster`, B2a-v2). Tanpa invariant, tanpa buruan/PoC/verdict.
- Tahap D — Eksplorasi: buruan per segmen/handoff/simpul; merumuskan invariant tiap kandidat (wajib cantumkan sumber: field handoff atau docs/NatSpec) + kartu lead (tiap kartu lead wajib klaim finansial sendiri). Tanpa PoC. [RIWAYAT 16 Nov 2026: unit round per-alur + EV.] Berlaku v2.1: unit round = per-Lintasan, dua gelombang (buta → berpengetahuan + katalog plugin); prasyarat sebelum D = inventaris Lintasan lulus `check-c` + B8 Live-Match Lintasan. Gerbang tambahan: tiap Lintasan ≥ 1 kartu ATAU catatan `NIHIL_KANDIDAT: <alasan per segmen>`; tiap baris `BEDA` Tabel Selisih yang menyentuh nilai/autentikasi ≥ 1 kartu; tiap `CY-x` dengan `Storage ditulis SESUDAH` ≠ kosong DAN guard `none` ≥ 1 kartu atau catatan. Diputus 17 Nov 2026: gate finansial — plafon live 0 TIDAK lagi membuat lead DORMAN; yang menentukan kerugian yang bisa dibuktikan (C10). Diputus 17 Nov 2026: standar TERBUKTI — kartu E yang buktinya cuma satu fungsi pendek harus dinilai ulang; Gelombang 1/2 tidak memberi verdict TERBUKTI (C11). Diputus 18 Nov 2026 (moneyflow v2.0): unit round = per-Stream (B2a-v2); urutan kartu QUEUED di dalam Stream menurut bobot struktural — P1 konservasi (INV-Jx, INV-Fx), P2 handoff/state-bridge (INV-Hx, INV-HBx), P3 anomali segmen (INV-Sx, S1→Sn); anti-kuota mutlak sampai QUEUED == 0 dan ACTIVE == 0; Koridor Stream berlaku + 1-hop peek State-Bridge (HB-x). Diputus 19 Nov 2026 (Post-Audit Hot-Zone): urutan Stream mengikuti `B2a-PostAudit` dua tier (Hot Streams `[DELTA]`/`[SCAR]`/`[SEAM]` dulu + `Prerequisite C-Only Pass`, lalu Tier 2 sampai sisa 0); Gelombang 1/2 wajib menjalankan **Tiga Deep-Check** (Handoff & State-Bridge: batas ekstrem input + state interleaving EP+SM; Simpul Fork/Join: pembulatan insolvensi/mengendap + kelabu-klaim via transfer/merge/split; Twin-Path & Patch-Scar: selisih penjaga antar-jalur kembar) — dilarang sekadar merangkum tabel Tahap C; `[SCAR]` memicu `M-004`, `[SEAM]` memicu `M-008` di Lazy Skill Router.
- Tahap E — Uji test: PoC fork-live + P&L terukur per kandidat; membuktikan/membantah mekanisme. v2.1: Lintasan `MULTI-DOMAIN` menguji di fork domain sumber DAN domain tujuan bila handoff lintas-domain berada di rantai (a)+(b)+(c); pengiriman pesan disimulasikan dengan impersonasi pengirim sah sesuai autentikasi domain (alias, `crossChainSender`, messenger), dicatat di `E-PROOF`. Diputus 22:33 WIB 16 Nov 2026: bentuk rinci = yang sudah dipraktikkan (batch maks 3, fork blok pin + P&L terukur); verdict mengikuti bentuk yang sekarang (06/07/08/09). Diputus 17 Nov 2026: Tahap E membuktikan rantai (a)+(b)+(c) sebagai satu rantai, bukan hanya satu fungsi (C11). Diputus 18 Nov 2026 (moneyflow v2.0): Gate E mengukur plafon di fork blok pin dua mode — `Observed Live Ceiling` (saldo/likuiditas live > 0 → ukur langsung) dan `Proven Potential Ceiling` (saldo live 0 tapi kontrak terbuka menerima aktivitas pengguna normal → simulasi transaksi penyetoran/aktivitas korban secara sah lewat entrypoint normal lebih dulu di atas fork blok pin, lalu eksekusi transaksi akun penguji terpisah tanpa hak istimewa; plafon ≥ $1). Diputus 19 Nov 2026 (fork multi-chain): fork mengikuti chain kontrak koridor kartu; kartu yang menyentuh override/behavior per-chain (admin sender verification, leaf hooks, unwrap fork, gas-token, light client) **wajib diuji di fork chain tersebut** (bukan selalu Ethereum); multi-chain fork diizinkan dan dicatat di `E-PROOF`; dasar pengetahuan per-chain = implementasi yang sudah dibaca di Tahap B/C — fork mengonfirmasi eksekusi.
- Tahap F — Komposisi Inkremental & Akhir (moneyflow v2.0, 18 Nov 2026; meneruskan penerimaan bersyarat 22:33 WIB 16 Nov 2026): bila Stream aktif berbagi `State-Bridge` (`B07`) atau brankas saldo yang sama dengan Stream yang sudah selesai dan keduanya membentuk rantai dampak multi-stream, evaluasi komposisi dijalankan SEGERA setelah Tahap E Stream aktif selesai (selagi konteks segar), tanpa menunggu seluruh proyek; komposisi lintas-Stream akhir tetap di penutupan. Tetap HANYA untuk lead multi-segmen. Uji F TIDAK menjalankan fork ulang dan TIDAK menjalankan PoC ulang — pakai data terbaru (hasil Tahap E); bukti komposisi = lemma (segmen terbukti + handoff cocok + simpul terbukti + jalur gabungan dirangkai dari data terbaru). Lead satu segmen LEWATI Tahap F (PoC Tahap E sudah final).
- Tahap G — Verdict: verdict per kandidat (06/07/08/09; tiga verdict terpisah; severity dari plafon teramati); distribusi akhir dihitung di seluruh protokol. Diputus 22:33 WIB 16 Nov 2026: bentuk rinci = yang sudah dipraktikkan (verdict mengikuti bentuk yang sekarang). Diputus 17 Nov 2026: verdict 09 TIDAK lagi mensyaratkan P&L live > 0; syaratnya kerugian yang bisa dibuktikan (C10). Diputus 17 Nov 2026: verdict memakai standar TERBUKTI (C11) bersama C10.

Rolling per-Stream (moneyflow v2.0): Tahap C Stream → Tahap D Stream → Tahap E Stream, dan seterusnya berulang; klaster = papan kontrol kelengkapan Tahap B (B2a-v2), bukan pagar. Tahap F komposisi inkremental + lintas-Stream akhir + Tahap G di akhir. Bentuk rinci Tahap D/E/G sudah diputus 22:33 WIB 16 Nov 2026 (lihat butir di atas); bentuk rinci Tahap C sudah terbukti di pilot (8 round). Deep-run per jalur (diputus Kim 22:33 WIB 16 Nov 2026): satu perintah berdiri hulu→hilir sampai verdict per lead, tanpa tap antar langkah; berlaku mulai jalur berikut (P4 — P3 sudah jalan step-by-step).

Just-in-time lintas-klaster (15 Nov 2026, perintah Kim; KOREKSI 15 Nov 2026 — dipindah dari Tahap C ke Tahap D atas pertanyaan Kim 'bukankah ini harusnya pas eksplorasi?'): materi terkait dan urgent dari klaster lain ditarik just-in-time di Tahap D (eksplorasi) — saat memburu satu alur, pemburu mengikuti alur itu melewati klaster, hanya yang dilewati alur itu. DIGANTI moneyflow v2.0 (18 Nov 2026) oleh **Aturan Koridor Stream (`Corridor-Bound Cross-Cluster`, B2a-v2)** — berlaku di Tahap C dan Tahap D Gelombang 1: ikuti garis aliran nilai Stream aktif menembus batas klaster (fungsi penerima = `S(k+1)`, tandai EP+VM selesai di `B05-LEDGER-SISA.md`), tanpa melebar horizontal ke fungsi lain di klaster seberang; jeda aliran pada variabel storage dicatat sebagai `HB-x` di `B07-STATE-BRIDGES.md` dengan `1-hop peek` di Tahap D. [ARSIP RIWAYAT PILOT] Keputusan klaster era pilot yang dipenuhi: (2) round 1 Tahap C = K1 SAJA (loop K1+K2 diburu bersama di Tahap D, dirangkai di Tahap F); (3) K8 = round sendiri di Tahap C (diinventarisasi sekali, dirujuk konsumen). Urutan EV (K1 dulu) tetap sebagai prioritas, bukan pagar.


## Diputus 20 Nov 2026 (moneyflow v2.1 — Universal Topology) — MENUNGGU PUTUSAN KIM

1. B0 Profil Topologi + 3 mode.
2. B17 Katalog Ingress `IN-x` + populasi ketiga ledger.
3. B18 Titik Serah Kendali `CY-x`.
4. B19 5 pemicu batas segmen + anggaran Segmen/Lintasan/Stream; Lintasan = unit kerja satu sesi.
5. B20 Tabel Selisih Varian.
6. B21 LP-x dibaca di domain eksekusi; `UNVERIFIED` menggantikan `TIDAK-TERBACA -> LIVE`.
7. B22 Larangan Stream sapu sisa.
8. B6-v2 AST diizinkan untuk lokalisasi & enumerasi; verdict tetap dari baca badan.
9. B9 sapuan akhir = enumerasi AST independen (atau rerun manual).
10. B10 rekonsiliasi ledger berbasis nama.
11. B14 nilai `no` (iv) `COSMETIC_NON_ECONOMIC` + konvensi 8 modifier non-standar.
12. B07 enum `Sync_Status` + kolom waktu (lihat skill C Bagian 5).
