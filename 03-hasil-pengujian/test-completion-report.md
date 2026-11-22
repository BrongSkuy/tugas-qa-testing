# Test Completion Report (Test Summary Report — `TC1`–`TC4`)

Dokumen ini merupakan **Test Completion Report (`7.4.5`)** yang merangkum penyelesaian **Test Completion Process (`7.4`, aktivitas `TC1–TC4`)** sesuai **ISO/IEC/IEEE 29119-2:2021(E)** dan **ISO/IEC/IEEE 29119-3** untuk pengujian **Black Box** dan **Performance Testing** (disertai analisis pelengkap *White/Gray Box* & audit *ISO/IEC 25010:2023*) pada **Portal Booking GOR Permata Badminton Hall** (`https://gorpermatabadminton.com`).

---

## 1. Ringkasan Eksekutif Pengujian yang Dilaksanakan (`TC4 — 7.4.4.5 a, b`)

1. **Cakupan Pengujian:** Seluruh alur proses ISO/IEC/IEEE 29119-2:2021 telah dijalankan secara utuh mulai dari *Organizational Test Specification* (`Clause 6`), *Master & Performance Test Planning* (`7.2`), permodelan uji edisi 2021 berbasis *Test Model -> TCI -> Test Case -> Test Procedure* (`8.2`), kesiapan lingkungan & data (`8.3`), eksekusi otomatis nyata (`8.4`), pelaporan insiden (`8.5`), hingga monitoring & penutupan (`7.3–7.4`).
2. **Hasil Agregat Eksekusi:**
   - **Black Box Testing (`TC-BB-01..23`):** `23` kasus uji dieksekusi -> **`16 PASS`**, **`7 FAIL`** *(seluruhnya merupakan konfirmasi cacat aktual yang terdokumentasi di `incident-reports.md`)*. `0` error konsol JS, **`0` request `POST /bookings/store` terkirim ke server produksi**.
   - **Performance Testing (`TC-PERF-01..10`):** `10` kasus uji dieksekusi -> **`7 PASS`**, **`3 FAIL`** *(pelanggaran SLA `10 VUs` pada `/booking` `p95 = 5314,28 ms`, bobot HTML mentah `/booking` `535,37 KB`, dan cold-start TTFB `/` `2618,3 ms`)*. Sebanyak `104` request HTTP `GET` konkuren mencatat **`0,0%` Error Rate**.
   - **Kualitas Produk (`ISO/IEC 25010:2023`):** Pembaruan audit 9 dimensi mutu selesai dengan angka empiris pada [`evaluasi-iso-25010-gor-permata.md`](../01-standar-ieee-iso/evaluasi-iso-25010-gor-permata.md).

---

## 2. Evaluasi terhadap *Test Completion Criteria* (`TP-GOR-01 §4.3`)

| Kriteria Penyelesaian (`Exit Criteria`) | Target | Hasil Terverifikasi | Status |
| :--- | :---: | :--- | :---: |
| Cakupan desain & eksekusi `TCI-BB` | `100%` (`23/23`) | `23/23 TCI-BB` tertelusur ke `TC-BB-01..23` & dieksekusi | **TERPENUHI** |
| Cakupan desain & eksekusi `TCI-PERF` | `100%` (`10/10`) | `10/10 TCI-PERF` tertelusur ke `TC-PERF-01..10` & dieksekusi | **TERPENUHI** |
| Keamanan non-destruktif produksi | `0` POST ke server | `network_posts_sent_to_server = 0`; `0%` error load test | **TERPENUHI** |
| Dokumentasi *Incident Reports* & Bukti | Lengkap & reproducible | `10` insiden (`IR-GOR-01..10`), 12 bukti visual (`01`–`12`), 2 JSON, 2 log TXT | **TERPENUHI** |
| Penyelesaian sebelum tahap wawancara (`04/`) | Siap sebelum wawancara | Proyek uji `01`–`03` tuntas sebelum menghubungi praktisi QA | **TERPENUHI** |

---

## 3. Rekapitulasi Insiden Terbuka (*Open Incidents — `IR-GOR-01..10`*)

Seluruh **`10` insiden** masih berstatus **Open** (karena pengujian bersifat observasi eksternal tanpa akses modifikasi kode sumber portal UMKM):
- **Prioritas Tinggi (`High`):** `IR-GOR-04` (eksposur `205` slot `data-phone` & `data-name` + skrip admin), `IR-GOR-05` (`612` slot aktif pada tanggal lampau `2020-01-01`), `IR-GOR-06` (`HTTP 500 Server Error` pada `?start_date=invalid-date`), dan `IR-GOR-07` (`p95` `/booking` melonjak ke `5314,28 ms` pada `10 VUs`).
- **Prioritas Menengah/Rendah (`Medium/Low`):** `IR-GOR-01` (`/register` `404`), `IR-GOR-02` (`normPhone` `+62 08...`), `IR-GOR-03` (`#custName` tanpa `.trim()`), `IR-GOR-08` (HTML `/booking` `535,37 KB`), `IR-GOR-09` (cold TTFB `/` `2618,3 ms`), dan `IR-GOR-10` (navbar mobile `390px` terpotong).

---

## 4. Pengarsipan Aset Uji (*Archive Test Assets — `TC1`, `7.4.4.2`*)

