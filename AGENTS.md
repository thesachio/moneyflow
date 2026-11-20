# AGENTS — Konstitusi Operasional Flow Money First (moneyflow v2.0 — Lapis Konstitusi)

## 0. Bootloader (keras)

Sebelum kerja apa pun, baca `SOUL.md` dan `methodology/aturan-alur-first.md` sampai paham. Berkas aturan kanonik adalah sumber kebenaran metode; bila berkas lain (termasuk berkas ini) berbeda dengannya, berkas aturan yang berlaku. Preferensi mengikat ada di `methodology/resume-aturan-preferensi-alur-first.md` (ringkasan) — yang mengikat tetap berkas aturan.

Repo ini adalah MESIN/METODE, bukan proyek audit. Tidak memuat kode kontrak target dan tidak memuat temuan. Dipakai dengan cara disalin ke folder kerja audit baru, lalu dijalankan tahap demi tahap.

## 1. Tahap A–G

| Tahap | Nama | Output | Batas |
| :--- | :--- | :--- | :--- |
| A | INTEL | `A01-INTEL` (brief 9 butir), `A02-INTEL-discovery` | Brief saja (A1–A5); tanpa cek onchain |
| B | Mapping | `B01-SCOPE`, `B02-CENSUS-STATIC`, `B03-CENSUS-LIVE`, `B04-CLUSTERS` (klasifikasi 4 tipe), `B05-LEDGER-SISA`, `B06-REGISTRY-INVARIANT`, `B07-STATE-BRIDGES` | Tanpa invariant, tanpa pemetaan mendalam, tanpa buruan/PoC/verdict |
| C | Pemetaan mendalam per klaster (rolling per-Stream) | `C00-SHARED-PRIMITIVES` (sekali di awal), `C<NN>-STREAM-INVENTORY` | Deskriptif saja; tanpa invariant/buruan/PoC/verdict; Aturan Koridor Stream (`Corridor-Bound Cross-Cluster`) |
| D | Eksplorasi | Kartu lead + invariant (`INV-Sx/Hx/Jx/Fx` + `INV-HBx` State-Bridge) | Per-Stream, dua gelombang (buta → berpengetahuan + katalog); tanpa PoC; koridor + `1-hop peek`; **dua mode eksekusi: `MODE: AUTO` (default, otonom penuh per Stream) dan `MODE: PAIR` (co-audit kolaboratif fungsi demi fungsi bersama peneliti manusia — hanya bila user eksplisit meminta; sorotan titik sensitif + panduan cek invariant per segmen + pelestarian temuan `[USER-INSIGHT]`)** |
| E | Uji test | PoC fork-live + P&L per kandidat | Fork blok pin; P&L terukur; batch maks 3; plafon dua mode (`Observed Live Ceiling` / `Proven Potential Ceiling`) |
| F | Komposisi Inkremental & Akhir | Lemma dari data terbaru (tanpa fork/PoC ulang) | Inkremental segera setelah E bila Stream berbagi `State-Bridge` (`B07`)/brankas; lintas-Stream akhir di penutupan |
| G | Verdict | Verdict 06/07/08/09 per kandidat + distribusi akhir | Tiga verdict terpisah |

Rolling per-Stream (moneyflow v2.0, B2a-v2): C → D → E per-Stream; klaster = papan kontrol kelengkapan Tahap B, bukan pagar. Tahap F komposisi inkremental + Tahap G di akhir. **Lapis 1 — urutan antar-Stream = pintu masuk pertama kali (B2a, diputus 17 Nov 2026): entrypoint paling awal yang dilalui pengguna, BUKAN EV. Lapis 2 — urutan kartu dalam-Stream = bobot struktural: P1 konservasi (`INV-Jx`/`INV-Fx`) → P2 handoff/state-bridge (`INV-Hx`/`INV-HBx`) → P3 anomali segmen (`INV-Sx`, S1→Sn); anti-kuota mutlak sampai `QUEUED == 0` dan `ACTIVE == 0`.** Deep-run per jalur (diputus 22:33 WIB 16 Nov 2026): satu perintah berdiri hulu→hilir sampai verdict per lead, tanpa tap antar langkah; berlaku mulai jalur berikut (P4). Acuan kerja Tahap B: `methodology/acuan-workflow-tahap-B.md`. Aturan hemat Fase D + prinsip efisiensi + lantai bawah: `methodology/rancangan-hemat-fase-d.md`.

## 2. Delegasi (keras)

