# moneyflow — Flow Money First

Metode audit keamanan smart contract yang mempartisi berdasarkan **aliran uang**, bukan wadahnya (berkas). Unitnya satu aliran uang ujung-ke-ujung; tiap aliran diukur nilai live-nya (EV) sejak awal, diburu per segmen dan handoff, dan dibuktikan di fork live dengan P&L terukur.

Status: **pilot** (16 Nov 2026). Metode ini sedang diuji di audit Across dan belum diputuskan sebagai pengganti metode Segitiga. Aturan di sini adalah hasil revisi terbaru; kalau pilot berubah, berkas di sini yang diperbarui.

## Isi

- `aturan-alur-first.md` — aturan kanonik metode (Tahap A–G, A1–A5, B1–B16, C1–C9). **Ini sumber kebenaran.** Baca ini dulu.
- `resume-aturan-preferensi-alur-first.md` — ringkasan aturan + preferensi. Kalau berbeda dengan berkas aturan, berkas aturan yang berlaku.
- `acuan-workflow-tahap-B.md` — acuan kerja Tahap B: sensus, klaster, daftar jahitan.
- `rancangan-hemat-fase-d.md` — aturan hemat Fase D + prinsip efisiensi waktu + lantai bawah (floor).

## Cara pakai

1. Baca `aturan-alur-first.md` sampai paham struktur Tahap A–G.
2. Baca `resume-aturan-preferensi-alur-first.md` untuk preferensi yang mengikat.
3. Jalankan Tahap B dari `acuan-workflow-tahap-B.md`.
4. Terapkan aturan hemat dan lantai bawah dari `rancangan-hemat-fase-d.md` mulai Fase D.

## Lantai bawah (tidak boleh dipangkas)

Baca kode, ukur live, verifikasi parent atas bukti penentu. Segala penghematan hanya boleh memotong di atas lantai ini.

## Prinsip kunci

- Alur = keluarga jalur yang berbagi segmen + kontrak handoff yang sama.
- Tiap lead wajib klaim finansial; tiap PoC mengukur P&L.
- Fork live (bukan HEAD) adalah bukti; mekanisme tanpa P&L live bukan temuan.
- Tiga verdict terpisah (mekanisme / eligibility / dampak); severity dari plafon teramati.
- Submisi dan kontak program hanya dengan persetujuan eksplisit.
