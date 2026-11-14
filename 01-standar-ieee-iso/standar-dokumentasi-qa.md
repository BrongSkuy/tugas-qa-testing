# Standar Dokumentasi QA & Testing IEEE / ISO (2022–2026)

Dokumen ini menjadi acuan format dokumentasi pengujian pada repositori `tugas-qa-testing` agar memenuhi **Poin 2** instruksi perkuliahan (menerapkan standar dokumentasi QA & Testing IEEE serta ISO periode 2022–2026) untuk kedua objek pengujian (`objek-1-gor-permata/` dan `objek-2-kolam-renang-tasa/`).

---

## 1. Kerangka Standar yang Dirujuk

| Standar | Fokus Dokumen & Penerapan di Proyek Ini |
| :--- | :--- |
| **ISO/IEC/IEEE 29119-3** *(Test Documentation — penyempurnaan historis IEEE 829)* | Mengatur struktur baku artefak pengujian: **Test Plan** (identifikasi, ruang lingkup, fitur diuji/tidak diuji, strategi, kriteria masuk/keluar, risiko), **Test Case Specification** (ID, langkah, input, *expected result*), **Test Execution Log**, dan **Incident / Defect Report** (*severity, priority, steps to reproduce, actual vs expected*). |
| **ISO/IEC/IEEE 29119-1 & 29119-2** | Proses pengujian berbasis risiko (*risk-based testing*) dan siklus uji (*Test Planning -> Test Design & Implementation -> Test Execution -> Test Completion*). |
| **ISO/IEC/IEEE 29119-4** | Teknik perancangan *Test Case* baku: *Specification-Based* (*Black Box*: *Equivalence Partitioning*, *Boundary Value Analysis*, *State Transition*, *Use Case*) dan *Structure-Based* (*White Box*: *Decision/Branch* & *Basis Path*). |
| **ISO/IEC 25010** *(Product Quality Model, edisi 2023)* | Acuan penilaian mutu non-fungsional: *Functional Suitability, Performance Efficiency, Compatibility, Interaction Capability / Usability, Reliability, Security, Maintainability, Flexibility*. |

---

## 2. Template Baku Laporan Defect (Mengikuti ISO/IEC/IEEE 29119-3)

Setiap temuan cacat pada `objek-1-gor-permata/` (`BUG-GOR-XX`) maupun `objek-2-kolam-renang-tasa/` (`BUG-TASA-XX`) dicatat dengan atribut minimal:
1. **ID Defect & Kategori:** (`Functional / UI / Security / Accessibility / Validation`)
2. **Severity / Priority:** *Critical / Major / Minor*
3. **URL / Modul Terdampak**
4. **Steps to Reproduce:** Langkah berurutan yang dapat diulang
5. **Expected Result vs Actual Result**
6. **Bukti Verifikasi Teknis:** Respons HTTP, cuplikan DOM/JS, atau log eksekusi skrip otomasi

