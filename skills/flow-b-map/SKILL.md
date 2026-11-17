---
name: flow-b-map
description: Tahap B — Mapping. Sensus statis 100% peristiwa pemindah nilai (B1/B6, 7 konvensi B14 lengkap, tanpa AST), sensus live ringan B7 wajib, cek live-match B8 + TUNDA-LIVE, ledger sisa (B10), handoff dari batas unit (B11), scope lock (B13). Skill ini memuat aturan yang dibutuhkan sampai Tahap B selesai. Dipakai saat memetakan scope proyek, sensus, atau saat user menyebut tahap B, mapping, sensus, scope.
---

# Skill flow-b-map — Tahap B (Mapping)

Tahap B = tahu scope menyeluruh di awal (sensus utuh + peta alur), **tanpa buruan**.
Skill ini memuat aturan yang dibutuhkan untuk menjalankan Tahap B sampai selesai. `methodology/aturan-alur-first.md` (B1–B16) hanya rujukan bila ada sengketa tafsir — jangan buka methodology untuk mencari langkah; langkahnya ada di sini.

## Uji pemisah (pakai ini untuk memutuskan "ini pekerjaan B atau bukan")

Tahap B mengerjakan **hanya** yang butuh pandangan seluruh protokol dan **tidak bisa direkonstruksi** tahap berikut tanpa baca ulang seluruh protokol.
Butuh konteks satu klaster saja → bukan Tahap B; kerjakan di giliran klaster itu (C/D/E).

## Keluaran (sekali, untuk seluruh protokol)

| Artefak | Isi |
| :--- | :--- |
| `B01-SCOPE.md` | daftar scope + scope lock (B13) |
| `B02-CENSUS-STATIC.md` + `scripts/out/*.jsonl` | sensus statis 100% (satu baris JSON per fungsi) |
| `B03-CENSUS-LIVE.md` | inventaris alamat live (daftar) + sensus live ringan B7 |
| `B04-CLUSTERS.md` | identifikasi klaster + daftar handoff (B11) |
| `B05-LEDGER-SISA.md` | ledger sisa seed (B10) |
| `B06-REGISTRY-INVARIANT.md` | struktur + penomoran, **isi kosong** (diisi Tahap D) |

## Langkah 1 — B13 Scope lock (gerbang masuk; sebelum sensus)

Tiga syarat, semuanya harus benar sebelum satu baris sensus ditulis:

1. **Daftar berkas cocok persis** inventaris kanonik — `diff` kosong antara daftar yang dipakai sensus dan daftar scope yang dikunci.
2. **Commit terverifikasi** — `git rev-parse HEAD` pada repo target, dan `git status --porcelain` bersih (nol baris).
3. **`contracts/` bersih** — tidak ada berkas build/artefak yang menyamar sebagai sumber.

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
| 3 | **Fungsi payable yang memanggil sistem eksternal yang diketahui** (relayMessage adapter → messenger bridge, dsb.) = `value_moves: yes`. Tahap alur **WAJIB** verifikasi penerusan value per adapter dari badan — bila ternyata tidak meneruskan, **turunkan ke `no`**. | `yes` sementara, wajib dikonfirmasi |
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
- `value_moves`: `yes` / `no` / `unknown` — **hanya** menurut B14.
- `mechanisms`: mekanisme yang terlihat di badan (transfer, mint, burn, delegatecall, assembly, dsb.).
- `notes`: alasan verdict bila tidak obvious; **wajib** untuk `unknown`.

**EP+VM** (entrypoint DAN `value_moves: yes`) = angka yang **mengikat** untuk inventaris alur. Bukan EP total.

### Kontrol positif (wajib, bukan opsional)

Pilih **9 fungsi yang sudah diketahui pasti memindah nilai** (fungsi transfer/withdraw/swap/deposit utama), lalu buktikan tiap satunya **ada** di sensus dengan baris yang benar dan `value_moves: yes`.
Hasil wajib **9/9**. Kurang satu = sensus buta, ulangi bagian itu.

### Nol mekanis wajib dipecahkan

Hitungan mekanis yang menghasilkan **0** untuk sesuatu yang seharusnya ada = **wajib dipecahkan** (cari nama sebenarnya, cek regex, cek warisan), **bukan diterima** sebagai "memang tidak ada".

### Yang TIDAK dilakukan saat sensus

- Baca mendalam untuk memahami logika tiap fungsi — sensus **mengklasifikasi**, bukan memahami. Baca mendalam hanya untuk fungsi EP+VM + di Tahap C.
- Menyelesaikan semua `unknown` — `unknown` **dicatat sebagai unknown**, diselesaikan di Tahap C saat konteks alurnya ada.
- Rerun sensus penuh sebagai syarat.

## Langkah 3 — B03 Sensus live ringan (B7 — WAJIB, bukan opsional)

Anggaran **maks 5 menit** untuk seluruh B7. Isi:

1. `getCode` **1–3 alamat inti** pada **blok referensi**.
2. Bila ada kode: **satu** panggilan view murah (`owner()`, `liveness()`, `totalSupply()`).

Aturan rantai:

- Rantai utama = rantai tempat kontrak inti ter-deploy (menurut INTEL + `deployments/`). Bila INTEL tidak eksplisit: rantai dengan alamat deployment inti terbanyak.
- Rantai utama gagal (RPC mati / tidak ada kode / tidak ada blok referensi) → **rantai utama kedua** (deployment inti terbanyak berikutnya).
- Satu rantai tidak merespons (timeout/403/429) → **jangan tunggu, langsung pindah**.
- Keduanya gagal → B7 selesai **dengan catatan** (apa yang dicoba + hasil); verifikasi pindah ke B8.