Seluruh aset uji yang dapat digunakan kembali (*reusable*) untuk pengujian regresi / pemeliharaan telah diberi versi dan diarsipkan dalam kontrol versi Git (`https://github.com/BrongSkuy/tugas-qa-testing`):
- **Tata Kelola & Rencana:** [`organizational-test-specification.md`](../01-standar-ieee-iso/organizational-test-specification.md), [`test-plan-gor-permata.md`](../02-objek-umkm-dan-rencana-uji/test-plan-gor-permata.md), [`performance-test-plan.md`](../02-objek-umkm-dan-rencana-uji/performance-test-plan.md).
- **Test Models & Specifications:** [`test-model-blackbox.md`](../02-objek-umkm-dan-rencana-uji/test-model-blackbox.md), [`test-model-performance.md`](../02-objek-umkm-dan-rencana-uji/test-model-performance.md), [`test-case-blackbox.md`](./test-case-blackbox.md), [`test-case-performance.md`](./test-case-performance.md).
- **Dataset & Skrip Otomasi Reusable:** [`test-data/blackbox-testdata.json`](./test-data/blackbox-testdata.json), [`test-data/performance-profiles.json`](./test-data/performance-profiles.json), [`automation-scripts/test_gor_permata.py`](./automation-scripts/test_gor_permata.py), [`automation-scripts/test_performance_gor_permata.py`](./automation-scripts/test_performance_gor_permata.py), [`automation-scripts/gor-permata.cy.js`](./automation-scripts/gor-permata.cy.js).
- **Bukti & Laporan:** [`test-execution-log.md`](./test-execution-log.md), [`incident-reports.md`](./incident-reports.md), [`evidence/performance-summary.md`](./evidence/performance-summary.md), [`evidence/performance-metrics.json`](./evidence/performance-metrics.json), [`evidence/blackbox-results.json`](./evidence/blackbox-results.json), dan 12 berkas bukti visual (`01`–`12`) di [`evidence/screenshots/`](./evidence/screenshots/).

---

## 5. Pembersihan Lingkungan Uji (*Clean Up Test Environment — `TC2`, `7.4.4.3`*)

- Seluruh instance peramban Chromium *headless* (`Playwright`) dan sesi koneksi `aiohttp` telah ditutup bersih pasca-eksekusi.
- Basis data produksi **GOR Permata Badminton Hall** dipastikan **100% bersih** dari data uji fiktif (`network_posts_sent_to_server = 0`).
- Direktori lokal bebas dari file sementara maupun data pribadi pelanggan (PII pada screenshot dimasking `[TERISI]` dan nilai `data-phone`/`data-name` tidak disimpan).

---

## 6. *Lessons Learned* (`TC3`, `7.4.4.4` -> Umpan Balik ke `OT3`)

1. **Apa yang Berjalan Baik:**
   - Penerapan alur **Test Model (`TD1`) -> TCI (`TD2`) -> Test Case (`TD3`) -> Test Procedure (`TD4`)** edisi 2021 membuat ketertelusuran BVA/EP/STT/Workload sangat jelas dan tidak ada skenario batas yang terlewat.
   - Proteksi ganda (`page.route` abort + pemantauan `requestfinished`) memungkinkan uji regresi berulang aman pada sistem live UMKM.
   - Kombinasi inspeksi visual tangkapan layar dan otomatisasi DOM berhasil mengungkap cacat navbar mobile (`IR-GOR-10`) yang tersembunyi di balik `document.scrollWidth`.
2. **Kendala yang Ditemui & Solusi:**
   - `aiohttp` membutuhkan paket eksternal untuk dekode *Brotli (`br`)*; diselesaikan dengan `Accept-Encoding: gzip, deflate` (stdlib `zlib`).
   - `chromium-headless-shell` tidak selalu memancarkan entri `LCP` tanpa interaksi pengguna; didokumentasikan transparan sebagai `N/A(headless)` dan divalidasi lewat `TTFB`, `FCP`, `DCL`, `Load`, dan `CLS`.
   - Paket biner `cypress` tidak terpasang lokal sehingga eksekusi penuh difokuskan pada Playwright Python.
3. **Rekomendasi Perbaikan Proses Organisasi (`OT3`):** Tambahkan pengecekan bounding box komponen navigasi responsif serta pemeriksaan kompresi HTTP (`gzip`/`br`) ke daftar praktik baku pada [`organizational-test-specification.md`](../01-standar-ieee-iso/organizational-test-specification.md) di iterasi berikutnya.

---

## 7. Persetujuan Penutupan Uji (`TC4 — 7.4.4.5 c, d`)

| Peran | Nama | Keputusan | Tanggal |
| :--- | :--- | :---: | :---: |
| Anggota Tim QA | Muhammad Faiz Rabbani (`231011402539`) | **Approved & Sinkron Repo — Siap Tahap Wawancara (`04/`)** | 18 Nov 2026 |
| Anggota Tim QA | Robi Farhan Anshori (`231011401468`) | **Approved & Sinkron Repo — Siap Tahap Wawancara (`04/`)** | 18 Nov 2026 |
| Anggota Tim QA | Dzikri Attariq Samayaki (`221011401148`) | **Approved & Sinkron Repo — Siap Tahap Wawancara (`04/`)** | 18 Nov 2026 |
| Anggota Tim QA | Nurlaelasari (`231011403531`) | **Approved & Sinkron Repo — Siap Tahap Wawancara (`04/`)** | 18 Nov 2026 |
| Dosen Pengampu *(Stakeholder Akademik)* | Asep Erlan Maulana, S.Kom., M.Kom | *Menunggu Asesmen* | — |
