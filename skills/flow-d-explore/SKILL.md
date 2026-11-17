---
name: flow-d-explore
description: Tahap D — Eksplorasi per-alur, dua gelombang (buta → berpengetahuan + katalog 52), kartu lead + invariant tiga lapis, gate finansial C10, label DIANALISIS wajib di gelombang 1/2 (C11). Skill ini memuat aturan dan format sampai Tahap D selesai. Dipakai saat memburu alur, atau saat user menyebut tahap D, eksplorasi, gelombang, kartu lead.
---

# Skill flow-d-explore — Tahap D (Eksplorasi)

Tahap D = buruan **per alur**. Unit round = per-alur, dua gelombang (buta → berpengetahuan + katalog).
Skill ini memuat aturan dan format sampai Tahap D selesai. `methodology/aturan-alur-first.md` (seksi D — Tahap D, B12, C10, C11) hanya rujukan sengketa.

## Prasyarat (tanpa ini D tidak mulai)

- Daftar alur klaster: enumerasi per alur + entrypoint pertama tiap alur, dari `B02` + `B04`.
- Inventaris alur klaster (`C<NN>-K<n>-FLOW-INVENTORY.md`).
- Registry invariant (`B06`) sudah punya struktur penomoran.

**Definisi alur:** satu alur = **KELUARGA jalur** yang berbagi segmen + kontrak handoff yang sama. Bila intinya beda, **pecah** jadi kartu lead sendiri atau round sendiri. Alur ≠ klaster: satu klaster bisa berisi beberapa alur.

## Gelombang 1 — buta

Bekal: L-VALUE + L-PATH + inventaris alur klaster + premis parent.

**DILARANG:**

- membuka katalog (`_ROUTER.md` atau plugin `M-*` / `AF-*` / `DOM-*` / `POV-*` / `CHAIN-*` apa pun)
- membaca badan fungsi klaster lain
- memakai laporan audit lama sebagai sumber dugaan

**Pengecualian wajib:** baca `M-005` §3 sebelum menulis entri `04`.

Keluaran gelombang 1 (4 label):

| Label | Arti |
| :--- | :--- |
| `OBS` | observasi anomali (fakta kode, belum jalur) |
| `G` | jalur yang terbukti dijaga penjaga kode eksak |
| `R` | sinyal RADAR (menyentuh modul/variabel lain) |
| `Q` | pertanyaan untuk gelombang 2 |

## Gelombang 2 — berpengetahuan + katalog

Silang empat hal:

1. **Inversi handoff** — patahkan jaminan produsen / asumsi konsumen dari `C<NN>`.
2. **Konservasi** — Σkeluaran vs masukan di tiap simpul fork/join.
3. **Jejak event live** — dipakai sebagai enumerasi independen, bukan cara kerja utama (pindai log = verifikator terakhir).
4. **Katalog 52 plugin** — baca **hanya** plugin yang gejalanya cocok. Tidak ada yang cocok → tulis `[NO-CATALOG]`. **Kandidat DILARANG gugur hanya karena tidak cocok katalog.** Temuan di luar katalog = kandidat plugin baru.

Keluaran gelombang 2: kandidat `QUEUED` (`QD..`) + `DORMAN` (hanya bila gagal gate C10) + disposisi `Q`/RADAR.

### Urutan prioritas QUEUED

Urutkan menurut **pintu masuk pertama kali** (B2a, diputus 17 Nov 2026): kandidat yang menyentuh **entrypoint paling awal** pada alur pengguna dikerjakan lebih dulu; bila beberapa kandidat menyentuh entrypoint yang sama, urutkan menurut urutan segmen (S1 sebelum S2).

EV live **tidak** dipakai sebagai penentu urutan. Boleh dicatat sebagai data pendukung, bukan penentu.

> Catatan jujur: label `P1–P5` yang dipakai di beberapa berkas adalah kosakata warisan katalog dan **tidak punya definisi di methodology repo ini**. Jangan mengarang definisinya. Kalau user meminta label prioritas, minta definisinya lebih dulu.

## Kartu lead + invariant

### Kartu lead (1:1 dari QUEUED)

Tiap kartu **wajib punya klaim finansial sendiri** — bukan "ini mencurigakan", tapi "kalau ini pecah, X unit nilai berpindah dari A ke B".

**C11 mengikat bentuk kartu:** kartu merumuskan rantai **(a)+(b)+(c)** sebagai **satu rantai** yang akan diuji utuh di Tahap E:

