---
name: flow-a-intel
description: Tahap A — INTEL proyek baru. Brief 9 butir (nama, lingkup, stage, repo, website, docs, audit, bugbounty, severity) + tangga penemuan A4 lengkap per butir (maks 3 cek/butir, status DITEMUKAN / TIDAK ADA / TIDAK KETEMU) + pin A5. Skill ini memuat tangga dan aturan penulisan sampai Tahap A selesai. Dipakai saat memulai proyek audit baru atau saat user menyebut INTEL, brief proyek, penemuan proyek.
---

# Skill flow-a-intel — Tahap A (INTEL)

Tahap A = **brief proyek**, bukan dokumen teknis. Keluarannya tipis dan harus cepat.
Skill ini memuat tangga penemuan dan aturan penulisan sampai Tahap A selesai. `methodology/aturan-alur-first.md` (A1–A5) hanya rujukan sengketa.

## Batas keras (baca dulu sebelum mulai)

| Dikerjakan di A | BUKAN di A |
| :--- | :--- |
| 9 butir brief + statusnya | cek onchain (`cast code`, saldo, blok) |
| daftar docs pendukung (Pre-0) | verifikasi teknis atas isi docs |
| pin commit + stage | menentukan blok referensi (itu Tahap B) |
| jejak apa yang sudah dicoba | menyimpulkan kerentanan |

**A2 mengikat:** Pre-0 = **daftar docs pendukung saja**, bukan verifikasi teknis. Kalau Anda tergoda menjalankan `cast` di Tahap A, itu Tahap B (B7) — berhenti.

## Keluaran

| Berkas | Isi |
| :--- | :--- |
| `INTEL.md` | brief 9 butir + pin (A5) + Catatan Ketiadaan |
| `A01-INTEL.md` | penunjuk kanonik ke `INTEL.md` + status + sifat berkas (jangan duplikasi isi) |
| `A02-INTEL-discovery.md` | jejak tangga penemuan per butir + bukti URL hidup + daftar docs Pre-0 |

## 9 butir brief (A1)

1. Nama proyek (singkat) — sertakan nama internal/protokol bila ada.
2. Deskripsi lingkup (bridge/swap/LP/AI/dst, singkat) — **satu paragraf**.
3. Deployment stage: **MAINNET / TESTNET / DEVNET**.
4. Repo (alamat github atau setara).
5. Website (tempat user mengakses & berinteraksi dengan UI aktif).
6. Docs (link).
7. Audit (singkat: siapa + link).
8. Bugbounty (URL).
9. Brief severity (singkat bila ada).

Tidak ada butir ke-10. Materi uang/kontrak/saldo **bukan** isi Tahap A.

## Tangga penemuan (A4) — maks 3 cek per butir

Mulai **hanya** dari nama proyek (+ tautan yang user beri, bila ada). Tiap butir punya tangga sumber berurutan. Berhenti di cek pertama yang memberi hasil.

| # | Butir | Cek 1 | Cek 2 | Cek 3 |
| :-: | :--- | :--- | :--- | :--- |
| 1 | Nama | dari user, **tanpa pencarian** | — | bila ambigu: satu putaran klarifikasi, lalu catat apa adanya |
| 2 | Lingkup | docs intro | README repo | deskripsi repo GitHub |
| 3 | Stage | docs (apakah mainnet live?) | app UI (apakah hidup?) | repo (`deployments/`, README) |
| 4 | Repo | tautan di docs | GitHub search nama proyek | tautan di website |
| 5 | Website | tautan di docs | tautan di README repo | web search `<proyek> app` |
| 6 | Docs | tautan di README | tautan di website | web search `<proyek> docs` |
| 7 | Audit | halaman audit/security di docs | folder `audits/` di repo | web search `<proyek> audit report` (1 pencarian, 3 hasil teratas) |
| 8 | Bugbounty | halaman bug bounty di docs | `SECURITY.md`/README repo | web search `<proyek> bug bounty` (1 pencarian) |
| 9 | Severity | **diturunkan dari halaman bounty butir 8** | — | **tidak ada pencarian terpisah** |

