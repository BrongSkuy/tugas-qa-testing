# Performance Test Plan: Portal Booking GOR Permata Badminton Hall

Dokumen ini merupakan rencana uji spesifik untuk jenis pengujian performa (**`TP-GOR-PERF-01`**) sesuai standar acuan **`>= 2022`** (**ISO/IEC/IEEE 29119-1:2022**, **ISO/IEC/IEEE 29119-5:2024**, & **ISO/IEC 25010:2023** — *Performance Efficiency*) serta metode uji beban bertingkat **Winasis, dkk. (2026)** (*Sinkron, SINTA 3*), yang melengkapi *Master Test Plan* [`TP-GOR-01`](./test-plan-gor-permata.md).

---

## 1. Tujuan & Ruang Lingkup Uji Performa (`TP1`)

### 1.1 Tujuan Pengujian
Mengukur secara objektif dan berulang tingkat efisiensi waktu (*Time Behaviour*), pemanfaatan sumber daya (*Resource Utilization*), dan kapasitas aman (*Capacity*) pada **Portal Booking GOR Permata Badminton Hall** (`https://gorpermatabadminton.com`) tanpa mengganggu operasional layanan UMKM.

### 1.2 Rute & Komponen yang Diuji (*In Scope*)
1. **Halaman Beranda (`/`)** — Landing page, ringkasan jadwal, aset statis & CDN.
2. **Halaman Jadwal & Booking (`/booking` & `/booking?start_date=<besok>`)** — Halaman paling berat karena merender seluruh tabel grid slot mingguan beserta skrip inline (`~550 KB` HTML mentah).
3. **Halaman Autentikasi (`/login`)** — Halaman form ringan sebagai pembanding baseline.
4. **Halaman Fasilitas (`/fasilitas/lapangan`)** — Rute konten pendukung dengan gambar/aset fasilitas.
5. **Interaksi DOM Sisi Klien (`/booking`)** — Responsivitas pemanggilan `openBooking()`, `updateTotal()`, dan pergantian tanggal `changeDate()`.

### 1.3 Pengecualian (*Out of Scope*)
- Tidak menembak endpoint tulis (`POST /bookings/store`, `/login` POST, atau `/bookings/confirm|reject|delete`).
- Tidak melakukan *Spike/Stress Test* skala besar (> 10 pengguna konkuren) yang menyerupai DDoS pada infrastruktur UMKM (`Server: hcdn`).

---

## 2. Profil Pengujian & Metodologi (`TP5 - Test Strategy`)

Uji performa dibagi menjadi tiga lapis (*tier*) yang saling melengkapi:

| Tier | Fokus Pengukuran | Alat & Teknik | Kondisi / Variasi |
| :---: | :--- | :--- | :--- |
| **Tier 1: Browser Rendering & Web Vitals** | `DNS`, `TCP`, `TLS`, `TTFB`, `DOMContentLoaded (DCL)`, `Load Event`, `First Contentful Paint (FCP)`, `Largest Contentful Paint (LCP)`, `Cumulative Layout Shift (CLS)`, jumlah request & *transfer size* | **Playwright Python (Chromium Headless)** via `PerformanceNavigationTiming`, `PerformanceObserver`, & `PerformanceResourceTiming` | • **Cold Cache** (konteks baru) vs **Warm Cache** (navigasi ulang)<br>• **Desktop** (`1280×800`) vs **Mobile** (`390×844`) |
| **Tier 2: Client-Side DOM Interaction Latency** | Waktu eksekusi `openBooking()`, `updateTotal()`, dan reload navigasi `changeDate()` | **Playwright Python** dengan `performance.now()` / wall-clock timer | Diukur pada slot kosong tanggal besok (`/booking?start_date=<besok>`) |
| **Tier 3: Non-Destructive Concurrent HTTP `GET` Benchmark** | Latensi ujung-ke-ujung (`min`, `mean`, `p50`, `p90`, `p95`, `p99`, `max`), throughput (`req/s`), rasio kompresi (`br`/`gzip`), dan `Error Rate (%)` | **Python `asyncio` + `aiohttp`** (header `Accept-Encoding: gzip, deflate` per `CD-01`) | • **Level A (Baseline):** `1 VU` × 6 putaran × 4 rute (**24 req**, *think-time* `250 ms`)<br>• **Level B (Normal UMKM):** `5 VUs` × 2 putaran/VU × 4 rute (**40 req**, *think-time* `500 ms`)<br>• **Level C (Peak-Safe UMKM):** `10 VUs` × 1 putaran/VU × 4 rute (**40 req**, *think-time* `500 ms`) — Total **`104` request GET** |

