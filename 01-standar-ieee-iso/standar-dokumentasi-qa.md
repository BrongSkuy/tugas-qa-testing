# Standar Dokumentasi QA & Testing IEEE / ISO (2022–2026)

Dokumen ini menjadi acuan format dokumentasi dan evaluasi mutu pada repositori `tugas-qa-testing` untuk studi kasus **Portal Booking GOR Permata Badminton Hall** (`https://gorpermatabadminton.com`), agar memenuhi **Poin 2** instruksi perkuliahan (menerapkan standar dokumentasi QA & Testing IEEE serta ISO periode **2022–2026**).

---

## 1. Kerangka Standar Resmi yang Dirujuk (2022–2026 & Seri Terkait)

| Standar | Tahun / Status | Fokus Utama & Penerapan di Proyek GOR Permata |
| :--- | :---: | :--- |
| **ISO/IEC/IEEE 29119-1** *(Concepts and Definitions)* | **2022** *(Edisi ke-2)* | Menetapkan kosakata baku pengujian (*test case, defect, incident, test condition*) serta prinsip *risk-based testing* yang melandasi pemisahan pengujian non-destruktif (`In Scope`) vs transaksi produksi (`Out of Scope`). |
| **ISO/IEC/IEEE 29119-2** *(Test Processes)* | **2021** *(Acuan Proses Aktif)* | Mengatur siklus proses uji organisasi & proyek: *Test Planning -> Test Monitoring & Control -> Test Design & Implementation -> Test Execution -> Test Completion*. |
| **ISO/IEC/IEEE 29119-3** *(Test Documentation — penyempurnaan historis IEEE 829)* | **2021** *(Acuan Artefak Aktif)* | Mengatur struktur baku artefak: **Test Plan**, **Test Case Specification**, **Test Execution Log**, **Incident / Defect Report**, dan **Test Completion Report**. |
| **ISO/IEC/IEEE 29119-4** *(Test Techniques)* | **2021** *(Acuan Teknik Aktif)* | Membakukan teknik perancangan uji **Specification-Based** (*Black Box*: *Equivalence Partitioning, Boundary Value Analysis, State Transition, Use Case*) dan **Structure-Based** (*White Box*: *Branch / Decision & Basis Path Testing*). |
| **ISO/IEC/IEEE 29119-5** *(Keyword-Driven Testing)* | **2024** *(Edisi ke-2)* | Menjadi acuan pengorganisasian skenario uji otomasi modular terstruktur pada skrip Playwright Python & Cypress di folder `03-hasil-pengujian/automation-scripts/`. |
| **ISO/IEC 25010** *(Product Quality Model — SQuaRE)* | **2023** *(Edisi Revisi 9 Karakteristik)* | Memperbarui model kualitas produk perangkat lunak menjadi **9 karakteristik**: *Functional Suitability, Performance Efficiency, Compatibility, **Interaction Capability** (pengganti Usability), Reliability, Security, Maintainability, **Flexibility** (pengganti Portability), dan **Safety** (karakteristik baru 2023)*. Audit rinci ada pada [`evaluasi-iso-25010-gor-permata.md`](./evaluasi-iso-25010-gor-permata.md). |

---

## 2. Matriks Kepatuhan Artefak Proyek terhadap ISO/IEC/IEEE 29119-3

| Artefak Wajib ISO/IEC/IEEE 29119-3 | Lokasi Berkas pada Repositori Ini | Status Saat Ini |
| :--- | :--- | :---: |
| **Test Plan** | [`../02-objek-umkm-dan-rencana-uji/test-plan-gor-permata.md`](../02-objek-umkm-dan-rencana-uji/test-plan-gor-permata.md) | Lengkap (`TP-GOR-01` + justifikasi Sinta) |
| **Test Design / Specification** | [`../02-objek-umkm-dan-rencana-uji/analisis-white-black-gray-box.md`](../02-objek-umkm-dan-rencana-uji/analisis-white-black-gray-box.md) | Lengkap (*CFG*, *Basis Path*, *EP/BVA*) |
| **Test Case Specification** | [`../03-hasil-pengujian/test-cases-dan-laporan-bug.md`](../03-hasil-pengujian/test-cases-dan-laporan-bug.md) | Terdokumentasi (`TC-GOR-01` s.d. `TC-GOR-10`) |
| **Incident / Defect Report** | [`../03-hasil-pengujian/test-cases-dan-laporan-bug.md`](../03-hasil-pengujian/test-cases-dan-laporan-bug.md) | Terdokumentasi (`BUG-GOR-01` s.d. `BUG-GOR-04`) |
| **Test Execution Log** | [`../03-hasil-pengujian/automation-scripts/execution-log.txt`](../03-hasil-pengujian/automation-scripts/execution-log.txt) | Terisi eksekusi Playwright (`9/9 PASS`; akan diperluas) |
| **Evaluasi Kualitas Produk (`ISO 25010:2023`)** | [`./evaluasi-iso-25010-gor-permata.md`](./evaluasi-iso-25010-gor-permata.md) | Lengkap *(Tahap 1)* |

---

## 3. Template Baku Laporan Defect (Mengikuti ISO/IEC/IEEE 29119-3)

Setiap temuan cacat pada objek **GOR Permata Badminton Hall** (`BUG-GOR-XX`) di folder [`../03-hasil-pengujian/`](../03-hasil-pengujian/) dicatat dengan atribut minimal:
1. **ID Defect & Kategori:** (`Functional / UI / Security / Accessibility / Validation`)
2. **Severity / Priority:** *Critical / Major / Minor* dan *High / Medium / Low*
3. **URL / Modul Terdampak**
4. **Steps to Reproduce:** Langkah berurutan yang dapat diulang secara deterministik
5. **Expected Result vs Actual Result**
6. **Bukti Verifikasi Teknis:** Respons HTTP, cuplikan DOM/JS, tangkapan layar, atau log eksekusi skrip otomasi

---

## 4. Akses Resmi & Arsip Ringkasan PDF

> **Catatan Hak Cipta Standar:** Naskah penuh resmi standar ISO/IEC dan IEEE merupakan dokumen berhak cipta berbayar pada ISO Store / IEEE Xplore dan tidak diperkenankan untuk diunggah secara ilegal ke repositori publik.
- **Kanal Pratinjau & Katalog Resmi Gratis:**
  - ISO Online Browsing Platform (OBP): https://obp.iso.org/
  - Portal Informasi ISO/IEC/IEEE 29119: https://softwaretestingstandard.org/
  - Katalog Pratinjau ISO 29119-1:2022: https://standards.iteh.ai/catalog/standards/sist/9ecff7b0-b812-4c9b-a9e0-81ce4428d7ab/iso-iec-ieee-29119-1-2022
- **Dokumen PDF Ringkasan & Audit Karya Kelompok (Siap Baca/Cetak di Folder [`./pdf-standar/`](./pdf-standar/)):**
  - [`Ringkasan-Standar-ISO-IEC-IEEE-29119-2022-2024.pdf`](./pdf-standar/Ringkasan-Standar-ISO-IEC-IEEE-29119-2022-2024.pdf)
  - [`Audit-Mutu-ISO-IEC-25010-2023-GOR-Permata.pdf`](./pdf-standar/Audit-Mutu-ISO-IEC-25010-2023-GOR-Permata.pdf)
