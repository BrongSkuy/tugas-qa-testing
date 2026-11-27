# Panduan Bahasa Sederhana: Prinsip Pengujian Aman (Non-Destruktif) & Cara Menjalankan Script

Dokumen ini menjelaskan dalam bahasa sehari-hari apa maksud **Prinsip Pengujian Aman (Non-Destruktif)** pada proyek **Portal Booking GOR Permata Badminton Hall** (`https://gorpermatabadminton.com`), serta **di mana letak script-nya dan ke mana perintah harus di-copy-paste**.

---

## 1. Apa Arti "Pengujian Aman (Non-Destruktif)"?

Website **GOR Permata Badminton Hall** sedang **aktif dipakai oleh pelanggan sungguhan setiap hari** untuk memesan lapangan bulu tangkis. Karena itu, saat menguji website tersebut, kita tidak boleh:
1. Mengirimkan pesanan palsu secara terus-menerus sampai memenuhi jadwal asli di database website.
2. Membuka menu admin tanpa izin.
3. Menyerang website dengan ribuan akses sekaligus sampai server *down* (lemot/mati).

### Bagaimana Cara Skrip Otomatis Menjaganya Tetap Aman?
1. **Saat mengetes form pemesanan lapangan (23 tes Black Box):**
   - Skrip otomatis (`test_gor_permata.py`) memang mengisi kolom **Nama** dan **Nomor WA** memakai data contoh palsu (misalnya `"Test QA"` dan `"08123456789"`).
   - Namun, sebelum data benar-benar terkirim ke server website (`POST /bookings/store`), skrip otomatis **langsung membatalkan proses kirimnya di dalam browser** (`page.route` -> `route.abort()`).
   - Akibatnya, saat skrip otomatis dijalankan berulang kali, **tidak ada pesanan palsu yang masuk ke jadwal asli GOR Permata** (`network_posts_sent_to_server = 0`).
   - *Catatan Penting:* Pengaman otomatis ini **hanya aktif ketika kamu menjalankan skrip Playwright/Cypress**. Jika kamu mengetes sendiri secara manual dengan mengklik tombol *"Booking Sekarang"* di Google Chrome biasa tanpa menyalakan pemblokir di DevTools (`F12`), maka data pesanan bisa benar-benar terkirim dan tersimpan ke website.
2. **Saat mengetes kecepatan website (10 tes Performance):**
   - Skrip (`test_performance_gor_permata.py`) hanya melakukan aksi **baca halaman (`GET`)**, tidak pernah mengirim data formulir.
   - Simulasi pengguna bersamaan dibatasi maksimal **1, 5, dan 10 orang** dengan jeda istirahat antar-tahap, dan langsung berhenti otomatis (*circuit breaker*) jika error melebihi 5%.

---

## 2. Script-nya Ada di Mana dan Harus Di-Copy-Paste ke Mana?

Banyak pemula bingung: *"Apakah seluruh isi kode script Python/JS ini harus di-copy-paste ke Terminal?"*  
Jawabannya: **TIDAK PERLU copy-paste seluruh isi kodenya!**

Karena seluruh file programnya **sudah tersedia dan siap pakai** di dalam folder repositori ini (`03-hasil-pengujian/automation-scripts/`). Yang kamu **copy-paste ke Terminal (CMD / PowerShell / Terminal VS Code)** hanyalah **baris perintah pendek untuk memanggil filenya**.

### Daftar File Script & Kegunaannya

| Nama File | Lokasi Folder | Fungsi Singkat | Apakah Kode Isinya Di-copy ke Terminal? |
| :--- | :--- | :--- | :--- |
| `test_gor_permata.py` | `03-hasil-pengujian/automation-scripts/` | Menjalankan **23 tes fungsi website** (Playwright) secara otomatis + foto bukti | **Tidak.** Copy-paste perintah `python ...` saja ke Terminal. |
| `test_performance_gor_permata.py` | `03-hasil-pengujian/automation-scripts/` | Menjalankan **10 tes kecepatan website** + simulasi `1, 5, 10` orang bersamaan | **Tidak.** Copy-paste perintah `python ...` saja ke Terminal. |
| `generate_laporan_pengujian.py` | `03-hasil-pengujian/` | Membuat ulang grafik performa dan file laporan resmi Word (`.docx`) & PDF (`.pdf`) | **Tidak.** Copy-paste perintah `python ...` saja ke Terminal. |
| `gor-permata.cy.js` | `03-hasil-pengujian/automation-scripts/` | Contoh kode pembanding untuk **Cypress** (bukan Python) | **Tidak.** Dipakai hanya jika kamu menyalin isinya ke proyek aplikasi **Cypress**. |

---

## 3. Langkah Praktis Copy-Paste Perintah ke Terminal (Windows)

Ikuti langkah ini dari nol di komputer Windows:

