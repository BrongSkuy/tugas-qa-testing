# Master Test Plan: Portal Booking GOR Permata Badminton Hall

Dokumen ini merupakan **Master Test Plan (`TP-GOR-01`)** yang disusun mematuhi seluruh aktivitas **Test Strategy and Planning Process (`7.2`, aktivitas `TP1–TP9`)** pada standar **ISO/IEC/IEEE 29119-2:2021(E)** ([`10.1109@IEEESTD.2021.9591508.pdf`](../01-standar-ieee-iso/pdf-standar/10.1109@IEEESTD.2021.9591508.pdf)), dipadukan dengan kosakata `29119-1:2022`, struktur dokumentasi `29119-3:2021`, teknik uji `29119-4:2021`, serta model mutu **ISO/IEC 25010:2023**.

---

## 1. Identifikasi Dokumen, Konteks, & Ruang Lingkup (`TP1 — Understand Context`)

### 1.1 Identifikasi Dokumen & Test Item
- **ID Master Test Plan:** `TP-GOR-01` (Versi `2.0` — Final)
- **Sub-Plan Terkait:** `TP-GOR-PERF-01` ([`performance-test-plan.md`](./performance-test-plan.md))
- **Klaim Kepatuhan:** *Tailored Conformance* terhadap `ISO/IEC/IEEE 29119-2:2021` (lihat [`../01-standar-ieee-iso/organizational-test-specification.md`](../01-standar-ieee-iso/organizational-test-specification.md))
- **Sistem yang Diuji (*Test Item / SUT*):** Portal Web Publik **GOR Permata Badminton Hall** (`https://gorpermatabadminton.com`)
- **Lokasi UMKM:** Kp. Cipari, Desa Ciakar, Kec. Panongan, Kab. Tangerang, Banten
- **Karakteristik Bisnis Teramati:** Portal reservasi 4 lapangan bulu tangkis dengan tarif `PRICE_PER_HOUR = 40000` (`Rp 40.000`/jam), slot operasional `07:00–23:00` (tutup `00:00`), dan konfirmasi WhatsApp admin.

### 1.2 Pemangku Kepentingan (*Stakeholders*) & Rencana Komunikasi (`7.2.4.2 b, d`)
| Peran Pemangku Kepentingan | Nama / Pihak | Kepentingan & Tanggung Jawab | Kanal & Frekuensi Komunikasi |
| :--- | :--- | :--- | :--- |
| **Dosen Pengampu (Reviewer Akademik)** | Asep Erlan Maulana, S.Kom., M.Kom | Asesmen kelengkapan standar IEEE/ISO, sitasi SINTA 1–3, & kesiapan hasil uji sebelum wawancara | Presentasi kelas mingguan & repositori GitHub *Public* |
| **Tim QA & Penguji (Setara)** | Muhammad Faiz Rabbani (`231011402539`), Robi Farhan Anshori (`231011401468`), Dzikri Attariq Samayaki (`221011401148`), & Nurlaelasari (`231011403531`) | Penyusunan strategi, *Test Plan*, *Test Models*, pengadaan acuan standar, eksekusi pengujian manual/otomasi, reviu silang temuan, & laporan penutupan | Commit & kolaborasi GitHub pada `tugas-qa-testing` |
| **Pemilik / Pengelola UMKM** | Pengelola GOR Permata Badminton Hall | Terlindungi dari gangguan transaksi fiktif maupun lonjakan beban server selama pengujian | Tidak dihubungi untuk transaksi fiktif (*zero-impact testing*) |

### 1.3 Inventarisasi *Test Basis* (`7.2.4.2 c`)
1. **Perilaku Antarmuka & Fungsional Web Publik (`TB-BB-01..07`):** Halaman beranda (`/`), grid jadwal `/booking` beserta parameter `?start_date=`, modul modal `#bookingModal`, form `/login`, tautan `/register`, halaman `/fasilitas/*`, serta kompatibilitas viewport *Desktop* vs *Mobile*.
2. **Kode JavaScript Klien Publik `/booking` (`7.473` karakter):** Fungsi `rupiah()`, `changeDate()`, `updateTotal()`, `openBooking()`, `closeModal()`, `submitBooking()`, `normPhone()`, `manageBooking()` (`TB-WB` & `TB-BB`).
3. **Standar Kualitas Produk ISO/IEC 25010:2023 (`TB-PERF-01..04`):** Karakteristik *Functional Suitability*, *Performance Efficiency*, *Compatibility*, *Interaction Capability*, *Security*, dan *Safety* (batas jam tutup `00:00`).
4. **Pedoman Perkuliahan & Jurnal SINTA 1–3:** Modul Pertemuan 1–7 ([`00-materi-perkuliahan/`](../00-materi-perkuliahan/README.md)) dan 9 rujukan jurnal terakreditasi ([`referensi-sinta-1-3.md`](./referensi-sinta-1-3.md)).

