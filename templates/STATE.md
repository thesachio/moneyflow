# STATE — Kursor Checkpoint & Resume (moneyflow v2.1)

> **Batas 50 baris.** `Working Memory Scratchpad` maks 10 baris. Temuan final → `05-raw-leads.md`, bukan di sini.
> **Write-ahead:** perbarui `CURRENT_ACTIVE_ITEM` + `Domain Coverage Meter` + `Do-Not-Reopen List` **sebelum** pindah unit, bukan sesudahnya.
> Verifier: `python3 tools/verify_flow.py` (check-staging/check-b0/check-b/check-c/check-d/check-stream/check-e/check-final).

## Kursor

| Field | Nilai |
| :--- | :--- |
| `Active Phase` | `A — INTEL` |
| `Active Sub-Stage` | `A1 — brief 9 butir` |
| `CURRENT_ACTIVE_ITEM` | `A01-INTEL.md` — **belum dibuat** |
| `Mode Topologi (B0)` | `BELUM DITENTUKAN` (diputus di Tahap B Langkah 0) |
| `Target Repo` | `BELUM DITENTUKAN` |
| `Pin / Blok Referensi` | `BELUM DITETAPKAN` (Tahap B) |

## Domain Coverage Meter

| Domain | Terpetakan | Total | Catatan |
| :--- | :--- | :--- | :--- |
| — | 0 | 0 | sensus belum jalan (Tahap B belum dimulai) |

## Do-Not-Reopen List

*(kosong — belum ada item yang gugur atau terkunci)*

## Working Memory Scratchpad (maks 10 baris)

1. Metode = moneyflow **v2.1**: Stream ⊃ Lintasan ⊃ Segmen; `Stream` **bukan** wadah — ia siklus hidup nilai.
2. Urutan: B0 topologi → sensus `B02` → `B04` katalog → rolling per-Lintasan `C → B8 → D → E` → penutupan `F antar-Lintasan → G → F antar-Stream`.
3. Verifier: `check-staging` · `check-b0` · `check-b` · `check-c` · `check-d` · `check-stream` · `check-e` · `check-final`.
4. Status kartu: `MENUNGGU-RANGKAI` (rantai lewat batas Lintasan, ditutup F pemicu 1) dan `TUNDA-VERIFIKASI` (bergantung `LP-x` `UNVERIFIED`).
5. Artefak C = 9 bagian baku (A04); `S0` = Ingress tidak resmi, tidak dihitung di rumus handoff.
6. Langkah berikut: isi `A01-INTEL.md` (brief 9 butir).

## Log Checkpoint

| ID | Item | Status | Catatan |
| :--- | :--- | :--- | :--- |
| CP-001 | inisialisasi proyek | START | skeleton v2.1 disalin dari `moneyflow`; `STATE.md` dibuat |
