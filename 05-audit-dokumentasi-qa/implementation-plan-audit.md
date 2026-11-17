# Implementation Plan: Audit Dokumentasi QA Repositori `tugas-qa-testing`

Dokumen ini merupakan **rencana implementasi audit dokumentasi (*Documentation Audit Implementation Plan*)** pada folder `05-audit-dokumentasi-qa/` untuk memverifikasi secara objektif dan deterministik bahwa seluruh dokumentasi, desain uji, skrip, bukti eksekusi, serta laporan Word/PDF di repositori [`tugas-qa-testing`](../README.md) telah selaras penuh dengan **ISO/IEC/IEEE 29119-2:2021(E)**, **ISO/IEC 25010:2023**, dan ketentuan perkuliahan **Poin 1–7**.

---

## 1. Tujuan & Ruang Lingkup Audit Dokumentasi

### 1.1 Tujuan Audit
1. Memastikan seluruh *Information Items* wajib dari tiga lapisan proses **ISO/IEC/IEEE 29119-2:2021** (*Organizational*, *Test Management*, dan *Dynamic Test Processes*) tersedia lengkap dan saling tertelusur (*bidirectional traceability*).
2. Memverifikasi konsistensi angka empiris antara luaran eksekusi mentah (`blackbox-results.json`, `performance-metrics.json`) dengan seluruh dokumen Markdown maupun laporan resmi Word (`.docx`) & PDF (`.pdf`).
3. Memastikan kepatuhan etika pengujian **non-destruktif** (`network_posts_sent_to_server == 0`) dan bebas kebocoran data pribadi (**zero PII**) di seluruh berkas repositori.
4. Memvalidasi integritas seluruh tautan internal Markdown, kelengkapan rujukan **SINTA 1–3**, serta keterbaruan indeks pada [`README.md`](../README.md).

### 1.2 Objek yang Diaudit (*In Scope*)
Seluruh folder pada repositori `tugas-qa-testing/`:
- `README.md` (Root indeks & progres 8 langkah)
- `00-materi-perkuliahan/` (Modul Pertemuan 1–7)
- `01-standar-ieee-iso/` (Clause 4 & 6 + Audit ISO/IEC 25010:2023 + PDF standar)
- `02-objek-umkm-dan-rencana-uji/` (Clause 7.2 + Clause 8.2 `TD1–TD2` + Rujukan SINTA 1–3)
- `03-hasil-pengujian/` (Clause 8.2 `TD3–TD4`, `8.3–8.5`, `7.3–7.4`, skrip, data, bukti, & laporan Word/PDF)
- `04-wawancara-praktisi-qa/` (Kesiapan panduan wawancara pasca-selesai proyek uji)

---

## 2. Dimensi Pemeriksaan Audit & Kriteria Kelulusan (`AUD-01` s.d. `AUD-06`)

