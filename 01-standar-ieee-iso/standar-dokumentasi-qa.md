# Standar Dokumentasi QA & Testing IEEE / ISO (2022–2026)

Dokumen ini menjadi indeks acuan standar QA & Testing pada repositori `tugas-qa-testing` untuk studi kasus **Portal Booking GOR Permata Badminton Hall** (`https://gorpermatabadminton.com`), agar memenuhi **Poin 2** instruksi perkuliahan serta patuh penuh pada **ISO/IEC/IEEE 29119-2:2021(E)**.

---

## 1. Kerangka Standar Resmi yang Dirujuk

| Standar | Tahun / Status | Fokus Utama & Penerapan di Proyek GOR Permata |
| :--- | :---: | :--- |
| **ISO/IEC/IEEE 29119-1** *(Concepts and Definitions)* | **2022** *(Edisi ke-2)* | Menetapkan kosakata baku pengujian (*test case, defect, incident, test model, test basis*) serta prinsip *risk-based testing* yang melandasi pemisahan pengujian non-destruktif (`In Scope`) vs transaksi produksi (`Out of Scope`). |
| **ISO/IEC/IEEE 29119-2** *(Test Processes)* | **2021** *(Edisi ke-2 — Acuan Utama Aktif)* | Menetapkan model proses 3 lapis: **Organizational Test Process** (`Clause 6`), **Test Management Processes** (`Clause 7`: Planning, Monitoring & Control, Completion), dan **Dynamic Test Processes** (`Clause 8`: Test Model -> TCI -> Test Case -> Test Procedure, Environment/Data, Execution, Incident Reporting). |
| **ISO/IEC/IEEE 29119-3** *(Test Documentation — penyempurnaan historis IEEE 829)* | **2021** *(Acuan Artefak Aktif)* | Mengatur struktur baku artefak: **Organizational Test Spec**, **Test Plan**, **Test Specification** (Model, Case, Procedure), **Environment/Data Readiness**, **Test Execution Log**, **Test Status Report**, **Incident Report**, dan **Test Completion Report**. |
| **ISO/IEC/IEEE 29119-4** *(Test Techniques)* | **2021** *(Acuan Teknik Aktif)* | Membakukan teknik perancangan uji **Specification-Based** (*Black Box*: *Equivalence Partitioning, Boundary Value Analysis, Decision Table, State Transition, Use Case*) dan **Structure-Based** (*White Box*: *Branch/Decision & Basis Path Testing*). |
| **ISO/IEC/IEEE 29119-5** *(Keyword-Driven Testing)* | **2024** *(Edisi ke-2)* | Landasan pengorganisasian skenario otomasi modular & pemisahan dataset JSON pada skrip Playwright Python & Cypress di folder `03-hasil-pengujian/`. |
| **ISO/IEC 25010** *(Product Quality Model — SQuaRE)* | **2023** *(Edisi Revisi 9 Karakteristik)* | Memperbarui model kualitas produk perangkat lunak menjadi **9 karakteristik**: *Functional Suitability, Performance Efficiency, Compatibility, **Interaction Capability** (pengganti Usability), Reliability, Security, Maintainability, **Flexibility** (pengganti Portability), dan **Safety** (karakteristik baru 2023)*. Audit rinci ada pada [`evaluasi-iso-25010-gor-permata.md`](./evaluasi-iso-25010-gor-permata.md). |

---

## 2. Matriks Kepatuhan Artefak Proyek terhadap ISO/IEC/IEEE 29119-2:2021 & 29119-3

