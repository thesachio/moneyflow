---
name: flow-f-compose
description: "Tahap F — Komposisi Tiga Lapis (moneyflow v2.1). Antar-Lintasan saat penutupan Stream (wajib dievaluasi; menutup kartu MENUNGGU-RANGKAI dan rantai yang melewati batas pecahan Lintasan), antar-Stream inkremental (State-Bridge / brankas / Ingress bersama), antar-varian di sapuan akhir (replay lintas-domain, perluasan temuan representatif). Lemma 4 Syarat (handoff lintas-domain wajib menutup autentikasi, anti-replay, urutan pesan) tanpa fork ulang; pengecualian presisi = 1 kartu gabungan ke FlowFixtures. Dipakai saat merangkai jalur ujung-ke-ujung, menutup Stream, atau saat user menyebut tahap F, komposisi."
---

# Skill flow-f-compose — Tahap F (Komposisi)

Tahap F = merangkai segmen/handoff/simpul/Lintasan/Stream yang **sudah terbukti** jadi jalur ujung-ke-ujung. Sejak v2.1 Stream dipecah menjadi beberapa Lintasan, sehingga ada rantai yang melewati batas Lintasan di dalam satu Stream — rantai ini tidak diuji utuh oleh satu sesi E. Karena itu F berjalan di **tiga titik pemicu** (lihat di bawah); pemicu 1 **wajib dievaluasi** setiap penutupan Stream, pemicu 2 dan 3 bersyarat. Skill ini memuat gerbang dan format sampai Tahap F selesai. `methodology/aturan-alur-first.md` (seksi D — Tahap F) hanya rujukan sengketa.

## Tiga Titik Pemicu

| # | Lapis | Kapan | Menyala bila |
| :--- | :--- | :--- | :--- |
| **1** | **ANTAR-LINTASAN** (penutupan Stream) | setelah Lintasan terakhir satu Stream selesai E, **sebelum triage G Stream itu** | ada kartu `MENUNGGU-RANGKAI` di Stream ini; **ATAU** rantai (a)+(b)+(c) melewati batas pecahan Lintasan (batas fase masuk/akuntansi/keluar, atau handoff lintas-domain pemicu e); **ATAU** `HB-x` yang penulis dan pembacanya berada di Lintasan berbeda dalam Stream yang sama |
| **2** | **ANTAR-STREAM** (inkremental) | segera setelah Stream ditutup | Stream yang baru ditutup menyentuh `HB-x` di `B07`, **ATAU** berbagi brankas dengan Stream yang sudah ditutup, **ATAU** menulis `IN-x` yang dibaca Stream lain (B17) — **dan** gabungannya membentuk dampak baru atau melipatgandakan plafon |
| **3** | **ANTAR-VARIAN + siklus** (sapuan akhir) | setelah semua Stream ditutup, sebelum `G01` | siklus 3+ Stream / loop umpan-balik nilai; **ATAU** pesan/bukti sah di satu domain bisa dipakai di domain lain (replay lintas-domain); **ATAU** temuan representatif yang anggota variannya berstatus `SAMA` di Tabel Selisih perlu dinyatakan cakupannya |

**Pemicu 1 wajib dievaluasi:** bila tidak menyala, tulis satu baris `F-ANTAR-LINTASAN: TIDAK MENYALA — <alasan per batas Lintasan>` di `B05` (kursor Stream). Stream **tidak boleh** masuk triage G selama masih ada kartu `MENUNGGU-RANGKAI`. Di luar tiga pemicu ini, Tahap F tidak dijalankan — jangan mengadakan fork/PoC baru tanpa pemicu.

## Gerbang masuk (dua syarat, keduanya harus benar — setelah pemicu menyala)

| Syarat | Cara memutuskan |
| :--- | :--- |
| **Multi-segmen** | lead melewati **>=2 segmen** atau **>=1 handoff** (atau >=1 `State-Bridge HB-x`) yang masing-masing sudah punya bukti Tahap E |
| **Penting dan urgent** | rangkaian ini mengubah keputusan: tanpa F, dampak tidak bisa dinyatakan utuh (mis. dampak hanya muncul saat dua Stream dirangkai) |

