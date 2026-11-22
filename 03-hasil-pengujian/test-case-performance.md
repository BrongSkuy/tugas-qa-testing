# Test Case & Test Procedure Specification — Performance Testing (`TD3` & `TD4`)

Dokumen ini mengimplementasikan aktivitas **`TD3` (*Derive test cases*)** dan **`TD4` (*Create test procedures*)** sesuai standar resmi **`>= 2022`** (**ISO/IEC/IEEE 29119-1:2022**, **29119-5:2024**, & **ISO/IEC 25010:2023** — *Performance Efficiency*) bersama model beban **Winasis, dkk. (2026)**, diturunkan dari [`../02-objek-umkm-dan-rencana-uji/test-model-performance.md`](../02-objek-umkm-dan-rencana-uji/test-model-performance.md) dengan konfigurasi profil beban pada [`test-data/performance-profiles.json`](./test-data/performance-profiles.json).

---

## 1. *Test Case Specification* Performance (`TD3` — `TC-PERF-01` s.d. `TC-PERF-10`)

| ID TC | Prioritas | TCI Terkait | Prasyarat (*Preconditions*) | Skenario & Parameter Uji | Expected Result / SLA Target |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **`TC-PERF-01`** | Tinggi | `TCI-PERF-01` | BrowserContext baru (*Cold Cache*), Desktop `1280×800` | Buka `/` dan rekam `TTFB`, `DCL`, `Load`, `FCP`, `LCP`, `CLS` | `TTFB <= 800 ms`, `FCP <= 3000 ms`, `LCP <= 4000 ms`, `CLS <= 0.25`. |
| **`TC-PERF-02`** | Tinggi | `TCI-PERF-02` | BrowserContext baru (*Cold Cache*), Desktop `1280×800` | Buka `/booking?start_date=<besok>` dan rekam metrik Web Vitals | `TTFB <= 1800 ms`, `FCP <= 3000 ms`, `LCP <= 4000 ms`, `CLS <= 0.25`. |
| **`TC-PERF-03`** | Sedang | `TCI-PERF-03` | BrowserContext baru (*Cold Cache*), Desktop `1280×800` | Buka `/login` dan `/fasilitas/lapangan`, rekam metrik Web Vitals masing-masing | Kedua rute memenuhi `TTFB <= 800 ms`, `FCP <= 3000 ms`, `LCP <= 4000 ms`. |
| **`TC-PERF-04`** | Sedang | `TCI-PERF-04` | Konteks yang baru selesai memuat rute pada `TC-PERF-01/02` | Muat ulang (*Warm Cache*) `/` dan `/booking?start_date=<besok>`, bandingkan waktu *Load* & *transferSize* vs *Cold Cache* | *Warm Load* & *Transfer Bytes* lebih rendah atau setara *Cold Cache* tanpa error aset. |
| **`TC-PERF-05`** | Tinggi | `TCI-PERF-05` | BrowserContext baru (*Cold Cache*), Mobile `390×844` | Buka `/` dan `/booking?start_date=<besok>` pada viewport seluler, rekam Web Vitals | `TTFB <= batas SLA`, `LCP <= 4000 ms`, `CLS <= 0.25` di layar mobile. |
| **`TC-PERF-06`** | Tinggi | `TCI-PERF-06` | `PerformanceResourceTiming` & HTTP headers aktif | Audit ukuran *HTML raw*, *Brotli (`br`)/Gzip encoded bytes*, jumlah total request aset per halaman, dan header `Cache-Control` | Rasio kompresi terukur baik (`br`/`gzip` aktif); tidak ada aset gagal muat (`HTTP >= 400`); catat jika *HTML raw* `/booking` > `500 KB`. |
| **`TC-PERF-07`** | Sedang | `TCI-PERF-07` | `/booking?start_date=<besok>` terbuka di Chromium | Ukur latensi klien saat memanggil `openBooking()`, 4× perubahan `updateTotal()`, dan reload `changeDate()` | Interaksi DOM lokal (`openBooking`, `updateTotal`) `<= 250 ms`. |
| **`TC-PERF-08`** | Tinggi | `TCI-PERF-08` | Engine `aiohttp`, *circuit breaker* aktif, `GET`-only | Jalankan **Level A (`1 VU`, 6 putaran × 4 rute = 24 req)** dengan `think_time = 250 ms` | `Error Rate = 0%`, `p95` `/` & `/login` `<= 1500 ms`, `p95` `/booking` `<= 3000 ms`. |
| **`TC-PERF-09`** | Tinggi | `TCI-PERF-09` | Cool-down `2s` pasca Level A selesai | Jalankan **Level B (`5 VUs`, 2 putaran × 4 rute = 40 req)** dengan `think_time = 500 ms` | `Error Rate = 0%`, `p95` tetap di bawah batas SLA tanpa `HTTP 429/5xx`. |
| **`TC-PERF-10`** | Tinggi | `TCI-PERF-10` | Cool-down `2s` pasca Level B selesai | Jalankan **Level C (`10 VUs`, 1 putaran × 4 rute = 40 req)** dengan `think_time = 500 ms` | `Error Rate = 0%`, tidak ada `HTTP 429/5xx`, hitung rasio degradasi `p95` terhadap `1 VU`. |

---

## 2. *Test Procedure Specification* (`TD4` — `PROC-PERF-01` s.d. `PROC-PERF-03`)