| ID Pemeriksaan | Dimensi Audit | Objek / Berkas Diperiksa | Kriteria Lulus (*Pass Criteria*) |
| :---: | :--- | :--- | :--- |
| **`AUD-01`** | **Kepatuhan Klausul ISO/IEC/IEEE 29119-2:2021** | Seluruh artefak folder `01`, `02`, `03` | `100%` *Information Items* wajib Klausul `4`, `6`, `7.2–7.4`, dan `8.2–8.5` tersedia dan memakai pendekatan **Test Model** edisi 2021. |
| **`AUD-02`** | **Bidirectional Traceability ID Artefak** | `test-model-*.md`, `test-case-*.md`, `test-execution-log.md`, `incident-reports.md`, JSON bukti | Seluruh ID `TCI-BB-01..22`, `TC-BB-01..22`, `TCI-PERF-01..10`, `TC-PERF-01..10`, dan `IR-GOR-01..10` terpetakan utuh tanpa *orphan ID*. |
| **`AUD-03`** | **Akurasi Data Empiris & Keamanan Non-PII** | `blackbox-results.json`, `performance-metrics.json`, log TXT, seluruh `.md`, & laporan Word/PDF | Ringkasan angka pass/fail cocok 100% dengan JSON bukti; `network_posts_sent_to_server == 0`; `0` kebocoran nomor telepon nyata pelanggan di repo. |
| **`AUD-04`** | **Integritas Tautan Markdown & Arsip PDF** | Seluruh file `.md`, `pdf-standar/*.pdf`, `pdf-jurnal/*.pdf`, `screenshots/*.png` | `0` *broken relative link* di seluruh file `.md`; semua berkas PDF & gambar yang dirujuk tersedia fisik di repositori. |
| **`AUD-05`** | **Kepatuhan Ketentuan Akademik (Poin 1–7)** | `README.md`, `00/`, `01/`, `02/`, `04/` | Objek UMKM tunggal terkonfirmasi, standar IEEE/ISO ada, `7` PDF SINTA 2–3 + `2` DOI tersedia, catatan item tunggu (anggota 3–4 & modul Pertemuan 8+) teridentifikasi jujur. |
| **`AUD-06`** | **Sinkronisasi Word/PDF & Kelengkapan `README.md`** | `Laporan_Hasil_Pengujian_*.docx/.pdf` & `README.md` | File `.docx` dan `.pdf` lebih baru/sinkron dengan JSON bukti terbaru; seluruh struktur `00` s.d. `05` tercantum lengkap di `README.md`. |

---

## 3. Tahapan Pelaksanaan Audit (*Execution Phases*)

1. **Tahap 1 — Penyiapan Instrumen Audit (`05-audit-dokumentasi-qa/`):**
   - Menyusun *Implementation Plan* audit ini ([`implementation-plan-audit.md`](./implementation-plan-audit.md)).
   - Mengembangkan skrip audit otomatis deterministik [`audit_dokumentasi.py`](./audit_dokumentasi.py) untuk menjalankan pemeriksaan `AUD-01` s.d. `AUD-06` secara terukur.
2. **Tahap 2 — Eksekusi Audit Awal & Pencatatan Temuan:**
   - Menjalankan `python 05-audit-dokumentasi-qa/audit_dokumentasi.py` terhadap repositori `tugas-qa-testing/`.
   - Menyimpan luaran terstruktur pada [`audit-results.json`](./audit-results.json).
3. **Tahap 3 — Remediasi Temuan Audit (Jika Ditemukan Gap):**
   - Menindaklanjuti temuan yang bisa langsung diperbaiki (seperti tautan hilang, ketidaksinkronan `README.md`, atau metadata), serta mencatat secara transparan temuan eksternal yang memang masih menunggu pihak lain (anggota 3–4, modul Pertemuan 8+, & tahap wawancara `04/`).
4. **Tahap 4 — Penyusunan Laporan Audit Final & Re-Verifikasi:**
   - Menyusun [`laporan-audit-dokumentasi.md`](./laporan-audit-dokumentasi.md) dan [`README.md`](./README.md) di folder `05-audit-dokumentasi-qa/`.
   - Memperbarui [`../README.md`](../README.md) root dengan dokumentasi folder `05-audit-dokumentasi-qa/` dan ringkasan hasil audit.
   - Menjalankan ulang `audit_dokumentasi.py` setelah penyuntingan akhir hingga seluruh pemeriksaan otomatis berstatus `PASS`.
5. **Tahap 5 — Sinkronisasi Git & Push ke GitHub:**
   - Verifikasi `git status`, lakukan `git add`, `git commit`, dan `git push origin main`.

---

## 4. Kriteria Selesai (*Audit Exit Criteria*)
- Skrip [`audit_dokumentasi.py`](./audit_dokumentasi.py) selesai dieksekusi setelah pembaruan akhir dengan status keseluruhan **PASS** pada seluruh pemeriksaan otomatis (`AUD-01` s.d. `AUD-06`).
- Laporan [`laporan-audit-dokumentasi.md`](./laporan-audit-dokumentasi.md) dan [`../README.md`](../README.md) lengkap, konsisten, dan sudah ter-*push* ke branch `main` GitHub (`BrongSkuy/tugas-qa-testing`).