### 1.4 Ruang Lingkup (*In Scope vs Out of Scope*)
- **In Scope:**
  1. **Black Box Testing (Fungsional & Interaksi):** Navigasi rute publik, parameter `?start_date=`, pembukaan/penutupan `#bookingModal`, kalkulasi tarif `updateTotal()`, validasi negatif dan nilai batas `#custName`, `#custPhone`, `#custDuration`, validasi klien `/login`, serta responsivitas *Desktop* (`1280×800`) dan *Mobile* (`390×844`).
  2. **Performance Testing (Non-Destruktif):** Profiling *Navigation Timing / Core Web Vitals* (`TTFB`, `DCL`, `Load`, `FCP`, `LCP`, `CLS`), analisis bobot payload HTML/aset (`Cold` vs `Warm`), *client interaction latency*, dan *concurrent HTTP GET benchmark* (`1`, `5`, `10 VUs`) pada [`performance-test-plan.md`](./performance-test-plan.md).
  3. **White Box & Gray Box Testing (Pelengkap):** Perhitungan *Cyclomatic Complexity* $V(G)$ pada `normPhone()` & `submitBooking()`, inspeksi atribut DOM, token CSRF, dan *HTTP Security Headers*.
- **Out of Scope (*Tailored Exclusion*):**
  1. Pengiriman transaksi nyata `POST /bookings/store` ke basis data UMKM (dicegat via interceptor `page.route` / `cy.intercept` dan validasi berhenti di sisi klien).
  2. Pengujian fitur internal admin/penjaga (`/bookings/confirm/*`, `/bookings/reject/*`, `/bookings/delete/*`) karena tidak memiliki kredensial resmi.
  3. Uji beban destruktif (*DDoS / High-Load Stress* > 10 VUs) serta eksploitasi keamanan aktif (*SQLi / Brute Force*).

---

## 2. Pengorganisasian Penyusunan Test Plan (`TP2 — Organize Test Plan Development`)

| Tahap Penyusunan | Aktivitas | Penanggung Jawab | Target Selesai |
| :---: | :--- | :--- | :---: |
| 1 | Pengumpulan konteks UMKM, standar PDF `29119-2:2021`, & rujukan SINTA 1–3 | Tim QA | 14–17 Nov 2026 |
| 2 | Identifikasi *Test Basis*, analisis risiko Project/Product, & rancangan *Test Strategy* | Tim QA | 17 Nov 2026 |
| 3 | Penyusunan *Sub-Plan Performance* & *Test Models* (Black Box + Performance) | Tim QA | 17 Nov 2026 |
| 4 | Reviu, kelengkapan anggota, & sinkronisasi repositori oleh seluruh tim | Tim QA | 17–18 Nov 2026 |

---

## 3. Identifikasi, Klasifikasi, & Perlakuan Risiko (`TP3` & `TP4`)

Sesuai **ISO/IEC/IEEE 29119-2 §7.2.4.4 c**, daftar risiko wajib membedakan **Project Risks** dan **Product Risks**, menetapkan tingkat *Exposure* (*Likelihood × Impact*), serta mendokumentasikan **Risk Treatment Approaches** (`7.2.4.5`):

