# AGENTS — Konstitusi Operasional Flow Money First (moneyflow v2.0 — Lapis Konstitusi)

## 0. Bootloader (keras)

Sebelum kerja apa pun, baca `SOUL.md` dan `methodology/aturan-alur-first.md` sampai paham. Berkas aturan kanonik adalah sumber kebenaran metode; bila berkas lain (termasuk berkas ini) berbeda dengannya, berkas aturan yang berlaku. Preferensi mengikat ada di `methodology/resume-aturan-preferensi-alur-first.md` (ringkasan) — yang mengikat tetap berkas aturan.

Repo ini adalah MESIN/METODE, bukan proyek audit. Tidak memuat kode kontrak target dan tidak memuat temuan. Dipakai dengan cara disalin ke folder kerja audit baru, lalu dijalankan tahap demi tahap.

## 1. Tahap A–G

| Tahap | Nama | Output | Batas |
| :--- | :--- | :--- | :--- |
| A | INTEL | `A01-INTEL` (brief 9 butir), `A02-INTEL-discovery` | Brief saja (A1–A5); tanpa cek onchain |
| B | Mapping | `B00-TOPOLOGY`, `B01-SCOPE`, `B02-CENSUS-STATIC`, `B03-CENSUS-LIVE` (kolom `domain` wajib), `B04-STREAMS-AND-CLUSTERS` (klaster 4 tipe + katalog Stream/Lintasan + Katalog Ingress `IN-x`), `B05-LEDGER-SISA` (3 populasi), `B06-REGISTRY-INVARIANT`, `B07-STATE-BRIDGES` | Tanpa invariant, tanpa pemetaan mendalam, tanpa buruan/PoC/verdict; AST boleh untuk lokalisasi (B6-v2) |
| C | Stream-Slice Inventory (rolling per-Lintasan) | `C00-SHARED-PRIMITIVES` (sekali), `C<NN>-<STR>-<Lk>-INVENTORY` | Deskriptif saja; koridor (`Corridor-Bound Cross-Cluster`); segmen menurut 5 pemicu B19; `CY-x`, Ingress `S0`, Tabel Selisih, LP-x per domain |
| D | Eksplorasi | Kartu lead + invariant (`INV-Sx/Hx/HBx/Jx/Fx` + `INV-CYx` serah kendali + `INV-Vx` selisih varian) | Per-Lintasan; dua gelombang; gerbang ≥1 kartu atau `NIHIL_KANDIDAT`; mode `AUTO`/`PAIR` tetap |
| E | Uji test | PoC fork-live + P&L per kandidat | Fork blok pin; P&L terukur; batch maks 3; plafon dua mode (`Observed Live Ceiling` / `Proven Potential Ceiling`) |
| F | Komposisi Inkremental & Akhir | Lemma dari data terbaru (tanpa fork/PoC ulang) | Inkremental segera setelah E bila Stream berbagi `State-Bridge` (`B07`)/brankas; lintas-Stream akhir di penutupan |
| G | Verdict | Verdict 06/07/08/09 per kandidat + distribusi akhir | Tiga verdict terpisah |

Rolling per-Lintasan (moneyflow v2.1, B19): C → B8 → D → E per Lintasan; Lintasan dalam satu Stream dikerjakan berurutan; klaster = papan kontrol kelengkapan Tahap B, bukan pagar. Mode topologi (B0) menentukan bentuk pemecahan; rule sama untuk semua proyek. **Lapis 1 — urutan antar-Lintasan = pintu masuk pertama kali (B2a, diputus 17 Nov 2026): entrypoint paling awal yang dilalui pengguna, BUKAN EV. Lapis 2 — urutan kartu dalam-Lintasan = bobot struktural: P1 konservasi (`INV-Jx`/`INV-Fx`) → P2 handoff/state-bridge (`INV-Hx`/`INV-HBx`) → P3 anomali segmen (`INV-Sx`, S1→Sn); anti-kuota mutlak sampai `QUEUED == 0` dan `ACTIVE == 0`.** Deep-run per jalur (diputus 22:33 WIB 16 Nov 2026): satu perintah berdiri hulu→hilir sampai verdict per lead, tanpa tap antar langkah; berlaku mulai jalur berikut (P4). Acuan kerja Tahap B: `methodology/acuan-workflow-tahap-B.md`. Aturan hemat Fase D + prinsip efisiensi + lantai bawah: `methodology/rancangan-hemat-fase-d.md`.

## 2. Delegasi (keras)

