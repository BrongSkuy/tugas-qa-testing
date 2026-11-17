# Test Case & Test Procedure Specification — Black Box Testing (`TD3` & `TD4`)

Dokumen ini mengimplementasikan aktivitas **`TD3` (*Derive test cases*)** dan **`TD4` (*Create test procedures*)** sesuai **ISO/IEC/IEEE 29119-2:2021(E) §8.2**, diturunkan langsung dari *Test Model* dan *Test Coverage Items* pada [`../02-objek-umkm-dan-rencana-uji/test-model-blackbox.md`](../02-objek-umkm-dan-rencana-uji/test-model-blackbox.md) dengan sumber data [`test-data/blackbox-testdata.json`](./test-data/blackbox-testdata.json).

---

## 1. *Test Case Specification* Black Box (`TD3` — `TC-BB-01` s.d. `TC-BB-23`)

Seluruh kasus uji bersifat **non-destruktif**: pengiriman `POST /bookings/store` diblokir di browser oleh `page.route` sebelum menyentuh jaringan produksi.

| ID TC *(Cross-Ref Lama)* | Prioritas | TCI Terkait | Prasyarat (*Preconditions*) | Input / Langkah Uji | Expected Result |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **`TC-BB-01`** *(`TC-GOR-01`)* | Tinggi | `TCI-BB-01` | Situs target aktif | Akses HTTP `GET` ke `/`, `/booking`, `/login`, `/fasilitas/{lapangan,umum,tunggu,parkir}` | Semua 7 rute mengembalikan `HTTP 200 OK` dan 0 error JS konsol. |
| **`TC-BB-02`** *(`TC-GOR-02`)* | Sedang | `TCI-BB-02` | Situs target aktif | Akses HTTP `GET` ke `/register` | Rute registrasi aktif (`HTTP 200`/redirect) *(bila `HTTP 404`, catat sebagai insiden `IR-GOR-01`)*. |
| **`TC-BB-03`** *(`TC-GOR-03`)* | Tinggi | `TCI-BB-03` | `/booking` dapat diakses | Buka `/booking?start_date=<besok>` | `HTTP 200`, nilai `#jumpDate` sesuai `<besok>`, dan tombol `openBooking(` > 0. |
| **`TC-BB-04`** | Tinggi | `TCI-BB-04` | `/booking` dapat diakses | Buka `/booking?start_date=2020-01-01` (tanggal masa lalu) | Slot masa lalu semestinya dinonaktifkan (`openBooking == 0`) *(bila > 0, catat insiden `IR-GOR-05`)*. |
| **`TC-BB-05`** | Tinggi | `TCI-BB-05` | `/booking` dapat diakses | Buka `/booking?start_date=invalid-date` | Server menangani aman (`HTTP 400/422` atau redirect fallback) tanpa error `HTTP 500` *(bila 500, catat `IR-GOR-06`)*. |
| **`TC-BB-06`** *(`TC-GOR-04`)* | Tinggi | `TCI-BB-06` | Di `/booking?start_date=<besok>`, ada slot kosong | Klik elemen `[onclick*="openBooking("]` pertama | `#bookingModal` tampil (`display: flex`), `#custDuration == "1"`, `#dispTotal` memuat `"40.000"`, info jam/lap/tanggal terisi. |
| **`TC-BB-07`** *(`TC-GOR-05`)* | Sedang | `TCI-BB-07` | `#bookingModal` terbuka | Pilih opsi `#custDuration` berurutan `1`, `2`, `3`, `4`, `5` | `#dispTotal` masing-masing menampilkan `"40.000"`, `"80.000"`, `"120.000"`, `"160.000"`, `"200.000"`. |
| **`TC-BB-08`** *(`TC-GOR-06`)* | Tinggi | `TCI-BB-08` | `#bookingModal` terbuka, interceptor aktif | `#custName = ""`, `#custPhone = ""`, klik `#btnSubmit` | Alert `"⚠️Halo kak! Nama dan Nomor WA harus diisi lengkap!"`; `delta_post = 0`. |
| **`TC-BB-09`** | Sedang | `TCI-BB-09` | `#bookingModal` terbuka, interceptor aktif | Uji `#custName = "   "` dan `#custName = "A"` dengan WA `"08123456789"`, durasi `1`, klik `#btnSubmit` | Semestinya ditolak validasi nama *(bila lolos ke `fetch` dan dicegat interceptor -> `BUG-GOR-03` / `IR-GOR-03` terkonfirmasi)*. |
| **`TC-BB-10`** *(`TC-GOR-07`)* | Tinggi | `TCI-BB-10` | `#bookingModal` terbuka, interceptor aktif | `#custName = "Test QA"`, `#custPhone = "12345"` lalu `"abc"`, klik `#btnSubmit` | Alert `"⚠️ Nomor WA belum benar..."` pada kedua input; `delta_post = 0`. |
| **`TC-BB-11`** | Tinggi | `TCI-BB-11` | `#bookingModal` terbuka, interceptor aktif | `#custName = "Test QA"`, `#custPhone = "081234567"` (`10` digit -> `628`+7), klik `#btnSubmit` | Ditolak alert format WA *(BVA batas bawah -1)*; `delta_post = 0`. |
| **`TC-BB-12`** | Tinggi | `TCI-BB-12` | `#bookingModal` terbuka, interceptor aktif | `#custName = "Test QA"`, `#custPhone = "0812345678"` (`11` digit -> `628`+8), klik `#btnSubmit` | Lolos validasi klien *(BVA batas bawah valid)* dan dicegat aman oleh `page.route` (`delta_post = 1`, alert koneksi `.catch()`, `#btnSubmit` aktif kembali). |
| **`TC-BB-13`** | Tinggi | `TCI-BB-13` | `#bookingModal` terbuka, interceptor aktif | `#custName = "Test QA"`, `#custPhone = "0812345678901"` (`14` digit -> `628`+11), klik `#btnSubmit` | Lolos validasi klien *(BVA batas atas valid)* dan dicegat aman oleh `page.route` (`delta_post = 1`). |
| **`TC-BB-14`** | Tinggi | `TCI-BB-14` | `#bookingModal` terbuka, interceptor aktif | `#custName = "Test QA"`, `#custPhone = "08123456789012"` (`15` digit -> `628`+12), klik `#btnSubmit` | Ditolak alert format WA *(BVA batas atas +1)*; `delta_post = 0`. |
| **`TC-BB-15`** | Sedang | `TCI-BB-15` | `#bookingModal` terbuka, interceptor aktif | Uji `#custPhone = "81234567890"` dan `"6281234567890"`, `#custName = "Test QA"`, klik `#btnSubmit` | Keduanya dinormalisasi menjadi `628...`, lolos regex klien, dan dicegat aman `page.route` (`delta_post = 1` masing-masing). |
| **`TC-BB-16`** *(`TC-GOR-08`)* | Tinggi | `TCI-BB-16` | `#bookingModal` terbuka, interceptor aktif | `#custName = "Test QA"`, `#custPhone = "+62 08123456789"`, klik `#btnSubmit` | Semestinya dinormalisasi menjadi `628123456789` *(aktual: gagal regex `6208...` -> konfirmasi `IR-GOR-02`, `delta_post = 0`)*. |
| **`TC-BB-17`** *(`TC-GOR-09`)* | Tinggi | `TCI-BB-17` | Di `/booking?start_date=<besok>`, pilih slot `22:00` | Isi `"Test QA"` + `"08123456789"`, pilih `#custDuration = "3"` (`22+3=25 > 24`), klik `#btnSubmit` | Alert `"🚨 GAGAL! GOR Permata tutup jam 00:00..."`; `delta_post = 0`. |
| **`TC-BB-18`** | Tinggi | `TCI-BB-18` | Modal pada slot `22:00` terbuka, interceptor aktif | Isi `"Test QA"` + `"08123456789"`, pilih `#custDuration = "2"` (`22+2=24 <= 24`), klik `#btnSubmit` | Lolos pengecekan jam tutup `00:00` *(BVA batas tutup)* dan dicegat aman di interceptor `page.route` (`delta_post = 1`). |
| **`TC-BB-19`** *(`TC-GOR-10`)* | Sedang | `TCI-BB-19` | `#bookingModal` terbuka dengan isi input | Panggil `closeModal()` (atau klik tombol Tutup) | `#bookingModal` tersembunyi (`is_visible() == False`), `#custName == ""`, `#custPhone == ""`. |
| **`TC-BB-20`** | Sedang | `TCI-BB-20` | Halaman `/login` termuat | Cek `<input name="_token">`, uji `checkValidity()` dengan email `""` dan `"bukan-email"`, serta password `""` | `_token` terisi non-kosong; validasi klien HTML5 menolak input kosong/format salah sebelum submit. |
| **`TC-BB-21`** | Sedang | `TCI-BB-21` | Halaman `/` & `/booking?start_date=<besok>` | Render pada viewport *Desktop* (`1280×800`) dan *Mobile* (`390×844`); buka `#bookingModal` di mobile | Halaman `/` & `#bookingModal` tidak overflow horizontal parah (`scrollWidth <= innerWidth`), modal dapat dilihat & dioperasikan di mobile. |
| **`TC-BB-22`** | Tinggi | `TCI-BB-22` | Halaman `/booking` aktif | Inspeksi boolean keberadaan atribut `data-phone` & `data-name` non-kosong pada elemen `manageBooking(this)` (tanpa menyimpan PII) | Atribut data pribadi pelanggan semestinya tidak disematkan pada HTML publik *(bila ditemukan -> konfirmasi `IR-GOR-04`)*. |
| **`TC-BB-23`** | Sedang | `TCI-BB-23` | Halaman `/booking` aktif memiliki slot biru terkonfirmasi **`RTBC`** | Temukan `[data-status="confirmed"][data-name*="RTBC"]`, masker slot lain `[TERISI]`, klik slot `RTBC`, dan tangkap pesan dialog `manageBooking(this)` | Pop-up `alert()` bertuliskan *"Halo Kak [MEMBER] RTBC, bookingan Anda SUDAH DIKONFIRMASI. Kami tunggu kedatangannya di GOR Permata! 🏸"* tampil utuh tanpa mengubah state server. |

