# Test Execution Log & Results (`TE1`–`TE3`)

Dokumen ini merupakan rekaman resmi **Test Execution Process (`8.4`, aktivitas `TE1–TE3`)** dan *Information Items* (`Actual Results`, `Test Results`, `Test Execution Log`) sesuai **ISO/IEC/IEEE 29119-2:2021(E)** untuk seluruh pengujian **Black Box** dan **Performance Testing** pada **Portal Booking GOR Permata Badminton Hall** (`https://gorpermatabadminton.com`).

---

## 1. Informasi Sesi Eksekusi

| Jenis Suite | Skrip Pelaksana | Timestamp Eksekusi | Ringkasan Hasil | Bukti Log & JSON Mentah |
| :--- | :--- | :--- | :---: | :--- |
| **Black Box Testing (`TC-BB-01..22`)** | [`test_gor_permata.py`](./automation-scripts/test_gor_permata.py) | `2026-11-17T22:06:36+07:00` | **`15 / 22 PASS`**, `7 FAIL` *(temuan cacat)*, **`0` Network POST Terkirim** | [`execution-log.txt`](./automation-scripts/execution-log.txt) & [`blackbox-results.json`](./evidence/blackbox-results.json) |
| **Performance Testing (`TC-PERF-01..10`)** | [`test_performance_gor_permata.py`](./automation-scripts/test_performance_gor_permata.py) | `2026-11-17T22:05:00+07:00` | **`7 / 10 PASS`**, `3 FAIL` *(temuan bottleneck/SLA)*, **`0,0%` HTTP Error** | [`performance-log.txt`](./automation-scripts/performance-log.txt) & [`performance-metrics.json`](./evidence/performance-metrics.json) |
| **Cypress E2E Suite** | [`gor-permata.cy.js`](./automation-scripts/gor-permata.cy.js) | *Tidak dieksekusi lokal* | **Not Run** *(biner `cypress` belum terpasang; logika dicover penuh di Playwright)* | [`test-environment-dan-data.md`](./test-environment-dan-data.md#2-test-environment-readiness-report-8342-b-c--835-b) |

---

## 2. Log Hasil Eksekusi Black Box Testing (`TC-BB-01` s.d. `TC-BB-22`)

| ID TC | Nama Uji | Expected Result | Actual Result Teramati | Status | Ref. Insiden |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **`TC-BB-01`** | Rute Publik HTTP 200 | Semua 7 rute publik `HTTP 200 OK` | `/`, `/booking`, `/login`, `/fasilitas/{lapangan,umum,tunggu,parkir}` semua `200`; `0` console error | **PASS** | — |
| **`TC-BB-02`** | Endpoint `/register` | `HTTP 200 OK` atau redirect aktif | Mengembalikan `HTTP 404 Not Found` (bukti: `04_register_404.png`) | **FAIL** | `IR-GOR-01` |
| **`TC-BB-03`** | Query `?start_date=2026-11-18` | `jumpDate=2026-11-18`, slot > 0 | `jumpDate=2026-11-18`, ditemukan `407` slot `openBooking()` aktif | **PASS** | — |
| **`TC-BB-04`** | Query `?start_date=2020-01-01` | `0` slot aktif di masa lalu | Masih merender **`612` slot `openBooking()`** aktif | **FAIL** | `IR-GOR-05` |
| **`TC-BB-05`** | Query `?start_date=invalid-date` | Fallback aman (`!= 500`) | Server crash **`HTTP 500 Server Error`** (bukti: `05_invalid_date_500.png`) | **FAIL** | `IR-GOR-06` |
| **`TC-BB-06`** | State Transition Buka Modal | `visible=True`, durasi=`1`, total=`Rp 40.000` | `visible=True`, `durasi=1`, `dispTotal='Rp 40.000'` | **PASS** | — |
| **`TC-BB-07`** | Kalkulasi Tarif `1..5` Jam | `40.000` s.d. `200.000` | `{'1': 'Rp 40.000', '2': 'Rp 80.000', '3': 'Rp 120.000', '4': 'Rp 160.000', '5': 'Rp 200.000'}` | **PASS** | — |
| **`TC-BB-08`** | Decision R1: Nama & WA Kosong | Alert wajib isi, `delta_post=0` | Alert `'⚠️Halo kak! Nama dan Nomor WA harus diisi lengkap!'`, `delta_post=0` | **PASS** | — |
| **`TC-BB-09`** | BVA `#custName` `"   "` & `"A"` | Ditolak di klien (`delta_post=0`) | Keduanya lolos validasi klien dan menyentuh `fetch` (`delta_post=1` masing-masing, dicegat interceptor) | **FAIL** | `IR-GOR-03` |
| **`TC-BB-10`** | EP Format WA Invalid (`12345`, `abc`) | Alert format WA, `delta_post=0` | Alert `'⚠️ Nomor WA belum benar...'`, `deltas=[0, 0]` | **PASS** | — |
| **`TC-BB-11`** | BVA WA `10` Digit (`081234567`) | Ditolak regex, `delta_post=0` | Ditolak alert format WA, `delta_post=0` | **PASS** | — |
| **`TC-BB-12`** | BVA WA `11` Digit (`0812345678`) | Lolos regex, dicegat (`delta_post=1`) | Lolos validasi klien, dicegat interceptor (`delta_post=1`), `.catch()` tampil | **PASS** | — |
| **`TC-BB-13`** | BVA WA `14` Digit (`0812345678901`) | Lolos regex, dicegat (`delta_post=1`) | Lolos validasi klien, dicegat interceptor (`delta_post=1`), `.catch()` tampil | **PASS** | — |
| **`TC-BB-14`** | BVA WA `15` Digit (`08123456789012`) | Ditolak regex, `delta_post=0` | Ditolak alert format WA, `delta_post=0` | **PASS** | — |
| **`TC-BB-15`** | EP Prefiks `8...` & `628...` | Keduanya lolos (`delta_post=1`) | `prefix_8_delta=1`, `prefix_628_delta=1` | **PASS** | — |
| **`TC-BB-16`** | Edge Case `+62 08123456789` | Dinormalisasi ke `628...` | Ditolak regex (`6208...`), `delta_post=0` | **FAIL** | `IR-GOR-02` |
| **`TC-BB-17`** | BVA Tutup `00:00` (`22:00 + 3` Jam) | Alert tutup `00:00`, `delta_post=0` | Alert `'🚨 GAGAL! GOR Permata tutup jam 00:00...'`, `delta_post=0` | **PASS** | — |
| **`TC-BB-18`** | BVA Tutup `00:00` (`22:00 + 2` Jam) | Lolos batas tutup (`delta_post=1`) | Lolos validasi jam tutup, dicegat interceptor (`delta_post=1`) | **PASS** | — |
| **`TC-BB-19`** | State Transition `closeModal()` | `hidden=True`, input kosong | `hidden=True`, `cleared=True` | **PASS** | — |
| **`TC-BB-20`** | Form `/login` (CSRF & HTML5) | `_token` ada, invalid ditolak HTML5 | `hasToken=True`, `emptyValid=False`, `badEmailValid=False`, `missingPassValid=False` | **PASS** | — |
| **`TC-BB-21`** | Kompatibilitas Mobile `390×844` | Tidak ada overflow/clip navbar, modal muat | `home` & `booking` `scrollWidth=390`, modal muat (`350px`), namun **`clippedNavLinks=[{'text': 'BOOKING', 'right': 489}]`** (bukti: `07_home_mobile.png`) | **FAIL** | `IR-GOR-10` |
| **`TC-BB-22`** | Privasi DOM Publik (`manageBooking`) | `withPhone=0` di HTML publik | `total_slot_terisi=205`, `withPhone=205`, `withName=205` (tanpa pencatatan PII) | **FAIL** | `IR-GOR-04` |

> **Verifikasi Guardrail Non-Destruktif (`8.4`):** Sebanyak `7` pemanggilan `fetch('/bookings/store')` yang lolos validasi klien berhasil dicegat interceptor di dalam browser (`intercepted_post_attempts_inside_browser = 7`) dengan **`network_posts_sent_to_server = 0`**.

---

## 3. Log Hasil Eksekusi Performance Testing (`TC-PERF-01` s.d. `TC-PERF-10`)

Ringkasan lengkap tersedia pada [`evidence/performance-summary.md`](./evidence/performance-summary.md) dan [`evidence/performance-metrics.json`](./evidence/performance-metrics.json):

| ID TC | Skenario Uji Performa | Target SLA | Actual Result Terukur | Status | Ref. Insiden |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **`TC-PERF-01`** | Web Vitals Cold Desktop `/` | `TTFB<=800ms`, `FCP<=3000ms`, `CLS<=0.25` | `TTFB=2618,3ms`, `DCL=3031,1ms`, `Load=3343,4ms`, `FCP=3028ms`, `CLS=0` | **FAIL** | `IR-GOR-09` |
| **`TC-PERF-02`** | Web Vitals Cold Desktop `/booking` | `TTFB<=1800ms`, `FCP<=3000ms`, `CLS<=0.25` | `TTFB=1213,0ms`, `DCL=1722,2ms`, `Load=1826,2ms`, `FCP=1712ms`, `CLS=0` | **PASS** | — |
| **`TC-PERF-03`** | Web Vitals Cold `/login` & `/fasilitas/lapangan` | `TTFB<=800ms`, `FCP<=3000ms` | `/login` (`TTFB=98,9ms`, `FCP=572ms`); `/fasilitas/lapangan` (`TTFB=95,9ms`, `FCP=620ms`) | **PASS** | — |
| **`TC-PERF-04`** | Warm vs Cold Cache (`/`, `/booking`) | Warm load tanpa error aset | `/`: Cold `3343,4ms` -> Warm `289,3ms`; `/booking`: Cold `1826,2ms` -> Warm `1155,2ms`; `0` failed assets | **PASS** | — |
| **`TC-PERF-05`** | Web Vitals Mobile `390×844` | `/` `TTFB<=800`, `/booking` `<=1800`, `FCP<=3000` | Mobile `/`: `TTFB=108,2ms`, `FCP=708ms`; Mobile `/booking`: `TTFB=1016,5ms`, `FCP=1580ms` | **PASS** | — |
| **`TC-PERF-06`** | Payload & Kompresi HTML `/booking` | HTML raw `<= 500 KB`, `0` failed assets | HTML raw **`535,37 KB`** (`548.217 B`), encoded `br` `34,78 KB`, `5` aset (`27,5 KB`) | **FAIL** | `IR-GOR-08` |
| **`TC-PERF-07`** | Client DOM Interaction Latency | `<= 250 ms` | `openBooking=62,93ms`, `updateTotal avg=8,11ms (max 13,94ms)`, `changeDate=3,03ms` | **PASS** | — |
| **`TC-PERF-08`** | Concurrent HTTP Level A (`1 VU`) | `Error=0%`, `p95` sesuai SLA | `24 req`, `0,0% err`, `1,87 rps`, `p50=70,34ms`, `p95=966,44ms`, `/booking p95=1033,24ms` | **PASS** | — |
| **`TC-PERF-09`** | Concurrent HTTP Level B (`5 VUs`) | `Error=0%`, `p95` sesuai SLA | `40 req`, `0,0% err`, `4,54 rps`, `p50=88,75ms`, `p95=2181,37ms`, `/booking p95=2249,31ms` | **PASS** | — |
| **`TC-PERF-10`** | Concurrent HTTP Level C (`10 VUs`) | `Error=0%`, `p95 /booking <= 3000ms` | `40 req`, `0,0% err`, `4,97 rps`, `p50=280,39ms`, **`/booking p95=5314,28ms`** (`max=5323,45ms`) | **FAIL** | `IR-GOR-07` |

---

## 4. Indeks Bukti Tangkapan Layar (`evidence/screenshots/`)
- [`01_home_desktop.png`](./evidence/screenshots/01_home_desktop.png) — Beranda pada desktop `1280×800`
- [`02_booking_grid_desktop.png`](./evidence/screenshots/02_booking_grid_desktop.png) — Grid jadwal `/booking` (label slot disamarkan `[TERISI]`)
- [`03_booking_modal_desktop.png`](./evidence/screenshots/03_booking_modal_desktop.png) — Modal `#bookingModal` pada desktop (`TC-BB-06`)
- [`04_register_404.png`](./evidence/screenshots/04_register_404.png) — Bukti defect `HTTP 404 Not Found` pada `/register` (`IR-GOR-01`)
- [`05_invalid_date_500.png`](./evidence/screenshots/05_invalid_date_500.png) — Bukti defect `HTTP 500 Server Error` pada `?start_date=invalid-date` (`IR-GOR-06`)
- [`06_login_page.png`](./evidence/screenshots/06_login_page.png) — Halaman `/login` admin (`TC-BB-20`)
- [`07_home_mobile.png`](./evidence/screenshots/07_home_mobile.png) — Bukti pemotongan navbar pada viewport mobile `390×844` (`IR-GOR-10`)
- [`08_booking_modal_mobile.png`](./evidence/screenshots/08_booking_modal_mobile.png) — Modal `#bookingModal` pada viewport mobile `390×844` (`TC-BB-21`)
