# Organizational Test Specification (Test Policy & Test Practices)

Dokumen ini merupakan **Organizational Test Specification** sesuai arsitektur pengujian multi-lapis **ISO/IEC/IEEE 29119-1:2022 (*General Concepts*)**, **ISO/IEC/IEEE 29119-5:2024 (*Keyword-Driven Testing*)**, dan **ISTQB CTFL Syllabus v4.0.1 (`2024`)** ([`pdf-standar/`](./pdf-standar/)). Dokumen ini memayungi seluruh aktivitas manajemen dan eksekusi pengujian pada repositori `tugas-qa-testing` untuk studi kasus **Portal Booking GOR Permata Badminton Hall** (`https://gorpermatabadminton.com`).

---

## 1. Identitas Dokumen & Pernyataan Kepatuhan (*Conformance Statement — Clause 4*)

- **ID Dokumen:** `OTS-QA-2026-01`
- **Versi / Tanggal Berlaku:** `2.1` — 18 November 2026
- **Lingkup Organisasi:** Kelompok QA Mata Kuliah *Testing dan QA Perangkat Lunak* (Kelas 07TPLE001 / Reguler C, Teknik Informatika S1, Universitas Pamulang)
- **Standar Acuan Utama (`>= 2022`):** `ISO/IEC/IEEE 29119-1:2022` (*General Concepts*), `ISO/IEC/IEEE 29119-5:2024` (*Keyword-Driven Testing*), `ISTQB CTFL Syllabus v4.0.1 (2024)`, `ISO/IEC 25010:2023` (*Product Quality*), `ISO/IEC 25019:2023` (*Quality-in-Use*), `ISO/IEC 25002:2024` (*Quality Model Overview*), dan `ISO/IEC 40500:2025` (*W3C WCAG 2.2*).

### 1.1 Deklarasi Kepatuhan (*Tailored Conformance*)
Tim menetapkan klaim **Tailored Conformance** terhadap arsitektur proses multi-lapis **ISO/IEC/IEEE 29119-1:2022** & **ISTQB CTFL v4.0.1 (Bab 1.4)** untuk seluruh lapisan **Organizational** (`OT1–OT3`), **Test Management** (`TP1–TP9`, `TMC1–TMC4`, `TC1–TC4`), dan **Dynamic Test Processes** (`TD1–TD4`, `ED1–ED4`, `TE1–TE3`, `IR1–IR2`) pada **2 jenis pengujian utama proyek: Black Box Testing dan Performance Testing** *(diotomatiskan dengan Playwright Python / `aiohttp`, ditambah catatan baca kode JS publik sebagai pendukung diagnostic)*. *(Catatan kepatuhan tahun >= 2022: berkas PDF referensi 2021 telah dihapus sesuai arahan dosen dan seluruh acuan PDF beredisi 2022–2025).*

### 1.2 Justifikasi & Pertimbangan Risiko *Tailoring* (*Clause 4.1.3*)
| Proses / Aspek yang Di-*tailor* | Bentuk Penyesuaian (*Tailoring*) | Justifikasi Teknis, Etika, & Risiko UMKM | Persetujuan Pemangku Kepentingan |
| :--- | :--- | :--- | :--- |
| **Penyimpanan Transaksi ke Server (`POST /bookings/store`)** | Formulir tetap diisi **data pemesanan fiktif** (`"Test QA"`), lalu dihentikan di validasi sisi klien atau dicegat via interceptor browser (`page.route` / `cy.intercept`). | Portal terhubung ke jadwal produksi nyata UMKM; pengisian memakai data uji fiktif boleh dilakukan selama pengiriman ke server diblokir browser agar `0` order fiktif mengunci slot asli bisnis. | Disepakati Tim QA & mengacu arahan etika dosen |
| **Modul Admin / Penjaga (`/bookings/confirm\|reject\|delete`)** | Dikeluarkan dari eksekusi dinamis (*Out of Scope*), hanya dianalisis pada kajian statis *White/Gray Box*. | Tim tidak memiliki kredensial akun admin/penjaga dan tidak melakukan akses tidak sah. | Disepakati Tim QA |
| **Beban Uji Performa Agresif (*Stress / DDoS*)** | Dibatasi ke uji *Browser Rendering / Web Vitals* + *Concurrent HTTP GET* maksimal **`10 VUs`** dengan jeda *think-time* `500 ms` & *auto-abort circuit breaker*. | Mencegah penurunan ketersediaan layanan (*availability*) dan kuota server/CDN (`hcdn`) milik UMKM selama jam operasional. | Disepakati Tim QA |
| **Tata Kelola Korporat (`OT2`/`OT3`)** | Peran peninjau disederhanakan menjadi Tim QA (keempat anggota setara) dan Dosen Pengampu. | Proyek berskala kelompok akademik dengan satu objek uji utama dan siklus rilis tunggal. | Disepakati Tim QA |