---

## 2. *Test Procedure Specification* (`TD4` — `PROC-BB-01` s.d. `PROC-BB-05`)

Urutan eksekusi disusun berdasarkan dependensi *precondition* dan prioritas risiko, diotomatiskan pada [`automation-scripts/test_gor_permata.py`](./automation-scripts/test_gor_permata.py) (dan dipetakan ke [`automation-scripts/gor-permata.cy.js`](./automation-scripts/gor-permata.cy.js)):

- **`PROC-BB-01` (Verifikasi Rute Publik, `/register`, & Query `?start_date=`):**
  1. `STEP-1`: Muat `test-data/blackbox-testdata.json` dan verifikasi target aktif.
  2. `STEP-2`: Jalankan `TC-BB-01`, `TC-BB-02`, `TC-BB-03`, `TC-BB-04` (termasuk `11_past_date_2020_bug.png`), dan `TC-BB-05`.
- **`PROC-BB-02` (Verifikasi Modal, Kalkulasi Tarif, & Reset State):**
  1. `STEP-3`: Buka `/booking?start_date=<tomorrow>` pada Chromium *Desktop* dengan interceptor `page.route("**/bookings/store", guard)` aktif.
  2. `STEP-4`: Jalankan `TC-BB-06`, `TC-BB-07`, dan simpan tangkapan layar modal (`evidence/screenshots/03_booking_modal_desktop.png`).
