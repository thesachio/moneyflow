---
name: flow-c-inventory
description: Tahap C — Pemetaan mendalam per klaster. Inventaris alur + segmentasi + kontrak handoff deskriptif per klaster (C01-Kn) dengan format segmen/handoff/simpul lengkap, tanpa invariant, tanpa buruan, tanpa PoC. Skill ini memuat format dan aturan sampai Tahap C selesai. Dipakai saat memetakan klaster, atau saat user menyebut tahap C, pemetaan mendalam, inventaris alur.
---

# Skill flow-c-inventory — Tahap C (Pemetaan mendalam per klaster)

Tahap C membangun **yang riil/teramati** per klaster: inventaris alur + segmentasi + kontrak handoff **deskriptif** (apa kata kode, bukan apa yang seharusnya).
Skill ini memuat format dan aturan sampai Tahap C selesai. `methodology/aturan-alur-first.md` (seksi D — Tahap C) hanya rujukan sengketa.

## Satu klaster per round — dan hanya itu

- Kerja **satu klaster (K) saja** per round. Bukan dua, bukan "sekalian".
- Urutan kerja = **pintu masuk pertama kali** (B2a, diputus 17 Nov 2026): entrypoint paling awal yang dilalui pengguna dikerjakan lebih dulu, bukan EV live. Kalau user memerintah urutan lain lagi, catat alasannya di `B04-CLUSTERS.md`.
- **Jahitan adalah batas.** Jangan baca badan fungsi klaster lain. Sisi produsen/konsumen yang klasternya belum dipetakan **dicatat terbuka**, dilengkapi di round klaster itu.
- **Tarikan just-in-time lintas klaster adalah milik Tahap D**, bukan C. Alasannya: kebutuhan tarik lintas klaster muncul saat memburu alur (alur tidak mengenal batas klaster); di C, tarikan dini menyeret penilaian ("apakah handoff cocok?") ke kerja deskriptif.

## Keluaran

| Berkas | Isi |
| :--- | :--- |
| `C<NN>-K<n>-FLOW-INVENTORY.md` | inventaris alur klaster itu (segmen + handoff + simpul + pintu masuk) |
| `C<NN>-K8-PRIMITIVES.md` | khusus klaster primitif — inventaris **primitif**, bukan alur |

## Format wajib: 4 bagian per klaster

### 1. Segmen (S1..Sn)

Tiap segmen = potongan alur yang **bisa diamati** di handoff. Untuk tiap segmen tulis:

| Kolom | Isi |
| :--- | :--- |
| ID | `S1`, `S2`, … |
| Nama segmen | ringkas, 1 baris |
| Fungsi + berkas | `Path/File.ext:Lxx-Lyy` — satu baris per fungsi yang terlibat |
| Batas masuk | apa yang menandai segmen mulai (event, perubahan state, pesan, waktu) |
| Batas keluar | apa yang menandai segmen selesai |
| Aktor | siapa yang bisa memicu (user / keeper / relayer / admin / otomatis) |

Segmen harus **bersambung**: keluaran S1 = masukan S2. Bila tidak bersambung, itu **handoff terbuka**, bukan segmen baru.

### 2. Kontrak handoff (B11)

Dienumerasi **dari batas unit** — rantai linear N segmen → **N−1 handoff**. Jangan dilabeli tangan.

| Kolom | Isi |
| :--- | :--- |
| ID | `H1`, `H2`, … |
| Produsen | segmen + fungsi yang menulis |
| Konsumen | segmen + fungsi yang membaca |
| Field | **nama + tipe + satuan/desimal** (mis. `uint128 amount`, 18 desimal) |
| Jaminan produsen | apa yang produsen pastikan (mis. "amount sudah dikurangi fee") — **apa adanya di kode** |
| Asumsi konsumen | apa yang konsumen anggap benar (mis. "amount ≤ saldo kontrak") — **apa adanya di kode** |
| Status | `TERTUTUP` / `TERBUKA` |

Handoff `TERBUKA` = konsumennya di luar kode yang dipetakan (mis. messenger eksternal). Tetap **dienumerasi**, jangan dihapus, jangan ditutup sepihak — dibuka saat alur yang diburu menyentuhnya.

### 3. Simpul (fork/join)

- **Fork** = percabangan aliran. Uji: Σkeluaran = masukan − fee.
- **Join** = penggabungan. Uji: konsumsi tepat sekali (tidak dobel, tidak hilang).
- Simpul adalah **unit sendiri** dengan prioritas tinggi — bukan catatan kaki segmen.

### 4. Pintu masuk klaster + data nilai (opsional)

**Pintu masuk klaster** = entrypoint paling awal yang dilalui pengguna untuk klaster ini (`Path/File.ext:Lxx`). Inilah yang menentukan urutan kerja (B2a), bukan nilai.

Data nilai live (jejak event live bila ada) boleh dicatat sebagai konteks, tetapi **bukan penentu urutan** dan **bukan penilaian** klaster.

## Klaster khusus

- **K8 (primitif):** inventaris **primitif**, bukan inventaris alur. Tiap primitif: jaminan produsen (mis. wrap/unwrap 1:1), peran yang dipegang, cap/batas, event yang diemisikan. Diinventarisasi **sekali**, dirujuk semua konsumen.
- **K9:** **DILEWATI** — mock/fixture test, bukan kode live.

## Yang TIDAK dilakukan di Tahap C

1. **Menulis invariant** — itu Tahap D (B12). Invariant = klaim asumsi tentang apa yang *seharusnya* berlaku, bukan fakta teramati.
2. **Buruan** saat memetakan.
3. **PoC / verifikasi / verdict.**
4. **Menutup handoff** yang konsumennya di luar kode tanpa keputusan user.
5. **Menilai klaster** ("ini bersih", "ini berbahaya") — itu Tahap G.
6. **Filter di dalam klaster** (hanya mengambil data yang dibutuhkan alur live) — dinilai berisiko, tidak diadopsi. Filter yang aman hanya utuh per klaster/alur.
7. **Membaca badan fungsi klaster lain** — jahitan adalah batas.

## Definition of done Tahap C (per klaster)

- [ ] semua segmen punya batas masuk/keluar dan bersambung (atau tercatat sebagai handoff terbuka)
- [ ] handoff berjumlah **N−1** untuk N segmen, tiap handoff punya field + jaminan produsen + asumsi konsumen
- [ ] simpul fork/join terdaftar sebagai unit sendiri
- [ ] handoff terbuka dicatat, tidak ditutup sepihak
- [ ] nol invariant, nol buruan, nol PoC
- [ ] ledger sisa diperbarui (klaster ini: sisa menyusut)
