# PROJECT INTELLIGENCE BRIEF — `INTEL.md` (moneyflow v2.1, Tahap A)

> **Posisi berkas.** `INTEL.md` diletakkan **di root folder kerja audit**, sejajar dengan `STATE.md`.
> Ia diisi **sekali** di awal, dan **hanya diperbarui bila jaringan/deployment berubah**.
> Ia **bukan tahap baru** — ia **keluaran Tahap A**. Selama INTEL belum sah, Tahap B tidak boleh dimulai.
> Verifier: `python3 tools/verify_flow.py` (tidak ada `--gate 0` di metode ini).

> **Pembagian tugas (jangan dicampur).**
> - `INTEL.md` = **fakta proyek yang dapat ditunjuk**: identitas, URL, commit, klaim stage, jejak ketiadaan.
> - `STATE.md` = **posisi eksekusi**: `Active Phase`, `CURRENT_ACTIVE_ITEM`, `Domain Coverage Meter`, `Do-Not-Reopen List`.
> - `B00`–`B07` = **peta kode + live**: topologi, sensus statis, sensus live, katalog Stream/Lintasan, ledger, invariant, State-Bridge.
>
> `INTEL.md` **DILARANG** memuat hipotesis kerentanan, status wilayah, atau hasil audit.

> **Hukum kejujuran.** Bila sesuatu tidak ditemukan, tulis `TIDAK_DITEMUKAN` **beserta alasannya**.
> DILARANG mengarang URL, mengisi nama auditor dari ingatan, atau menebak commit.
> `TIDAK_DITEMUKAN` adalah hasil yang sah; URL palsu menghancurkan seluruh laporan.

---

```markdown
# PROJECT INTELLIGENCE BRIEF

- Target Repo Path  : <path absolut proyek lokal>
- Last Updated     : <YYYY-MM-DD>
- Intel Status     : COMPLETE | PARTIAL (catat bagian yang belum ditemukan)
- Diverifikasi Oleh: <perintah yang dijalankan untuk membuktikan tiap URL/klaim>

## 0. Deployment Stage (klaim bersumber — BUKAN keputusan teknis)

- Deployment Stage : MAINNET | TESTNET | DEVNET | TIDAK KETEMU
- Sumber Klaim     : <URL/halaman resmi yang menyatakan stage itu, atau TIDAK KETEMU (sumber: <yang dicoba>)>
- Perubahan Stage  : <tanggal + alasan, bila pernah berubah; selain itu "belum pernah berubah">

> **Batas Tahap A.** Kolom ini mencatat **apa yang diklaim sumber resmi**, bukan hasil verifikasi.
> Tahap A dilarang menjalankan `cast`/`eth_getCode` (A2). Kelangsungan-hidup **per komponen**
> ditetapkan nanti di **B8 Live-Match Lintasan** — per Lintasan, dengan alasan `REPO_ONLY` atau
> `LIVE_MISMATCH`. Proyek bisa `MAINNET` sementara sebagian Lintasan `TUNDA-LIVE (REPO_ONLY)`.
> **Tidak ada nilai `PRE-DEPLOY`** — stage hanya tiga.

## 1. Project Identity & Brief Overview
- Project Name : <Nama Resmi Proyek & Organisasi>
- Brief Overview : <1–3 kalimat ringkas mengenai fungsi dan mekanisme inti protokol>

## 2. Core Reference Links (Direct URLs Only)
- Main UI (dApp) : <URL langsung ke aplikasi web/UI utama tempat pengguna berinteraksi, atau TIDAK_DITEMUKAN>
- Official Docs  : <URL langsung ke dokumentasi teknis resmi, atau TIDAK_DITEMUKAN>
- Specific GitHub Repo : <URL langsung ke repositori GitHub spesifik yang menjadi target audit>
- Audited Commit / Branch : <branch> @ <commit_hash>

## 3. Bug Bounty Rules (Direct Link)
- Platform : <Docs Resmi | Immunefi | Cantina | Sherlock | Code4rena | CodeHawks | Lainnya | TIDAK_DITEMUKAN>
- Direct Bounty URL : <URL langsung ke halaman aturan/scope bug bounty spesifik proyek ini>
- High-Level Scope Note : <1–2 baris catatan faktual bila halaman bounty menyebut repo/kontrak/
  chain spesifik atau aturan pengecualian utama>

## 3b. Brief Severity (butir 9 — hanya bila halaman bounty menyebutnya)
- Skala / Tier : <ringkasan skala severity yang dipakai program (mis. Critical/High/Medium/Low + ambang), atau TIDAK_DITEMUKAN>
- Sumber       : <URL halaman bounty yang memuat skala itu — sama dengan §3, bukan pencarian baru>

## 4. Past Audit Reports (Direct File/Report Links)
- [<Nama Auditor 1 — Tanggal/Tahun>](<URL langsung ke file PDF / repo / halaman laporan audit>) — Fokus/Versi: <singkat>
- [<Nama Auditor 2 — Tanggal/Tahun>](<URL langsung ke file PDF / repo / halaman laporan audit>) — Fokus/Versi: <singkat>
- *(Bila belum ditemukan laporan publik, ganti KEDUA baris di atas dengan:)*
  `TIDAK_DITEMUKAN — tidak ada laporan audit publik di docs/, folder audits/, maupun situs auditor.`
- *(Bila README hanya MENYEBUT adanya audit tanpa tautan:)*
  `TIDAK_DITEMUKAN — README menyebut "audit by X" tanpa tautan laporan (klaim tak terverifikasi).`

## 5. Deployment & Live Surface — **DIISI DI TAHAP B, BUKAN DI A**

> Tahap A **dilarang** menjalankan `cast`/`eth_getCode` (A2). Semua kolom di bawah diisi di
> **B03-CENSUS-LIVE (B7)** per domain, dan keputusan per komponen di **B8** per Lintasan.
> Di Tahap A cukup tulis `DIISI_B7` pada semua baris.

- Chain / Network Aktif : `DIISI_B7`
- Kontrak Utama (alamat) : `DIISI_B7`
- Implementation Aktif : `DIISI_B7`
- Blok Referensi      : `DIISI_B7` (ditetapkan di B7, bukan di A)
- VERSION_RELATION    : `DIISI_B7`
- Bukti Live : `DIISI_B7`

## 6. Catatan Ketiadaan (WAJIB bila Intel Status = PARTIAL)
| Butir | Status | Alasan + sumber dicoba | Dampak |
|---|---|---|---|
| UI | DITEMUKAN/TIDAK_DITEMUKAN | <alasan + sumber yang dicoba> | <dampak bila tak ditemukan> |
| Docs | DITEMUKAN/TIDAK_DITEMUKAN | <alasan + sumber yang dicoba> | <dampak> |
| Repo | DITEMUKAN/TIDAK_DITEMUKAN | <alasan + sumber yang dicoba> | <dampak> |
| Bounty | DITEMUKAN/TIDAK_DITEMUKAN | <alasan + sumber yang dicoba> | <dampak> |
| Audits | DITEMUKAN/TIDAK_DITEMUKAN | <alasan + sumber yang dicoba> | <dampak> |
| Deployment | DITEMUKAN/TIDAK_DITEMUKAN | <alasan + sumber yang dicoba> | <dampak> |
- Ringkasan : <butir TIDAK_DITEMUKAN, atau "tidak ada — INTEL COMPLETE">
```

