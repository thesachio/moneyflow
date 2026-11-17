---
name: flow-money-first
description: Pintu masuk metode Flow Money First — audit smart contract yang mempartisi berdasarkan aliran uang, bukan wadah berkas. Memuat bootloader, peta tahap A–G dengan batas tiap tahap, gerbang keras, aturan katalog, dan protokol delegasi. Dipakai bila user menyebut flow money first / alur-first, meminta audit Tahap A–G, atau memulai proyek audit baru dengan metode ini.
---

# flow-money-first — Pintu masuk metode

Audit keamanan smart contract yang mempartisi pekerjaan berdasarkan **aliran uang**, bukan wadahnya (berkas).

**Unit kerja = satu aliran uang ujung-ke-ujung.** Tiap aliran diukur nilai live-nya sejak awal, diburu per segmen dan handoff, dibuktikan di fork live dengan P&L terukur.

Skill ini adalah **peta dan aturan gerbang**. Kerja tiap tahap mengikuti skill tahapnya (`flow-a-intel` … `flow-g-verdict`), bukan berkas ini.

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
| **B** | Mapping | `B01`–`B06` + `scripts/out/*.jsonl` | tanpa invariant, tanpa pemetaan mendalam, tanpa buruan/PoC/verdict |
| **C** | Pemetaan mendalam per klaster | `C<nn>-K<n>-FLOW-INVENTORY.md` | deskriptif saja; **jahitan adalah batas**; tanpa invariant/buruan/PoC |
| **D** | Eksplorasi per alur | `D<nn>-…-WAVE1/WAVE2/LEAD-CARDS` | dua gelombang; gelombang 1 **dilarang** buka katalog; tanpa PoC; gelombang 1/2 **tidak** memberi TERBUKTI |
| **E** | Uji test | `E<nn>-…-BATCH<n>-PROOF.md` + `poc/` | fork blok pin; P&L terukur; **batch maks 3**; parent rerun forge |
| **F** | Komposisi (bersyarat) | `F<nn>-…-COMPOSITION.md` | hanya multi-segmen **dan** penting-urgent; **tanpa fork/PoC ulang** |
| **G** | Verdict | `G01-VERDICT.md` + draf 09 | tiga verdict terpisah; severity dari plafon teramati; **HOLD** |

**Rolling:** per klaster `C → D → E`; Tahap F lintas-klaster + Tahap G di akhir.

**Satu klaster/alur diselesaikan dulu.** Dilarang menyentuh klaster/alur berikut selama yang aktif masih punya antrean > 0.

## Gerbang keras (tidak boleh dilewati)

1. **B13 — scope lock sebelum sensus.** Daftar berkas cocok **persis** inventaris kanonik (diff kosong), commit terverifikasi, `contracts/` bersih.
2. **B8 — live-match per klaster sebelum PoC.** Tidak live-match → wadah `TUNDA-LIVE` (tercatat di ledger, **nol waktu eksekusi**). Tanpa B8, PoC klaster itu **terblokir**.
3. **Gate finansial C10 di Tahap D.** Lead masuk E bila kerugian **bisa dibuktikan**: mekanisme jalan di fork/test atas kode+state nyata + plafon terukur + pemicu terjangkau lewat operasi normal (tanpa peran istimewa, tanpa state eksotis). **Plafon live 0 TIDAK membuat lead DORMAN.**
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
- **Induk satu-satunya penulis berkas kanonik + ledger sisa.** Subagent menulis **hanya** ke `notes/staging-<jalur>-<tahap>-<item>.md`, diawali `## STAGING MANIFEST` maks 16 baris.
- **Koordinator memverifikasi verdict dari berkas bukti** sebelum menerapkannya ke antrean bersama.
- **Brief Tahap E memakai bahasa verifikasi invariant**, bukan bahasa serangan.
- **Penolakan safety classifier tidak boleh diulang, diparafrase, atau diputar lewat jalur lain.** Pivot saja.
- **Verifikasi jangkar:** periksa **fungsinya** lewat `grep -n`, bukan hanya nomor baris. Baris yang ada ≠ jangkar yang benar. Rantai koreksi bukan bukti.

## Alur kerja yang benar (urutan operasional)

```
A  INTEL            → brief 9 butir + pin commit          (skill flow-a-intel)
B  Mapping          → scope lock → sensus 100% → live B7
                      → klaster + handoff → ledger → registry   (flow-b-map)
   ↓ per klaster, urut EV live:
C  Inventaris alur  → segmen + handoff + simpul            (flow-c-inventory)
D  Eksplorasi       → gelombang 1 buta → gelombang 2 katalog
                      → kartu lead + invariant            (flow-d-explore)
E  Uji test         → fork blok pin → PoC + P&L, batch ≤3  (flow-e-test)
F  Komposisi        → hanya bila multi-segmen & urgent     (flow-f-compose)
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
