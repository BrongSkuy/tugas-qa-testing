# Incident / Defect Reports (`IR1`–`IR2`)

Dokumen ini mengimplementasikan **Test Incident Reporting Process (`IR1–IR2`)** sesuai standar **`>= 2022`** (**ISO/IEC/IEEE 29119-1:2022**, **ISO/IEC 25010:2023**, & **ISO/IEC 40500:2025 / WCAG 2.2**). Seluruh `10` insiden (`IR-GOR-01` s.d. `IR-GOR-10`) berasal dari **2 pengujian utama proyek** — **Black Box Testing (`TC-BB-*`)** dan **Performance Testing (`TC-PERF-*`)** — pada `https://gorpermatabadminton.com`.

---

## 0. Ringkasan Dokumen & Cara Pakai Script

- **Dokumen ini isinya apa?** Ini adalah **"Daftar `10` Masalah / Bug yang Ditemukan"** (`IR-GOR-01` s.d. `IR-GOR-10`) dari hasil eksekusi pengujian website GOR Permata (`7` masalah dari **23 uji Black Box** yang mencatat `16 Pass, 7 Fail`, dan `3` masalah dari **10 uji Performance** yang mencatat `7 Pass, 3 Fail`) — misalnya link `/register` error `404`, format nomor `+62 08...` ditolak, tanggal tahun `2020` masih bisa diklik, parameter tanggal rusak bikin `HTTP 500`, nomor HP pemesan muncul di HTML halaman publik, halaman `/booking` melambat ke `5,31 detik` saat dibuka `10` orang, dan tombol menu terpotong di layar HP.
- **Apakah ada script yang harus di-copy-paste dari dokumen ini?** **Tidak ada.** Semua potongan kode atau rumus di dalam dokumen ini (`normPhone()`, `.trim()`, `Carbon::parse`) hanyalah **saran perbaikan untuk pembuat/developer website GOR Permata**—**bukan** perintah untuk Terminal kamu. Jika ingin mengecek ulang temuan secara otomatis, cukup **copy-paste perintah ini ke Terminal (CMD / PowerShell)** dari folder utama `tugas-qa-testing`:
  ```bash
  python 03-hasil-pengujian/automation-scripts/test_gor_permata.py
  python 03-hasil-pengujian/automation-scripts/test_performance_gor_permata.py
  ```

---

## 1. Ringkasan Status Siklus Hidup Insiden

| ID Insiden | Cross-Ref Lama | TC Pemicu | Kategori | Severity | Priority | Status | Ringkasan Masalah |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **`IR-GOR-01`** | `BUG-GOR-01` | `TC-BB-02` | Functional | Major | Medium | **Open** | Endpoint `/register` mengembalikan `HTTP 404 Not Found` |
| **`IR-GOR-02`** | `BUG-GOR-02` | `TC-BB-16` | Validation (Black Box) | Minor | Medium | **Open** | `normPhone()` gagal menormalisasi awalan `+62 08...` |
| **`IR-GOR-03`** | `BUG-GOR-03` | `TC-BB-09` | Validation / UX | Minor | Low | **Open** | `#custName` meloloskan spasi `"   "` dan `1` huruf di klien |
| **`IR-GOR-04`** | `BUG-GOR-04` | `TC-BB-22` | Security / Privacy | **Major** | **High** | **Open** | DOM publik `/booking` menyematkan `data-phone` & `data-name` (`205` slot) + fungsi internal `manageBooking()` |
| **`IR-GOR-05`** | *(Temuan Baru)* | `TC-BB-04` | Functional / Validation | Major | High | **Open** | `?start_date=2020-01-01` (tanggal lampau) merender `612` slot booking aktif |
| **`IR-GOR-06`** | *(Temuan Baru)* | `TC-BB-05` | Error Handling | **Major** | **High** | **Open** | `?start_date=invalid-date` memicu crash **`HTTP 500 Server Error`** |
| **`IR-GOR-07`** | *(Temuan Baru)* | `TC-PERF-10` | Performance (Concurrency) | **Major** | **High** | **Open** | Latensi `/booking` melonjak ke `p95 = 5314,28 ms` pada `10 VUs` (> SLA `3000 ms`) |
| **`IR-GOR-08`** | *(Temuan Baru)* | `TC-PERF-06` | Performance (Payload) | Minor | Medium | **Open** | HTML mentah `/booking` mencapai `535,37 KB` (`> 500 KB`) |
| **`IR-GOR-09`** | *(Temuan Baru)* | `TC-PERF-01` | Performance (TTFB Spike) | Minor | Medium | **Open** | Spike *Cold-Start TTFB* `/` mencapai `2618,3 ms` (`FCP = 3028 ms`) |
| **`IR-GOR-10`** | *(Temuan Baru)* | `TC-BB-21` | Compatibility / UI Mobile | Minor | Medium | **Open** | Navbar di mobile `390×844` memotong teks `LOGIN` & mendorong `BOOKING` ke `x = 489px` |

---

## 2. Rincian Laporan Insiden