- **`PROC-BB-03` (Validasi Input *Decision Table* & *BVA* Digit/Jam Tutup):**
  1. `STEP-5`: Jalankan `TC-BB-08` s.d. `TC-BB-16` berurutan pada slot tersedia (pantau counter `blocked_posts` & alert).
  2. `STEP-6`: Tutup modal (`TC-BB-19`), pilih slot `22:00` (atau cari slot `22:00` di tanggal aktif/`tomorrow`), jalankan `TC-BB-17` dan `TC-BB-18`, lalu tutup modal.
- **`PROC-BB-04` (Verifikasi `/login`, Privasi DOM Publik, & Slot Terkonfirmasi `RTBC`):**
  1. `STEP-7`: Jalankan `TC-BB-22` pada `/booking`, `TC-BB-20` pada `/login`, serta `TC-BB-23` untuk slot `RTBC` (`09_slot_confirmed_rtbc.png` & pop-up konfirmasi `10_popup_booking_confirmed_rtbc.png`).
- **`PROC-BB-05` (Verifikasi Kompatibilitas Mobile & Wrap-up):**
  1. `STEP-8`: Jalankan `TC-BB-21` pada viewport `390×844`, ambil screenshot mobile (`07_home_mobile.png`, `08_booking_modal_mobile.png`), pastikan total `POST` terkirim ke jaringan `= 0`, tutup browser, dan tulis log ke [`automation-scripts/execution-log.txt`](./automation-scripts/execution-log.txt).

---

## 3. *End-to-End Traceability Matrix* (Black Box — `8.2.4.5 e`)

| Test Basis | Test Model (`TD1`) | TCI (`TD2`) | Test Case (`TD3`) | Test Procedure (`TD4`) |
| :--- | :--- | :--- | :--- | :--- |
| `TB-BB-01` | `TM-BB-04` | `TCI-BB-01..02` | `TC-BB-01..02` | `PROC-BB-01` (`test_gor_permata.py`) |
| `TB-BB-02` | `TM-BB-01` | `TCI-BB-03..05` | `TC-BB-03..05` | `PROC-BB-01` (`test_gor_permata.py`) |
| `TB-BB-03` | `TM-BB-03` | `TCI-BB-06`, `TCI-BB-19` | `TC-BB-06`, `TC-BB-19` | `PROC-BB-02`, `PROC-BB-03` (`test_gor_permata.py` & `gor-permata.cy.js`) |
| `TB-BB-03` | `TM-BB-03` | `TCI-BB-23` | `TC-BB-23` | `PROC-BB-04` (`test_gor_permata.py`) |
| `TB-BB-04` | `TM-BB-01` | `TCI-BB-07` | `TC-BB-07` | `PROC-BB-02` (`test_gor_permata.py` & `gor-permata.cy.js`) |
| `TB-BB-05` | `TM-BB-01`, `TM-BB-02` | `TCI-BB-08..18` | `TC-BB-08..18` | `PROC-BB-03` (`test_gor_permata.py` & `gor-permata.cy.js`) |
| `TB-BB-06` | `TM-BB-04` | `TCI-BB-20` | `TC-BB-20` | `PROC-BB-04` (`test_gor_permata.py`) |
| `TB-BB-07` | `TM-BB-05` | `TCI-BB-21..22` | `TC-BB-21..22` | `PROC-BB-04`, `PROC-BB-05` (`test_gor_permata.py`) |
