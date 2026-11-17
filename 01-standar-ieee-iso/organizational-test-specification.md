# Organizational Test Specification (Test Policy & Test Practices)

Dokumen ini merupakan **Organizational Test Specification** sesuai **Clause 6 (6.2.5)** serta deklarasi kepatuhan **Clause 4** pada standar acuan resmi **ISO/IEC/IEEE 29119-2:2021(E) (*Test Processes*)** ([`pdf-standar/10.1109@IEEESTD.2021.9591508.pdf`](./pdf-standar/10.1109@IEEESTD.2021.9591508.pdf)). Dokumen ini memayungi seluruh aktivitas manajemen dan eksekusi pengujian pada repositori `tugas-qa-testing` untuk studi kasus **Portal Booking GOR Permata Badminton Hall** (`https://gorpermatabadminton.com`).

---

## 1. Identitas Dokumen & Pernyataan Kepatuhan (*Conformance Statement — Clause 4*)

- **ID Dokumen:** `OTS-QA-2026-01`
- **Versi / Tanggal Berlaku:** `2.0` — 17 November 2026
- **Lingkup Organisasi:** Kelompok QA Mata Kuliah *Testing dan QA Perangkat Lunak* (Kelas 07TPLE001 / Reguler C, Teknik Informatika S1, Universitas Pamulang)
- **Standar Acuan Utama:** `ISO/IEC/IEEE 29119-2:2021(E)` (*Test Processes*), diselaraskan dengan `29119-1:2022`, `29119-3:2021`, `29119-4:2021`, `29119-5:2024`, dan `ISO/IEC 25010:2023`.

### 1.1 Deklarasi Kepatuhan (*Clause 4.1.3 — Tailored Conformance*)
Tim menetapkan klaim **Tailored Conformance** terhadap **ISO/IEC/IEEE 29119-2:2021** untuk seluruh proses pada **Clause 6** (Organizational), **Clause 7** (`7.2`, `7.3`, `7.4` Test Management), dan **Clause 8** (`8.2`, `8.3`, `8.4`, `8.5` Dynamic Test Processes) yang diterapkan pada **Black Box Testing**, **Performance Testing**, serta analisis pelengkap *White/Gray Box*.

### 1.2 Justifikasi & Pertimbangan Risiko *Tailoring* (*Clause 4.1.3*)
| Proses / Aspek yang Di-*tailor* | Bentuk Penyesuaian (*Tailoring*) | Justifikasi Teknis, Etika, & Risiko UMKM | Persetujuan Pemangku Kepentingan |
| :--- | :--- | :--- | :--- |
| **Eksekusi Transaksi Nyata (`POST /bookings/store`)** | Dihentikan pada validasi sisi klien atau dicegat via interceptor (`page.route` / `cy.intercept`). | Portal terhubung ke jadwal produksi nyata UMKM; pengiriman order fiktif berisiko mengunci slot dan merugikan operasional bisnis. | Disepakati Tim QA & mengacu arahan etika dosen |
| **Modul Admin / Penjaga (`/bookings/confirm\|reject\|delete`)** | Dikeluarkan dari eksekusi dinamis (*Out of Scope*), hanya dianalisis pada kajian statis *White/Gray Box*. | Tim tidak memiliki kredensial akun admin/penjaga dan tidak melakukan akses tidak sah. | Disepakati Tim QA |
| **Beban Uji Performa Agresif (*Stress / DDoS*)** | Dibatasi ke uji *Browser Rendering / Web Vitals* + *Concurrent HTTP GET* maksimal **`10 VUs`** dengan jeda *think-time* `500 ms` & *auto-abort circuit breaker*. | Mencegah penurunan ketersediaan layanan (*availability*) dan kuota server/CDN (`hcdn`) milik UMKM selama jam operasional. | Disepakati Tim QA |
| **Tata Kelola Korporat (`OT2`/`OT3`)** | Peran peninjau disederhanakan menjadi Koordinator QA, Anggota Tim Uji, dan Dosen Pengampu. | Proyek berskala kelompok akademik dengan satu objek uji utama dan siklus rilis tunggal. | Disepakati Tim QA |

---

## 2. Organizational Test Policy (*Clause 6.1 & 6.2*)