---

## 2. Organizational Test Policy (*Clause 6.1 & 6.2*)

### 2.1 Tujuan & Prinsip Dasar Pengujian
1. **Risk-Based Testing:** Seluruh perancangan, prioritisasi cakupan, dan alokasi upaya pengujian berlandaskan analisis risiko produk (*Product Risk*) dan risiko proyek (*Project Risk*), sehingga fitur kritis (validasi form booking, keutuhan rute layanan, dan performa halaman `/booking`) memperoleh prioritas tertinggi.
2. **Non-Destructive Production Testing:** Pengujian pada sistem publik milik UMKM **wajib** menjaga integritas data dan ketersediaan layanan. Setiap skrip otomatis harus menyertakan mekanisme pengaman (*guardrail*) terhadap permintaan tulis (`POST`/`PUT`/`DELETE`).
3. **Evidence-Based & Reproducible:** Setiap klaim hasil uji (*Pass/Fail*) maupun temuan insiden wajib ditopang bukti aktual deterministik (log eksekusi terstruktur, data mentah JSON, tangkapan layar, atau cuplikan respons HTTP/DOM).
4. **Scientific Justification (Ketentuan Akademik Poin 7):** Setiap pemilihan teknik **Black Box**, **Performance Testing**, alat otomasi, dan audit mutu `ISO 25010` wajib berlandaskan pustaka ilmiah terakreditasi **SINTA 1–3 (`>= 2022`)**.
5. **Pemisahan Pengujian & Wawancara (Arahan Kelas 14 Nov 2026):** Tahap wawancara praktisi QA pada folder `04-wawancara-praktisi-qa/` hanya dilakukan **setelah** seluruh proses pengujian Clause 7 dan 8 selesai terdokumentasi.

### 2.2 Ruang Lingkup Jenis Pengujian Utama (`2` Metode Uji)
- **1. Black Box Testing (Fungsional, Interaksi, & Kompatibilitas):** Evaluasi perilaku antarmuka, navigasi, validasi input, perpindahan status modal, dan kompatibilitas lintas viewport (*Desktop* & *Mobile*), diotomatiskan dengan Playwright Python.
- **2. Performance Testing (*ISO/IEC 25010:2023 Performance Efficiency* & *Winasis, dkk. 2026*):** Evaluasi *time behaviour* (TTFB, FCP, LCP, DOMContentLoaded, p50/p95/p99 latensi), *resource utilization* (ukuran HTML/aset, kompresi `br`/`gzip`), dan *safe capacity* (`1–10 VUs`), diotomatiskan dengan Playwright + `aiohttp`.
- **Catatan Pendukung (Bukan Pengujian Terpisah):** Inspeksi kode JS tampilan `/booking` (`normPhone()`, CSRF token, atribut DOM publik, dan HTTP headers) hanya dipakai untuk menjelaskan akar penyebab bug yang tertangkap oleh Black Box & audit keamanan ISO 25010.

---

## 3. Organizational Test Practices (*Clause 6.1 & 6.2*)

