# Test Cases Manual & Laporan Temuan Bug: GOR Permata Badminton Hall

Mengacu pada format **ISO/IEC/IEEE 29119-3** (*Test Case Specification* & *Defect Report*). Seluruh eksekusi pada portal produksi dilakukan secara **non-destruktif** (berhenti pada validasi sisi klien tanpa memanggil `POST /bookings/store`).

---

## A. Daftar Test Case Utama (`TC-GOR-01` s.d. `TC-GOR-10`)

| ID TC | Modul / Fitur | Teknik | Input / Langkah Uji | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| `TC-GOR-01` | Navigasi Halaman Publik | Functional | Akses `/`, `/booking`, `/login`, `/fasilitas/lapangan`, `/fasilitas/umum`, `/fasilitas/tunggu`, `/fasilitas/parkir` | Semua rute mengembalikan HTTP `200 OK` dan merender konten tanpa error. |
| `TC-GOR-02` | Rute Pendaftaran | Functional | Akses langsung `https://gorpermatabadminton.com/register` | Halaman form pendaftaran tampil atau redirect ke info pendaftaran (tercatat defect HTTP `404`). |
| `TC-GOR-03` | Filter Tanggal Grid | Black Box | Ubah tanggal pada grid `/booking?start_date=<besok>` | URL berubah sesuai `start_date` dan kolom tanggal grid menyesuaikan. |
| `TC-GOR-04` | Pembukaan Modal Slot | State Transition | Klik salah satu slot kosong (`openBooking`) | `#bookingModal` tampil (`display: flex`), `#dispTime`, `#dispCourt`, `#dispDate`, `#custDuration = 1`, `#dispTotal = "Rp 40.000"`. |
| `TC-GOR-05` | Kalkulasi Tarif | Black Box / BVA | Ubah `#custDuration` menjadi `2` jam dan `3` jam | `#dispTotal` otomatis berubah menjadi `"Rp 80.000"` dan `"Rp 120.000"` (`updateTotal()`). |
| `TC-GOR-06` | Validasi Nama & WA Kosong | White/Black Box | Kosongkan `#custName` dan `#custPhone`, klik `#btnSubmit` | Muncul `alert`: `⚠️Halo kak! Nama dan Nomor WA harus diisi lengkap!`; tidak ada request `POST`. |
| `TC-GOR-07` | Validasi Format WA Salah | Black Box (EP) | Isi `#custName = "Test QA"`, `#custPhone = "12345"` atau `"abc"`, klik `#btnSubmit` | Muncul `alert`: `⚠️ Nomor WA belum benar...`; tidak ada request `POST`. |
| `TC-GOR-08` | Edge Case `+62 08...` | White Box | Isi `#custName = "Test QA"`, `#custPhone = "+62 08123456789"`, klik `#btnSubmit` | `normPhone()` menghasilkan `6208123456789` dan gagal regex `/^628\d{8,11}$/` -> muncul alert error meski nomor maksudnya valid. |
| `TC-GOR-09` | Batas Jam Tutup `00:00` | Black Box (BVA) | Pilih slot `22:00` (`startHour = 22`), isi nama + WA valid `08123456789`, pilih durasi `3` jam (`22 + 3 = 25 > 24`), klik `#btnSubmit` | Ditolak sebelum `fetch`: muncul `alert` jam operasional tutup `00:00`. |
| `TC-GOR-10` | Reset Input Tutup Modal | State Transition | Isi `#custName` & `#custPhone`, lalu tutup modal via `closeModal()` | Modal tersembunyi (`display: none`) dan input `#custName` & `#custPhone` kembali kosong `""`. |

---

## B. Laporan Temuan Bug Awal (*Defect Report*)

### `BUG-GOR-01`: Endpoint `/register` Mengembalikan HTTP `404 Not Found`
- **Severity / Priority:** Major / Medium
- **Steps to Reproduce:** Buka `https://gorpermatabadminton.com/register`.
- **Expected Result:** Menampilkan halaman registrasi akun atau mengarahkan ke halaman penjelasan pendaftaran anggota.
- **Actual Result:** Server mengembalikan status **HTTP `404 Not Found`**.

### `BUG-GOR-02`: Fungsi `normPhone()` Gagal Menormalisasi Awalan `+62 08...`
- **Severity / Priority:** Minor / Medium *(White Box Finding)*
- **Lokasi Kode:** Inline script `/booking` fungsi `normPhone(p)`
- **Steps to Reproduce:** Masukkan nomor dengan format `+62 08123456789` (umum disalin dari kontak ponsel) ke `#custPhone`, lalu klik `#btnSubmit`.
- **Expected Result:** Digit `0` setelah kode negara `62` dinormalisasi menjadi `628123456789`.
- **Actual Result:** Karena kondisi pertama `if (d.startsWith('62')) return d;` langsung dijalankan sebelum menghapus `0`, hasilnya `6208123456789` yang gagal regex `/^628\d{8,11}$/` dan memicu alert error.

### `BUG-GOR-03`: Tidak Ada Batas Minimal Panjang/Validasi Karakter pada `#custName` di Sisi Klien
- **Severity / Priority:** Minor / Low
- **Lokasi Kode:** Inline script `/booking` fungsi `submitBooking()`
- **Actual Result:** Pemeriksaan hanya memakai `if (!name || !phone)` tanpa `.trim()` maupun batas panjang karakter, sehingga spasi `"   "` atau 1 karakter/simbol lolos tahap validasi nama di sisi klien.

### `BUG-GOR-04`: Pesan & Nama Penjaga Internal Hardcoded di JavaScript Sisi Klien Publik
- **Severity / Priority:** Minor / Low *(Gray Box Information Note)*
- **Lokasi Kode:** Fungsi `manageBooking(el)` di halaman `/booking`
- **Actual Result:** Teks operasional internal (`alert('Akun penjaga tidak bisa menghapus booking. Hubungi Koko atau Aan.')`) serta daftar endpoint manajemen (`/bookings/confirm/`, `/bookings/reject/`, `/bookings/delete/`) ikut dimuat pada halaman publik pengunjung biasa.

