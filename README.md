# Tugas Testing dan QA Perangkat Lunak

Repositori dokumentasi tugas kelompok mata kuliah **Testing dan Quality Assurance (QA) Perangkat Lunak** — Program Studi Teknik Informatika (S1), Universitas Pamulang.

- **Dosen Pengampu:** Asep Erlan Maulana, S.Kom., M.Kom
- **Kelas / Shift:** 07TPLE001 / Reguler C
- **Repositori:** https://github.com/BrongSkuy/tugas-qa-testing
- **Standar Proses Acuan:** **ISO/IEC/IEEE 29119-2:2021(E) (*Test Processes*)** ([`10.1109@IEEESTD.2021.9591508.pdf`](./01-standar-ieee-iso/pdf-standar/10.1109@IEEESTD.2021.9591508.pdf))

---

## Anggota Kelompok
> *Keempat anggota kelompok berikut tergabung sebagai tim QA kolaboratif dan kolaborator pada repositori GitHub ini.*

| No | Nama Lengkap | NIM | Akun GitHub |
| :--- | :--- | :--- | :--- |
| 1 | Muhammad Faiz Rabbani | 231011402539 | [@BrongSkuy](https://github.com/BrongSkuy) |
| 2 | Robi Farhan Anshori | 231011401468 | [@robifr](https://github.com/robifr) |
| 3 | Dzikri Attariq Samayaki | 221011401148 | [@meongasli](https://github.com/meongasli) |
| 4 | Nurlaelasari | 231011403531 | [@ela123-code](https://github.com/ela123-code) |

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
| 1 | Pengisian lengkap data keempat anggota kelompok (`07TPLE001 / Reguler C`). | Seluruh Anggota (`Tim QA`) | ✅ Selesai |
| 2 | Mengambil & mempelajari modul lengkap (Pertemuan 1–7 di [`00-materi-perkuliahan/`](./00-materi-perkuliahan/); Pertemuan 8–akhir menyusul dari Ketua Kelas). | Semua Anggota | ⏳ Proses |
| 3 | Membuat repositori GitHub *Public* (`https://github.com/BrongSkuy/tugas-qa-testing`), melengkapi [tabel anggota](./README.md#anggota-kelompok), & mengundang kolaborator (`@robifr`, `@meongasli`, `@ela123-code`). | Tim QA | ✅ Selesai |
| 4 | Finalisasi objek UMKM terpilih di repo: **Portal Booking GOR Permata Badminton Hall** ([`kandidat-objek-pengujian.md`](./02-objek-umkm-dan-rencana-uji/kandidat-objek-pengujian.md)). | Tim Riset Objek | ✅ Selesai |
| 5 | Menyusun dokumentasi standar QA & Testing IEEE/ISO lengkap ([`01-standar-ieee-iso/`](./01-standar-ieee-iso/): *Organizational Test Spec*, `29119-2:2021`, audit `ISO 25010:2023`, 3 PDF standar) & 7 PDF jurnal **SINTA 2–3** ([`pdf-jurnal/`](./02-objek-umkm-dan-rencana-uji/pdf-jurnal/)). | Tim Dokumentasi & Riset | ✅ Selesai |
| 6 | Memfinalkan *Master Test Plan* (`TP-GOR-01`), *Performance Test Plan* (`TP-GOR-PERF-01`), *Test Model Specifications* & *TCI* (Black Box + Performance), serta *White/Gray Box CFG* di [`02-objek-umkm-dan-rencana-uji/`](./02-objek-umkm-dan-rencana-uji/). | Tim QA & Riset | ✅ Selesai |
| 7 | Menjalankan pengujian aktual Black Box (`23 TC`: `16 PASS`, `7` temuan cacat) & Performance (`10 TC`: `7 PASS`, `3` temuan SLA/payload) beserta *Environment/Data Readiness*, *Execution Log*, *Incident Reports* (`IR-GOR-01..10`), *Status/Control Report*, *Test Completion Report*, bukti `12` gambar/grafik & JSON ([`03-hasil-pengujian/`](./03-hasil-pengujian/)), serta menyimpan **Laporan Resmi Word & PDF** di [`05-dokumentasi-laporan/`](./05-dokumentasi-laporan/). | Tim Penguji | ✅ Selesai |
| 8 | Menghubungi & mewawancarai 1 praktisi QA / Software Tester **SETELAH** *project* GOR Permata selesai ([`04-wawancara-praktisi-qa/`](./04-wawancara-praktisi-qa/), arahan dosen 14 Nov 2026). | Tim Wawancara | ⬜ Siap Dilaksanakan |

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
  - [`test-model-blackbox.md`](./02-objek-umkm-dan-rencana-uji/test-model-blackbox.md) — *Test Basis* (`TB-BB-*`), *Test Models* (`TM-BB-01..05`), & *Test Coverage Items* (`TCI-BB-01..23`)
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
  - [`generate_laporan_pengujian.py`](./03-hasil-pengujian/generate_laporan_pengujian.py) — Skrip generator laporan Word & PDF menuju folder `05-dokumentasi-laporan/`
  - [`automation-scripts/`](./03-hasil-pengujian/automation-scripts/) & [`evidence/`](./03-hasil-pengujian/evidence/) — Skrip Playwright & `aiohttp`, Cypress, log TXT, metrik JSON, & screenshot bukti
- [`04-wawancara-praktisi-qa/`](./04-wawancara-praktisi-qa/) — Panduan wawancara praktisi QA *(siap dijalankan setelah fase `01`–`03` tuntas)*
- [`05-dokumentasi-laporan/`](./05-dokumentasi-laporan/) — **Arsip Dokumen Resmi Format Word (`.docx`) & PDF (`.pdf`):**
  - [`Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.docx`](./05-dokumentasi-laporan/Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.docx) — Laporan hasil pengujian lengkap format Microsoft Word
  - [`Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.pdf`](./05-dokumentasi-laporan/Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.pdf) — Laporan hasil pengujian lengkap format PDF dengan bahasa populer/mudah dipahami (`11` halaman, termasuk `12` bukti visual `01`–`12`)

---

## Menjalankan Skrip Pengujian & Generator Laporan Secara Lokal
Pastikan Python (`>= 3.9`), `playwright`, `aiohttp`, `python-docx`, dan `Pillow` terpasang (`pip install playwright aiohttp python-docx pillow && playwright install chromium`), lalu jalankan dari *root* repositori:

```bash
# 1. Suite Black Box Testing (23 TC, non-destruktif)
python 03-hasil-pengujian/automation-scripts/test_gor_permata.py

# 2. Suite Performance Testing (10 TC: Web Vitals + Concurrent GET 1/5/10 VUs)
python 03-hasil-pengujian/automation-scripts/test_performance_gor_permata.py

# 3. Regenerasi Laporan Resmi Word & PDF ke folder 05-dokumentasi-laporan/
python 03-hasil-pengujian/generate_laporan_pengujian.py
```
Skrip pengujian bersifat **non-destruktif** (memblokir permintaan `POST **/bookings/store` melalui interceptor `page.route` dan membatasi uji beban hanya `GET` hingga `10 VUs` dengan *circuit breaker* otomatis).