### 3.1 Model Proses Multi-Layer (`ISO/IEC/IEEE 29119-1:2022` & `ISTQB CTFL v4.0.1`)
Seluruh pekerjaan pengujian wajib mengikuti tiga lapisan proses terstruktur:
1. **Organizational Test Process (`OT1–OT3`):** Dituangkan pada dokumen ini (`OTS-QA-2026-01`).
2. **Test Management Processes (`TP1–TP9`, `TMC1–TMC4`, `TC1–TC4`):** Dikelola melalui *Master Test Plan* (`TP-GOR-01`), *Performance Test Plan* (`TP-GOR-PERF-01`), *Test Status & Control Report*, dan *Test Completion Report*.
3. **Dynamic Test Processes (`TD1–TD4`, `ED1–ED4`, `TE1–TE3`, `IR1–IR2`):** Dijalankan per jenis pengujian (**Black Box** dan **Performance**) secara iteratif hingga kriteria penyelesaian (*completion criteria*) terpenuhi.

### 3.2 Standar Desain Uji Berbasis *Test Model* (`TD1–TD4`)
Seluruh desain uji pada repositori ini **wajib** mengikuti alur empat aktivitas berbasis *Test Model*:
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

### 3.4 Praktik Baku Teknik & Alat Uji (`>= 2022`)
- **Black Box Testing (`ISTQB CTFL v4.0.1 Bab 4.2` & `ISO/IEC/IEEE 29119-1:2022`):** Wajib menerapkan 5 teknik terpilih sesuai karakteristik aplikasi: *Equivalence Partitioning (EP)*, *Boundary Value Analysis (BVA)*, *Decision Table Testing*, *State Transition Testing*, dan *Use Case & Compatibility Testing (`ISO/IEC 40500:2025 / WCAG 2.2`)* — selaras dengan modul Pertemuan 6–7 & rujukan SINTA 2–3 (`2022–2026`).
- **Performance Testing (`ISO/IEC 25010:2023 Performance Efficiency` & `Winasis, dkk. 2026`):** Mengukur latensi sisi klien melalui *Chromium Navigation & Resource Timing / Web Vitals* (`Playwright Python`) serta *concurrent GET benchmarking* asinkron (`aiohttp`/`asyncio`) dengan metrik `min`, `mean`, `p50`, `p90`, `p95`, `p99`, `max`, `throughput (req/s)`, dan `error rate (%)`.
- **Otomasi Berulang (`ISO/IEC/IEEE 29119-5:2024`):** Skrip otomasi dikelompokkan secara modular (*keyword-driven helpers*) dengan pemisahan data uji eksternal di `03-hasil-pengujian/test-data/*.json`.

---

## 4. Pemantauan Kepatuhan & Pemeliharaan (*OT2 & OT3*)

- **Monitoring (`OT2`):** Setiap pergantian fase di *Implementation Plan*, Tim QA memeriksa apakah dokumen pada folder `02` dan `03` menggunakan konvensi ID yang konsisten, bebas *broken link*, dan tidak melanggar aturan non-destruktif.
- **Feedback & Update (`OT3`):** Temuan dari *Test Monitoring & Control* (`7.3`) serta *Lessons Learned* pada *Test Completion* (`7.4`) dicatat sebagai masukan pembaruan spesifikasi organisasi ini.

| Versi | Tanggal | Ringkasan Perubahan | Penyusun |
| :---: | :---: | :--- | :--- |
| `1.0` | 14 Nov 2026 | Rangkuman awal standar pada `standar-dokumentasi-qa.md` | Tim QA |
| `2.0` | 17 Nov 2026 | Pembuatan *Organizational Test Specification* formal penuh sesuai arsitektur proses multi-lapis | Tim QA |
| `2.1` | 18 Nov 2026 | Penyeragaman struktur peran keempat anggota (`Tim QA`) secara setara | Tim QA (Faiz, Robi, Dzikri, Nurlaelasari) |
| `2.2` | 22 Nov 2026 | Pemutakhiran acuan standar wajib **`>= 2022`** (`29119-1:2022`, `29119-5:2024`, `25010:2023`, `25019:2023`, `25002:2024`, `40500:2025`, & `ISTQB v4.0.1`) | Tim QA |