### 3.1 Product Risks (Risiko Kualitas Produk)
| ID Risiko | Deskripsi Risiko Produk | Likelihood | Impact | Risk Exposure | Risk Treatment (`TP4`) |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`PR-01`** | Validasi nomor WhatsApp `normPhone()` gagal menangani format `+62 08...` atau digit batas (10/11/14/15 digit) sehingga pelanggan sah tertolak atau nomor salah lolos | Tinggi (3) | Tinggi (3) | **9 (Tinggi)** | **Mitigasi via Pengujian:** Terapkan *EP/BVA* lengkap pada `#custPhone` (`TM-BB-01`) + verifikasi *Basis Path* $V(G)=4$ dan catat di `Incident Report`. |
| **`PR-02`** | Parameter `?start_date=` menerima format rusak (picu `HTTP 500`) atau tanggal lampau yang masih merender tombol booking aktif | Tinggi (3) | Tinggi (3) | **9 (Tinggi)** | **Mitigasi via Pengujian:** Uji *EP/BVA* parameter `?start_date=` (hari ini, besok, tanggal lampau `2020-01-01`, string invalid) dan laporkan sebagai insiden prioritas tinggi. |
| **`PR-03`** | Ukuran HTML `/booking` besar (`~550 KB` un-compressed) dan *inline script* tunggal berpotensi memperlambat *TTFB / LCP* atau memicu *bottleneck* saat diakses beberapa pengguna serentak | Sedang (2) | Tinggi (3) | **6 (Sedang-Tinggi)** | **Mitigasi via Pengujian:** Jalankan *Performance Test Plan* (`TP-GOR-PERF-01`) mengukur *Web Vitals* (*Cold/Warm*, *Desktop/Mobile*) dan benchmark `1/5/10 VUs`. |
| **`PR-04`** | Input `#custName` tanpa `.trim()` / batas minimal memungkinkan nama kosong spasi lolos di sisi klien | Tinggi (3) | Sedang (2) | **6 (Sedang)** | **Mitigasi via Pengujian:** Uji *BVA* `#custName` (`""`, `"   "`, `"A"`, string normal) pada `TC-BB-*` dan catat defect validasi. |
| **`PR-05`** | Tautan `/register` mengembalikan `404` serta data slot DOM (`data-name`, `data-phone`) dan fungsi admin `manageBooking()` terpapar ke publik | Tinggi (3) | Sedang (2) | **6 (Sedang)** | **Mitigasi via Pengujian:** Verifikasi rute publik (`TC-BB-01..02`), audit *HTTP Security Headers* & atribut DOM pasif, lalu catat di `Incident Report` & audit `ISO 25010`. |
| **`PR-06`** | Kesalahan kalkulasi tarif `updateTotal()` atau gagal penolakan batas tutup `00:00` (`startHour + duration > 24`) | Rendah (1) | Tinggi (3) | **3 (Rendah-Sedang)** | **Mitigasi via Pengujian:** Uji *BVA* durasi `1..5` jam pada slot `21:00`, `22:00`, dan `23:00` melalui Playwright/Cypress dengan blocker `POST`. |

### 3.2 Project Risks (Risiko Pelaksanaan Proyek Uji)
| ID Risiko | Deskripsi Risiko Proyek | Likelihood | Impact | Risk Exposure | Risk Treatment (`TP4`) |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`PJ-01`** | Pengujian berulang menyentuh database jadwal produksi dan mengunci slot nyata UMKM | Sedang (2) | Kritis (4) | **8 (Tinggi)** | **Avoidance:** Seluruh form submission dibatasi hanya validasi negatif sisi klien; interceptor `page.route('**/bookings/store')` wajib aktif dan `post_attempts == 0` diverifikasi di log. |
| **`PJ-02`** | Uji performa konkuren membebani server/CDN UMKM (`hcdn`) selama jam operasional | Sedang (2) | Tinggi (3) | **6 (Sedang-Tinggi)** | **Mitigasi & Pembatasan:** Batasi maksimum `10 VUs` (`GET`-only), jeda *think-time* `500 ms`, serta pasang *auto-abort circuit breaker* bila error rate > 5%. |
| **`PJ-03`** | Slot jadwal live pada portal target berubah setiap hari mengikuti tanggal berjalan | Sedang (2) | Rendah (1) | **2 (Rendah)** | **Optimasi:** Gunakan tanggal dinamis (`tomorrow`) & pemilih slot kosong dinamis pada skrip otomasi; seluruh data keempat anggota kelompok sudah lengkap terdokumentasi. |
| **`PJ-04`** | Perangkat lokal tidak memasang *runner* Cypress CLI penuh (hanya Python Playwright) | Sedang (2) | Rendah (1) | **2 (Rendah)** | **Retensi & Alternatif:** Eksekusi utama dijalankan melalui **Playwright Python** & `aiohttp`; skrip Cypress (`gor-permata.cy.js`) disinkronkan sebagai artefak kode modular dan perbedaan lingkungan dicatat pada `8.3.4.2 c`. |

