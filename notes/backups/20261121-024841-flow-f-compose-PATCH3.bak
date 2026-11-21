---
name: flow-f-compose
description: "Tahap F — Komposisi Inkremental Lintas-Stream (moneyflow v2.0). Dua titik pemicu bersyarat: inkremental seusai Tahap E satu Stream (menyentuh State-Bridge/brankas bersama) + sapuan akhir sebelum penutupan proyek; Lemma 4 Syarat tanpa fork ulang; pengecualian presisi = 1 kartu gabungan ke FlowFixtures Tahap E. Dipakai saat merangkai jalur ujung-ke-ujung, atau saat user menyebut tahap F, komposisi."
---

# Skill flow-f-compose — Tahap F (Komposisi)

Tahap F = merangkai segmen/handoff/simpul/Stream yang **sudah terbukti** jadi jalur ujung-ke-ujung.
**DITERIMA BERSYARAT** — bukan tahap wajib, tapi berjalan di **dua titik pemicu** (lihat di bawah), bukan hanya di akhir proyek. Skill ini memuat gerbang dan format sampai Tahap F selesai. `methodology/aturan-alur-first.md` (seksi D — Tahap F) hanya rujukan sengketa.

## Dua Titik Pemicu Bersyarat

**1. Pemicu Inkremental (Segera seusai Tahap E satu Stream).** Dijalankan langsung apabila Stream yang baru selesai diuji:
- menyentuh `State-Bridge (HB-x)` di `B07-STATE-BRIDGES.md`, **atau**
- berbagi brankas dana yang sama dengan Stream yang sudah selesai sebelumnya,

**dan** gabungan keduanya membentuk dampak finansial baru atau melipatgandakan plafon dampak yang tidak terlihat pada satu Stream tunggal.

**2. Pemicu Sapuan Akhir (Sebelum penutupan proyek).** Merangkai siklus multi-stream (3+ stream atau loop umpan-balik nilai) setelah seluruh `STR` selesai.

Di luar dua pemicu ini, Tahap F tidak dijalankan — jangan mengadakan fork/PoC baru tanpa pemicu.

## Gerbang masuk (dua syarat, keduanya harus benar — setelah pemicu menyala)

| Syarat | Cara memutuskan |
| :--- | :--- |
| **Multi-segmen** | lead melewati **>=2 segmen** atau **>=1 handoff** (atau >=1 `State-Bridge HB-x`) yang masing-masing sudah punya bukti Tahap E |
| **Penting dan urgent** | rangkaian ini mengubah keputusan: tanpa F, dampak tidak bisa dinyatakan utuh (mis. dampak hanya muncul saat dua Stream dirangkai) |

Bila salah satu tidak terpenuhi:

- **Lead satu segmen → LEWATI Tahap F.** PoC Tahap E sudah final; langsung ke Tahap G.
- **Tidak urgent → lewati.** Jangan menjalankan F hanya karena "bisa".

## Langkah 1 — Rangkai, jangan ulang

- Per Stream dulu; lintas Stream pada sapuan akhir.
- Bahan rangkaian: **hasil Tahap E yang sudah ada** (segmen terbukti, handoff cocok, simpul terbukti, State-Bridge tertutup).
- Urutan rangkaian mengikuti alur: S1 → H1 → S2 → H2 → S3 dan seterusnya sesuai inventaris Stream aktif.

## Langkah 2 — TIDAK fork ulang, TIDAK PoC ulang

Uji F **memakai data terbaru** (hasil Tahap E). Alasannya: bukti segmen sudah **dieksekusi** di E; F **merangkai** bukti itu, bukan mengulang eksekusinya.

Yang masih **boleh** di F: membaca state live terbaru untuk memastikan angka masih berlaku, dan menghitung ulang aritmetika rangkaian dari angka E. Yang **dilarang**: menjalankan fork baru, menulis PoC baru, mengulang skenario E.

### Pengecualian presisi (satu-satunya jalur eksekusi gabungan)

Apabila dampak finansial komposisi **hanya menyala** ketika transaksi Stream A dan Stream B dieksekusi **berurutan dalam satu skenario gabungan** pada fork yang sama (sementara masing-masing segmen sendiri tampak normal/tidak merugikan), kirimkan **tepat 1 kartu komposisi gabungan** (`INV-Fx`) kembali ke harness bersama Tahap E (`FlowFixtures`) untuk **satu eksekusi gabungan utuh** — agar memenuhi standar `DIEKSEKUSI` Tingkat A pada `verify/VERDICT.md`, bukan dibiarkan menggantung sebagai hipotesis kertas.

## Langkah 3 — Lemma: 4 syarat wajib

Sebuah lemma sah **hanya bila keempatnya ada**:

1. **Segmen terbukti** — tiap segmen punya bukti Tahap E (DIEKSEKUSI, bukan DIANALISIS).
2. **Handoff cocok** — keluaran segmen N memenuhi masukan segmen N+1: nama field, tipe, satuan/desimal, dan rentang nilai; untuk `State-Bridge` keluaran-vs-masukan lintas Stream (jeda asinkron) juga ditutup dari `B07-STATE-BRIDGES.md`.
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
| Rangkaian | S1 → H1 → S2 → H2 → Sn dengan jangkar `Path/File.ext:Lxx-Lyy` per simpul |
| Lemma | pernyataan lemma + 4 syarat terpenuhi (satu per satu) |
| Aritmetika | angka dirantai eksplisit: masuk → keluar → masuk berikutnya |
| Ketidakcocokan | daftar temuan + ke mana dikembalikan |
| Status | `LEMMA TERBUKTI` / `HIPOTESIS` (+ syarat yang kurang) |

**Wajib setiap pemicu inkremental:** perbarui kolom `Sync_Status` di `B07-STATE-BRIDGES.md` untuk setiap `HB-x` yang dirangkai (nilai: `OPEN` / `COMPOSED` / `CONSUMED` — sesuai keadaan jembatan setelah komposisi).

## Definition of done Tahap F

- [ ] gerbang dua syarat lulus (multi-segmen **dan** penting-urgent)
- [ ] tiap segmen punya bukti DIEKSEKUSI dari Tahap E
- [ ] handoff dicek per field (nama, tipe, satuan, rentang)
- [ ] simpul dicek konservasi / konsumsi-sekali
- [ ] angka dirantai eksplisit, bukan disimpulkan
- [ ] nol fork baru, nol PoC baru (pengecualian tunggal: 1 eksekusi gabungan via FlowFixtures bila pengecualian presisi menyala)
- [ ] ketidakcocokan dicatat + dikembalikan, bukan ditambal
- [ ] status akhir jelas: LEMMA TERBUKTI atau HIPOTESIS
- [ ] pemicu inkremental yang menyala sudah dijalankan seusai Tahap E Stream terkait (bukan ditunda ke akhir proyek)
- [ ] `Sync_Status` kolom `HB-x` terkait di `B07` diperbarui tiap komposisi
