# Additional Black Box Test Cases — Usulan Pengembangan TD2–TD4

**Objek:** Portal Booking GOR Permata Badminton Hall  
**Penyusun:** Dzikri Attariq Samayaki (@meongasli) — Test Design  
**Status:** Not Executed (seluruh kasus); menunggu review tim.

## 1. Dasar rancangan

Dokumen ini menindaklanjuti [Test Design Review](../02-objek-umkm-dan-rencana-uji/test-design-review.md) dan melengkapi [Test Case awal](test-case-blackbox.md). ID 24–32 merupakan usulan lanjutan, bukan penggantian kasus 01–23. Expected result diturunkan dari test basis yang tersedia; kebutuhan dan slot aktual tetap harus dikonfirmasi.

## 2. Prasyarat keselamatan

- Gunakan lingkungan uji yang diizinkan. Untuk setiap skenario submit, gunakan data sintetis dari test data tim dan interceptor yang telah diverifikasi untuk mencegah seluruh request transaksi mencapai server. Jangan melanjutkan submit apabila pemblokiran tidak dapat dipastikan.
- Gunakan slot kosong pada tanggal mendatang dan durasi yang tidak melewati jam tutup kecuali untuk uji batas. Reset modal dan penghitung request sebelum tiap kasus.
- `delta_post` berarti jumlah percobaan POST yang dicegat secara lokal selama kasus, bukan jumlah transaksi yang dikirim ke server. Untuk semua kasus, jumlah POST transaksi yang benar-benar dikirim harus 0.
- Jangan menyimpan data pribadi pelanggan. Jika prasyarat tidak tersedia, catat Blocked/Not Executed, bukan Fail.
- Untuk kasus tanggal tidak valid, gunakan lingkungan uji yang diizinkan, tanpa pengujian berulang yang membebani layanan.

## 3. Spesifikasi kasus uji tambahan

| ID TC / TCI usulan | Acuan | Teknik | Prasyarat | Input dan langkah uji | Expected Result | Prioritas |
|---|---|---|---|---|---|---|
| TC-BB-24 / TCI-BB-24 | REV-01; TB-BB-05; TM-BB-02 | Decision Table R1 | Modal terbuka; interceptor aktif | Kosongkan nama, isi WA sintetis valid sesuai test data tim, durasi 1; klik Booking. | Alert wajib isi; delta_post = 0. | Tinggi |
| TC-BB-25 / TCI-BB-25 | REV-02; TB-BB-05; TM-BB-02 | Decision Table R2 | Modal terbuka; interceptor aktif | Isi nama Test QA, kosongkan WA, durasi 1; klik Booking. | Alert wajib isi; delta_post = 0. | Tinggi |
| TC-BB-26 / TCI-BB-26 | REV-03; TB-BB-02; TM-BB-01 | EP | Lingkungan uji tersedia | Buka /booking dengan start_date=2027-02-30 sekali. | Penolakan terkontrol atau fallback ke tanggal valid yang jelas; tidak HTTP 500. | Tinggi |
| TC-BB-27 / TCI-BB-27 | REV-04; TB-BB-05; TM-BB-01 | BVA | Slot 23.00 tersedia; interceptor aktif | Isi nama dan WA sintetis valid, durasi 1; klik Booking. | Lolos aturan jam tutup (23+1=24); jika validasi lain terpenuhi, delta_post = 1, dicegat lokal. | Sedang |
| TC-BB-28 / TCI-BB-28 | REV-04; TB-BB-05; TM-BB-01 | BVA | Slot 23.00 tersedia; interceptor aktif | Isi data valid, durasi 2; klik Booking jika opsi tersedia. | Durasi ditolak atau opsi tidak tersedia karena melewati jam tutup (23+2=25); delta_post = 0. | Sedang |
| TC-BB-29 / TCI-BB-29 | REV-05; TB-BB-04; TM-BB-01/03 | State Transition | Modal terbuka pada slot yang memungkinkan 5 jam | Pilih durasi 5, periksa total; ubah ke 1. Jangan submit. | Total berubah dari Rp200.000 menjadi Rp40.000 tanpa memuat ulang halaman. | Sedang |
| TC-BB-30 / TCI-BB-30 | REV-06; TB-BB-05; TM-BB-03 | State Transition | Modal terbuka; interceptor aktif | Isi nama Test QA dan WA abc; submit; tutup alert; perbaiki WA menjadi data sintetis valid; submit ulang. | Submit pertama ditolak (delta_post = 0); modal tetap terbuka; submit kedua lolos validasi dan dicegat lokal (delta_post = 1 untuk percobaan kedua); tombol aktif kembali setelah penanganan kegagalan jaringan. | Tinggi |
| TC-BB-31 / TCI-BB-31 | REV-07; TB-BB-07; TM-BB-05 | Compatibility | Viewport 360×800 | Buka beranda dan jadwal; buka modal slot kosong; periksa menu dan kontrol modal. Jangan submit. | Menu dan kontrol utama dapat diakses; tidak ada overflow yang membuat kontrol tidak dapat digunakan. | Sedang |
| TC-BB-32 / TCI-BB-32 | REV-08; TB-BB-03; TM-BB-03 | State Transition | Modal slot kosong tersedia | Isi nama dan WA sintetis; tutup modal; buka kembali slot yang sama. Jangan submit. | Nama dan WA kosong; durasi default 1 dan total Rp40.000. | Sedang |

## 4. Prosedur dan status

| Prosedur usulan | Kasus | Pelaksanaan |
|---|---|---|
| PROC-ADD-01 | TC-BB-24/25/30 | Validasi input dan pemulihan dengan interceptor terverifikasi. |
| PROC-ADD-02 | TC-BB-26 | Penanganan tanggal kalender tidak valid pada lingkungan uji yang diizinkan. |
| PROC-ADD-03 | TC-BB-27/28 | Variasi batas jam tutup dengan interceptor terverifikasi. |
| PROC-ADD-04 | TC-BB-29/32 | Kalkulasi dan siklus modal tanpa submit. |
| PROC-ADD-05 | TC-BB-31 | Pemeriksaan viewport tambahan tanpa submit. |

Actual result, bukti dan verdict seluruh kasus belum tersedia. Seluruh status tetap **Not Executed** hingga tester melakukan eksekusi. Kasus nama satu karakter tidak ditambahkan karena menunggu klarifikasi kebutuhan (REV-09). Usulan penegasan interceptor (REV-10) diterapkan pada prasyarat dokumen ini.

## 5. Batasan

Review berdasarkan dua spesifikasi awal; script, log dan test data belum diperiksa. Cakupan tambahan dan ID harus disetujui tim sebelum integrasi. Tidak ada klaim bahwa skenario ini telah dijalankan atau bahwa website memiliki defect baru.