### Aturan tangga yang sering dilanggar

- **Butir 3 (stage)** di Tahap A = **klaim** docs/app/repo saja. Bukan verifikasi teknis. Konfirmasi teknis di Tahap B (B7).
- **Butir 4 (repo)**: hanya pilih bila **jelas resmi** — org cocok dan ditaut dari docs. Beberapa kandidat tanpa kejelasan → `TIDAK KETEMU (ambigu)` + eskalasi. **JANGAN menebak URL dari nama proyek.**
- **Butir 5 & 6**: URL ketemu tapi **tidak merespons** → **catat kodenya** (mis. `HTTP 403`), **bukan** `TIDAK KETEMU`. "Gagal diakses" ≠ "tidak ada".
- **Butir 9**: bila bounty `TIDAK KETEMU`, severity ikut `TIDAK KETEMU`. Jangan cari terpisah, jangan karang angka.

## Tiga status (jangan dicampur)

| Status | Arti | Wajib |
| :--- | :--- | :--- |
| **DITEMUKAN** | ada, dengan tautan | tulis tautannya |
| **TIDAK ADA** | sumber resmi menyatakan tidak ada | tulis sumber yang menyatakan |
| **TIDAK KETEMU** | tangga habis tanpa hasil | **wajib catat apa yang sudah dicoba** (sumber + hasil) |

`TIDAK KETEMU` **bukan** bukti tidak ada. Menulis `TIDAK KETEMU` tanpa daftar percobaan = brief tidak jujur.

## Butir penahan beban (stage + repo)

**Stage (3) dan Repo (4)** adalah penahan beban. Bila salah satunya `TIDAK KETEMU`:

- Tahap A **BERHENTI**
- eskalasi ke user
- **jangan menebak** untuk melanjutkan

Alasan: stage menentukan seluruh Mode Uji; repo menentukan seluruh scope. Salah di salah satunya = seluruh audit salah arah.

## Anggaran

Total penemuan **maks 30 menit**. Habis → berhenti dengan hasil yang ada + `TIDAK KETEMU` untuk sisanya.

## Status INTEL

- **COMPLETE** — hanya bila **semua 9 butir** `DITEMUKAN` (atau `TIDAK ADA` dengan sumber).
- **PARTIAL** — bila ada satu saja `TIDAK KETEMU`. Wajib disertai **tabel Catatan Ketiadaan**.

Tabel Catatan Ketiadaan: satu baris per butir yang tidak lengkap, berisi status + alasan + sumber yang dicoba + dampak bila tak ditemukan.

## Pin (A5)

INTEL dikunci dengan pin: **commit + blok referensi + stage**. Kanonik read-only selama audit.

- Commit yang dipin di run dari-0 = **HEAD saat penemuan** (hasil `git rev-parse`, bukan `main`/`latest`).
- **Blok referensi ditentukan di Tahap B** (sensus live B7) — di Tahap A tulis `belum ditetapkan`.
- Bila Tahap B/D menemukan INTEL salah, koreksi **dicatat eksplisit dan terbuka**, tidak diam-diam ditimpa.

## Cara membuktikan URL hidup (tanpa keluar dari Tahap A)

Cukup cek murah, satu perintah per URL, dan catat hasilnya di `A02`:

```bash
curl -sIL -o /dev/null -w '%{http_code}' <url>     # 200 / 30x = hidup
```

Simpan **semua** kode status apa adanya (termasuk 403/429) — itu bukti, bukan kegagalan.

## Definition of done Tahap A

- [ ] `INTEL.md` memuat 9 butir, tiap butir berstatus
- [ ] stage dan repo keduanya `DITEMUKAN` (bila tidak → berhenti + eskalasi, bukan lanjut)
- [ ] pin commit tercatat sebagai hash nyata; blok referensi ditandai `belum ditetapkan`
- [ ] `A02` memuat tangga per butir + kode HTTP tiap URL + daftar docs Pre-0
- [ ] nol `cast`/cek onchain di Tahap A
- [ ] nol hipotesis kerentanan di INTEL