- Brief berdiri sendiri: tiap brief delegasi membawa semua konteks yang dibutuhkannya (identifikasi, jangkar, batasan) — subagent tidak mewarisi konteks parent.
- Sekuensial: satu anak aktif per antrean. Koordinator memverifikasi verdict dari berkas bukti sebelum menerapkannya ke antrean bersama; subagent tidak menulis antrean bersama secara langsung.
- Induk satu-satunya penulis berkas kanonik + ledger sisa.
- Brief Tahap E memakai bahasa verifikasi invariant, bukan bahasa serangan.
- Verifikasi parent atas bukti penentu wajib jalan (jangkar, angka, rerun forge) — ini lantai bawah, tidak boleh dipangkas.
- Penolakan safety classifier TIDAK boleh diulang, diparafrase, atau diputar lewat jalur lain. Pivot saja.
- Verifikasi jangkar: periksa FUNGSI-nya lewat `grep -n`, bukan hanya barisnya. Baris yang ada ≠ jangkar yang benar. Rantai koreksi bukan bukti — tiap langkah berikut wajib memeriksa ulang jangkar yang dikoreksi dari kode bernomor.
- **Stream Context Capsule (moneyflow v2.1, keras):** brief delegasi subagent Tahap C/D/E hanya boleh menyertakan konteks yang terikat pada **Lintasan aktif** — `C00-SHARED-PRIMITIVES.md`, `C<NN>-<STR>-<Lk>-INVENTORY.md` (termasuk Tabel Selisih + baris `B00` domain terkait) beserta potongan kode bernomor `File:Lxx-Lyy` pada koridor Lintasan tersebut, baris relevan dari `B07-STATE-BRIDGES.md`, maksimal 1 ringkasan tabel Handoff/Simpul dari Lintasan kembar (*twin-path*) bila relevan, serta (khusus Tahap D Gelombang 2) maksimal 2–4 berkas plugin katalog yang cocok dengan gejala kode. Dilarang meneruskan riwayat percakapan panjang atau berkas Lintasan lain yang tidak bersinggungan.
- Lantai bawah tetap utuh: baca badan fungsi penuh saat sensus (AST hanya alat bantu, B6-v2), uji fork blok pin, kontrol positif untuk setiap hasil nol, rerun forge oleh parent dengan kecocokan gas identik, tiga verdict terpisah, bahasa brief berbasis verifikasi invariant, aturan `HOLD` dan `/stop`.

## 3. Gerbang (keras)

- **B0 profil topologi sebelum sensus (v2.1):** `B00-TOPOLOGY.md` wajib ada: hitungan `DOM-x`/`VK-x`/`VC-x` + mode (`TUNGGAL`/`TUNGGAL-BERINSTANS`/`MULTI-DOMAIN`) + Matriks Domain (bila MULTI-DOMAIN). Tanpa itu sensus belum sah.
- **B22 dua larangan (v2.1):** LP-x dibaca pada domain tempat kontrak koridor hidup (bukan hanya rantai utama); DILARANG membuat Stream "sisa/admin/misc" — setiap Stream wajib punya Ingress + Egress bernama + rumus plafon.
- **B17 ingress (v2.1):** enam kelas `IN-x` (`USER`/`ACTOR`/`CALLBACK`/`PASSIVE`/`ACCRUAL`/`ADMIN`) dicatat di `B04` Bagian 2b; tiap baris terikat ke Lintasan yang **membaca** efeknya; `check-final` menolak sisa `BELUM_TERIKAT`.
- **B0 Profil Topologi wajib ada sebelum katalog Stream**; mode tidak boleh di bawah hasil hitungan mekanis (`DOM-x`/`VK-x`/`VC-x`).
- **Gate D (v2.1) menambah:** `LP-x` pengendali nilai tidak boleh `UNVERIFIED`; Lintasan ≥ 1 kartu atau `NIHIL_KANDIDAT`.
- B13 scope lock sebelum sensus: daftar berkas cocok persis inventaris kanonik (diff kosong), commit terverifikasi.
- **B8 Live-Match Lintasan — dijalankan di awal Tahap D, wajib lulus sebelum Gate D** (per domain eksekusi segmen, B21). Tidak live-match → TUNDA-LIVE (tercatat di ledger, nol waktu eksekusi). Cara kerja B8 (17 Nov 2026, mengikat): utamakan alur + cek desain kode dulu; pindai log tx = verifikator TERAKHIR saja (Tahap G / sapuan akhir), bukan cara kerja B8.
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
- `tools/verify_flow.py` = verifier format artefak A–G (metode aktif), termasuk `check-b0` (profil topologi).
- Katalog 52 plugin (`references/` + `methodology/attack-forms/` + `methodology/domains/`) diwarisi utuh dari theadvers dan tumbuh dari hasil jelajah (temuan di luar katalog = kandidat plugin baru).
