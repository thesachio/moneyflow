---
name: flow-f-compose
description: Tahap F — Komposisi (bersyarat). Hanya lead multi-segmen, hanya bila penting dan urgent; uji pakai data terbaru, tanpa fork/PoC ulang; bukti = lemma dengan format 4 syarat. Skill ini memuat gerbang dan format sampai Tahap F selesai. Dipakai saat merangkai jalur ujung-ke-ujung, atau saat user menyebut tahap F, komposisi.
---

# Skill flow-f-compose — Tahap F (Komposisi)

Tahap F = merangkai segmen/handoff/simpul yang **sudah terbukti** jadi jalur ujung-ke-ujung.
**DITERIMA BERSYARAT** — bukan tahap wajib. Skill ini memuat gerbang dan format sampai Tahap F selesai. `methodology/aturan-alur-first.md` (seksi D — Tahap F) hanya rujukan sengketa.

## Gerbang masuk (dua syarat, keduanya harus benar)

| Syarat | Cara memutuskan |
| :--- | :--- |
| **Multi-segmen** | lead melewati **≥2 segmen** atau **≥1 handoff** yang masing-masing sudah punya bukti Tahap E |
| **Penting dan urgent** | rangkaian ini mengubah keputusan: tanpa F, dampak tidak bisa dinyatakan utuh (mis. dampak hanya muncul saat dua segmen dirangkai) |

Bila salah satu tidak terpenuhi:

- **Lead satu segmen → LEWATI Tahap F.** PoC Tahap E sudah final; langsung ke Tahap G.
- **Tidak urgent → lewati.** Jangan menjalankan F hanya karena "bisa".

## Langkah 1 — Rangkai, jangan ulang

- Per klaster dulu; lintas klaster di akhir.
- Bahan rangkaian: **hasil Tahap E yang sudah ada** (segmen terbukti, handoff cocok, simpul terbukti).
- Urutan rangkaian mengikuti alur: S1 → H1 → S2 → H2 → S3 …

## Langkah 2 — TIDAK fork ulang, TIDAK PoC ulang

Uji F **memakai data terbaru** (hasil Tahap E). Alasannya: bukti segmen sudah **dieksekusi** di E; F **merangkai** bukti itu, bukan mengulang eksekusinya.

Yang masih **boleh** di F: membaca state live terbaru untuk memastikan angka masih berlaku, dan menghitung ulang aritmetika rangkaian dari angka E. Yang **dilarang**: menjalankan fork baru, menulis PoC baru, mengulang skenario E.

## Langkah 3 — Lemma: 4 syarat wajib

Sebuah lemma sah **hanya bila keempatnya ada**:

1. **Segmen terbukti** — tiap segmen punya bukti Tahap E (DIEKSEKUSI, bukan DIANALISIS).
2. **Handoff cocok** — keluaran segmen N memenuhi masukan segmen N+1: nama field, tipe, satuan/desimal, dan rentang nilai.
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

`F<nn>-<JALUR>-COMPOSITION.md` (atau seksi komposisi di berkas verdict) memuat:

| Bagian | Isi |
| :--- | :--- |
| Rangkaian | S1 → H1 → S2 → … dengan jangkar `Path/File.ext:Lxx-Lyy` per simpul |
| Lemma | pernyataan lemma + 4 syarat terpenuhi (satu per satu) |
| Aritmetika | angka dirantai eksplisit: masuk → keluar → masuk berikutnya |
| Ketidakcocokan | daftar temuan + ke mana dikembalikan |
| Status | `LEMMA TERBUKTI` / `HIPOTESIS` (+ syarat yang kurang) |

## Definition of done Tahap F

- [ ] gerbang dua syarat lulus (multi-segmen **dan** penting-urgent)
- [ ] tiap segmen punya bukti DIEKSEKUSI dari Tahap E
- [ ] handoff dicek per field (nama, tipe, satuan, rentang)
- [ ] simpul dicek konservasi / konsumsi-sekali
- [ ] angka dirantai eksplisit, bukan disimpulkan
- [ ] nol fork baru, nol PoC baru
- [ ] ketidakcocokan dicatat + dikembalikan, bukan ditambal
- [ ] status akhir jelas: LEMMA TERBUKTI atau HIPOTESIS