Kartu `MENUNGGU-RANGKAI` dari Tahap E **otomatis memenuhi kedua syarat** (sudah multi-segmen lintas-Lintasan dan menentukan keputusan verdict).

Bila salah satu tidak terpenuhi:

- **Lead satu segmen → LEWATI Tahap F.** PoC Tahap E sudah final; langsung ke Tahap G.
- **Tidak urgent → lewati.** Jangan menjalankan F hanya karena "bisa".

## Langkah 1 — Rangkai, jangan ulang

- Urutan lapis: **antar-Lintasan** (penutupan Stream) → **antar-Stream** (inkremental) → **antar-varian + siklus** (sapuan akhir).
- Bahan rangkaian: **hasil Tahap E yang sudah ada** (segmen terbukti, handoff cocok, simpul terbukti, State-Bridge tertutup).
- Urutan rangkaian mengikuti alur dengan **ID lengkap**: `STR-nn.L1.S3 → H3 → STR-nn.L1.S4 ‖ STR-nn.L2.S1 → …` — tanda `‖` menandai **batas Lintasan**; handoff di batas itu diambil dari kolom handoff terakhir Lintasan hulu dan Bagian 1 Lintasan hilir.
- Untuk rantai lintas-domain: tulis domain tiap segmen (`[DOM-x]`) di rangkaian.

## Langkah 2 — TIDAK fork ulang, TIDAK PoC ulang

Uji F **memakai data terbaru** (hasil Tahap E). Alasannya: bukti segmen sudah **dieksekusi** di E; F **merangkai** bukti itu, bukan mengulang eksekusinya.

Yang masih **boleh** di F: membaca state live terbaru untuk memastikan angka masih berlaku, dan menghitung ulang aritmetika rangkaian dari angka E. Yang **dilarang**: menjalankan fork baru, menulis PoC baru, mengulang skenario E.

### Pengecualian presisi (satu-satunya jalur eksekusi gabungan)

Apabila dampak finansial komposisi **hanya menyala** ketika transaksi Lintasan/Stream A dan B dieksekusi **berurutan dalam satu skenario gabungan** (pada fork yang sama, atau pada fork dua domain dengan relay pesan untuk rantai lintas-domain) (sementara masing-masing segmen sendiri tampak normal/tidak merugikan), kirimkan **tepat 1 kartu komposisi gabungan** (`INV-Fx`) kembali ke harness bersama Tahap E (`FlowFixtures`) untuk **satu eksekusi gabungan utuh** — agar memenuhi standar `DIEKSEKUSI` Tingkat A pada `verify/VERDICT.md`, bukan dibiarkan menggantung sebagai hipotesis kertas.

## Langkah 3 — Lemma: 4 syarat wajib

Sebuah lemma sah **hanya bila keempatnya ada**:

1. **Segmen terbukti** — tiap segmen punya bukti Tahap E (DIEKSEKUSI, bukan DIANALISIS).
2. **Handoff cocok** — keluaran segmen N memenuhi masukan segmen N+1: nama field, tipe, satuan/desimal, dan rentang nilai; untuk `State-Bridge` keluaran-vs-masukan lintas Lintasan/Stream (jeda asinkron) juga ditutup dari `B07-STATE-BRIDGES.md` termasuk `Window_&_Trigger`. **Handoff lintas-domain** (pemicu e) wajib menutup tiga hal tambahan: (i) **autentikasi** pengirim di domain tujuan sesuai kode; (ii) **anti-replay** — penanda unik pesan per domain/nonce; (iii) **urutan dan jendela waktu** pesan.
3. **Simpul terbukti** — fork: Σkeluaran = masukan − fee; join: konsumsi tepat sekali.
4. **Jalur gabungan dirangkai dari data terbaru** — angka dirantai secara eksplisit (nilai keluar S1 = nilai masuk S2), bukan "kira-kira cukup".

Kurang satu syarat = **bukan lemma**, tulis sebagai HIPOTESIS dengan syarat yang kurang disebut.

### C11 berlaku ke lemma