---

## 4. Test Strategy (`TP5 — Design Test Strategy`)

### 4.1 Pendekatan & Teknik Pengujian (`ISO/IEC/IEEE 29119-4`)
1. **Black Box Testing (Fungsional, Interaksi, & Kompatibilitas):**
   - *Equivalence Partitioning (EP)* & *Boundary Value Analysis (BVA)* pada `#custName`, `#custPhone`, `#custDuration`, `?start_date=`, dan `/login`.
   - *Decision Table Testing* untuk kombinasi multi-kondisi pada `submitBooking()`.
   - *State Transition Testing (STT)* untuk alur status slot & modal `#bookingModal`.
   - *Use Case Testing* untuk alur lengkap pengunjung pada viewport *Desktop* (`1280×800`) dan *Mobile* (`390×844`).
   - *Rujukan Ilmiah SINTA 2–3:* **Yulistina, dkk. (2020)**, **Nurudin, dkk. (2019)** (*JIUP, SINTA 3*), **Putri & Susanto (2024)** (*Sinkron, SINTA 3*), serta **Fhonna, dkk. (2026)** (*Sisfo, SINTA 3*).
2. **Performance Testing (*Time Behaviour, Resource Utilization, Safe Capacity*):**
   - Dirinci lengkap pada [`performance-test-plan.md`](./performance-test-plan.md) (`TP-GOR-PERF-01`).
   - Mengukur *Navigation Timing / Web Vitals* (`TTFB`, `DCL`, `Load`, `FCP`, `LCP`, `CLS`, *payload bytes*) serta uji beban HTTP `GET` bertingkat (`1`, `5`, `10 VUs`).
   - *Rujukan Ilmiah SINTA 2–3:* **Zahra & Kraugusteeliana (2023)** (*JTIIK, SINTA 2*) untuk evaluasi performa berbasis ISO 25010 dan **Putra, dkk. (2026)** (*JAIC, SINTA 3*) untuk komparasi *framework* otomasi UI (Playwright vs Cypress).
3. **White Box & Gray Box Testing (Pelengkap):**
   - *Basis Path* & *Cyclomatic Complexity* $V(G)$ pada [`analisis-white-black-gray-box.md`](./analisis-white-black-gray-box.md) (*Pratala, dkk., 2020; Alirridlo, dkk., 2025*).

### 4.2 Metrik Pemantauan & Pengendalian (`7.2.4.6 c` -> `TMC1–TMC4`)
- **Black Box Coverage:** `% TCI-BB` yang tercakup & dieksekusi; rasio `PASS / FAIL / INCONCLUSIVE` per prioritas risiko.
- **Performance Metrics:** `TTFB`, `FCP`, `LCP`, `CLS`, `DOMContentLoaded`, `p50/p90/p95/p99 HTTP latency`, `RPS`, `Payload KB`, dan `HTTP Error Rate (%)`.
- **Safety Guardrail Metric:** Jumlah `POST /bookings/store` yang lolos ke jaringan (**wajib = `0`**).
- **Incident Density:** Jumlah `IR-GOR-*` berdasarkan kategori & *Severity*.

### 4.3 Kriteria Masuk, Penyelesaian, Penangguhan, & Kelanjutan (`7.2.4.6 a Note 2`)
- **Entry Criteria:**
  1. Target `https://gorpermatabadminton.com` aktif (`HTTP 200 OK`).
  2. *Test Environment* (`Python 3.9`, `Playwright`, `aiohttp`) & dataset JSON terverifikasi siap pada [`test-environment-dan-data.md`](../03-hasil-pengujian/test-environment-dan-data.md).
- **Test Completion / Exit Criteria:**
  1. **100%** `TCI-BB` dan `TCI-PERF` prioritas Tinggi & Sedang telah diturunkan menjadi `TC` dan dieksekusi.
  2. Seluruh skrip otomasi berjalan tanpa *unhandled exception* dengan `post_attempts == 0`.
  3. Seluruh deviasi hasil atau pelanggaran SLA tercatat resmi sebagai *Incident Report* pada [`incident-reports.md`](../03-hasil-pengujian/incident-reports.md).
  4. *Test Status Report*, *Test Completion Report*, dan pembaruan audit `ISO 25010:2023` telah selesai disusun.
