# Skills

## Metode aktif: Flow Money First (diputus 22:33 WIB 16 Nov 2026)

- `flow-money-first/` — pintu masuk runtime (bootloader: baca 4 berkas `methodology/`; sumber kebenaran = `methodology/aturan-alur-first.md`). Identitas + konstitusi flow (`SOUL.md`, `AGENTS.md`) kini ada di root repo ini (di-upload 17 Nov 2026); versi Segitiga-nya diarsipkan sebagai `archive/segitiga-v2/SOUL-segitiga-v2.md` dan `archive/segitiga-v2/AGENTS-segitiga-v2.md`.
- `flow-a-intel/` — Tahap A: intel proyek (brief 9 butir, stage deployment termasuk `PRE-DEPLOY / REPO-ONLY`).
- `flow-b-map/` — Tahap B: mapping — B0 Profil Topologi (`B00-TOPOLOGY`), Katalog Ingress `IN-x` (B17), AST untuk lokalisasi (B6-v2), sensus statis/live, klaster 4 tipe (`B04-STREAMS-AND-CLUSTERS`), jembatan state (`B07-STATE-BRIDGES`), ledger sisa (3 populasi, rekonsiliasi by-name), registry invariant.
- `flow-c-inventory/` — Tahap C: Stream-Slice Inventory per Lintasan — `C00-SHARED-PRIMITIVES` sekali di awal (+ `C00-Uxx/CY`) + `C<NN>-<STR>-<Lk>-INVENTORY` **9 bagian baku**: identitas (+ hitungan anggaran / `KEPUTUSAN_ANGGARAN`), segmen (`S0` opsional — tidak dihitung di rumus handoff — + `S1..Sn`, 5 pemicu B19), `CY-x` (10 kolom, enum `EXT_CALL`/`DELEGATECALL`/`NATIVE_SEND`/`TOKEN_HOOK`/`ORACLE_READ`/`CALLBACK`/`TRY_CATCH`), handoff (`N−1+Σ(m−1)` + kolom Lintas-domain), simpul, State-Bridge (enum `Sync_Status` + `Window_&_Trigger`), Tabel Selisih Varian (`TIDAK_BERLAKU` bila tunggal), LP-x per domain + slot storage (`UNVERIFIED`), rekonsiliasi ledger berbasis nama.
- `flow-d-explore/` — Tahap D: eksplorasi per Lintasan — Gelombang 1 bebas katalog (3 Lensa Fisika Nilai + Twin-Path Diff), Gelombang 2 Symptom-Triggered Lazy Skill Augmentation (maks 2-4 plugin via Lazy Skill Router), kartu lead (a)+(b)+(c), Gate D C10-v2; gerbang ≥1 kartu/Lintasan atau `NIHIL_KANDIDAT`; kartu wajib untuk baris `BEDA` Tabel Selisih dan `CY-x` tanpa guard dengan tulis-sesudah.
- `flow-e-test/` — Tahap E: pembuktian fork blok pin — pustaka kumulatif `FlowFixtures`, dua metrik plafon (`Observed Live Ceiling` / `Proven Potential Ceiling` + victim seeding), plafon wajib `>= $1`, batch maks 3; fork dua domain untuk handoff lintas-domain + impersonasi pengirim sah per autentikasi domain.
- `flow-f-compose/` — Tahap F: komposisi inkremental lintas-Stream (pemicu seusai E per Stream + sapuan akhir), Lemma 4 Syarat, pembaruan `Sync_Status` di `B07` (enum `SEED`/`WRITER_MAPPED`/`READER_MAPPED`/`SINKRON`/`DESINKRON:<OBS-id>`/`TERBUKA_EKSTERNAL` + kolom `Window_&_Trigger`).

**moneyflow v2.1 (Universal Topology):** Tahap B dimulai dari `B00-TOPOLOGY` (hitungan `DOM-x`/`VK-x`/`VC-x` → mode `TUNGGAL`/`TUNGGAL-BERINSTANS`/`MULTI-DOMAIN` + Matriks Domain) dan Katalog Ingress `IN-x`; Tahap C berjalan per **Lintasan** (`STR-nn.Lk`) dengan `CY-x`, Ingress `S0`, Tabel Selisih Varian, dan LP-x per domain. Gerbang baru: `verify_flow.py check-b0`.
- `flow-g-verdict/` — Tahap G: triage per-Stream ke wadah `06/07/08/09` + rekapitulasi akhir; kedua metrik plafon transparan pada verdict dampak.
- `flow-autopilot/` — orkestrator full-autopilot Stream-First (mesin status dua lapis Lapis Proyek + Lapis Stream, `Stream Context Capsule`, ekspansi dinamis `STR` baru dari sisa ledger; `/stop` mencabut otorisasi seketika).

Pemeriksa gerbang pendamping: `tools/verify_flow.py` — pra-cek deterministik sebelum merge staging (`check-staging`) dan gerbang tahap (`check-b0`, `check-b`, `check-c`, `check-d`, `check-e`, `check-final`); exit 0 = lulus, 1 = gagal beserta daftar pelanggaran spesifik.

Berkas metode flow ada di `methodology/aturan-alur-first.md`, `methodology/resume-aturan-preferensi-alur-first.md`, `methodology/acuan-workflow-tahap-B.md`, `methodology/rancangan-hemat-fase-d.md`. Identitas + konstitusi operasional flow (`SOUL.md`, `AGENTS.md`) ada di repo `thesachio/moneyflow`.

## Rujukan / legacy: Metode Segitiga v2.0 (diarsipkan 17 Nov 2026)

- Skill Segitiga (`sc-pre-intel/`, `sc-a-scope/`, `sc-b-map/`, `sc-c-hunt/`, `sc-d-prove/`, `sc-e-verdict/`, `sc-f-report/`, `sc-autopilot/`) dipindahkan utuh ke `archive/segitiga-v2/skills/` beserta seluruh berkas profil Segitiga lainnya (metode, gerbang, SOUL/AGENTS, PERSONA/CONSTITUTION, catatan SYNC). Bukan metode aktif; dipakai hanya sebagai rujukan untuk proyek yang sudah berjalan di bawahnya.