- Brief berdiri sendiri: tiap brief delegasi membawa semua konteks yang dibutuhkannya (identifikasi, jangkar, batasan) — subagent tidak mewarisi konteks parent.
- Sekuensial: satu anak aktif per antrean. Koordinator memverifikasi verdict dari berkas bukti sebelum menerapkannya ke antrean bersama; subagent tidak menulis antrean bersama secara langsung.
- Induk satu-satunya penulis berkas kanonik + ledger sisa.
- Brief Tahap E memakai bahasa verifikasi invariant, bukan bahasa serangan.
- Verifikasi parent atas bukti penentu wajib jalan (jangkar, angka, rerun forge) — ini lantai bawah, tidak boleh dipangkas.
- Penolakan safety classifier TIDAK boleh diulang, diparafrase, atau diputar lewat jalur lain. Pivot saja.
- Verifikasi jangkar: periksa FUNGSI-nya lewat `grep -n`, bukan hanya barisnya. Baris yang ada ≠ jangkar yang benar. Rantai koreksi bukan bukti — tiap langkah berikut wajib memeriksa ulang jangkar yang dikoreksi dari kode bernomor.
- **Stream Context Capsule (moneyflow v2.0, keras):** brief delegasi subagent Tahap C/D/E hanya boleh menyertakan konteks yang terikat pada Stream aktif — `C00-SHARED-PRIMITIVES.md`, `C<NN>-STREAM-INVENTORY.md` beserta potongan kode bernomor `File:Lxx-Lyy` pada koridor stream tersebut, baris relevan dari `B07-STATE-BRIDGES.md`, maksimal 1 ringkasan tabel Handoff/Simpul dari stream kembar (*twin-path*) bila relevan, serta (khusus Tahap D Gelombang 2) maksimal 2–4 berkas plugin katalog yang cocok dengan gejala kode. Dilarang meneruskan riwayat percakapan panjang atau berkas stream lain yang tidak bersinggungan.
- Lantai bawah tetap utuh: baca kode manual penuh saat sensus, uji fork blok pin, kontrol positif untuk setiap hasil nol, rerun forge oleh parent dengan kecocokan gas identik, tiga verdict terpisah, bahasa brief berbasis verifikasi invariant, aturan `HOLD` dan `/stop`.

## 3. Gerbang (keras)