- **Suspension Criteria (Kriteria Penangguhan Uji):**
  1. Target mengalami *downtime* berkepanjangan (`HTTP 502/503/504`) atau *rate-limiting* (`HTTP 429`) dengan rasio error > 5% selama *performance benchmark*.
  2. Interceptor `page.route` terdeteksi gagal memblokir request `POST`.
- **Resumption Criteria (Kriteria Melanjutkan Uji):**
  1. Layanan target kembali stabil (`HTTP 200 OK` pada pemeriksaan awal) setelah jeda pendinginan minimal 5 menit, atau *bug* pada guardrail skrip telah diperbaiki.

### 4.4 Kebutuhan Data, Lingkungan, & Deliverables (`7.2.4.6 d–f`)
- **Test Environment Requirements:** Browser headless Chromium (`Playwright`), runtime Python 3.9 (`aiohttp`), resolusi `1280×800` dan `390×844`, serta interceptor jaringan lokal.
- **Test Data Requirements:** Data sintetik non-PII untuk batas input Black Box ([`blackbox-testdata.json`](../03-hasil-pengujian/test-data/blackbox-testdata.json)) dan profil beban performa ([`performance-profiles.json`](../03-hasil-pengujian/test-data/performance-profiles.json)).
- **Test Deliverables:** Seluruh berkas pada folder `01`, `02`, dan `03` sesuai matriks kepatuhan pada [`standar-dokumentasi-qa.md`](../01-standar-ieee-iso/standar-dokumentasi-qa.md).

---

## 5. Staffing, Jadwal, & Estimasi Upaya (`TP6` & `TP7`)

| Peran | Penanggung Jawab | Fokus Tugas *(Kolaboratif & Setara)* | Estimasi Upaya | Jadwal Pelaksanaan |
| :--- | :--- | :--- | :---: | :---: |
| **Anggota Tim QA** | Muhammad Faiz Rabbani (`231011402539`) | Standar ISO/IEEE, *Test Plan*, *Test Models*, pengujian manual/otomasi, reviu bukti, & laporan | ~4–5 jam | 14–18 Nov 2026 |
| **Anggota Tim QA** | Robi Farhan Anshori (`231011401468`) | Standar ISO/IEEE (`459203e`), *Test Plan*, pengujian manual/otomasi, reviu bukti, & laporan | ~4–5 jam | 14–18 Nov 2026 |
| **Anggota Tim QA** | Dzikri Attariq Samayaki (`221011401148`) | Rujukan, pengujian manual silang, verifikasi bukti, reviu laporan, & persiapan wawancara (`04/`) | ~4–5 jam | 14–18 Nov 2026 |
| **Anggota Tim QA** | Nurlaelasari (`231011403531`) | Rujukan, pengujian manual silang, verifikasi bukti, reviu laporan, & persiapan wawancara (`04/`) | ~4–5 jam | 14–18 Nov 2026 |

---

## 6. Persetujuan & Distribusi Test Plan (`TP8` & `TP9`)

| Pemangku Kepentingan | Peran | Status Persetujuan | Tanggal |
| :--- | :--- | :---: | :---: |
| Muhammad Faiz Rabbani (`231011402539`) | Anggota Tim QA | **Disetujui & Sinkron Repo** | 18 Nov 2026 |
| Robi Farhan Anshori (`231011401468`) | Anggota Tim QA | **Disetujui & Sinkron Repo** | 18 Nov 2026 |
| Dzikri Attariq Samayaki (`221011401148`) | Anggota Tim QA | **Disetujui & Sinkron Repo** | 18 Nov 2026 |
| Nurlaelasari (`231011403531`) | Anggota Tim QA | **Disetujui & Sinkron Repo** | 18 Nov 2026 |
| Asep Erlan Maulana, S.Kom., M.Kom | Dosen Pengampu *(Reviewer Eksternal)* | *Menunggu Asesmen Kelas* | — |

Dokumen tersedia secara terbuka pada repositori publik `https://github.com/BrongSkuy/tugas-qa-testing` (`02-objek-umkm-dan-rencana-uji/test-plan-gor-permata.md`).