---

## Aturan pengisian (mengikat)

1. **URL harus langsung.** `https://docs.protokol.xyz/security` ✅ — bukan `https://docs.protokol.xyz` bila halaman itu tidak memuat aturan buruannya. DILARANG menaruh URL mesin pencari.
2. **Setiap URL wajib dibuktikan hidup** pada sesi yang sama (`curl -sI` → status 200/30x, atau pembacaan halaman). Catat perintahnya di baris `Diverifikasi Oleh`. URL mati → `TIDAK_DITEMUKAN`.
3. **Commit wajib dipin.** `Audited Commit / Branch` harus berisi hash hasil `git rev-parse`, bukan "latest". Ini input untuk `VERSION_RELATION` (§5) yang diisi di **B7**, dan untuk gerbang scope di `verify/VERDICT.md` §0.2c.
4. **Dilarang mengarang nama auditor.** Bila repo/docs menyebut "audit oleh X" tanpa tautan laporan, tulis `TIDAK_DITEMUKAN` di §4 dan sebutkan klaim tak terverifikasi itu di §6.
5. **§5 diisi di Tahap B, bukan di A.** Deployment dinyatakan ada hanya bila ada `eth_getCode`/`cast code` non-kosong atau transaksi deploy — tetapi pembacaan itu dilakukan di **B7**, bukan di Tahap A (A2 melarang `cast` di A). "Seharusnya live" bukan bukti.
6. **§6 tidak boleh kosong** bila `Intel Status = PARTIAL`. Bagian inilah yang melindungi audit dari klaim berlebih di Tahap E dan G.

### Aturan khusus §0 — `Deployment Stage`

`Deployment Stage` adalah **klaim bersumber**, bukan kesimpulan teknis. Ia menjadi **filter awal** Mode Uji, tetapi keputusan akhir per komponen dibuat di **B8**:

