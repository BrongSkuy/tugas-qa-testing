# Ringkasan Hasil Pengujian Black Box (`TC-BB-01` s.d. `TC-BB-23`)

Dokumen ini merangkum hasil eksekusi pengujian fungsional dan tampilan (**Black Box Testing**) pada **Portal Booking GOR Permata Badminton Hall** (`https://gorpermatabadminton.com`) yang dijalankan melalui [`test_gor_permata.py`](../automation-scripts/test_gor_permata.py) pada `2026-11-17T22:55:33+07:00` (data mentah: [`blackbox-results.json`](./blackbox-results.json)).

---

## 1. Ringkasan Eksekutif

- **Total Skenario Dijalankan:** `23` kasus uji (`5` teknik standar: *Equivalence Partitioning*, *Boundary Value Analysis*, *Decision Table*, *State Transition*, dan *Use Case / Compatibility*).
- **Hasil Eksekusi:** **`16` Berhasil (`PASS`)** dan **`7` Bermasalah (`FAIL`)** *(status `FAIL` menandakan pengujian berhasil menemukan kekurangan nyata pada website)*, dengan `0` error konsol JavaScript.
- **Yang Sudah Berjalan Baik (`16 Pass`):**
  - Seluruh `7` halaman utama publik (`/`, `/booking`, `/login`, dan `4` halaman `/fasilitas/*`) dapat dibuka normal (`HTTP 200 OK`).
  - Perhitungan harga otomatis durasi `1–5` jam (`Rp 40.000` s.d. `Rp 200.000`) tepat.
  - Aturan batas jam tutup `00:00` bekerja akurat (pesanan melewati jam `00:00` ditolak, sedangkan tepat sampai `00:00` lolos).
  - Validasi panjang nomor WhatsApp (`11–14` digit valid; `10` dan `15` digit ditolak), format huruf/pendek ditolak, token pengaman form `/login` aktif, pop-up booking reset bersih saat ditutup, serta notifikasi slot terkonfirmasi (`RTBC`) tampil sesuai.
- **7 Masalah yang Ditemukan (`7 Fail`):**
  1. **`IR-GOR-01` (`TC-BB-02`):** Halaman `/register` mengembalikan error `HTTP 404 Not Found`.
  2. **`IR-GOR-02` (`TC-BB-16`):** Nomor WhatsApp berawalan `+62 08...` gagal dinormalisasi dan ditolak sistem.
  3. **`IR-GOR-03` (`TC-BB-09`):** Kolom nama pemesan masih meloloskan isian spasi kosong (`"   "`) atau hanya `1` huruf (`"A"`).
  4. **`IR-GOR-04` (`TC-BB-22`):** Kode HTML halaman publik `/booking` menyertakan data nomor telepon dan nama pemesan pada `205` jadwal terisi.
  5. **`IR-GOR-05` (`TC-BB-04`):** Akses jadwal tanggal masa lalu (`?start_date=2020-01-01`) masih menampilkan `612` slot yang bisa diklik pesan.
  6. **`IR-GOR-06` (`TC-BB-05`):** Penulisan format tanggal rusak (`?start_date=invalid-date`) memicu crash server `HTTP 500 Server Error`.
  7. **`IR-GOR-10` (`TC-BB-21`):** Pada layar HP (`390×844`), menu atas halaman utama terpotong (`LOGIN` terpotong dan tombol `BOOKING` bergeser keluar layar).

---

## 2. Tabel Hasil 23 Kasus Uji Black Box

