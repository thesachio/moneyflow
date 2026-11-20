---
name: flow-money-first
description: Pintu masuk metode Flow Money First — audit smart contract yang mempartisi berdasarkan aliran uang, bukan wadah berkas. Memuat bootloader, peta tahap A–G dengan batas tiap tahap, gerbang keras, aturan katalog, dan protokol delegasi. Dipakai bila user menyebut flow money first / alur-first, meminta audit Tahap A–G, atau memulai proyek audit baru dengan metode ini.
---

# flow-money-first — Pintu masuk metode

Audit keamanan smart contract yang mempartisi pekerjaan berdasarkan **aliran uang**, bukan wadahnya (berkas).

**Unit kerja = satu Stream — aliran nilai ujung-ke-ujung** (`Ingress` → `State/Share Accounting` → `Egress`). Tiap Stream menurut urutan `B2a` / `B2a-v2`; klaster = papan kontrol cakupan Tahap B (moneyflow v2.0 — Lapis Konstitusi). Diburu per segmen dan handoff, dibuktikan di fork blok pin dengan P&L terukur.

Skill ini adalah **peta dan aturan gerbang**. Kerja tiap tahap mengikuti skill tahapnya (`flow-a-intel` sampai `flow-g-verdict`), bukan berkas ini.

## Bootloader — baca sebelum kerja apa pun

| # | Berkas | Kenapa |
| :-: | :--- | :--- |
| 1 | `SOUL.md` | identitas + hukum kognitif + lantai bawah (versi flow) |
| 2 | `methodology/aturan-alur-first.md` | **aturan kanonik** A1–A5, B1–B16, C1–C11, Tahap C–G |
| 3 | `methodology/resume-aturan-preferensi-alur-first.md` | ringkasan preferensi mengikat |
| 4 | `methodology/acuan-workflow-tahap-B.md` | bila mengerjakan Tahap B (detail terdalam) |
| 5 | `methodology/rancangan-hemat-fase-d.md` | bila mengerjakan D/E (aturan hemat + lantai bawah) |
| 6 | `AGENTS.md` | konstitusi operasional: delegasi, gerbang |

**Hirarki bila berbeda:** skill tahap memuat aturan yang dibutuhkan untuk menjalankannya. Bila skill berbeda dengan `aturan-alur-first.md`, **berkas aturan yang berlaku** — dan skill itu wajib diperbaiki, bukan diabaikan.

`SOUL.md` / `AGENTS.md` di root repo ini adalah **versi flow**. Versi Segitiga diarsipkan di `archive/segitiga-v2/` — **bukan** metode aktif, jangan dipakai untuk proyek baru.

## Peta tahap A–G dan batas kerasnya

| Tahap | Nama | Keluaran | Batas keras (jangan dilanggar) |
| :-: | :--- | :--- | :--- |
| **A** | INTEL | `INTEL.md`, `A01-INTEL.md`, `A02-INTEL-discovery.md` | brief 9 butir saja; **tanpa cek onchain**; blok referensi belum ditetapkan |
| **B** | Mapping | `B01`–`B07` (`B04-STREAMS-AND-CLUSTERS` + `B07-STATE-BRIDGES`) + `scripts/out/*.jsonl` | tanpa invariant, tanpa pemetaan mendalam, tanpa buruan/PoC/verdict |
| **C** | Stream-Slice Inventory per-Lintasan | `C00-SHARED-PRIMITIVES.md` (sekali di depan) + `C<NN>-<STR>-<Lk>-INVENTORY.md` per-Stream | deskriptif saja; **`Corridor-Bound Cross-Cluster`** (wajib menembus batas klaster sepanjang koridor aliran dana aktif; dilarang melebar horizontal ke cabang luar stream; jeda asinkron dicatat ke `B07-STATE-BRIDGES.md`); tanpa invariant/buruan/PoC |
| **D** | Eksplorasi per-Stream | `D<nn>-<TOPIK>-WAVE1/WAVE2/LEAD-CARDS` | Gelombang 1 bebas/buta katalog (3 Lensa Fisika Nilai + Twin-Path Diff); Gelombang 2 = **Symptom-Triggered Lazy Skill Loading** (maks 2–4 plugin relevan) + `1-hop peek` pada `State-Bridge`; tanpa PoC; gelombang 1/2 **tidak** memberi TERBUKTI; **dua mode eksekusi: `MODE: AUTO` (default — otonom penuh per Stream, dipakai flow-autopilot) dan `MODE: PAIR` (co-audit kolaboratif fungsi demi fungsi bersama peneliti manusia — hanya bila user eksplisit meminta `pair`/`bareng`/`co-audit`/`interaktif`/`pandu per fungsi`; sorotan titik sensitif + panduan cek invariant per segmen + pelestarian temuan `[USER-INSIGHT]`)** |
| **E** | Uji test | `E<nn>-<TOPIK>-BATCH<n>-PROOF.md` + `poc/` | satu fork blok pin + pustaka kumulatif transaksi normal; batch maks 3 kartu diurutkan bobot struktural (**Simpul/Komposisi > Handoff/State-Bridge > Segmen Lokal**); mengukur `Observed Live Ceiling` atau `Proven Potential Ceiling`; parent rerun forge |
| **F** | Komposisi Inkremental & Akhir | `F<nn>-<TOPIK>-COMPOSITION.md` | Inkremental: langsung jalan begitu Stream aktif menyentuh `State-Bridge`/brankas Stream sebelumnya; sapuan komposisi akhir bila multi-stream; **tanpa fork/PoC ulang** |
| **G** | Verdict | `G01-VERDICT.md` + draf 09 | tiga verdict terpisah; severity dari plafon teramati; **HOLD** |