### `IR-GOR-01` (`BUG-GOR-01`): Endpoint `/register` Mengembalikan `HTTP 404 Not Found`
- **Terkait TC / TCI:** `TC-BB-02` / `TCI-BB-02` | **Status:** `Open` | **Action Owner:** Developer Portal GOR Permata
- **Steps to Reproduce:** Akses `https://gorpermatabadminton.com/register` melalui `HTTP GET`.
- **Expected vs Actual:** Diharapkan tampil halaman pendaftaran anggota atau redirect informasi ke WhatsApp admin; aktual mengembalikan **`HTTP 404 Not Found`**.
- **Bukti & Rekomendasi:** [`04_register_404.png`](./evidence/screenshots/04_register_404.png). Tambahkan rute informasi registrasi atau hapus seluruh referensi `/register`.

### `IR-GOR-02` (`BUG-GOR-02`): `normPhone()` Gagal Menormalisasi Awalan `+62 08...`
- **Terkait TC / TCI:** `TC-BB-16` / `TCI-BB-16` | **Status:** `Open` | **Action Owner:** Developer Frontend `/booking`
- **Steps to Reproduce:** Buka modal slot kosong di `/booking`, isi `#custName = "Test QA"`, `#custPhone = "+62 08123456789"`, klik `#btnSubmit`.
- **Expected vs Actual:** Diharapkan dinormalisasi menjadi `628123456789`; aktual kondisi `if (d.startsWith('62')) return d;` langsung mengembalikan `6208123456789` sehingga ditolak regex `/^628\d{8,11}$/` dengan alert error.
- **Rekomendasi:** Ubah logika normalisasi menjadi `if (d.startsWith('620')) d = '62' + d.slice(3);` sebelum validasi regex.

### `IR-GOR-03` (`BUG-GOR-03`): `#custName` Meloloskan Spasi `"   "` dan `1` Karakter di Klien
- **Terkait TC / TCI:** `TC-BB-09` / `TCI-BB-09` | **Status:** `Open` | **Action Owner:** Developer Frontend `/booking`
- **Steps to Reproduce:** Buka modal booking, isi `#custName = "   "` (atau `"A"`) dan `#custPhone = "0812345678"`, klik `#btnSubmit`.
- **Expected vs Actual:** Diharapkan ditolak di sisi klien (`delta_post = 0`); aktual lolos pengecekan `if (!name || !phone)` dan langsung memanggil `fetch('/bookings/store')` (`delta_post = 1`, berhasil dicegat interceptor uji).
- **Rekomendasi:** Gunakan `.trim()` dan wajibkan panjang minimal (mis. `name.trim().length >= 2`).

### `IR-GOR-04` (`BUG-GOR-04`): Eksposur Atribut `data-phone` & `data-name` (`205` Slot) serta Skrip Internal di DOM Publik `/booking`
- **Terkait TC / TCI:** `TC-BB-22` / `TCI-BB-22` | **Status:** `Open` | **Action Owner:** Developer Backend & Keamanan
- **Steps to Reproduce:** Buka `https://gorpermatabadminton.com/booking` dan inspeksi elemen `[onclick*="manageBooking"]` di HTML publik.
- **Expected vs Actual:** Halaman publik semestinya hanya menampilkan status ketersediaan slot tanpa menyematkan nomor telepon pelanggan dan kode admin (`manageBooking`, teks `"Hubungi Koko atau Aan."`, endpoint `/bookings/confirm|reject|delete`). Aktual ditemukan `205` elemen slot memuat `data-phone` dan `data-name` terisi di HTML publik.
- **Rekomendasi:** Hapus atribut `data-phone` dan detail PII pelanggan dari view publik `/booking` dan pisahkan file JS panel admin agar hanya dimuat setelah login terautentikasi. *(Catatan: Nilai PII nyata sengaja tidak disimpan maupun dicetak di repositori ini.)*

### `IR-GOR-05`: Parameter Tanggal Masa Lalu (`?start_date=2020-01-01`) Tetap Merender `612` Slot Booking Aktif
- **Terkait TC / TCI:** `TC-BB-04` / `TCI-BB-04` | **Status:** `Open` | **Action Owner:** Developer Backend `/booking`
- **Steps to Reproduce:** Buka `https://gorpermatabadminton.com/booking?start_date=2020-01-01`.
- **Expected vs Actual:** Diharapkan tanggal sebelum hari ini menonaktifkan tombol `openBooking` (`0` slot aktif) atau mengarahkan ke tanggal hari ini; aktual halaman merender **`612` tombol `openBooking(...)`** yang masih bisa diklik dan dibuka modal pemesanannya.
- **Bukti & Rekomendasi:** [`11_past_date_2020_bug.png`](./evidence/screenshots/11_past_date_2020_bug.png). Batasi `start_date >= today` pada controller backend serta beri atribut `min` pada `#jumpDate` dan nonaktifkan tombol booking untuk jam/tanggal yang sudah lewat.