| ID Uji | Skenario yang Diuji | Hasil yang Diharapkan | Hasil Aktual di Website | Status | Ref. Insiden |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **`TC-BB-01`** | Akses `7` halaman publik utama | Semua terbuka normal (`HTTP 200`) | Ketujuh halaman terbuka normal (`200 OK`), `0` error konsol | **PASS** | — |
| **`TC-BB-02`** | Akses halaman `/register` | Tampil halaman daftar atau dialihkan dengan aman | Mengembalikan error `HTTP 404 Not Found` | **FAIL** | `IR-GOR-01` |
| **`TC-BB-03`** | Pilih tanggal valid (`2026-11-18`) | Jadwal tanggal terpilih tampil dengan slot tersedia | Jadwal tampil dengan `407` slot kosong aktif | **PASS** | — |
| **`TC-BB-04`** | Buka jadwal tanggal masa lalu (`2020-01-01`) | Tidak ada slot yang bisa dipesan (`0` slot) | Masih menampilkan `612` slot aktif yang bisa diklik | **FAIL** | `IR-GOR-05` |
| **`TC-BB-05`** | Buka jadwal dengan format tanggal rusak (`invalid-date`) | Kembali aman ke tanggal hari ini / pesan error terkontrol | Server crash `HTTP 500 Server Error` | **FAIL** | `IR-GOR-06` |
| **`TC-BB-06`** | Klik slot kosong `+` untuk membuka pop-up booking | Pop-up tampil, durasi default `1` jam, total `Rp 40.000` | Pop-up tampil sesuai (`durasi = 1`, `Rp 40.000`) | **PASS** | — |
| **`TC-BB-07`** | Ubah pilihan durasi main `1` sampai `5` jam | Harga berubah tepat (`Rp 40.000` s.d. `Rp 200.000`) | Seluruh `5` tingkat durasi dihitung tepat | **PASS** | — |
| **`TC-BB-08`** | Kirim form saat Nama dan WA kosong | Muncul peringatan wajib isi, tidak dikirim | Muncul peringatan wajib isi, tidak dikirim | **PASS** | — |
| **`TC-BB-09`** | Isi Nama dengan spasi `"   "` atau `1` huruf `"A"` | Ditolak sebelum dikirim ke server | Lolos pengecekan di browser sebelum dicegat skrip uji | **FAIL** | `IR-GOR-03` |
| **`TC-BB-10`** | Isi Nomor WA tidak valid (`12345` dan `abc`) | Muncul peringatan format WA salah | Muncul peringatan format WA salah, tidak dikirim | **PASS** | — |
| **`TC-BB-11`** | Isi Nomor WA terlalu pendek (`10` digit) | Ditolak karena di bawah batas `11` digit | Ditolak dengan peringatan format WA | **PASS** | — |
| **`TC-BB-12`** | Isi Nomor WA batas bawah valid (`11` digit) | Lolos pengecekan format WA | Lolos validasi klien dan dicegat aman oleh skrip uji | **PASS** | — |
| **`TC-BB-13`** | Isi Nomor WA batas atas valid (`14` digit) | Lolos pengecekan format WA | Lolos validasi klien dan dicegat aman oleh skrip uji | **PASS** | — |
| **`TC-BB-14`** | Isi Nomor WA terlalu panjang (`15` digit) | Ditolak karena melebihi batas `14` digit | Ditolak dengan peringatan format WA | **PASS** | — |
| **`TC-BB-15`** | Isi Nomor WA awalan `8...` dan `628...` | Keduanya dikenali sebagai format sah | Keduanya dinormalisasi dan lolos validasi klien | **PASS** | — |
| **`TC-BB-16`** | Isi Nomor WA awalan `+62 08123456789` | Dinormalisasi menjadi `628...` dan diterima | Berubah menjadi `6208...` sehingga ditolak sistem | **FAIL** | `IR-GOR-02` |
| **`TC-BB-17`** | Pesan jam `22:00` durasi `3` jam (selesai `01:00`) | Ditolak karena melewati jam tutup `00:00` | Muncul peringatan tutup jam `00:00`, tidak dikirim | **PASS** | — |
| **`TC-BB-18`** | Pesan jam `22:00` durasi `2` jam (tepat `00:00`) | Lolos batas jam operasional | Lolos pengecekan jam tutup dan dicegat aman | **PASS** | — |
| **`TC-BB-19`** | Tutup pop-up booking (`closeModal()`) | Pop-up tertutup dan kolom nama/WA kembali kosong | Pop-up tertutup dan seluruh kolom ter-reset bersih | **PASS** | — |
| **`TC-BB-20`** | Cek keamanan dasar & validasi form `/login` | Token CSRF tersedia; email/password kosong/salah ditolak | Token CSRF aktif dan seluruh validasi HTML5 bekerja | **PASS** | — |
| **`TC-BB-21`** | Cek tampilan layar HP (`390×844`) | Tidak ada menu terpotong; pop-up muat di layar | Pop-up booking muat (`350 px`), namun menu atas beranda terpotong | **FAIL** | `IR-GOR-10` |
| **`TC-BB-22`** | Cek privasi data pemesan pada kode HTML publik `/booking` | Nomor HP pelanggan tidak muncul di kode halaman publik | Ditemukan `205` jadwal memuat nomor WA dan nama di HTML publik | **FAIL** | `IR-GOR-04` |
| **`TC-BB-23`** | Klik slot biru terkonfirmasi (sampel `RTBC`) | Muncul pesan bahwa booking sudah dikonfirmasi | Ditemukan `114` slot `RTBC`; dialog konfirmasi tampil sesuai | **PASS** | — |

---

## 3. Catatan Pengembangan & Review Desain Uji (Tim Test Design)

Sebagai tindak lanjut evaluasi terhadap `23` kasus uji di atas, anggota tim peran *Test Design* (`@meongasli` / Dzikri Attariq Samayaki) telah menambahkan dokumen review (`REV-01` s.d. `REV-10`) dan **`9` usulan kasus uji lanjutan** (`TC-BB-24` s.d. `TC-BB-32`, mencakup nama kosong dengan WA valid, nama terisi dengan WA kosong, tanggal kalender mustahil `2027-02-30`, batas jam `23:00`, durasi `5 -> 1` jam, pemulihan setelah alert, layar HP `360×800`, serta buka ulang modal). Seluruh `9` kasus tambahan tersebut berstatus **`Not Executed`** (draf usulan pengembangan) dan tidak mengubah hasil `23` kasus uji yang telah dieksekusi:
- Dokumen review desain: [`test-design-review.md`](../../02-objek-umkm-dan-rencana-uji/test-design-review.md)
- Dokumen `9` kasus uji usulan: [`test-case-additional.md`](../test-case-additional.md)

---

## 4. Dokumen Pendukung & Laporan Lengkap

- **Spesifikasi Skenario & Prosedur:** [`test-case-blackbox.md`](../test-case-blackbox.md)
- **Log Eksekusi & Daftar Screenshot:** [`test-execution-log.md`](../test-execution-log.md) | [`execution-log.txt`](../automation-scripts/execution-log.txt) | [`blackbox-results.json`](./blackbox-results.json)
- **Rincian 10 Masalah & Saran Perbaikan:** [`incident-reports.md`](../incident-reports.md)
- **Laporan Resmi Lengkap (Word & PDF):** [`05-dokumentasi-laporan/`](../../05-dokumentasi-laporan/)