**Rolling vertikal per Stream** (moneyflow v2.0, B2a-v2): setelah Tahap B selesai + `C00-SHARED-PRIMITIVES.md` dipetakan sekali di awal, siklus berjalan per satu Stream — `C (Stream Inventory) → B8 (Live-Match Stream) → D (Dual-Wave Stream Hunt) → E (Shared-State Proof) → F (Incremental Composition bila bersinggungan) → G (Triage Kartu Stream)`; Tahap G akhir memutakhirkan wadah 06/07/08/09.

**Satu Stream diselesaikan dulu (anti-kuota mutlak).** Dilarang menyentuh Stream berikut selama Stream aktif masih punya `QUEUED > 0` atau `ACTIVE > 0`.

## Gerbang keras (tidak boleh dilewati)

1. **B13 — scope lock sebelum sensus.** Daftar berkas cocok **persis** inventaris kanonik (diff kosong), commit terverifikasi, `contracts/` bersih.
2. **B8 — live-match per Stream sebelum PoC.** Tidak live-match → wadah `TUNDA-LIVE` (tercatat di ledger, **nol waktu eksekusi**). Tanpa B8, PoC Stream itu **terblokir**.
3. **Gate finansial C10-v2 (Permissionless & Reachable Potential Ceiling, moneyflow v2.0).** Syarat kandidat sah naik D → E dan layak 09 bila terbukti di E: **Permissionless + Reachable Action/State lewat operasi normal + Measurable Potential Ceiling ≥ $1**. Tegas terpisah: **Gate D = statis/desain** (verifikasi dari kode + bacaan state blok pin: pemicu permissionless, state reachable, B8 live-match, rumus plafon ≥ $1 terdefinisi); **Gate E = eksekusi fork** (PoC + P&L aktual). `DORMAN` HANYA bila jalur diblokir keras saklar konfigurasi admin aktif di live (`paused == true`, `cap == 0` terkunci, modul belum terdaftar) + syarat buka-ulang konkret.
4. **Batch E maksimal 3 kartu.**
5. **Lantai bawah — tidak boleh dipangkas:** baca kode, ukur live, verifikasi parent atas bukti penentu.
6. **HOLD.** Nol submisi / kontak program / draf kirim tanpa persetujuan eksplisit **per kandidat**. Tersimpan ≠ tersubmit.
7. **`/stop` mencabut otorisasi seketika.** Hentikan subagent, tulis nol berkas, lanjut hanya atas perintah eksplisit baru.
8. **B10 — ledger sisa.** Round selesai hanya bila sisa **menyusut**. Target buruan harus ada di sensus; kalau tidak, di luar scope menurut konstruksi.

## Katalog (basis pengetahuan) — aturan pakai

Katalog 52 plugin: `references/` (CHAIN 10 + M 10 + POV 15) + `methodology/attack-forms/` (AF 10) + `methodology/domains/` (DOM 7).

- **Gelombang 1 (buta): DILARANG membuka katalog** — termasuk `_ROUTER.md`.
- **Gelombang 2:** muat **hanya** plugin yang gejalanya cocok.
- Tidak ada yang cocok → `[NO-CATALOG]`. **Kandidat dilarang gugur hanya karena tidak cocok katalog.**
- Temuan di luar katalog = **kandidat plugin baru** (jangan batasi eksplorasi).