### `IR-GOR-06`: Parameter `?start_date=invalid-date` Menyebabkan Crash `HTTP 500 Server Error`
- **Terkait TC / TCI:** `TC-BB-05` / `TCI-BB-05` | **Status:** `Open` | **Action Owner:** Developer Backend `/booking`
- **Steps to Reproduce:** Akses `https://gorpermatabadminton.com/booking?start_date=invalid-date`.
- **Expected vs Actual:** Diharapkan validasi query parameter mengembalikan fallback tanggal hari ini atau `HTTP 400/422`; aktual server melempar unhandled exception **`HTTP 500 Server Error`**.
- **Bukti & Rekomendasi:** [`05_invalid_date_500.png`](./evidence/screenshots/05_invalid_date_500.png). Bungkus parsing tanggal (`Carbon::parse`) dengan blok `try/catch` atau Laravel Request Validation agar jatuh aman ke `today()`.

### `IR-GOR-07`: Degradasi Latensi `/booking` di Bawah Konkurensi `10 VUs` (`p95 = 5314,28 ms`)
- **Terkait TC / TCI:** `TC-PERF-10` / `TCI-PERF-10` | **Status:** `Open` | **Action Owner:** Developer Backend & Infrastruktur
- **Steps to Reproduce:** Jalankan [`test_performance_gor_permata.py`](./automation-scripts/test_performance_gor_permata.py) Level C (`10 VUs`, `GET`-only, `think_time=500ms`).
- **Expected vs Actual:** Target SLA `p95 /booking <= 3000 ms`; aktual `mean = 4932,01 ms`, `p50 = 5138,42 ms`, **`p95 = 5314,28 ms`**, `max = 5323,45 ms` (`5,14x` lebih lambat dari `1 VU` baseline `p95 = 1033,24 ms`), sementara rute `/`, `/login`, dan `/fasilitas/lapangan` tetap `< 400 ms`.
- **Bukti & Rekomendasi:** [`12_performance_latency_chart.png`](./evidence/screenshots/12_performance_latency_chart.png), [`performance-summary.md`](./evidence/performance-summary.md), & [`performance-metrics.json`](./evidence/performance-metrics.json). Tambahkan indeks query database jadwal, cache short-TTL (mis. 15–30 detik) untuk grid publik, atau muat data slot secara asinkron via endpoint JSON ringan.

### `IR-GOR-08`: Pembengkakan Ukuran HTML Mentah `/booking` (`535,37 KB`)
- **Terkait TC / TCI:** `TC-PERF-06` / `TCI-PERF-06` | **Status:** `Open` | **Action Owner:** Developer Frontend / Backend
- **Steps to Reproduce:** Muat `/booking?start_date=<besok>` melalui Playwright dan baca `PerformanceNavigationTiming.decodedBodySize`.
- **Expected vs Actual:** Target HTML un-compressed `<= 500 KB`; aktual **`548.217 bytes` (`535,37 KB`)** akibat rendering seluruh grid 7 hari dalam satu dokumen HTML plus CSS/JS inline (meski `br` mengompres transfer ke `34,78 KB`).
- **Rekomendasi:** Render 1–3 hari aktif secara default atau pakai pagination/JSON API agar ukuran DOM dan waktu parsing berkurang signifikan.

### `IR-GOR-09`: Fluktuasi *Cold-Start TTFB* Beranda `/` (`2618,3 ms`)
- **Terkait TC / TCI:** `TC-PERF-01` / `TCI-PERF-01` | **Status:** `Open` | **Action Owner:** Developer Backend / Konfigurasi Hosting
- **Steps to Reproduce:** Buka `/` pada konteks Chromium *Cold Cache* (`1280×800`).
- **Expected vs Actual:** Target `TTFB <= 800 ms` dan `FCP <= 3000 ms`; aktual pada *Cold Desktop* terjadi spike `TTFB = 2618,3 ms` (`FCP = 3028 ms`, `Load = 3343,4 ms`), sementara *Warm Reload* hanya `TTFB = 89,4 ms` (`Load = 289,3 ms`) dan *Cold Mobile* `108,2 ms`.
- **Rekomendasi:** Pertimbangkan caching halaman beranda statis/semi-statis di level aplikasi atau edge CDN (`Cache-Control` publik untuk bagian non-sensitif) untuk mencegah latensi *cold origin miss*.

### `IR-GOR-10`: Pemotongan Navbar pada Viewport Mobile `390×844`
- **Terkait TC / TCI:** `TC-BB-21` / `TCI-BB-21` | **Status:** `Open` | **Action Owner:** Developer Frontend
- **Steps to Reproduce:** Buka `https://gorpermatabadminton.com/` pada viewport `390×844`.
- **Expected vs Actual:** Seluruh tautan menu header harus muat atau masuk ke hamburger menu dalam lebar `390 px`; aktual menu `LOGIN` terpotong menjadi `LOGI` dan tombol `BOOKING` terdorong hingga `right = 489 px` di luar layar (`clippedNavLinks: [{'text': 'BOOKING', 'right': 489}]`).
- **Bukti & Rekomendasi:** [`07_home_mobile.png`](./evidence/screenshots/07_home_mobile.png). Sederhanakan label menu atau implementasikan menu responsif (*collapse/hamburger*) di bawah breakpoint `640px`.