Jalur gabungan wajib memuat **cukup jalur pendek yang saling bergantung** dari pelanggaran invariant sampai kerugian terukur.
Rangkaian yang **berhenti di satu segmen** = masih **HIPOTESIS**, bukan lemma TERBUKTI.

## Langkah 4 — Ketidakcocokan: catat, jangan tambal

Bila rangkaian menemukan:

- handoff yang **tidak menutup** (tipe/satuan beda, rentang tidak tercakup),
- **simpul macet** (konservasi gagal, konsumsi ganda),
- angka E yang **sudah basi** (state live berubah),

maka:

- catat sebagai **temuan komposisi**;
- **kembalikan** ke Tahap D/E yang bersangkutan;
- **jangan diam-diam menambal** (mis. mengasumsikan konversi desimal yang tidak ada di kode).

## Keluaran

`F<NN>-<COMPOSITION_ID>.md` (atau seksi komposisi di berkas verdict) memuat:

| Bagian | Isi |
| :--- | :--- |
| Rangkaian | `STR-nn.L1.S1 → H1 → … ‖ STR-nn.L2.S1 → …` dengan jangkar `Path/File.ext:Lxx-Lyy` per simpul |
| **Lapis** | `ANTAR-LINTASAN` / `ANTAR-STREAM` / `ANTAR-VARIAN` |
| **Kartu yang ditutup** | daftar kartu `MENUNGGU-RANGKAI` yang diselesaikan komposisi ini + status barunya |
| Lemma | pernyataan lemma + 4 syarat terpenuhi (satu per satu) |
| Aritmetika | angka dirantai eksplisit: masuk → keluar → masuk berikutnya |
| Ketidakcocokan | daftar temuan + ke mana dikembalikan |
| Status | `LEMMA TERBUKTI` / `HIPOTESIS` (+ syarat yang kurang) |

**Wajib setiap pemicu:** perbarui `Sync_Status` di `B07-STATE-BRIDGES.md` untuk setiap `HB-x` yang dirangkai memakai **enum v2.1**: `SINKRON` (jaminan penulis menutup asumsi pembaca, terbukti rangkaian) / `DESINKRON:<OBS-id>` (tidak menutup — temuan komposisi) / `TERBUKA_EKSTERNAL`. Rujukan berkas komposisi dicatat di **kolom catatan** `B07` (`F<NN>-<ID>`), bukan sebagai nilai enum baru. Nilai lama `OPEN`/`COMPOSED`/`CONSUMED` **dicabut**.

## Definition of done Tahap F

- [ ] gerbang dua syarat lulus (multi-segmen **dan** penting-urgent)
- [ ] tiap segmen punya bukti DIEKSEKUSI dari Tahap E
- [ ] handoff dicek per field (nama, tipe, satuan, rentang)
- [ ] simpul dicek konservasi / konsumsi-sekali
- [ ] angka dirantai eksplisit, bukan disimpulkan
- [ ] nol fork baru, nol PoC baru (pengecualian tunggal: 1 eksekusi gabungan via FlowFixtures bila pengecualian presisi menyala)
- [ ] ketidakcocokan dicatat + dikembalikan, bukan ditambal
- [ ] status akhir jelas: LEMMA TERBUKTI atau HIPOTESIS
- [ ] **pemicu 1 (antar-Lintasan) dievaluasi di setiap penutupan Stream:** dijalankan, atau tercatat `TIDAK MENYALA` beserta alasan per batas Lintasan
- [ ] **nol kartu `MENUNGGU-RANGKAI` tersisa** sebelum triage G Stream itu
- [ ] **pemicu 2 (antar-Stream)** yang menyala dijalankan segera setelah Stream ditutup (bukan ditunda ke akhir proyek)
- [ ] **pemicu 3 (antar-varian + siklus)** dievaluasi di sapuan akhir sebelum `G01`
- [ ] handoff lintas-domain dalam lemma menutup **autentikasi + anti-replay + urutan pesan**
- [ ] `Sync_Status` kolom `HB-x` terkait di `B07` diperbarui tiap komposisi dengan **enum v2.1**