| Klausul 29119-2 | *Information Item* Wajib | Lokasi Berkas pada Repositori Ini | Fokus Cakupan |
| :---: | :--- | :--- | :--- |
| **4 & 6 (`OT1–OT3`)** | **Organizational Test Specification** (*Policy*, *Practices*, & *Conformance Statement*) | [`./organizational-test-specification.md`](./organizational-test-specification.md) | *Tailored Conformance*, kebijakan non-destruktif, konvensi ID, alur `Test Model` 2021. |
| **7.2 (`TP1–TP9`)** | **Project / Master Test Plan** (`TP-GOR-01`) | [`../02-objek-umkm-dan-rencana-uji/test-plan-gor-permata.md`](../02-objek-umkm-dan-rencana-uji/test-plan-gor-permata.md) | Konteks, *Test Basis*, Risiko *Project vs Product* + *Exposure*, *Strategy*, *Schedule*, *Approval*. |
| **7.2 (`TP1–TP9`)** | **Performance Test Plan** (`TP-GOR-PERF-01`) | [`../02-objek-umkm-dan-rencana-uji/performance-test-plan.md`](../02-objek-umkm-dan-rencana-uji/performance-test-plan.md) | Strategi uji performa non-destruktif (`1/5/10 VUs` & *Web Vitals*), SLA/Threshold, *Circuit Breaker*. |
| **8.2 (`TD1–TD2`)** | **Test Model Specification & TCI** (*Black Box*) | [`../02-objek-umkm-dan-rencana-uji/test-model-blackbox.md`](../02-objek-umkm-dan-rencana-uji/test-model-blackbox.md) | `TB-BB-*`, `TM-BB-*` (`EP`, `BVA`, `Decision Table`, `STT`, `Use Case`), `TCI-BB-*`. |
| **8.2 (`TD1–TD2`)** | **Test Model Specification & TCI** (*Performance*) | [`../02-objek-umkm-dan-rencana-uji/test-model-performance.md`](../02-objek-umkm-dan-rencana-uji/test-model-performance.md) | `TB-PERF-*`, `TM-PERF-*` (*CWV*, *Interaction Timing*, *Workload `1/5/10 VUs`*), `TCI-PERF-*`. |
| **8.2 (`TD1–TD2`)** | **Analisis Pelengkap (*White/Gray Box*)** | [`../02-objek-umkm-dan-rencana-uji/analisis-white-black-gray-box.md`](../02-objek-umkm-dan-rencana-uji/analisis-white-black-gray-box.md) | *Control Flow Graph*, $V(G)$, *Basis Path*, analisis CSRF & DOM, serta tautan ke model Black Box. |
| **8.2 (`TD3–TD4`)** | **Test Case & Test Procedure Specs** (*Black Box*) | [`../03-hasil-pengujian/test-case-blackbox.md`](../03-hasil-pengujian/test-case-blackbox.md) | `TC-BB-*`, `PROC-BB-*`, *Traceability Matrix* penuh, & skrip Playwright/Cypress. |
| **8.2 (`TD3–TD4`)** | **Test Case & Test Procedure Specs** (*Performance*) | [`../03-hasil-pengujian/test-case-performance.md`](../03-hasil-pengujian/test-case-performance.md) | `TC-PERF-*`, `PROC-PERF-*`, *Traceability Matrix* penuh, & skrip `test_performance_gor_permata.py`. |
| **8.3 (`ED1–ED4`)** | **Test Environment & Data Readiness Reports** | [`../03-hasil-pengujian/test-environment-dan-data.md`](../03-hasil-pengujian/test-environment-dan-data.md) | Kesiapan environment, beda Test vs Operational (`8.3.4.2 c`), serta dataset `test-data/*.json`. |
| **8.4 (`TE1–TE3`)** | **Test Results & Test Execution Log** | [`../03-hasil-pengujian/test-execution-log.md`](../03-hasil-pengujian/test-execution-log.md) | Rekaman hasil aktual vs ekspektasi, log TXT mentah, JSON metrik performa, & screenshot bukti. |
| **8.5 (`IR1–IR2`)** | **Incident Reports** | [`../03-hasil-pengujian/incident-reports.md`](../03-hasil-pengujian/incident-reports.md) | Pelaporan terstandar (`IR-GOR-01..NN`), *Severity/Priority*, status retest, dan *action items*. |
| **7.3 (`TMC1–TMC4`)** | **Test Status, Risk Updates & Control Directives** | [`../03-hasil-pengujian/test-status-and-control-report.md`](../03-hasil-pengujian/test-status-and-control-report.md) | Pemantauan metrik cakupan, pembaruan risiko, *control directives*, dan kesiapan *Exit Criteria*. |
| **7.4 (`TC1–TC4`)** | **Test Completion Report** | [`../03-hasil-pengujian/test-completion-report.md`](../03-hasil-pengujian/test-completion-report.md) | Evaluasi *Completion Criteria*, aset terarsip, pembersihan environment, *Lessons Learned*, *Sign-off*. |
| **ISO 25010:2023** | **Evaluasi Mutu Produk (9 Karakteristik)** | [`./evaluasi-iso-25010-gor-permata.md`](./evaluasi-iso-25010-gor-permata.md) | Evaluasi 9 dimensi mutu termasuk angka performa & kompatibilitas hasil eksekusi aktual. |

