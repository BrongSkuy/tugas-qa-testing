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
| 2 | *[Diisi]* | *[Diisi]* | *[Diisi]* |
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

## Struktur Repositori (Poin 1–7 & Update 14 Nov 2026)
- [`00-materi-perkuliahan/`](./00-materi-perkuliahan/) — Arsip modul materi perkuliahan (`Pertemuan 1–7.pptx` sudah tersedia; Pertemuan 8–akhir menyusul dari Ketua Kelas)
- [`01-standar-ieee-iso/`](./01-standar-ieee-iso/) — Acuan standar dokumentasi ISO/IEC/IEEE 29119 (2022–2024), audit kualitas **ISO/IEC 25010:2023**, serta [`pdf-standar/`](./01-standar-ieee-iso/pdf-standar/) (2 PDF ringkasan & hasil audit standar)
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