---

## 3. Target Kriteria Penerimaan (*Performance SLA / Pass-Fail Thresholds*)

Target ambang batas ditetapkan mengacu pada praktik standar performa web modern (*Core Web Vitals*) dan karakteristik halaman UMKM:

| Metrik | Target Baik (*Pass*) | Batas Toleransi (*Warning*) | Gagal / Catat Insiden (*Fail*) |
| :--- | :---: | :---: | :---: |
| **TTFB (*Time to First Byte*) — `/`, `/login`, `/fasilitas/*`** | `<= 500 ms` | `501 – 800 ms` | `> 800 ms` |
| **TTFB — `/booking` (Query Jadwal Mingguan)** | `<= 1000 ms` | `1001 – 1800 ms` | `> 1800 ms` |
| **First Contentful Paint (FCP)** | `<= 1800 ms` | `1801 – 3000 ms` | `> 3000 ms` |
| **Largest Contentful Paint (LCP)** | `<= 2500 ms` | `2501 – 4000 ms` | `> 4000 ms` |
| **Cumulative Layout Shift (CLS)** | `<= 0.10` | `0.11 – 0.25` | `> 0.25` |
| **p95 HTTP Latency (`1–10 VUs`) — `/`, `/login`** | `<= 1000 ms` | `1001 – 1500 ms` | `> 1500 ms` |
| **p95 HTTP Latency (`1–10 VUs`) — `/booking`** | `<= 2000 ms` | `2001 – 3000 ms` | `> 3000 ms` |
| **HTTP Error Rate (`4xx/5xx/Timeout`)** | `0 %` | `—` | `> 0 %` *(catat insiden)* |
| **Client Interaction (`openBooking` / `updateTotal`)** | `<= 100 ms` | `101 – 250 ms` | `> 250 ms` |
| **Ukuran HTML Uncompressed `/booking`** | `<= 250 KB` | `251 – 500 KB` | `> 500 KB` *(indikasi pembengkakan DOM / perlunya optimasi)* |

---

## 4. Guardrail Keselamatan, Penangguhan, & Risiko (*TP3–TP5*)

1. **Circuit Breaker Otomatis:** Skrip [`test_performance_gor_permata.py`](../03-hasil-pengujian/automation-scripts/test_performance_gor_permata.py) langsung menghentikan (*abort*) beban lanjutan jika pada tahap mana pun rasio HTTP error (`>= 400` atau timeout) melebihi **5%** atau muncul respons **`HTTP 429 Too Many Requests`**.
2. **Jeda Pendinginan (*Cool-Down*):** Disediakan jeda **`2 detik`** antar-level konkurensi (`1 -> 5 -> 10 VUs`) serta *think-time* `500 ms` di setiap iterasi *virtual user*.
3. **Justifikasi Ilmiah (`>= 2022` — Poin 7):** Skenario beban bertingkat (`Baseline -> Busy/Normal -> Peak`) mengadopsi **Winasis, dkk. (2026)** (*Sinkron, SINTA 3*, sistem web + WhatsApp Laravel), evaluasi *Performance Efficiency* berbasis **ISO/IEC 25010** merujuk **Zahra & Kraugusteeliana (2023)** (*JTIIK, SINTA 2*), dan pemilihan eksekusi Playwright merujuk **Putra, dkk. (2026)** (*JAIC, SINTA 3*) pada [`referensi-sinta-1-3.md`](./referensi-sinta-1-3.md).
