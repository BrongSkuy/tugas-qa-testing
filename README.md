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

## Dua Objek Pengujian UMKM Terdokumentasi

Repositori ini mendokumentasikan **dua objek UMKM di wilayah Tangerang & Tangerang Selatan** dalam folder terpisah agar kelompok memiliki cakupan uji lengkap (baik sisi *White Box* maupun pengujian berulang tanpa *checkout*):

| Aspek | Objek 1: GOR Permata Badminton Hall | Objek 2: Website Kolam Renang TASA |
| :--- | :--- | :--- |
| **Folder Kerja** | [`objek-1-gor-permata/`](./objek-1-gor-permata/) | [`objek-2-kolam-renang-tasa/`](./objek-2-kolam-renang-tasa/) |
| **URL Situs** | https://gorpermatabadminton.com | https://www.kolamtasa.com/ |
| **Lokasi UMKM** | Desa Ciakar, Kec. Panongan, Kab. Tangerang | Pd. Benda, Kec. Pamulang, Kota Tangerang Selatan |
| **Kelebihan Utama untuk QA** | Sesuai 100% analogi dosen (*lapangan bulu tangkis lokal*); skrip JS `/booking` terbuka untuk hitung *Cyclomatic Complexity* ($V(G)$) secara nyata. | **Tanpa fitur checkout/payment** (redirect WhatsApp); aman uji berulang pada wizard `/lesrenang`; memiliki 6 temuan defect nyata (form `/kontak` mati, footer `404`, 5 *security header* hilang). |
| **Batasan Etika Uji** | Tidak submit booking nyata (`POST /bookings/store` diblokir pada skrip otomasi). | Tidak spam submit akhir `/lesrenang` dan form `/event` (`POST` diblokir pada skrip otomasi). |
| **Skrip Automation** | Playwright Python (`9/9 PASS`) + contoh Cypress | Playwright Python (`8/8 PASS`) + contoh Cypress |

---

## Struktur Repositori (Poin 1–3 & Update 14 Nov 2026)
- [`00-materi-perkuliahan/`](./00-materi-perkuliahan/) — Arsip modul materi perkuliahan (`Pertemuan 1–7.pptx` sudah tersedia; Pertemuan 8–akhir menyusul dari Ketua Kelas)
- [`01-standar-ieee-iso/`](./01-standar-ieee-iso/) — Acuan standar dokumentasi QA & Testing ISO/IEC/IEEE 29119 & ISO/IEC 25010 (2022–2026)
- [`02-objek-umkm-dan-rencana-uji/`](./02-objek-umkm-dan-rencana-uji/) — Penelusuran kandidat objek UMKM & daftar referensi jurnal Sinta 1–3
- [`objek-1-gor-permata/`](./objek-1-gor-permata/) — *Test Plan*, analisis *White/Black/Gray Box*, *Test Cases & Bug Report*, serta skrip otomasi + log untuk **GOR Permata Badminton Hall**
- [`objek-2-kolam-renang-tasa/`](./objek-2-kolam-renang-tasa/) — Profil rute, *Test Plan*, analisis *White/Black/Gray Box*, *Test Cases & 6 Bug Report*, serta skrip otomasi + log untuk **Kolam Renang TASA**
- [`03-hasil-pengujian/`](./03-hasil-pengujian/) — Ringkasan komparasi hasil pengujian dan defect dari kedua objek
- [`04-wawancara-praktisi-qa/`](./04-wawancara-praktisi-qa/) — Panduan wawancara praktisi QA / Software Tester *(dilaksanakan **setelah** project pengujian selesai, sesuai arahan dosen 14 November 2026)*

---

## Menjalankan Skrip Automation Testing Secara Lokal
Pastikan Python dan Playwright terpasang (`pip install playwright && playwright install chromium`), lalu jalankan:

```bash
# Objek 1: GOR Permata Badminton Hall
python objek-1-gor-permata/automation-scripts/test_gor_permata.py

# Objek 2: Kolam Renang TASA Pamulang
python objek-2-kolam-renang-tasa/automation-scripts/test_kolam_tasa.py
```
Kedua skrip bersifat **non-destruktif** (memblokir permintaan `POST` ke server produksi via interceptor `page.route`).
