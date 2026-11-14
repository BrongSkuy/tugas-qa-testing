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

## 4. Akses Resmi, Standar Gratis Terbuka, & Arsip PDF

> **Catatan Transparansi & Hak Cipta Standar:** Hasil verifikasi langsung pada katalog resmi **ISO Publicly Available Standards** (`https://standards.iso.org/ittf/PubliclyAvailableStandards/`) dan program **IEEE GET** menunjukkan bahwa naskah penuh resmi **ISO/IEC/IEEE 29119-1..5**, **ISO/IEC 25010:2023**, serta **IEEE 829 / 1012 / 730** seluruhnya berstatus **berbayar** (tidak tersedia PDF penuh resminya secara gratis) dan tidak diunggah ke repositori publik GitHub demi kepatuhan hak cipta. Sebagai pengganti yang **100% gratis, legal, dan dapat diunduh penuh**, tim menghimpun standar terbuka resmi (*Public Domain* / *CC BY*) dan rujukan pratinjau resmi berikut:

- **Berkas PDF Standar & Referensi Gratis Resmi (Tersimpan di [`./pdf-standar/`](./pdf-standar/)):**
  1. **NIST SP 800-218 v1.1 (Februari 2022 — *US Gov Public Domain*)**: [`NIST_SP_800-218_SSDF_v1.1_2022.pdf`](./pdf-standar/NIST_SP_800-218_SSDF_v1.1_2022.pdf) — Standar resmi gratis *Secure Software Development Framework (SSDF)* oleh NIST (`36` halaman, DOI: `https://doi.org/10.6028/NIST.SP.800-218`). Memuat praktik pengujian & verifikasi perangkat lunak **PW.8** (*Test Executable Code to Identify Vulnerabilities and Verify Compliance with Security Requirements*) serta **PW.9** (*Configure Software to Have Secure Settings by Default*).
  2. **OWASP Web Security Testing Guide (WSTG) v4.2 (*CC BY-SA 4.0*)**: [`OWASP_Web_Security_Testing_Guide_v4.2.pdf`](./pdf-standar/OWASP_Web_Security_Testing_Guide_v4.2.pdf) — Standar panduan terbuka industri untuk pengujian aplikasi web oleh The OWASP Foundation (`465` halaman; mencakup prinsip pengujian, *Configuration & Deployment Management Testing* termasuk *Test HTTP Strict Transport Security*, validasi input, dan pengujian sisi klien).
  3. **Xue, Wang, & Wang (2026 — *CC BY 4.0*)**: [`arXiv_2608_05594_Xue_2026_ISO29119_Testability.pdf`](./pdf-standar/arXiv_2608_05594_Xue_2026_ISO29119_Testability.pdf) — Artikel *open-access* 2026 (`11` halaman, *Beihang University*) berjudul *"JTA: Joint Testability Architecture for Scenario-Based Validation of Safety-Critical Software"* yang merujuk dan memodelkan langsung konsep **ISO/IEC/IEEE 29119-1:2022** dan **ISO/IEC 25010:2023**.
  4. **Jurnal SINTA 2 terkait ISO/IEC 25010 (Desember 2025 — *CC BY 4.0*)**: Tersedia PDF penuh [`RESTI_Alirridlo_2025_ISO25010_Cyclomatic.pdf`](../02-objek-umkm-dan-rencana-uji/pdf-jurnal/RESTI_Alirridlo_2025_ISO25010_Cyclomatic.pdf) di folder `02-objek-umkm-dan-rencana-uji/pdf-jurnal/`.
- **Standar Gratis Resmi (Versi Web — Tautan Langsung Tanpa Unduh Berbayar):**
  - **WCAG 2.2 / ISO/IEC 40500:2025** (Standar Internasional Aksesibilitas Web W3C–ISO): https://www.w3.org/TR/WCAG22/
  - **Almonte et al. (2025)** — Studi *LLM* berbasis **ISO/IEC 25010:2023** (*arXiv non-exclusive distribution*): https://arxiv.org/abs/2503.15248
  - **Vincekovič et al. (2026)** & **Kudriashova et al. (2026)** — *Applied Sciences* MDPI (*CC BY 4.0*, studi **ISO/IEC/IEEE 29119-1:2022** & **ISO/IEC 25010:2023**, buka via browser): `https://doi.org/10.3390/app16199787` dan `https://doi.org/10.3390/app162211110`
- **Kanal Pratinjau & Katalog Resmi ISO/IEEE Gratis:**
  - ISO Online Browsing Platform (OBP): https://obp.iso.org/
  - Portal Informasi ISO/IEC/IEEE 29119: https://softwaretestingstandard.org/
  - Katalog Pratinjau ISO 29119-1:2022: https://standards.iteh.ai/catalog/standards/sist/9ecff7b0-b812-4c9b-a9e0-81ce4428d7ab/iso-iec-ieee-29119-1-2022
- **Dokumen PDF Ringkasan & Audit Karya Kelompok (Siap Baca/Cetak di [`./pdf-standar/`](./pdf-standar/)):**
  - [`Ringkasan-Standar-ISO-IEC-IEEE-29119-2022-2024.pdf`](./pdf-standar/Ringkasan-Standar-ISO-IEC-IEEE-29119-2022-2024.pdf)
  - [`Audit-Mutu-ISO-IEC-25010-2023-GOR-Permata.pdf`](./pdf-standar/Audit-Mutu-ISO-IEC-25010-2023-GOR-Permata.pdf)