---

## 3. Template Baku Laporan Insiden / Defect (Mengikuti ISO/IEC/IEEE 29119-2 §8.5 & 29119-3)

Setiap temuan cacat atau pelanggaran SLA performa pada **GOR Permata Badminton Hall** dicatat pada [`incident-reports.md`](../03-hasil-pengujian/incident-reports.md) dengan atribut minimal:
1. **ID Insiden & Cross-Ref:** Kode unik (`IR-GOR-XX` / `BUG-GOR-XX`) dan `TC` pemicu
2. **Kategori & Status Siklus Hidup:** (`Functional / Validation / Error Handling / Performance / Security / Privacy`) dan status (`Open / Reported / Retest Pending / Closed`)
3. **Severity / Priority:** *Critical / Major / Minor* dan *High / Medium / Low*
4. **URL / Modul Terdampak & Test Environment**
5. **Steps to Reproduce:** Langkah deterministik non-destruktif yang dapat diulang penguji lain
6. **Expected Result vs Actual Result**
7. **Bukti Verifikasi Teknis & Action Item:** Respons HTTP, metrik/persentil, cuplikan DOM/JS, tangkapan layar, atau log eksekusi skrip otomasi beserta pemilik tindak lanjut

---

## 4. Referensi Resmi & Arsip PDF di `./pdf-standar/`

- **Kanal Resmi Pratinjau & Katalog Standar:**
  - **ISO Online Browsing Platform (OBP):** https://obp.iso.org/
  - **ISO/IEC 40500:2025 / W3C WCAG 2.2:** https://www.w3.org/TR/WCAG22/
  - **Portal Informasi ISO/IEC/IEEE 29119:** https://softwaretestingstandard.org/
- **Berkas PDF Acuan pada [`./pdf-standar/`](./pdf-standar/):**
  - [`10.1109@IEEESTD.2021.9591508.pdf`](./pdf-standar/10.1109@IEEESTD.2021.9591508.pdf) — Dokumen standar **ISO/IEC/IEEE 29119-2:2021(E)** (*Software and systems engineering — Software testing — Part 2: Test processes*) yang diarsipkan kelompok sebagai bahan referensi utama tugas akademik (*penggunaan internal pendidikan*).
  - [`Ringkasan-Standar-ISO-IEC-IEEE-29119-2022-2024.pdf`](./pdf-standar/Ringkasan-Standar-ISO-IEC-IEEE-29119-2022-2024.pdf) — Ringkasan struktur, proses, teknik uji, & matriks artefak **ISO/IEC/IEEE 29119** pada proyek GOR Permata (`2` halaman).
  - [`Audit-Mutu-ISO-IEC-25010-2023-GOR-Permata.pdf`](./pdf-standar/Audit-Mutu-ISO-IEC-25010-2023-GOR-Permata.pdf) — Ringkasan hasil audit 9 karakteristik model kualitas **ISO/IEC 25010:2023** (`2` halaman).
