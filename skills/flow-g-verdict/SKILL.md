---
name: flow-g-verdict
description: Tahap G — Verdict. Verdict 06/07/08/09 per kandidat dengan kriteria masuk/keluar tiap wadah, tiga verdict terpisah, severity dari plafon teramati (Impact x Likelihood), distribusi akhir, HOLD. Skill ini memuat aturan pengadilan sampai Tahap G selesai. Dipakai saat mengadili hasil, atau saat user menyebut tahap G, verdict.
---

# Skill flow-g-verdict — Tahap G (Verdict)

Tahap G = **mengadili** tiap kandidat dan menghitung distribusi akhir di seluruh protokol.
Skill ini memuat aturan pengadilan sampai Tahap G selesai. `methodology/aturan-alur-first.md` (seksi D — Tahap G + C1–C11), `verify/VERDICT.md`, dan `verify/SEVERITY-RUBRIC.md` hanya rujukan sengketa.

## Empat wadah — kriteria masuk yang tegas

| Wadah | Nama | Kriteria MASUK | Kriteria TIDAK boleh masuk |
| :--- | :--- | :--- | :--- |
| **09** | temuan terkonfirmasi | mekanisme **TERBUKTI** (C11: rantai (a)+(b)+(c) utuh, bukan satu fungsi) **DAN** kerugian bisa dibuktikan (C10) **DAN** lolos eligibility | mekanisme cuma DIANALISIS; rantai berhenti di satu fungsi |
| **08** | valid tapi tidak memenuhi syarat | mekanisme terbukti, tapi: out-of-scope · known issue · peran terpercaya/admin · debu < $1 | mekanisme **belum** terbukti (itu pelarian wadah) |
| **07** | butuh langkah lanjut | logika **belum terbantahkan**, butuh verifikasi lanjutan (state on-chain spesifik, komponen eksternal) | parkir tanpa usaha (LAZY_BAILOUT) |
| **06** | terbantahkan / tidak valid | mekanisme **patah** saat pembuktian, atau di bawah $1 (DUST) | penolakan kertas tanpa bukti eksekusi |

### Aturan 07 vs 08 (mengikat)

Bila **ragu** antara 07 dan 08 → **tetap di 07**, dan **wajib punya blok `PERCOBAAN`** (perintah + log nyata).

Dua pelanggaran keras:

- **(a) Pelarian wadah** — memindahkan lead yang mekanismenya **belum terbukti** ke 08 lalu melabelinya Low. Ini menutupi kegagalan pembuktian dengan label severity.
- **(b) Parkir malas di 07** — menaruh lead di 07 tanpa usaha sungguh-sungguh. Hasil: `LAZY_BAILOUT_DETECTED`, laporan ditolak.

### Aturan 06 (mengikat)

**Verdict 06 melarang penolakan kertas.** Tiap verdict 06 wajib melampirkan **bukti eksekusi yang benar-benar dijalankan** (perintah + log). Menolak karena "sepertinya tidak bisa" tanpa log = laporan ditolak.

## Tiga verdict terpisah (C6)

Tiap finding dinilai **tiga kali**, terpisah, jangan digabung:

| Verdict | Pertanyaan |
| :--- | :--- |
| **mekanisme** | apakah benar-benar terjadi, dengan bukti eksekusi? |
| **eligibility bounty** | masuk scope program atau tidak? |
| **dampak** | berapa, untuk siapa, dalam kondisi apa? |

Alasan pemisahan: mekanisme bisa TERBUKTI tapi out-of-scope (→08); mekanisme bisa masuk scope tapi dampaknya debu (→06 DUST). Menggabungkan tiga pertanyaan jadi satu label = kehilangan informasi yang menentukan wadah.

## Severity (dua sumbu, wajib)

- **Severity = Impact × Likelihood.** Dilarang menilai dari satu sumbu.
- Severity ditentukan **impact**, bukan siklus deployment. Temuan Critical yang terbukti di HEAD tetap **Critical** — yang berubah hanya **wadah** (09 vs 08).
- **Severity dari plafon TERAMATI**, bukan dari kapabilitas mekanisme. "Bisa drain seluruh pool" ≠ Critical bila plafon teramati $50.
- Tiap label severity **wajib menyebut rujukan** platform/rubrik. Tanpa rujukan = tidak sah.
- **Dilarang menaikkan** severity tanpa rujukan tertulis. Ragu → turunkan dan deklarasikan asumsi.
- Bila platform tidak mendeklarasikan apa pun → **default LOW** (irisan teraman; menurunkan tidak pernah membuat laporan salah).

