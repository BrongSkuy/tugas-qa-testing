# Indeks Hasil Pengujian, Test Cases, & Laporan Bug — GOR Permata Badminton Hall

Dokumen ini menjadi ringkasan indeks untuk folder `03-hasil-pengujian/` agar kompatibel dengan tautan lama sekaligus mengarahkan ke seluruh artefak resmi sesuai standar **`>= 2022`** (**ISO/IEC/IEEE 29119-1:2022**, **29119-5:2024**, & **ISTQB CTFL v4.0.1 2024**).

---

## 1. Peta Artefak Pengujian (`Flow Testing 7 Tahap — >= 2022`)

| Proses / Tahap | Dokumen / Berkas | Ringkasan Isi & Status Terverifikasi |
| :--- | :--- | :--- |
| **Environment & Data (`ED1–ED4`)** | [`test-environment-dan-data.md`](./test-environment-dan-data.md) | Readiness report lingkungan (`Python 3.9`, `Playwright 1.60`, `aiohttp 3.13`), beda Test vs Ops, & dataset `test-data/*.json`. |
| **Test Case, Ilmiah, & Step-by-Step (Black Box)** | [`test-case-blackbox.md`](./test-case-blackbox.md) | `23` *Test Case* (`TC-BB-01..23`), `5` *Test Procedure*, matriks penurunan ilmiah (`>=2022`), & **Panduan Step-by-Step (6 Langkah)**. |
| **Test Case & Step-by-Step (Performance)** | [`test-case-performance.md`](./test-case-performance.md) | `10` *Test Case* (`TC-PERF-01..10`), `3` *Test Procedure*, & **Panduan Step-by-Step Performance (6 Langkah)**. |
| **Test Execution Log (`TE1–TE3`)** | [`test-execution-log.md`](./test-execution-log.md) | Log eksekusi aktual: **Black Box `16/23 PASS` (`7` temuan defect, `0` POST terkirim)** & **Performance `7/10 PASS` (`3` temuan SLA/payload, `0%` error pada `104` request)**. |
| **Incident / Defect Reports (`IR1–IR2`)** | [`incident-reports.md`](./incident-reports.md) | `10` laporan insiden terstandar (`IR-GOR-01` s.d. `IR-GOR-10`, mencakup `BUG-GOR-01..04` + 6 temuan baru Black Box & Performance). |
| **Status & Control Report (`TMC1–TMC4`)** | [`test-status-and-control-report.md`](./test-status-and-control-report.md) | Progres cakupan `100%` TCI, 4 *Control Directives* (`CD-01..04`), pembaruan *Risk Register*, & persetujuan *Exit Criteria*. |
| **Test Completion Report (`TC1–TC4`)** | [`test-completion-report.md`](./test-completion-report.md) | Ringkasan penutupan uji, evaluasi *Completion Criteria*, daftar aset terarsip, pembersihan environment, & *Lessons Learned*. |
| **Automation & Evidence** | [`automation-scripts/`](./automation-scripts/) & [`evidence/`](./evidence/) | Skrip `test_gor_permata.py`, `test_performance_gor_permata.py`, `gor-permata.cy.js`, log TXT, metrik JSON, `performance-summary.md`, `00_flow_testing_gor_permata.png`, & 12 bukti visual (`01`–`12`). |
| **Laporan Resmi (Word & PDF)** | [`Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.docx`](../05-dokumentasi-laporan/Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.docx) & [`Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.pdf`](../05-dokumentasi-laporan/Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.pdf) | Dokumen laporan resmi berstandar **`>= 2022`** dengan bahasa Indonesia populer di folder `05-dokumentasi-laporan/` (dibangkitkan via [`generate_laporan_pengujian.py`](./generate_laporan_pengujian.py)), lengkap dengan diagram Flow Testing, alasan 5 teknik Black Box, penurunan ilmiah, step-by-step, dan 12 bukti visual (`01`–`12`). |

---

## 2. Ringkasan Cepat Temuan Utama (`IR-GOR-01` s.d. `IR-GOR-10`)

1. **`IR-GOR-01` (`BUG-GOR-01` — Major):** Endpoint `/register` mengembalikan `HTTP 404 Not Found`.
2. **`IR-GOR-02` (`BUG-GOR-02` — Minor):** `normPhone()` gagal menormalisasi awalan `+62 08...`.
3. **`IR-GOR-03` (`BUG-GOR-03` — Minor):** `#custName` meloloskan spasi `"   "` dan `1` huruf karena tidak ada `.trim()` & batas panjang minimum.
4. **`IR-GOR-04` (`BUG-GOR-04` — Major/High):** `205` elemen slot publik `/booking` menyematkan `data-phone` & `data-name` pelanggan di HTML publik serta skrip `manageBooking()` internal.
5. **`IR-GOR-05` (Major/High):** Query `?start_date=2020-01-01` (tanggal lampau) tetap merender `612` tombol booking aktif.
6. **`IR-GOR-06` (Major/High):** Query `?start_date=invalid-date` menyebabkan crash **`HTTP 500 Server Error`**.
7. **`IR-GOR-07` (Major/High — Performance):** Pada beban `10 VUs`, latensi `p95` `/booking` melonjak ke **`5314,28 ms`** (> batas SLA `3000 ms`).
8. **`IR-GOR-08` (Minor/Medium — Performance):** Ukuran HTML mentah `/booking` mencapai **`535,37 KB`** (`> 500 KB`).
9. **`IR-GOR-09` (Minor/Medium — Performance):** Spike *Cold-Start TTFB* `/` mencapai **`2618,3 ms`** (`FCP = 3028 ms`) sebelum turun ke `89,4 ms` saat *Warm Reload*.
10. **`IR-GOR-10` (Minor/Medium — Compatibility):** Navbar halaman `/` pada viewport mobile `390×844` memotong teks `LOGIN` dan mendorong tombol `BOOKING` keluar viewport (`right = 489 px`).

Rincian langkah reproduksi dan rekomendasi perbaikan masing-masing insiden tersedia pada [`incident-reports.md`](./incident-reports.md).