- (a) pelanggaran invariant (di mana, fungsi mana);
- (b) jalur pendek yang menyambungkannya ke nilai;
- (c) kerugian terukur (berapa, dari mana angkanya).

Kartu yang hanya berhenti di (a) = **HIPOTESIS**, bukan kandidat uji.

### Invariant tiga lapis

| Lapis | ID | Cakupan |
| :--- | :--- | :--- |
| L1 | `INV-Sx` | di dalam segmen |
| L2 | `INV-Hx`, `INV-Jx` | di handoff dan di simpul |
| L3 | `INV-Fx` | ujung-ke-ujung / komposisi |

Aturan wajib per invariant:

- **Wajib mencantumkan sumbernya**: field kontrak handoff, atau baris `docs`/NatSpec. **Bukan** perasaan agen.
- **Wajib punya akibat finansial bila pecah** — invariant tanpa akibat finansial bukan invariant, itu catatan.
- Cek **testability** dicatat saat perumusan: fork apa, data live apa; dilabeli bila tidak bisa diuji.
- Registry invariant **satu penomoran global** (`B06`), diisi mulai Tahap D.

## Gate finansial (C10) — gerbang masuk Tahap E

Lead **masuk** Tahap E bila **ketiganya** terpenuhi:

1. mekanisme jalan di fork/test atas **kode + state nyata**;
2. **plafon terukur** (angka, bukan perkiraan);
3. pemicu **terjangkau lewat jalur operasi normal** — tanpa peran istimewa, tanpa state eksotis.

**Yang TIDAK disyaratkan:** P&L live > 0, korban nyata, kejadian on-chain.

**Konsekuensi penting:** **plafon live 0 TIDAK lagi membuat lead DORMAN.** Nilai 0 di live hanya berarti pemicunya belum terjadi, bukan bahwa mekanismenya tidak bisa merugikan.

`DORMAN` hanya dipakai bila **gate C10 gagal**, dan wajib mencatat **syarat buka-ulang yang konkret** (mis. "buka bila pool X punya likuiditas", "buka bila parameter Y diubah").

## C11 — gelombang 1 dan 2 TIDAK memberi verdict TERBUKTI

Konsekuensi yang sering dilanggar:

- Gelombang 1/2 **tidak boleh** menyimpulkan `TERBUKTI`.
- Tiap observasi/jawaban dilabeli **`DIANALISIS`**.
- Wajib mencatat **alur terkait apa yang masih kurang** menuju kerugian terukur.
- `TERBUKTI` hanya boleh datang dari Tahap E yang menguji rantai (a)+(b)+(c) utuh.

## Aturan mengikat lain

- **Bahasa brief: verifikasi invariant, bukan bahasa serangan.** Brief Tahap E memakai bahasa verifikasi.
- **Tugas agen dibatasi ALUR, bukan klaster** — boleh baca lintas klaster **hanya sepanjang alur yang dilewati**.
- **Deep-run per jalur**: satu perintah berdiri hulu→hilir sampai verdict per lead, tanpa tap antar langkah.
- **`/stop` mencabut otorisasi seketika** — hentikan subagent, tulis nol berkas.

## Keluaran

- `D<nn>-<JALUR>-WAVE1-BLIND.md` — OBS / G / R / Q, semua berlabel `DIANALISIS`.
- `D<nn>-<JALUR>-WAVE2-QUEUED.md` — QUEUED berurut pintu masuk + DORMAN (dengan syarat buka-ulang) + disposisi.
- `D<nn>-<JALUR>-LEAD-CARDS.md` — kartu 1:1 dengan rantai (a)+(b)+(c) + klaim finansial.
- Registry invariant (`B06`) terisi dengan sumber tiap invariant.

## Definition of done Tahap D (per alur)

- [ ] gelombang 1 dijalankan **tanpa** membuka katalog
- [ ] gelombang 2 menyilang keempat sumber (handoff, konservasi, event live, katalog)
- [ ] tiap QUEUED punya kartu lead dengan rantai (a)+(b)+(c) dan klaim finansial
- [ ] tiap invariant punya sumber (field handoff / docs) + akibat finansial + cek testability
- [ ] gate C10 diuji untuk tiap kandidat; DORMAN hanya bila gagal, dengan syarat buka-ulang
- [ ] nol verdict `TERBUKTI` dari gelombang 1/2; semua berlabel `DIANALISIS`
- [ ] nol PoC (itu Tahap E)