Diotomatiskan pada [`automation-scripts/test_performance_gor_permata.py`](./automation-scripts/test_performance_gor_permata.py):

- **`PROC-PERF-01` (Frontend Web Vitals, Caching, & Resource Profiling):**
  1. `STEP-1`: Muat `test-data/performance-profiles.json` dan siapkan browser Chromium headless.
  2. `STEP-2`: Jalankan `TC-PERF-01`, `TC-PERF-02`, `TC-PERF-03` (*Cold Cache Desktop*), dilanjutkan `TC-PERF-04` (*Warm Cache*), lalu `TC-PERF-06` (audit payload + kompresi `br`/`gzip`).
  3. `STEP-3`: Buka konteks baru viewport `Mobile (390×844)` dan jalankan `TC-PERF-05`.
- **`PROC-PERF-02` (Client DOM Interaction Latency):**
  1. `STEP-4`: Pada halaman `/booking?start_date=<besok>`, jalankan `TC-PERF-07` (`openBooking`, `updateTotal`, `changeDate`), tutup browser Playwright.
- **`PROC-PERF-03` (Tiered Concurrent HTTP `GET` Benchmark & Wrap-up):**
  1. `STEP-5`: Jalankan `TC-PERF-08` (`1 VU`) -> jeda `2s` -> `TC-PERF-09` (`5 VUs`) -> jeda `2s` -> `TC-PERF-10` (`10 VUs`) dengan *auto-abort* bila error > `5%`.
  2. `STEP-6`: Simpan statistik JSON ke [`evidence/performance-metrics.json`](./evidence/performance-metrics.json) dan log mentah ke [`automation-scripts/performance-log.txt`](./automation-scripts/performance-log.txt).

---

## 3. *End-to-End Traceability Matrix* (Performance — `8.2.4.5 e`)

| Test Basis | Test Model (`TD1`) | TCI (`TD2`) | Test Case (`TD3`) | Test Procedure (`TD4`) |
| :--- | :--- | :--- | :--- | :--- |
| `TB-PERF-01` | `TM-PERF-01` | `TCI-PERF-01..03`, `TCI-PERF-05` | `TC-PERF-01..03`, `TC-PERF-05` | `PROC-PERF-01` (`test_performance_gor_permata.py`) |
| `TB-PERF-02` | `TM-PERF-01` | `TCI-PERF-04`, `TCI-PERF-06` | `TC-PERF-04`, `TC-PERF-06` | `PROC-PERF-01` (`test_performance_gor_permata.py`) |
| `TB-PERF-03` | `TM-PERF-02` | `TCI-PERF-07` | `TC-PERF-07` | `PROC-PERF-02` (`test_performance_gor_permata.py`) |
| `TB-PERF-04` | `TM-PERF-03` | `TCI-PERF-08..10` | `TC-PERF-08..10` | `PROC-PERF-03` (`test_performance_gor_permata.py`) |

---

## 4. Panduan *Step-by-Step* Menguji Kecepatan Website (Langkah 1 s.d. 6)

1. **Langkah 1 — Siapkan Pengaturan Uji Kecepatan:** Pastikan `playwright` dan `aiohttp` sudah terinstal. Pengaturan beban aman disimpan di `test-data/performance-profiles.json`: hanya membaca (`GET`) 4 halaman utama (`/`, `/booking`, `/login`, `/fasilitas/lapangan`) dan otomatis berhenti jika error > `5%`.
2. **Langkah 2 — Jalankan Program Uji Kecepatan:** Ketik satu perintah ini di terminal:
   ```bash
   python 03-hasil-pengujian/automation-scripts/test_performance_gor_permata.py
   ```
3. **Langkah 3 — Ukur Kecepatan Tampil Pertama vs Buka Ulang (`PROC-PERF-01`):** Program membuka beranda, jadwal, login, & fasilitas di layar laptop (`1280×800`) dan HP (`390×844`), mencatat berapa milidetik halaman mulai muncul (`TTFB`, `FCP`, `Load`) dan besar ukuran file HTML-nya.
4. **Langkah 4 — Ukur Respons Klik Tombol (`PROC-PERF-02`):** Di halaman `/booking`, program mengukur seberapa cepat form pesan terbuka, perhitungan tarif diperbarui, dan tanggal diganti.
5. **Langkah 5 — Simulasi `1`, `5`, dan `10` Pengunjung Bersamaan (`PROC-PERF-03`, Mengacu Winasis dkk. 2026):** Program menyimulasikan **`1` orang (`24` akses)** -> istirahat 2 detik -> **`5` orang bersamaan (`40` akses)** -> istirahat 2 detik -> **`10` orang bersamaan (`40` akses)** = total **`104` kali buka halaman**.
6. **Langkah 6 — Cek Hasil & Catat Halaman yang Lambat:** Lihat [`performance-log.txt`](./automation-scripts/performance-log.txt), [`performance-metrics.json`](./evidence/performance-metrics.json), dan grafik `12_performance_latency_chart.png`. Temuan lambat dicatat ke [`incident-reports.md`](./incident-reports.md): halaman `/booking` melambat ke `5,31 detik` saat dibuka `10` orang (`IR-GOR-07`), ukuran HTML `/booking` `535,37 KB` (`IR-GOR-08`), dan buka awal beranda sempat `2,62 detik` (`IR-GOR-09`).