### Insidensi

- Klaim insidensi **wajib analisis same-transaction**.
- **Plafon per-eksekusi tidak dikalikan** tanpa bukti pengulangan.
- Kerugian **≥ $1 = bukan debu** (kandidat sah, disimpan). Hanya **< $1** yang gugur DUST ke 06.

## C10 — kerugian yang bisa dibuktikan (dasar verdict 09)

Tiga syarat, semuanya harus ada:

1. mekanisme jalan di fork/test atas **kode + state nyata**;
2. **plafon terukur**;
3. pemicu **terjangkau lewat jalur operasi normal** — tanpa peran istimewa, tanpa state eksotis.

**Tidak disyaratkan:** P&L live > 0, korban nyata, kejadian on-chain.

## C11 — standar TERBUKTI (dasar verdict mekanisme)

`TERBUKTI` = ada **cukup jalur pendek yang saling bergantung** dari pelanggaran invariant sampai kerugian terukur, diverifikasi lewat alur terkait.

- Tes yang berhenti di **satu fungsi pendek** lalu menyimpulkan = **HIPOTESIS** → bukan 09.
- Gelombang 1/2 Tahap D **tidak pernah** memberi `TERBUKTI`.

## Distribusi akhir

Hitung di **seluruh protokol**, bukan per klaster:

```
06 = ... (rincian: DUST ..., patah mekanisme ...)
07 = ... (rincian: butuh state on-chain ..., butuh komponen eksternal ...)
08 = ... (rincian: out-of-scope ..., known ..., admin ..., debu eligibility ...)
09 = ...
TUNDA-LIVE = ... (nol waktu eksekusi, dibuka bila live muncul)
DORMAN = ... (gagal C10, dengan syarat buka-ulang)
```

Angka-angka ini wajib konsisten dengan isi berkas wadah — jangan menulis ringkasan yang tidak cocok dengan daftar.

## HOLD (mengikat)

**NOL submisi / kontak program / draf kirim tanpa persetujuan eksplisit per kandidat.**

- Tahap F/G berhenti di **draf siap-kirim**.
- Pengiriman butuh persetujuan **eksplisit per pengiriman**, bukan per proyek.
- **Tersimpan ≠ tersubmit.**

## Preferensi mengikat lain yang menyentuh G

- **C7 — bahasa:** Indonesia ringan dan sederhana. Berlaku untuk verdict, laporan, dan draf.
- **C8 — keep-hunting:** tolak kesimpulan prematur "no vulnerability". Hasil kecil berharga. Tetapkan **target lanjutan konkret**, bukan menyatakan permukaan bersih.
- **C4 — $1 bukan ambang batas:** yang merugikan disimpan berapa pun kecilnya; floor $1 hanya konteks eligibility.
- **C2 — kejujuran bukti:** label DIEKSEKUSI / DIANALISIS / CODE-REVIEW-ONLY wajib; klaim yang gugur dicabut sampai ke dokumennya.

## Keluaran

- `G01-VERDICT.md` — verdict per kandidat (tiga verdict terpisah) + severity berujukan + distribusi akhir.
- Draf temuan 09 memakai format `templates/` (laporan teknis + email). **Identitas pengirim belum diisi** sampai user memerintah.

## Definition of done Tahap G

- [ ] tiap kandidat punya **tiga** verdict terpisah
- [ ] tiap severity menyebut rujukan; dua sumbu dipertimbangkan
- [ ] tiap 06 punya log eksekusi (nol penolakan kertas)
- [ ] tiap 07 punya blok PERCOBAAN
- [ ] nol pelarian wadah (mekanisme belum terbukti di 08)
- [ ] 09 hanya yang lulus C10 **dan** C11
- [ ] distribusi akhir konsisten dengan isi wadah
- [ ] nol submisi/kontak; HOLD dipatuhi
