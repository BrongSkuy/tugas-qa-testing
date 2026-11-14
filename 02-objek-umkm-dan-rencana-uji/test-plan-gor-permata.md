# Test Plan: Portal Booking GOR Permata Badminton Hall

Disusun mengacu pada struktur **ISO/IEC/IEEE 29119-3 (*Test Plan*)** dan diadaptasi dengan materi perkuliahan *Testing dan QA Perangkat Lunak* (termasuk update materi *Automation Testing* 14 November 2026).

---

## 1. Identifikasi Dokumen & Objek Uji
- **ID Test Plan:** `TP-GOR-01`
- **Sistem yang Diuji (*SUT*):** Portal Web Publik GOR Permata Badminton Hall (`https://gorpermatabadminton.com`)
- **Pemilik / Lokasi Usaha:** GOR Permata Badminton Hall — Kp. Cipari, Desa Ciakar, Kec. Panongan, Kab. Tangerang, Banten
- **Jenis Sistem:** Web Aplikasi *Booking* Lapangan Bulu Tangkis (tarif teramati pada skrip klien: `PRICE_PER_HOUR = 40000` / jam)

---

## 2. Ruang Lingkup Pengujian (*Scope*)

### A. Fitur yang Diuji (*In Scope*)
1. **Halaman Beranda (`/`):** Navigasi utama, tampilan ringkasan ketersediaan slot, tautan ke modul `/booking`, `/login`, `/fasilitas/*`, dan redirect WhatsApp.
2. **Modul Jadwal & Booking (`/booking`):**
   - Parameter URL `?start_date=YYYY-MM-DD` dan pemilih tanggal (`#jumpDate`, fungsi `changeDate()`).
   - Grid status slot per jam dan lapangan (`Kosong/+`, `Menunggu`, `Terisi/confirmed`, `Member`, `RTBC`).
   - Modal pemesanan (`#bookingModal`), fungsi `openBooking()`, `closeModal()`, `updateTotal()`, serta validasi input sisi klien pada `submitBooking()` (`#custName`, `#custPhone`, `#custDuration`) **berhenti sebelum pengiriman nyata ke server**.
3. **Modul Autentikasi & Informasi (`/login`, `/register`, `/fasilitas/*`):** Verifikasi tampilan, validasi form `/login`, dan ketersediaan rute (`/register`, `/fasilitas/lapangan`, `/fasilitas/umum`, `/fasilitas/tunggu`, `/fasilitas/parkir`).
4. **Aspek Non-Fungsional Dasar:** Waktu muat halaman, responsivitas viewport seluler/desktop, keutuhan tautan, dan pemeriksaan kode JS sisi klien (*White Box*).

### B. Fitur di Luar Ruang Lingkup (*Out of Scope*)
1. **Submit Transaksi Booking Nyata (`POST /bookings/store`):** Tidak mengirim pesanan palsu agar tidak merusak/mengunci jadwal operasional GOR tanpa izin tertulis pengelola.
2. **Panel Admin / Penjaga Internal (`/bookings/confirm/*`, `/bookings/reject/*`, `/bookings/delete/*`):** Memerlukan kredensial akun admin/guard milik pengelola; pengujian hanya menganalisis logika kode publik `manageBooking()` dan `sendAction()`.
3. **Uji Beban Agresif (*DDoS / Stress Load*) & Eksploitasi Keamanan Aktif:** Tidak dilakukan tanpa izin pengelola demi menjaga ketersediaan layanan UMKM.

---

## 3. Strategi & Pendekatan Pengujian
1. **Manual & Exploratory Testing:** Memeriksa langsung alur pengguna, pesan error/alert, *broken link*, dan tampilan responsif di browser.
2. **Black Box Testing:**
   - *Equivalence Partitioning (EP)* & *Boundary Value Analysis (BVA)* pada input nama, nomor WhatsApp, pilihan durasi (`1..n` jam vs tutup jam `00:00`), serta parameter `start_date`.
   - *State Transition Testing* untuk status slot dan alur buka/tutup modal booking.
   - *Use Case Testing* untuk skenario pemesanan pelanggan.
3. **White Box Testing (*Basis Path / Cyclomatic Complexity*):** Menganalisis alur kendali dan percabangan kode JavaScript klien pada halaman `/booking` (`normPhone`, `submitBooking`, `manageBooking`, `updateTotal`).
4. **Gray Box Testing:** Menggabungkan pengetahuan struktur DOM modal, parameter `?start_date=...`, dan header CSRF (`X-CSRF-TOKEN`) dengan pengujian tampilan.
5. **Automation Testing (Playwright Python & skrip contoh Cypress):** Sesuai materi 14 Nov 2026 (*Test Plan -> Test Script -> Eksekusi -> Validasi -> Log*), otomasi dijalankan pada skenario non-destruktif yang aman diulang.

---

## 4. Kriteria Masuk & Keluar (*Entry & Exit Criteria*)
- **Entry Criteria:** URL target `https://gorpermatabadminton.com` aktif (`HTTP 200 OK`), struktur *Test Plan* dan aturan etika non-destruktif telah disepakati tim.
- **Exit Criteria:** Seluruh *Test Case* non-destruktif pada folder `03-hasil-pengujian/` telah dieksekusi, temuan *defect* tercatat beserta bukti, skrip otomasi menghasilkan *log* bebas error eksekusi, dan siap digunakan sebelum tahap wawancara praktisi QA.

---

## 5. Manajemen Risiko & Kendala Khusus Objek
| Risiko | Dampak | Rencana Mitigasi |
| :--- | :--- | :--- |
| **Pengujian berulang memicu kunci jadwal di database** | Merugikan operasional UMKM dan membuat jadwal uji tidak bisa diulang | Pengujian hanya menyentuh validasi negatif sisi klien (`nama`/`WA` kosong, format WA salah, jam melewati `24:00`) yang langsung dihentikan `alert()` sebelum `fetch('/bookings/store')` berjalan. |
| **Token CSRF & konten jadwal berubah harian** | Skrip otomasi atau selector tanggal kadaluarsa | Gunakan tanggal dinamis (tanggal hari ini) dan pilih tombol slot kosong secara dinamis di DOM pada skrip otomasi. |
| **Belum ada akses akun admin/penjaga** | Alur `approveBooking` / `rejectBooking` tidak bisa diuji secara end-to-end | Analisis alur tetap didokumentasikan pada kajian *White Box* dan dicatat sebagai batasan ruang lingkup (*Out of Scope*). |