### 2.1 Tujuan & Prinsip Dasar Pengujian
1. **Risk-Based Testing:** Seluruh perancangan, prioritisasi cakupan, dan alokasi upaya pengujian berlandaskan analisis risiko produk (*Product Risk*) dan risiko proyek (*Project Risk*), sehingga fitur kritis (validasi form booking, keutuhan rute layanan, dan performa halaman `/booking`) memperoleh prioritas tertinggi.
2. **Non-Destructive Production Testing:** Pengujian pada sistem publik milik UMKM **wajib** menjaga integritas data dan ketersediaan layanan. Setiap skrip otomatis harus menyertakan mekanisme pengaman (*guardrail*) terhadap permintaan tulis (`POST`/`PUT`/`DELETE`).
3. **Evidence-Based & Reproducible:** Setiap klaim hasil uji (*Pass/Fail*) maupun temuan insiden wajib ditopang bukti aktual deterministik (log eksekusi terstruktur, data mentah JSON, tangkapan layar, atau cuplikan respons HTTP/DOM).
4. **Scientific Justification (Ketentuan Akademik Poin 7):** Setiap pemilihan metode pengujian (White Box, Black Box, Performance, Automation, dan Audit ISO 25010) wajib berlandaskan pustaka ilmiah terakreditasi **SINTA 1–3**.
5. **Pemisahan Pengujian & Wawancara (Arahan Kelas 14 Nov 2026):** Tahap wawancara praktisi QA pada folder `04-wawancara-praktisi-qa/` hanya dilakukan **setelah** seluruh proses pengujian Clause 7 dan 8 selesai terdokumentasi.

### 2.2 Ruang Lingkup Jenis Pengujian Organisasi
- **Functional & Interaction Testing (Black Box):** Evaluasi perilaku antarmuka, navigasi, validasi input, state modal, dan kompatibilitas lintas viewport (*Desktop* & *Mobile*).
- **Performance Testing (*ISO 29119-2 §3.11 & ISO 25010:2023 Performance Efficiency*):** Evaluasi *time behaviour* (TTFB, FCP, LCP, DOMContentLoaded, p50/p95/p99 latensi), *resource utilization* (ukuran HTML/aset, kompresi `br`/`gzip`), dan *safe capacity* (`1–10 VUs`).
- **Structural & Gray Box Testing (Pelengkap):** Evaluasi kompleksitas siklomatik $V(G)$ fungsi JS klien, token CSRF, atribut DOM, dan *HTTP Security Headers*.

---

## 3. Organizational Test Practices (*Clause 6.1 & 6.2*)

### 3.1 Model Proses Multi-Layer (*Clause 5, Figure 2*)
Seluruh pekerjaan pengujian wajib mengikuti tiga lapisan proses ISO/IEC/IEEE 29119-2:2021:
1. **Organizational Test Process (`OT1–OT3`):** Dituangkan pada dokumen ini (`OTS-QA-2026-01`).
2. **Test Management Processes (`TP1–TP9`, `TMC1–TMC4`, `TC1–TC4`):** Dikelola melalui *Master Test Plan* (`TP-GOR-01`), *Performance Test Plan* (`TP-GOR-PERF-01`), *Test Status & Control Report*, dan *Test Completion Report*.
3. **Dynamic Test Processes (`TD1–TD4`, `ED1–ED4`, `TE1–TE3`, `IR1–IR2`):** Dijalankan per jenis pengujian (**Black Box** dan **Performance**) secara iteratif hingga kriteria penyelesaian (*completion criteria*) terpenuhi.

### 3.2 Standar Desain Uji Berbasis *Test Model* (Pembaruan Edisi 2021 — *Annex A & E*)
Berbeda dari edisi 2013 yang memakai *test conditions*, seluruh desain uji pada repositori ini **wajib** mengikuti alur empat aktivitas `Clause 8.2`:
1. **`TD1` Create Test Model:** Menganalisis *Test Basis* (`TB-*`) dan memilih notasi model sesuai teknik yang dipakai (partisi ekuivalensi, nilai batas, *decision table*, diagram transisi status, *use case*, atau *workload model*), lalu mencatat **Test Model Specification (`TM-*`)**.
2. **`TD2` Identify Test Coverage Items:** Menurunkan **Test Coverage Items (`TCI-*`)** dari *Test Model* berdasarkan target persentase cakupan pada *Test Plan*, lalu memprioritaskannya menurut eksposur risiko.
3. **`TD3` Derive Test Cases:** Menyusun **Test Case Specification (`TC-*`)** berisi prasyarat (*preconditions*), data uji/input, aksi, dan hasil yang diharapkan (*expected results*) untuk melatih satu atau lebih `TCI-*`.
4. **`TD4` Create Test Procedures:** Mengurutkan `TC-*` berdasarkan ketergantungan prasyarat/risiko menjadi **Test Procedure Specification (`PROC-*`)** dan skrip otomasi yang dapat diulang.

