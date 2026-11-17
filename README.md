# Tugas Testing dan QA Perangkat Lunak

Repositori dokumentasi tugas kelompok mata kuliah **Testing dan Quality Assurance (QA) Perangkat Lunak** — Program Studi Teknik Informatika (S1), Universitas Pamulang.

- **Dosen Pengampu:** Bapak Ahmad Fauzi
- **Kelas / Shift:** 07TPLE001 / Reguler C (Kelompok *[Diisi nomor 1–8]*)
- **Repositori:** https://github.com/BrongSkuy/tugas-qa-testing
- **Standar Proses Acuan:** **ISO/IEC/IEEE 29119-2:2021(E) (*Test Processes*)** ([`10.1109@IEEESTD.2021.9591508.pdf`](./01-standar-ieee-iso/pdf-standar/10.1109@IEEESTD.2021.9591508.pdf))

---

## Anggota Kelompok
> *Daftar anggota Kelompok 1–8 wajib dilengkapi dan di-upload sesuai instruksi kelas 14 November 2026.*

| No | Nama Lengkap | NIM | Akun GitHub |
| :--- | :--- | :--- | :--- |
| 1 | Muhammad Faiz Rabbani | 231011402539 | [@BrongSkuy](https://github.com/BrongSkuy) |
| 2 | Robi Farhan Anshori | 231011401468 | [@robifr](https://github.com/robifr) |
| 3 | *[Diisi]* | *[Diisi]* | *[Diisi]* |
| 4 | *[Diisi]* | *[Diisi]* | *[Diisi]* |

---

## Objek Pengujian UMKM Terpilih (Keputusan Final)

- **Nama Objek / Portal:** **Portal Booking GOR Permata Badminton Hall**
- **URL Portal:** https://gorpermatabadminton.com
- **Lokasi UMKM:** Kp. Cipari, Desa Ciakar, Kec. Panongan, Kab. Tangerang, Banten
- **Alasan Pemilihan & Cakupan Teknik:**
  - Sesuai 100% dengan contoh kasus dosen (*portal lapangan bulu tangkis skala lokal*).
  - Mendukung penuh pengujian berstandar **ISO/IEC/IEEE 29119-2:2021**: **Black Box Testing** (*EP, BVA, Decision Table, State Transition, Use Case, & Mobile Compatibility*), **Performance Testing** (*Web Vitals Cold/Warm Desktop/Mobile, Payload Audit, Client Interaction Latency, & Safe Concurrent `GET` Load `1/5/10 VUs`*), **White Box** (*Cyclomatic Complexity* $V(G)$ pada `normPhone()` & `submitBooking()`), **Gray Box**, dan **Automation Testing** (Playwright Python, `aiohttp`, & Cypress).
- **Batasan Etika Uji (Non-Destruktif):** Tidak pernah mengirimkan *booking* fiktif ke jadwal produksi (`POST /bookings/store` diblokir di interceptor `page.route` dengan `network_posts_sent_to_server = 0`; benchmark performa dibatasi `GET`-only `<= 10 VUs`).

---

## Progres Pengerjaan Tugas Kelompok

| No | Langkah Kerja Kelompok | Penanggung Jawab | Status |
| :-: | :--- | :--- | :---: |
| 1 | Koordinasi pembagian kelompok acak (Kelompok 1–8) & pengunggahan daftar anggota kelompok. | Seluruh Mahasiswa | ⏳ Proses *(Menunggu anggota 3–4)* |
| 2 | Mengambil & mempelajari modul lengkap (Pertemuan 1–7 di [`00-materi-perkuliahan/`](./00-materi-perkuliahan/); Pertemuan 8–akhir menyusul dari Ketua Kelas). | Semua Anggota | ⏳ Proses |
| 3 | Membuat repositori GitHub *Public* (`https://github.com/BrongSkuy/tugas-qa-testing`) & melengkapi [tabel anggota](./README.md#anggota-kelompok). | Muhammad Faiz Rabbani | ⏳ Proses |
| 4 | Finalisasi objek UMKM terpilih di repo: **Portal Booking GOR Permata Badminton Hall** ([`kandidat-objek-pengujian.md`](./02-objek-umkm-dan-rencana-uji/kandidat-objek-pengujian.md)). | Tim Riset Objek | ✅ Selesai |
| 5 | Menyusun dokumentasi standar QA & Testing IEEE/ISO lengkap ([`01-standar-ieee-iso/`](./01-standar-ieee-iso/): *Organizational Test Spec*, `29119-2:2021`, audit `ISO 25010:2023`, 3 PDF standar) & 7 PDF jurnal **SINTA 2–3** ([`pdf-jurnal/`](./02-objek-umkm-dan-rencana-uji/pdf-jurnal/)). | Tim Dokumentasi & Riset | ✅ Selesai |
| 6 | Memfinalkan *Master Test Plan* (`TP-GOR-01`), *Performance Test Plan* (`TP-GOR-PERF-01`), *Test Model Specifications* & *TCI* (Black Box + Performance), serta *White/Gray Box CFG* di [`02-objek-umkm-dan-rencana-uji/`](./02-objek-umkm-dan-rencana-uji/). | Tim QA & Riset | ✅ Selesai |
| 7 | Menjalankan pengujian aktual Black Box (`22 TC`: `15 PASS`, `7` temuan cacat) & Performance (`10 TC`: `7 PASS`, `3` temuan SLA/payload) beserta *Environment/Data Readiness*, *Execution Log*, *Incident Reports* (`IR-GOR-01..10`), *Status/Control Report*, *Test Completion Report*, bukti screenshot/JSON, dan **Laporan Resmi Word/PDF** di [`03-hasil-pengujian/`](./03-hasil-pengujian/). | Tim Penguji | ✅ Selesai |
| 8 | Melaksanakan **Audit Dokumentasi QA** (`AUD-01..06` di [`05-audit-dokumentasi-qa/`](./05-audit-dokumentasi-qa/)) untuk memvalidasi kepatuhan ISO 29119-2:2021, *traceability*, akurasi data, zero PII, tautan Markdown, & sinkronisasi Word/PDF. | Tim QA & Audit | ✅ Selesai |
| 9 | Menghubungi & mewawancarai 1 praktisi QA / Software Tester **SETELAH** *project* GOR Permata selesai ([`04-wawancara-praktisi-qa/`](./04-wawancara-praktisi-qa/), arahan dosen 14 Nov 2026). | Tim Wawancara | ⬜ Siap Dilaksanakan |

---

## Struktur Dokumen Repositori (Sesuai Layer Proses ISO/IEC/IEEE 29119-2:2021)

- [`00-materi-perkuliahan/`](./00-materi-perkuliahan/) — Arsip modul materi perkuliahan (`Pertemuan 1–7.pptx`)
- [`01-standar-ieee-iso/`](./01-standar-ieee-iso/) — **Layer Organisasi (Clause 4 & 6) + Audit Kualitas Produk:**
  - [`organizational-test-specification.md`](./01-standar-ieee-iso/organizational-test-specification.md) — *Tailored Conformance*, *Organizational Test Policy*, & *Test Practices* (`OT1–OT3`)
  - [`standar-dokumentasi-qa.md`](./01-standar-ieee-iso/standar-dokumentasi-qa.md) — Matriks pemetaan seluruh *Information Items* ISO/IEC/IEEE 29119-2:2021
  - [`evaluasi-iso-25010-gor-permata.md`](./01-standar-ieee-iso/evaluasi-iso-25010-gor-permata.md) — Audit mutu 9 dimensi **ISO/IEC 25010:2023** dengan data eksekusi aktual
  - [`pdf-standar/`](./01-standar-ieee-iso/pdf-standar/) — Berkas PDF standar resmi `10.1109@IEEESTD.2021.9591508.pdf` (ISO 29119-2:2021) & ringkasan audit
- [`02-objek-umkm-dan-rencana-uji/`](./02-objek-umkm-dan-rencana-uji/) — **Layer Perencanaan (`7.2`) & Permodelan Uji (`8.2 TD1–TD2`):**
  - [`test-plan-gor-permata.md`](./02-objek-umkm-dan-rencana-uji/test-plan-gor-permata.md) — *Master Test Plan* (`TP-GOR-01`: konteks, *Test Basis*, risiko *Project vs Product*, strategi, jadwal, persetujuan)
  - [`performance-test-plan.md`](./02-objek-umkm-dan-rencana-uji/performance-test-plan.md) — *Performance Test Plan* (`TP-GOR-PERF-01`: *Web Vitals*, *Workload `1/5/10 VUs`*, SLA, *Circuit Breaker*)
  - [`test-model-blackbox.md`](./02-objek-umkm-dan-rencana-uji/test-model-blackbox.md) — *Test Basis* (`TB-BB-*`), *Test Models* (`TM-BB-01..05`), & *Test Coverage Items* (`TCI-BB-01..22`)
  - [`test-model-performance.md`](./02-objek-umkm-dan-rencana-uji/test-model-performance.md) — *Test Basis* (`TB-PERF-*`), *Workload/CWV Models* (`TM-PERF-01..03`), & `TCI-PERF-01..10`
  - [`analisis-white-black-gray-box.md`](./02-objek-umkm-dan-rencana-uji/analisis-white-black-gray-box.md) — *CFG* & $V(G)$ *White Box* serta analisis *Gray Box*
  - [`kandidat-objek-pengujian.md`](./02-objek-umkm-dan-rencana-uji/kandidat-objek-pengujian.md), [`referensi-sinta-1-3.md`](./02-objek-umkm-dan-rencana-uji/referensi-sinta-1-3.md), & [`pdf-jurnal/`](./02-objek-umkm-dan-rencana-uji/pdf-jurnal/)
- [`03-hasil-pengujian/`](./03-hasil-pengujian/) — **Layer Eksekusi (`8.2 TD3–TD4`, `8.3–8.5`) & Kontrol/Penutupan (`7.3–7.4`):**
  - [`test-environment-dan-data.md`](./03-hasil-pengujian/test-environment-dan-data.md) & [`test-data/`](./03-hasil-pengujian/test-data/) — Kesiapan lingkungan & data uji (`ED1–ED4`, beda Test vs Ops)
  - [`test-case-blackbox.md`](./03-hasil-pengujian/test-case-blackbox.md) & [`test-case-performance.md`](./03-hasil-pengujian/test-case-performance.md) — Spesifikasi *Test Case*, *Test Procedure*, & *Traceability Matrix*
  - [`test-execution-log.md`](./03-hasil-pengujian/test-execution-log.md) — Rekaman hasil aktual vs ekspektasi (`TE1–TE3`)
  - [`incident-reports.md`](./03-hasil-pengujian/incident-reports.md) — Laporan `10` insiden terverifikasi (`IR-GOR-01..10`)
  - [`test-status-and-control-report.md`](./03-hasil-pengujian/test-status-and-control-report.md) — Laporan pemantauan, *Control Directives*, & pembaruan risiko (`TMC1–TMC4`)
  - [`test-completion-report.md`](./03-hasil-pengujian/test-completion-report.md) — Laporan penutupan uji, aset terarsip, pembersihan lingkungan, & *Lessons Learned* (`TC1–TC4`)
  - [`test-cases-dan-laporan-bug.md`](./03-hasil-pengujian/test-cases-dan-laporan-bug.md) — Ringkasan eksekutif indeks hasil uji
  - [`Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.docx`](./03-hasil-pengujian/Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.docx) & [`Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.pdf`](./03-hasil-pengujian/Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.pdf) — Laporan resmi gabungan Word & PDF (`10` halaman, dibangkitkan via [`generate_laporan_pengujian.py`](./03-hasil-pengujian/generate_laporan_pengujian.py))
  - [`automation-scripts/`](./03-hasil-pengujian/automation-scripts/) & [`evidence/`](./03-hasil-pengujian/evidence/) — Skrip Playwright & `aiohttp`, Cypress, log TXT, metrik JSON, & screenshot bukti
- [`04-wawancara-praktisi-qa/`](./04-wawancara-praktisi-qa/) — Panduan wawancara praktisi QA *(siap dijalankan setelah fase `01`–`03` tuntas)*
- [`05-audit-dokumentasi-qa/`](./05-audit-dokumentasi-qa/) — **Audit Kepatuhan & Kualitas Dokumentasi (`AUD-01` s.d. `AUD-06`):**
  - [`implementation-plan-audit.md`](./05-audit-dokumentasi-qa/implementation-plan-audit.md) — Rencana implementasi audit dokumentasi
  - [`audit_dokumentasi.py`](./05-audit-dokumentasi-qa/audit_dokumentasi.py) & [`audit-results.json`](./05-audit-dokumentasi-qa/audit-results.json) — Skrip audit otomatis & keluaran metrik JSON
  - [`laporan-audit-dokumentasi.md`](./05-audit-dokumentasi-qa/laporan-audit-dokumentasi.md) — Laporan resmi hasil audit, remediasi, & status kesiapan asesmen

---

## Menjalankan Skrip Pengujian & Audit Secara Lokal
Pastikan Python (`>= 3.9`), `playwright`, `aiohttp`, dan `python-docx` terpasang (`pip install playwright aiohttp python-docx && playwright install chromium`), lalu jalankan dari *root* repositori:

```bash
# 1. Suite Black Box Testing (22 TC, non-destruktif)
python 03-hasil-pengujian/automation-scripts/test_gor_permata.py

# 2. Suite Performance Testing (10 TC: Web Vitals + Concurrent GET 1/5/10 VUs)
python 03-hasil-pengujian/automation-scripts/test_performance_gor_permata.py

# 3. Audit Otomatis Dokumentasi Repositori (AUD-01 s.d. AUD-06)
python 05-audit-dokumentasi-qa/audit_dokumentasi.py
```
Skrip pengujian bersifat **non-destruktif** (memblokir permintaan `POST **/bookings/store` melalui interceptor `page.route` dan membatasi uji beban hanya `GET` hingga `10 VUs` dengan *circuit breaker* otomatis).
