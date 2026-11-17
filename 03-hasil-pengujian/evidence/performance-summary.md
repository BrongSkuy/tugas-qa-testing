# Ringkasan Metrik Performance Testing (`TP-GOR-PERF-01`)

Dokumen ini merangkum hasil pengukuran kuantitatif dari eksekusi [`test_performance_gor_permata.py`](../automation-scripts/test_performance_gor_permata.py) pada `2026-11-17T22:05:00+07:00` terhadap `https://gorpermatabadminton.com` (sumber data mentah: [`performance-metrics.json`](./performance-metrics.json)).

---

## 1. Browser Rendering & Web Vitals (`Playwright Chromium Headless`)

### 1.1 Cold Cache — Desktop (`1280×800`)
| Rute | HTTP | TTFB (ms) | DCL (ms) | Load (ms) | FCP (ms) | CLS | HTML Raw | HTML Encoded (`br`) | Asset Req |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| `/` | `200` | **2618,3** *(spike)* | 3031,1 | 3343,4 | **3028,0** | 0,0 | 37,06 KB | 9,14 KB | 9 (`627,7 KB`) |
| `/booking?start_date=2026-11-18` | `200` | 1213,0 | 1722,2 | 1826,2 | 1712,0 | 0,0 | **535,37 KB** | 34,78 KB | 5 (`27,5 KB`) |
| `/login` | `200` | 98,9 | 551,8 | 689,8 | 572,0 | 0,0 | 12,85 KB | 4,39 KB | 5 (`27,5 KB`) |
| `/fasilitas/lapangan` | `200` | 95,9 | 595,8 | 708,0 | 620,0 | 0,0 | 9,20 KB | 3,06 KB | 8 (`627,7 KB`) |

> **Catatan `LCP`:** Observer `largest-contentful-paint` pada `chromium-headless-shell` tanpa *user navigation interaction* menghasilkan `null` (`N/A`); evaluasi rendering mengandalkan `TTFB`, `FCP`, `DCL`, `Load`, dan `CLS` terukur.

### 1.2 Warm Cache (`Desktop 1280×800`) & Cold Cache (`Mobile 390×844`)
| Kondisi / Viewport | Rute | TTFB (ms) | DCL (ms) | Load (ms) | FCP (ms) | Transfer Aset |
| :--- | :--- | :-: | :-: | :-: | :-: | :-: |
| **Warm Cache (Desktop)** | `/` | 89,4 | 172,2 | **289,3** | 156,0 | `0 B` *(cached)* |
| **Warm Cache (Desktop)** | `/booking?start_date=2026-11-18` | 963,1 | 1155,1 | **1155,2** | 1032,0 | `0 B` *(cached)* |
| **Cold Cache (Mobile `390×844`)** | `/` | 108,2 | 710,5 | **802,2** | 708,0 | `387,8 KB` |
| **Cold Cache (Mobile `390×844`)** | `/booking?start_date=2026-11-18` | 1016,5 | 1591,5 | **1687,5** | 1580,0 | `27,5 KB` |

---

## 2. Client-Side DOM Interaction Latency (`/booking`)
- **`openBooking()` (Klik slot -> modal tampil):** `62,93 ms` *(SLA <= 250 ms -> PASS)*
- **`updateTotal()` (Ubah durasi `2..5` jam):** Rata-rata `8,11 ms`, maksimum `13,94 ms` *(SLA <= 250 ms -> PASS)*
- **`changeDate()` (Pemicu navigasi tanggal lusa):** `3,03 ms` *(SLA <= 250 ms -> PASS)*

---

## 3. Tiered Concurrent HTTP `GET` Benchmark (`aiohttp`, `Accept-Encoding: gzip, deflate`)

Total `104` request `GET` terdistribusi di 3 level beban dengan **Error Rate `0,0%`** dan **tidak memicu circuit breaker (`Aborted = None`)**:

| Level Beban | VUs | Total Req | RPS | Error % | `/` `p95` (ms) | `/booking` `p50` (ms) | `/booking` `p95` (ms) | `/booking` `max` (ms) | `/login` `p95` (ms) | `/fasilitas/lapangan` `p95` (ms) |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| **Level A: Baseline** | `1` | 24 | 1,87 | `0,0%` | 89,47 | 885,31 | 1033,24 | 1054,09 | 76,71 | 79,81 |
| **Level B: Normal UMKM** | `5` | 40 | 4,54 | `0,0%` | 353,52 | 1949,95 | 2249,31 | 2278,17 | 148,63 | 86,27 |
| **Level C: Peak-Safe** | `10` | 40 | 4,97 | `0,0%` | 397,77 | 5138,42 | **5314,28** *(>3000ms)* | 5323,45 | 396,28 | 87,18 |

### Analisis Bottleneck Utama
1. **Degradasi Latensi `/booking` saat Konkurensi 10 VUs (`IR-GOR-07`):** Pada `1 VU`, `/booking` `p95 = 1033,24 ms`; pada `5 VUs`, naik menjadi `2249,31 ms` (`2,18x`); dan pada `10 VUs`, melonjak menjadi **`5314,28 ms` (`5,14x` dari baseline)** melampaui batas SLA `3000 ms`. Sementara rute `/`, `/login`, dan `/fasilitas/lapangan` tetap stabil di bawah `400 ms`. Penyebabnya adalah rendering *server-side* seluruh grid jadwal mingguan (`~548 KB` HTML un-compressed) dengan header `Cache-Control: no-cache, private` yang membebani CPU/query PHP setiap permintaan konkuren.
2. **Pembengkakan HTML `/booking` (`IR-GOR-08`):** Ukuran HTML mentah `/booking` mencapai `535,37 KB` (`548.217` bytes) melampaui batas rekomendasi `500 KB`, walaupun kompresi Brotli/Gzip menekan ukuran transfer menjadi `34,78 KB`.
3. **Fluktuasi Cold-Start TTFB Beranda `/` (`IR-GOR-09`):** Pada run *Cold Cache Desktop*, `/` mencatat spike `TTFB = 2618,3 ms` (`FCP = 3028 ms`) sebelum turun menjadi `89,4 ms` saat *Warm Reload*, menunjukkan sensitivitas ketika cache edge/origin dingin (`Cache-Control: no-cache, private`).