- B13 scope lock sebelum sensus: daftar berkas cocok persis inventaris kanonik (diff kosong), commit terverifikasi.
- B8 live-match diulang di awal fase uji per Stream, sebelum PoC. Tidak live-match → TUNDA-LIVE (tercatat di ledger, nol waktu eksekusi). Cara kerja B8 (17 Nov 2026, mengikat): utamakan alur + cek desain kode dulu; pindai log tx = verifikator TERAKHIR saja (Tahap G / sapuan akhir), bukan cara kerja B8.
- Gate finansial C10-v2 (moneyflow v2.0, diputus 18 Nov 2026) — **Gate D (sebelum PoC, statis):** jalur pemicu permissionless (akun publik biasa tanpa peran istimewa owner/admin/governance/whitelist; bot/keeper/relayer publik yang memproses input pengguna sesuai operasi normal tetap sah; "keanehan" susunan transaksi bukan alasan gugur) + state prasyarat reachable lewat transaksi normal di atas kode+state blok pin (tanpa `vm.store`) + kontrak lulus B8 live-match + rumus plafon potensial ≥ $1 terdefinisi. **Gate E (eksekusi PoC):** mekanisme + angka P&L aktual di fork blok pin; plafon dua mode — `Observed Live Ceiling` (saldo live > 0) atau `Proven Potential Ceiling` (saldo live 0 tapi kontrak terbuka menerima aktivitas normal → simulasi aktivitas korban sah lewat entrypoint normal lebih dulu, lalu eksekusi akun penguji tanpa hak istimewa; ≥ $1). `DORMAN` HANYA bila jalur diblokir keras saklar konfigurasi admin aktif (`paused == true`, `cap == 0` terkunci, modul belum terdaftar) + syarat buka-ulang konkret.
- **Live-Match & pegangan bukti (revisi 20 Nov 2026, mengikat):**
  - R1. Tujuan utama: setiap hasil eksplorasi dibuktikan lewat uji di fork lokal yang sejalan dengan keadaan live. Hasilnya harus bisa direproduksi oleh pengembang asli, sehingga mereka bisa melihat sendiri bahwa aksinya benar-benar terjadi bila dieksekusi.
  - R2. Celah yang sudah diperbaiki di HEAD atau di commit mana pun ditandai `FIXED_IN_HEAD` dan masuk ke 08, karena berisiko menjadi laporan duplikat. Turunan dari R1: bug yang hanya ada di kode HEAD yang belum di-deploy tidak bisa direproduksi di live. Masukkan ke 08 dengan kelas `PRE_LIVE_SCOPE`.
  - **Definisi live-match (4 syarat, semuanya wajib terpenuhi):**
    - **L1 Kode** — tetapkan sumber deployed untuk setiap kontrak koridor pada blok pin; untuk proxy, baca implementasinya dari slot EIP-1967 pada blok pin. Bandingkan per fungsi koridor: sumber ter-verifikasi di explorer dibandingkan HEAD — hasil `KORIDOR_SAMA` atau `KORIDOR_BEDA:<fungsi>`. Bytecode hanya bukti pendukung kalau cocok; bytecode berbeda tidak boleh jadi alasan menolak (VERDICT #2b). Sumber tidak ter-verifikasi → tulis `KORIDOR_TIDAK_TERBUKTI`, lalu uji langsung di alamat live.
    - **L2 Config** — setiap field ADMIN-CONFIG dibaca dari storage pada blok pin sesuai Lembar Parameter LP-x; cabang yang dimatikan config live → `DEAD-CONFIG` → `DORMAN`.
    - **L3 Payload** — CALLER-INPUT harus dalam bentuk dan batas yang diterima kontrak live; sertakan 3–5 contoh transaksi nyata per entrypoint sebagai acuan.
    - **L4 Target** — uji dijalankan terhadap alamat deployed, di fork pada blok pin.
  - Simpan hasil per Stream ke `audit/notes/live-match-<STREAM>.md` dengan kolom: chain, fork_block, alamat proxy, alamat impl@pin, sumber_deployed, status koridor per fungsi, LP-x terbaca.
- Batch Tahap E maksimal 3 kartu.
- B10: round selesai hanya bila ledger sisa menyusut. Target buruan harus ada di sensus.

## 4. Preferensi mengikat (C1–C11, ringkas — lengkapnya di berkas aturan)

C1 fork-live. C2 kejujuran bukti (DIEKSEKUSI vs DIANALISIS vs CODE-REVIEW-ONLY). C3 verify_zero_and_scan. C4 ambang $1 bukan ambang batas. C5 HOLD — nol submisi/kontak program/draf tanpa persetujuan eksplisit per kandidat. C6 tiga verdict terpisah; severity dari plafon teramati; insidensi same-tx. C7 bahasa Indonesia ringan dan sederhana. C8 keep-hunting. C9 /stop mencabut otorisasi round seketika. C10-v2 Permissionless & Reachable Potential Ceiling (moneyflow v2.0): pemicu permissionless + state reachable (blok pin, tanpa `vm.store`) + plafon potensial ≥ $1 dengan dua mode (`Observed Live Ceiling` / `Proven Potential Ceiling`); Gate D statis terpisah dari Gate E; DORMAN = blokir konfigurasi admin aktif saja; TIDAK harus live. C11 TERBUKTI = cukup jalur pendek saling bergantung dari pelanggaran invariant ke kerugian terukur; tes yang berhenti di satu fungsi pendek = masih HIPOTESIS.

## 5. Lantai bawah + hemat

Lantai bawah: baca kode, ukur live, verifikasi parent atas bukti penentu. Yang jangan dipangkas: bukti fork live, pemeriksaan parent atas bukti penentu, sensus 100%, jangan saring di HEAD dulu. Hemat yang diizinkan: satu fork per wilayah dipakai ulang, deploy_parity sekali + cache, satu harness dua mode, triase fork-testability di awal, pipeline (bukan paralel buta), cek mesin otomatis, pre-check murah sebelum gate. Prinsip efisiensi: bila satu tes penentu sudah bisa mengonfirmasi, jangan jalankan pindai sejarah panjang dulu — pindai hanya konteks pendukung, dibatasi atau lewat indexer.

## 6. Yang belum ada di repo ini (terbuka, bukan rule)

- Skill per Tahap A–G + autopilot SUDAH DITULIS (22:39 WIB 16 Nov 2026): `skills/flow-a-intel/`, `flow-b-map/`, `flow-c-inventory/`, `flow-d-explore/`, `flow-e-test/`, `flow-f-compose/`, `flow-g-verdict/`, `flow-autopilot/`. Autopilot ditulis ulang 22:47 WIB 16 Nov 2026 menjadi full-autopilot proyek penuh (semua klaster, semua jalur) — versi pertama hanya satu jalur. Skill `sc-*` theadvers sengaja TIDAK disalin — skill itu mengkodekan STAGE-0 + A–F Segitiga. Lihat `skills/README.md`. Skill pintu masuk `skills/flow-money-first/SKILL.md` SUDAH ADA.
- `tools/verify_flow.py` = verifier format artefak A–G (metode aktif). [ARSIP RIWAYAT PILOT] Pemeriksa era Segitiga sengaja TIDAK disalin — terikat format Segitiga.
- Inventory per-alur (Tahap C) — dievaluasi, tidak diadopsi; bisa dibuka lagi. Cara parser independen sapuan akhir (B9) — terbuka sebagai riset.
- Katalog 52 plugin (`references/` + `methodology/attack-forms/` + `methodology/domains/`) diwarisi utuh dari theadvers dan tumbuh dari hasil jelajah (temuan di luar katalog = kandidat plugin baru).
