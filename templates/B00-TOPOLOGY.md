# B00-TOPOLOGY — Profil Topologi (moneyflow v2.1, B0)

Proyek: `<nama>` · Repo: `<repo> @ <commit>` · Tanggal: `<ISO-8601>`

Dijalankan **setelah B13 scope lock, sebelum katalog Stream B04**.

## 1. Hitungan mekanis

| Hitungan | Jumlah | Daftar |
| :--- | :--- | :--- |
| `DOM-x` Domain eksekusi | | `DOM-1` dan seterusnya |
| `VK-x` Varian kode | | `VK-1` dan seterusnya (berkas/kontrak override per domain/versi) |
| `VC-x` Varian konfigurasi | | `VC-1` dan seterusnya (instance parameter beda dari kode sama) |

Kelas aset yang diterima (isi per `VC-x`): `native` / `wrapped-native` / `ERC-20 standar` / `fee-on-transfer` / `rebasing` / `hook-callback token` / `desimal non-18`.

## 2. Mode terpilih

| Field | Isi |
| :--- | :--- |
| Mode | `TUNGGAL` \| `TUNGGAL-BERINSTANS` \| `MULTI-DOMAIN` |
| Syarat yang terpenuhi | `<DOM/VK/VC vs tabel B0>` |
| Alasan (bila dinaikkan) | `<alasan tercatat; penurunan di bawah hasil hitungan DILARANG>` |

Bentuk pemecahan: `TUNGGAL` = Lintasan = Stream (pecah per fase bila lewat anggaran B19) · `TUNGGAL-BERINSTANS` = Stream x anggota representatif + Tabel Selisih (B20) · `MULTI-DOMAIN` = Stream pengguna x domain representatif + Stream lintas-domain per keluarga transport + Tabel Selisih per keluarga.

## 3. Matriks Domain (WAJIB bila `MULTI-DOMAIN`)

| Domain | Chain/VM | ChainId | Blok pin | Kontrak inti + alamat | Autentikasi pesan masuk | Transport keluar/masuk | Kelas aset dirutekan | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `DOM-1` | | | | | alias / messenger / `crossChainSender` / oracle | | | `LIVE` / `DEAD-CONFIG` / `UNVERIFIED` |

Status dibaca **di domain itu sendiri** (B7), bukan disimpulkan dari rantai utama. Domain representatif = satu per keluarga transport/autentikasi; sisanya masuk Tabel Selisih.

## 4. Katalog Ingress `IN-x` (B17)

| `IN_ID` | Kelas | Value_Holder | Pintu (fungsi:baris atau "transfer langsung") | Pembaca akuntansi (fungsi:baris) | Lintasan pengikat | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `IN-1` | `USER` | | | | | `BELUM_TERIKAT` / `TERIKAT_DI_<LINTASAN>` |
| `IN-2` | `ACTOR` | | | | | |
| `IN-3` | `CALLBACK` | | | | | |
| `IN-4` | `PASSIVE` | | | | | |
| `IN-5` | `ACCRUAL` | | | | | |
| `IN-6` | `ADMIN` | | | | | |

Aturan ikat: `IN-x` terikat ke **Lintasan yang membaca efeknya** (bukan penulisnya). `PASSIVE`/`ACCRUAL` → Lintasan yang rumusnya membaca saldo/waktu. `ADMIN` boleh diikat ke Lintasan admin dan diprioritaskan terakhir. `check-final` menolak sisa `BELUM_TERIKAT` pada `CORE-FLOW`.

## 5. Tabel Selisih Varian (B20 — wajib bila > 1 anggota per keluarga)

| Anggota | Fungsi override (jangkar) | Autentikasi | Jalur native/wrapped | Transport/route | Kelas aset diterima | Parameter live beda (LP-x) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| | | | | | | | `SAMA` / `BEDA:<kolom>` |

Baris `BEDA` yang menyentuh **nilai** atau **autentikasi** = wajib jadi kartu Tahap D (Twin-Path Differential otomatis).

## 6. Daftar Lintasan

| Lintasan | Stream | Domain | Ingress | Egress | Segmen | Penyeberangan (`HB-x`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STR-01.L1` | `STR-01` | `DOM-1` | | | `S1..Sn` | `HB-3 → STR-01.L2` |

Penamaan: `STR-nn` (Stream), `STR-nn.Lk` (Lintasan), `STR-nn.Lk.Sj` (segmen). Satu sesi kerja = satu Lintasan.

## 7. Perubahan profil (riwayat)

| Tanggal | Perubahan | Alasan | Dampak pemecahan |
| :--- | :--- | :--- | :--- |
| | | | |