**TIDAK termasuk B7:** jejak event, hitung log, verifikasi seluruh inventaris alamat, cek rantai lain — itu B8 per klaster.

**Blok referensi ditetapkan di sini** (A5) dan dicatat sebagai koreksi eksplisit bila berbeda dari dugaan Tahap A.

## Langkah 4 — B8 Cek live-match per klaster + TUNDA-LIVE

B8 **diulang di awal fase uji tiap klaster**, sebelum PoC ditulis. Tanpa B8, PoC klaster itu **TERBLOKIR**.

Tidak live-match → wadah **TUNDA-LIVE**:

- tercatat di ledger sisa (**tetap terhitung**, bukan hilang)
- **nol waktu eksekusi** (tanpa PoC, tanpa fork)
- dibuka lagi hanya bila deployment live muncul atau user memerintah cek ulang
- ditinjau ulang di sapuan akhir

**Cara kerja B8 (mengikat):**

1. **Utamakan alur.** Tahu mekanisme jalan atau tidak dari: baca kode + `cast`/cek live + uji fork di Tahap E. **Bukan** dari memindai log tx orang lain.
2. **Pindai log = verifikator terakhir.** Hanya untuk Tahap G / sapuan akhir. Preseden buruk: satu B8 memakan ~8,5 jam memindai event per rantai — jangan diulang.
3. **Cek desain kode dulu** untuk memutuskan "nilai ini 0 atau bukan": apakah kode **men-set 0** atau **bisa memuat**? Nilai yang di-set dari parameter input tanpa `require`/validasi = **bisa memuat non-zero by design**; live 0 berasal dari off-chain, bukan batasan kode.

## Langkah 5 — B04 Klaster + B11 Handoff

- **Klaster** = kelompok alur ujung-ke-ujung. Urutan default = **EV live** (prioritas, bukan pagar). Bila EV tidak dipakai (data live tidak ada, atau user memerintah urutan lain), pakai urutan lain **dan catat alasannya**.
- **Handoff (B11)**: dienumerasi **dari batas unit** — rantai linear N unit → **N−1 handoff**. Jangan dilabeli tangan.
- Tiap handoff memuat: **produsen, konsumen, field (nama + tipe + satuan/desimal), jaminan produsen, asumsi konsumen**.
- **Simpul fork/join jadi unit sendiri** — prioritas tinggi (fork → cek konservasi Σkeluaran = masukan − fee; join → cek konsumsi tepat sekali).

## Langkah 6 — B05 Ledger sisa (seed)

Seed berisi: semua entrypoint, semua klaster, semua handoff terbuka, klaster yang belum dikerjakan.

Aturan B10: ledger diperbarui **sesudah tiap round**; round selesai **hanya bila sisa menyusut**; round tanpa hasil baru = sinyal berhenti dan periksa. Target buruan **harus ada di sensus** — kalau tidak, di luar scope menurut konstruksi.

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
8. Menilai/menghakimi klaster saat memetakan ("klaster ini bersih/berbahaya") — itu Tahap G; peta harus netral.
9. Rerun sensus penuh sebagai syarat tetap.
10. Memoles artefak/laporan akhir — artefak B adalah berkas kerja (JSON, daftar, ledger).
11. **Filter di DALAM klaster saat inventory** (hanya data yang dibutuhkan alur live) — dinilai berisiko, tidak diadopsi. Filter yang aman hanya **utuh per klaster/alur**.

## B16 — TIDAK DIPAKAI

Field `keluar` per fungsi EP+VM **tidak wajib**; daftar jahitan `SM-xx` lengkap **tidak wajib**. Urutan klaster tetap EV live (B2). Jangan bangun pass enumerasi jahitan terpisah.

## Penutupan graf + sapuan akhir (B9) — dicatat di sini, dieksekusi di akhir

Sensus di depan adalah **rencana + daftar periksa, bukan bukti kelengkapan**. Bukti datang dari 4 mekanisme di eksplorasi:

1. baca ulang mendalam per klaster;
2. cek handoff + konservasi (delta tak terjawab diselidiki);
3. jejak event live sebagai enumerasi independen;
4. cek penutupan graf.

**Penopang wajib:** sapuan akhir dengan **enumerasi independen kedua** dibanding ledger akhir. Cara yang diterima: **rerun sensus manual** (pilot: rerun menemukan 15 baris yang sensus pertama lewatkan). Bukan AST, bukan regex yang sama.

Batasan jujur: cek penutupan tidak bisa menemukan item yang tidak ada di daftarnya.

## Definition of done Tahap B

Semua ini ada dan bisa ditunjuk:

- [ ] `B01-SCOPE.md` + scope lock tiga syarat lulus
- [ ] `B02-CENSUS-STATIC.md` + JSONL; kontrol positif **9/9**; nol mekanis terpecahkan; EP+VM dihitung
- [ ] `B03-CENSUS-LIVE.md`; B7 ≤5 menit; blok referensi ditetapkan; kegagalan RPC tercatat
- [ ] `B04-CLUSTERS.md`; klaster + handoff (N−1) + simpul
- [ ] `B05-LEDGER-SISA.md` seed lengkap
- [ ] `B06-REGISTRY-INVARIANT.md` struktur kosong
- [ ] nol invariant ditulis; nol buruan; nol PoC