### 3.3 Konvensi Penamaan ID & Ketertelusuran (*Bidirectional Traceability*)
Setiap artefak wajib menggunakan pengenal unik berikut agar *traceability* dua arah (`TB <-> TM <-> TCI <-> TC <-> PROC/Script <-> Log/IR`) terjaga penuh:

| Jenis Artefak | Format ID Black Box | Format ID Performance | Lokasi Utama |
| :--- | :--- | :--- | :--- |
| **Test Basis** | `TB-BB-01..NN` | `TB-PERF-01..NN` | `02-objek-umkm-dan-rencana-uji/test-model-*.md` |
| **Test Model** (`TD1`) | `TM-BB-01..NN` | `TM-PERF-01..NN` | `02-objek-umkm-dan-rencana-uji/test-model-*.md` |
| **Test Coverage Item** (`TD2`) | `TCI-BB-01..NN` | `TCI-PERF-01..NN` | `02-objek-umkm-dan-rencana-uji/test-model-*.md` |
| **Test Case** (`TD3`) | `TC-BB-01..NN` | `TC-PERF-01..NN` | `03-hasil-pengujian/test-case-*.md` |
| **Test Procedure** (`TD4`) | `PROC-BB-01..NN` | `PROC-PERF-01..NN` | `03-hasil-pengujian/test-case-*.md` |
| **Incident Report** (`IR2`) | `IR-GOR-01..NN` *(memetakan `BUG-GOR-*`)* | `IR-GOR-01..NN` | `03-hasil-pengujian/incident-reports.md` |

### 3.4 Praktik Baku Teknik & Alat Uji
- **Black Box Testing (ISO/IEC/IEEE 29119-4):** Wajib menerapkan *Equivalence Partitioning (EP)*, *Boundary Value Analysis (BVA)*, *Decision Table Testing*, *State Transition Testing*, dan *Use Case Testing* (selaras dengan modul Pertemuan 6–7 & rujukan SINTA 2–3).
- **Performance Testing (ISO/IEC/IEEE 29119-2 §3.11):** Mengukur latensi sisi klien melalui *Chromium Navigation & Resource Timing / Web Vitals* (`Playwright Python`) serta *concurrent GET benchmarking* asinkron (`aiohttp`/`asyncio`) dengan metrik `min`, `mean`, `p50`, `p90`, `p95`, `p99`, `max`, `throughput (req/s)`, dan `error rate (%)`.
- **Otomasi Berulang (`ISO/IEC/IEEE 29119-5`):** Skrip otomasi dikelompokkan secara modular dengan pemisahan data uji eksternal di `03-hasil-pengujian/test-data/*.json`.

---

## 4. Pemantauan Kepatuhan & Pemeliharaan (*OT2 & OT3*)

- **Monitoring (`OT2`):** Setiap pergantian fase di *Implementation Plan*, Koordinator QA memeriksa apakah dokumen pada folder `02` dan `03` menggunakan konvensi ID yang konsisten, bebas *broken link*, dan tidak melanggar aturan non-destruktif.
- **Feedback & Update (`OT3`):** Temuan dari *Test Monitoring & Control* (`7.3`) serta *Lessons Learned* pada *Test Completion* (`7.4`) dicatat sebagai masukan pembaruan spesifikasi organisasi ini.

| Versi | Tanggal | Ringkasan Perubahan | Penyusun |
| :---: | :---: | :--- | :--- |
| `1.0` | 14 Nov 2026 | Rangkuman awal standar pada `standar-dokumentasi-qa.md` | Tim Dokumentasi & Riset |
| `2.0` | 17 Nov 2026 | Pembuatan *Organizational Test Specification* formal penuh sesuai Clause 4 & Clause 6 ISO/IEC/IEEE 29119-2:2021 | Koordinator QA & Tim Riset |
