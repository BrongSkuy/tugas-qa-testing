# Tugas Testing dan QA Perangkat Lunak

Repositori dokumentasi tugas kelompok mata kuliah **Testing dan Quality Assurance (QA) Perangkat Lunak** — Program Studi Teknik Informatika (S1), Universitas Pamulang.

- **Dosen Pengampu:** Bapak Ahmad Fauzi
- **Kelas / Shift:** 07TPLE001 / Reguler C (Kelompok *[Diisi nomor 1–8]*)
- **Repositori:** https://github.com/BrongSkuy/tugas-qa-testing

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

Kelompok menetapkan **1 objek UMKM** utama sebagai studi kasus proyek pengujian hingga asesmen dan wawancara praktisi QA:

- **Nama Objek / Portal:** **Portal Booking GOR Permata Badminton Hall**
- **URL Portal:** https://gorpermatabadminton.com
- **Lokasi UMKM:** Kp. Cipari, Desa Ciakar, Kec. Panongan, Kab. Tangerang, Banten
- **Alasan Pemilihan:**
  - Sesuai 100% dengan contoh kasus yang disampaikan Bapak Ahmad Fauzi (*portal lapangan bulu tangkis skala lokal*).
  - Mendukung penuh seluruh teknik pengujian yang diwajibkan: **White Box** (skrip JS klien `normPhone()`, `submitBooking()`, dan `updateTotal()` pada `/booking` terbuka untuk dihitung *Cyclomatic Complexity*-nya secara nyata), **Black Box** (*Equivalence Partitioning*, *Boundary Value Analysis*, *State Transition*, *Use Case*), **Gray Box** (parameter URL `?start_date=`, token CSRF, dan *response handling*), **Manual Testing**, dan **Automation Testing** (Playwright Python & Cypress).
- **Batasan Etika Uji (Non-Destruktif):** Tidak pernah mengirimkan *booking* fiktif ke jadwal produksi (`POST /bookings/store` dihentikan pada validasi sisi klien dan diblokir via `page.route` di skrip otomasi).

---

## Progres Pengerjaan Tugas Kelompok

> Mengikuti **Checklist Rencana Tindak Lanjut Kelompok** (Bagian VI, Tabel 13 pada `Rangkuman_Tugas_QA_dan_Testing.docx`).

| No | Langkah Kerja Kelompok | Penanggung Jawab | Status |
| :-: | :--- | :--- | :---: |
| 1 | Koordinasi pembagian kelompok acak (Kelompok 1–8) & pengunggahan (*upload*) daftar nama anggota kelompok. | Seluruh Mahasiswa | ⏳ Proses |
| 2 | Mengambil & mempelajari modul lengkap (Pertemuan 1–7 sudah di [`00-materi-perkuliahan/`](./00-materi-perkuliahan/); Pertemuan 8–akhir menyusul dari Ketua Kelas). | Semua Anggota | ⏳ Proses |
| 3 | Membuat repositori GitHub *Public* (`https://github.com/BrongSkuy/tugas-qa-testing`) & melengkapi [tabel anggota](./README.md#anggota-kelompok). | Muhammad Faiz Rabbani | ⏳ Proses |
| 4 | Finalisasi objek UMKM terpilih di repo: fokus 1 objek yaitu **Portal Booking GOR Permata Badminton Hall** ([`kandidat-objek-pengujian.md`](./02-objek-umkm-dan-rencana-uji/kandidat-objek-pengujian.md)). | Tim Riset Objek | ✅ Selesai |
| 5 | Mengumpulkan & menyusun dokumentasi standar QA & Testing IEEE serta ISO periode 2022–2026 ([`01-standar-ieee-iso/`](./01-standar-ieee-iso/): 29119-1:2022 s.d. 29119-5:2024, audit ISO/IEC 25010:2023, 2 PDF ringkasan di `pdf-standar/`) serta 7 PDF *full paper* jurnal **SINTA 2–3** ([`pdf-jurnal/`](./02-objek-umkm-dan-rencana-uji/pdf-jurnal/)). | Tim Dokumentasi & Riset | ✅ Selesai |
| 6 | Menyusun & memfinalkan *Test Plan* (`TP-GOR-01` di [`test-plan-gor-permata.md`](./02-objek-umkm-dan-rencana-uji/test-plan-gor-permata.md)), analisis & *Flow Graph* White/Black/Gray Box ([`analisis-white-black-gray-box.md`](./02-objek-umkm-dan-rencana-uji/analisis-white-black-gray-box.md)), serta rancangan skenario uji *(draf awal sudah ada di folder `02`, belum final)*. | Tim QA & Riset | ⏳ Proses |
| 7 | Menjalankan pengujian berulang GOR Permata ([`03-hasil-pengujian/`](./03-hasil-pengujian/): Playwright `9/9 PASS` + log sudah di repo; lengkapi uji manual, eksekusi Cypress, & *screenshot* bukti) serta persiapan asesmen. | Tim Penguji | ⏳ Proses |
| 8 | Menghubungi & mewawancarai 1 praktisi QA / Software Tester **SETELAH** *project* GOR Permata selesai ([`04-wawancara-praktisi-qa/`](./04-wawancara-praktisi-qa/), arahan dosen 14 Nov 2026). | Tim Wawancara | ⬜ Belum |

---

## Struktur Repositori (Poin 1–7 & Update 14 Nov 2026)
- [`00-materi-perkuliahan/`](./00-materi-perkuliahan/) — Arsip modul materi perkuliahan (`Pertemuan 1–7.pptx` sudah tersedia; Pertemuan 8–akhir menyusul dari Ketua Kelas)
- [`01-standar-ieee-iso/`](./01-standar-ieee-iso/) — Acuan standar dokumentasi ISO/IEC/IEEE 29119 (2022–2024), audit kualitas **ISO/IEC 25010:2023**, serta [`pdf-standar/`](./01-standar-ieee-iso/pdf-standar/) (2 berkas PDF ringkasan standar ISO/IEC/IEEE 29119 & hasil audit mutu ISO/IEC 25010:2023)
- [`02-objek-umkm-dan-rencana-uji/`](./02-objek-umkm-dan-rencana-uji/) — Profil kandidat, *Test Plan*, analisis *White/Black/Gray Box* (dengan diagram *Control Flow Graph* Mermaid), daftar rujukan jurnal **SINTA 2–3**, serta [`pdf-jurnal/`](./02-objek-umkm-dan-rencana-uji/pdf-jurnal/) (7 berkas *full paper* PDF resmi)
- [`03-hasil-pengujian/`](./03-hasil-pengujian/) — Dokumentasi *Test Cases*, laporan bug terverifikasi (`BUG-GOR-01` s.d. `BUG-GOR-04`), serta folder [`automation-scripts/`](./03-hasil-pengujian/automation-scripts/) (Playwright Python `9/9 PASS`, contoh Cypress, dan `execution-log.txt`)
- [`04-wawancara-praktisi-qa/`](./04-wawancara-praktisi-qa/) — Panduan wawancara praktisi QA / Software Tester *(dilaksanakan **setelah** project pengujian selesai, sesuai arahan dosen 14 November 2026)*

---

## Menjalankan Skrip Automation Testing Secara Lokal
Pastikan Python dan Playwright terpasang (`pip install playwright && playwright install chromium`), lalu jalankan dari *root* repositori:

```bash
python 03-hasil-pengujian/automation-scripts/test_gor_permata.py
```
Skrip bersifat **non-destruktif** (memblokir permintaan `POST **/bookings/store` melalui interceptor `page.route` agar tidak pernah mengubah data jadwal nyata GOR Permata).
