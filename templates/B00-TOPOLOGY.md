# B00-TOPOLOGY — Profil Topologi (moneyflow v2.1, B0)

Proyek: `<nama>` · Repo: `<repo> @ <commit>` · Tanggal: `<ISO-8601>`

## 1. Mode terpilih

| Field | Isi |
| :--- | :--- |
| Mode | `TUNGGAL` \| `BERINSTANS` \| `MULTI-DOMAIN` |
| Alasan | `<fakta deployment yang memicu mode>` |
| Bukti | `<INTEL baris / deployments/File:Baris / B03 baris>` |

## 2. Domain (chain/VM/lingkup)

| Domain_ID | Chain/VM | ChainId | Blok referensi | Peran domain | Bukti |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `D1` | | | | `inti` / `turunan` / `luar-scope` | |

## 3. Instans per peran

| Peran | Jumlah instans | Alamat (ringkas) | Domain | Catatan varian |
| :--- | :--- | :--- | :--- | :--- |
| | | | | |

> Wajib bila mode `BERINSTANS`: isi §5 Tabel Selisih Varian.

## 4. Katalog Ingress `IN-x` (B17)

| ID | Kelas | Status | Bukti (`File:Baris`) atau alasan kode |
| :-- | :--- | :--- | :--- |
| `IN-1` | Donasi/force-feed native | `ADA` / `TIDAK ADA` | |
| `IN-2` | Token masuk langsung (transfer pihak ketiga, rebase, yield) | | |
| `IN-3` | Callback/hook eksternal (ERC-777/1363/1155, bridge, flash-loan) | | |
| `IN-4` | Keeper/relayer/bot publik (`poke`/`sync`/`harvest`/`update`) | | |
| `IN-5` | Urutan/insidensi same-block (sandwich, first/last depositor, JIT) | | |
| `IN-6` | Klaim/pre-mint eksternal (airdrop, merkelless claim, unlock vesting) | | |

Aturan: kelas `ADA` wajib punya unit penutup di `B05-LEDGER-SISA.md`; kelas `TIDAK ADA` wajib menyebut alasan kode (bukan "tidak terlihat").

## 5. Tabel Selisih Varian (B21 — wajib bila `BERINSTANS`)

| Varian/Instans | Alamat | Perbedaan kode (`File:Baris`) | Perbedaan konfigurasi | Perbedaan satuan | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| | | | | | `SAMA` / `BEDA-KODE:<fungsi>` / `BEDA-KONFIG:<field>` / `TIDAK-DIBACA` |

Aturan: minimal satu instans diperiksa penuh; `TIDAK-DIBACA` pada instans yang dipakai PoC = PoC tidak sah; "berlaku untuk semua instans" dilarang tanpa tabel terisi.

## 6. Daftar Lintasan (B20 — wajib bila `MULTI-DOMAIN`)

| Lintasan | Stream | Domain | Ingress | Egress | Segmen | Penyeberangan (`HB-x`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `LINT-01` | `STR-01` | `D1` | | | `S1..Sn` | `HB-3 → LINT-02` |

Aturan: satu Lintasan = satu domain; wajib punya Ingress + Egress bernama; urutan = urutan penyeberangan.

## 7. Perubahan profil (riwayat)

| Tanggal | Perubahan | Alasan | Dampak pemecahan |
| :--- | :--- | :--- | :--- |
| | | | |