| `Deployment Stage` | Artinya | Akibat pada audit |
| :--- | :--- | :--- |
| `MAINNET` | sumber resmi menyatakan protokol berjalan di produksi publik | `09` menuntut `Mode Uji: FORK_LIVE` **untuk Lintasan yang live**; Lintasan `TUNDA-LIVE (REPO_ONLY)` tidak bisa `09` |
| `TESTNET` | sumber resmi menyatakan hanya testnet publik | `09` menuntut `Mode Uji: FORK_TESTNET` |
| `DEVNET` | sumber resmi menyatakan jaringan dev privat/terbatas | `09` menuntut fork devnet; dicatat eksplisit |
| `TIDAK KETEMU` | sumber resmi tidak menyatakan stage | sah sebagai hasil; Tahap B menetapkan per domain, dan B8 memutuskan per Lintasan |

**Larangan:**
- `Deployment Stage` **DILARANG dikosongkan tanpa alasan** — isi salah satu dari empat nilai di atas; `TIDAK KETEMU` wajib menyebut sumber yang dicoba (A4).
- **DILARANG** menetapkan `MAINNET` hanya karena "seharusnya live" — tanpa klaim sumber, nilai yang sah adalah `TIDAK KETEMU`.
- **DILARANG** memakai nilai `PRE-DEPLOY`/`REPO-ONLY` di kolom ini — status itu milik **B8 per Lintasan**.
- Perubahan stage (mis. `TESTNET → MAINNET`) **wajib** mengisi baris `Perubahan Stage` + tanggal.

---

## Aturan Jujur per Bagian (WAJIB — "tidak ditemukan" bukan kegagalan)

Setiap bagian punya **cara sah mengatakan tidak ada**. Dilarang mengosongkan slot, dilarang mengisi dengan tebakan, dilarang memaksakan jawaban agar terlihat lengkap.

| Bagian | Bila TIDAK ditemukan, tulis PERSIS | DILARANG |
|---|---|---|
| 0 · Deployment Stage | **tidak boleh** — wajib salah satu dari tiga nilai | Mengosongkan, menebak, atau menyalin dari proyek lain |
| 1 · Project Name | `TIDAK_DITEMUKAN` diikuti sumber yang diperiksa (`README`/`git remote`) | Menebak nama dari nama folder |
| 1 · Brief Overview | `TIDAK_DITEMUKAN — tidak ada README/docs yang menjelaskan mekanisme` | Mengarang deskripsi dari pengetahuan umum/model |
| 2 · Main UI (dApp) | `TIDAK_DITEMUKAN` — protokol mungkin hanya kontrak/library tanpa UI | Menulis domain akar yang belum diuji |
| 2 · Official Docs | `TIDAK_DITEMUKAN` | Menulis URL hasil pencarian |
| 2 · Specific GitHub Repo | `TIDAK_DITEMUKAN` — bukan repo git / tanpa remote | Menebak `github.com/<org>/<nama>` dari nama proyek |
| 2 · Audited Commit | `TIDAK_DITEMUKAN` — bukan repo git | Menulis `latest`, `main`, atau hash karangan |
| 3 · Platform | `TIDAK_DITEMUKAN` | Mengisi `Immunefi` tanpa halaman bounty yang benar-benar ada |
| 3 · Direct Bounty URL | `TIDAK_DITEMUKAN` | Menunjuk beranda platform, bukan halaman proyek |
| 3 · High-Level Scope Note | `TIDAK_DITEMUKAN — tidak ada aturan scope tertulis` | **Menyimpulkan scope dari praktik umum** |
| 4 · Past Audit Reports | `TIDAK_DITEMUKAN` | Menaikkan *"disebut di README"* menjadi laporan |
| 5 · Chain / Kontrak / Impl / Blok / Bukti Live | `DIISI_B7` di Tahap A; di B7 `TIDAK_DITEMUKAN` per sub-baris | Menjalankan `cast` di Tahap A; menulis alamat tanpa `cast code` non-kosong |

### Empat hukum pengisian

1. **Satu alasan per ketiadaan.** `TIDAK_DITEMUKAN` saja tidak cukup — wajib disertai **alasan singkat + sumber yang sudah dicoba** di tabel §6. Tanpa itu, INTEL dianggap **tidak jujur**.
2. **"Gagal diakses" ≠ "tidak ada".** Bila penyebabnya 403/429/login/timeout, tulis `TIDAK_DITEMUKAN (batas akses: <penyebab>)`. DILARANG menyimpulkan aturan/laporan itu tidak eksis.
3. **Dilarang mengisi slot dengan asumsi.** Bila ragu, turunkan ke `TIDAK_DITEMUKAN`. Satu slot kosong yang jujur tidak merusak laporan; satu URL palsu membatalkan seluruhnya.
4. **Konsistensi wajib.** `Intel Status = COMPLETE` hanya sah bila **keenam** butir di tabel §6 berstatus `DITEMUKAN`. Satu saja `TIDAK_DITEMUKAN` ⇒ status **wajib** `PARTIAL`.