### Langkah 1 — Buka Terminal
Kamu bisa memakai salah satu aplikasi ini (pilih yang paling nyaman):
- **Command Prompt (CMD):** Tekan tombol `Windows`, ketik `cmd`, lalu klik **Command Prompt**.
- **PowerShell:** Klik kanan di dalam folder `tugas-qa-testing`, lalu pilih **Open in Terminal**.
- **Terminal VS Code:** Buka folder `tugas-qa-testing` di VS Code, lalu tekan `` Ctrl + ` `` (tombol di sebelah kiri angka `1`).

### Langkah 2 — Masuk ke Folder Proyek (`tugas-qa-testing`)
*(Lewati langkah ini jika kamu sudah membuka Terminal langsung dari dalam folder `tugas-qa-testing`.)*  
Copy-paste perintah berikut ke Terminal lalu tekan **Enter**:
```powershell
cd "c:\Users\Faiz\Dokumen\UNPAM\Semester 7\TESTING DAN QA PERANGKAT LUNAK\Tugas\tugas-qa-testing"
```
*(Sesuaikan alamat foldernya jika lokasi penyimpanan di komputermu berbeda.)*

### Langkah 3 — Pasang Alat Bantu Pengujian *(Cukup Sekali Saja)*
Pastikan **Python** (`>= 3.9`) sudah terpasang, lalu copy-paste kedua baris ini ke Terminal dan tekan **Enter**:
```bash
pip install playwright aiohttp python-docx pillow pywin32
playwright install chromium
```
*(Catatan: `pywin32` dan Microsoft Word di Windows dipakai khusus oleh `generate_laporan_pengujian.py` saat mengubah file `.docx` menjadi `.pdf`.)*

### Langkah 4 — Jalankan File `.py` (Lewat Terminal atau VS Code)
Ada **2 cara aman** untuk menjalankan kode Python di file `.py`:

1. **Lewat Terminal / CMD / PowerShell / Terminal VS Code *(Disarankan)*:**  
   Copy-paste perintah di bawah ke Terminal lalu tekan **Enter**:
   ```bash
   # 1. Jalankan 23 tes fungsi Black Box (aman, kirim form diblokir otomatis)
   python 03-hasil-pengujian/automation-scripts/test_gor_permata.py

   # 2. Jalankan 10 tes kecepatan & beban pengunjung (1, 5, 10 orang)
   python 03-hasil-pengujian/automation-scripts/test_performance_gor_permata.py

   # 3. Buat ulang file laporan Word (.docx) & PDF (.pdf)
   python 03-hasil-pengujian/generate_laporan_pengujian.py
   ```
2. **Lewat Tombol Run (`▶`) di VS Code:**  
   Buka file `.py` yang ingin dijalankan di **VS Code** (pastikan *extension* Python sudah terpasang), lalu klik tombol **Run Python File (`▶`)** di pojok kanan atas editor. VS Code akan otomatis menjalankan perintah `python ...` di Terminal bawah tanpa perlu mengetik manual.

> **Kenapa jangan klik 2x (double-click) file `.py` di File Explorer?**  
> Jika diklik 2x langsung dari folder Windows, jendela hitam akan langsung tertutup otomatis begitu script selesai atau error, sehingga pesan hasil / error-nya tidak sempat terbaca. Selain itu, pastikan komputer terhubung internet karena script pengujian membuka `https://gorpermatabadminton.com` di browser Chromium otomatis (*headless*/di belakang layar).

### Langkah 5 — Lihat Hasilnya
Setelah perintah selesai berjalan (tidak ada error di Terminal), hasilnya otomatis tersimpan di:
- **Catatan teks hasil uji:** `03-hasil-pengujian/automation-scripts/execution-log.txt` dan `performance-log.txt`
- **Data mentah JSON:** `03-hasil-pengujian/evidence/blackbox-results.json` dan `performance-metrics.json`
- **Gambar bukti & grafik:** `03-hasil-pengujian/evidence/screenshots/`
- **Laporan Word & PDF:** `05-dokumentasi-laporan/`

---

## 4. Kapan Ada Bagian yang TIDAK Di-Copy ke Terminal?

Di beberapa dokumen (seperti [`test-case-blackbox.md`](./test-case-blackbox.md) atau [`analisis-white-black-gray-box.md`](../02-objek-umkm-dan-rencana-uji/analisis-white-black-gray-box.md)), kamu akan melihat potongan kode atau langkah manual seperti:
1. **Kode JavaScript website (`normPhone`, `submitBooking`):** Itu hanya **cuplikan kode dari website GOR Permata** sebagai penjelasan kenapa bug bisa terjadi — **jangan di-copy ke Terminal**.
2. **Blokir manual saat tes lewat browser Chrome/Edge biasa:** Jika kamu mengetes form booking secara manual dengan klik di Chrome (bukan pakai `python ...`), pengaman dilakukan lewat **Google Chrome DevTools**: tekan `F12` -> tab **Network** -> cari menu **Request blocking** -> masukkan pola `*/bookings/store`.