## Delegasi

- **Brief berdiri sendiri** — tiap brief membawa semua konteks yang dibutuhkan; subagent tidak mewarisi konteks parent.
- **Sekuensial** — satu anak aktif per antrean.
- **Stream Context Capsule (keras):** tiap brief delegasi subagent Tahap C/D/E wajib **mandiri, bersih dari riwayat chat**, dan hanya memuat artefak yang terikat Stream aktif — `C00-SHARED-PRIMITIVES.md`, inventaris koridor `C<NN>-<STR>-<Lk>-INVENTORY.md` berikut potongan kode bernomor `File:Lxx-Lyy`, baris relevan `B07-STATE-BRIDGES.md`, maks 1 tabel Twin-Path bila relevan, maks 2–4 plugin katalog (khusus Gelombang 2).
- **Induk satu-satunya penulis berkas kanonik + ledger sisa.** Subagent menulis **hanya** ke `notes/staging-<jalur>-<tahap>-<item>.md`, diawali `## STAGING MANIFEST` maks 16 baris.
- **Koordinator memverifikasi verdict dari berkas bukti** sebelum menerapkannya ke antrean bersama.
- **Brief Tahap E memakai bahasa verifikasi invariant**, bukan bahasa serangan.
- **Penolakan safety classifier tidak boleh diulang, diparafrase, atau diputar lewat jalur lain.** Pivot saja.
- **Verifikasi jangkar + pra-cek deterministik:** periksa **fungsinya** lewat `grep -n`, bukan hanya nomor baris. Jalankan pra-cek format staging **deterministik** (`tools/verify_flow.py` bila sudah tersedia + pemeriksaan fungsi via `grep -n`) — bukan pemeriksaan manual pembaca penuh. Baris yang ada ≠ jangkar yang benar. Rantai koreksi bukan bukti.

## Alur kerja yang benar (urutan operasional)

```
A  INTEL            → brief 9 butir + pin commit          (skill flow-a-intel)
B  Mapping          → scope lock → sensus 100% → live B7 → klaster 4 tipe
                      + katalog Stream + B07 → ledger → registry (flow-b-map)
   ↓ per-Stream, urut pintu masuk pertama kali (B2a); C00 sekali di awal:
C  Stream Inventory → segmen + handoff + simpul, ikut Koridor  (flow-c-inventory)
D  Eksplorasi       → gelombang 1 buta (lensa + twin-path)
                      → gelombang 2 lazy-load 2–4 plugin + 1-hop peek
                      → kartu lead + invariant            (flow-d-explore)
                      → MODE: AUTO default (otonom); MODE: PAIR hanya bila user
                        eksplisit meminta co-audit fungsi demi fungsi
E  Uji test         → fork blok pin → PoC + P&L, batch ≤3  (flow-e-test)
F  Komposisi Inkrem.→ segera bila Stream sentuh State-Bridge/
                      brankas Stream selesai; sapuan akhir bila
                      multi-stream                          (flow-f-compose)
G  Verdict          → 06/07/08/09 + distribusi akhir       (flow-g-verdict)
```

Deep-run per jalur: satu perintah berdiri hulu→hilir sampai verdict per lead, tanpa tap antar langkah.

## Larangan lintas tahap (kesalahan yang paling sering terjadi)

| Kesalahan | Kenapa salah |
| :--- | :--- |
| `cast code` / saldo di Tahap A | itu Tahap B (B7); Tahap A = klaim saja (A2) |
| Menulis invariant di B atau C | invariant = klaim asumsi → Tahap D (B12) |
| Memburu celah saat memetakan | itu Tahap D; peta harus netral |
| Membuka katalog di gelombang 1 | merusak sifat buta; anchoring |
| Menyimpulkan TERBUKTI dari gelombang 1/2 | C11: butuh rantai (a)+(b)+(c) diuji di E |
| Menjalankan fork/PoC ulang di F | F merangkai bukti E, bukan mengulang |
| Memindahkan lead belum terbukti ke 08 lalu melabelinya Low | pelarian wadah |
| Menolak lead jadi 06 tanpa log eksekusi | penolakan kertas, laporan ditolak |
| Mengurutkan kartu `QUEUED` di dalam Stream berdasar EV | B2a-v2 Lapis 2: bobot struktural P1 Simpul/Komposisi → P2 Handoff/State-Bridge → P3 Segmen Lokal |
| Melebar horizontal ke fungsi lain klaster seberang | melanggar Koridor Stream; yang di luar garis aliran = Stream lain |
