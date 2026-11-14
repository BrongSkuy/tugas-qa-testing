# Test Plan: Portal Booking GOR Permata Badminton Hall

Disusun mengacu pada struktur **ISO/IEC/IEEE 29119-3 (*Test Plan*)** serta kosakata **29119-1:2022**, **29119-5:2024**, dan evaluasi mutu **ISO/IEC 25010:2023**, dipadukan dengan materi perkuliahan *Testing dan QA Perangkat Lunak* (termasuk materi *Automation Testing* 14 November 2026).

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
4. **Aspek Non-Fungsional Dasar & Audit `ISO/IEC 25010:2023`:** Waktu muat halaman, responsivitas viewport seluler/desktop, keutuhan tautan, pemeriksaan kode JS sisi klien (*White/Gray Box*), serta pemeriksaan pasif *HTTP Security Headers* (hasil audit terdokumentasi di [`../01-standar-ieee-iso/evaluasi-iso-25010-gor-permata.md`](../01-standar-ieee-iso/evaluasi-iso-25010-gor-permata.md)).

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
3. **White Box Testing (*Basis Path / Cyclomatic Complexity*):** Menganalisis *Control Flow Graph*, kompleksitas siklomatik $V(G)$, dan basis path kode JavaScript klien pada `/booking` (`normPhone`, `submitBooking`).
4. **Gray Box Testing:** Menggabungkan pengetahuan struktur DOM modal, parameter `?start_date=...`, header CSRF (`X-CSRF-TOKEN`), dan *HTTP Response Headers* dengan pengujian antarmuka.
5. **Automation Testing (Playwright Python & skrip Cypress):** Sesuai materi 14 Nov 2026 (*Test Plan -> Test Script -> Eksekusi -> Validasi -> Log*), otomasi dijalankan pada skenario non-destruktif dengan interceptor `page.route` yang memblokir `POST **/bookings/store`.

---

## 4. Justifikasi Pemilihan Strategi & Metode Pengujian (Poin 7)

Sesuai ketentuan **Poin 7** perkuliahan dan standar **ISO/IEC/IEEE 29119-4**, setiap metode pada *Test Plan* ini ditopang oleh rujukan jurnal terakreditasi **SINTA 2 & SINTA 3** pada [`referensi-sinta-1-3.md`](./referensi-sinta-1-3.md):

1. **Alasan Memakai White Box (*Basis Path & Cyclomatic Complexity*):**
   - Kode validasi pemesanan `/booking` berada pada skrip JS klien terbuka (`normPhone()`, `submitBooking()`), sehingga alur keputusannya dapat dipetakan menjadi *Control Flow Graph* untuk menjamin cakupan seluruh cabang logika dan menemukan anomali urutan `if` seperti kegagalan `+62 08...` (`BUG-GOR-02`).
   - *Rujukan SINTA:* **Pratala, dkk. (2020)** (*JIUP, SINTA 3*) membuktikan teknik *Basis Path Testing* dan $V(G)$ efektif mendeteksi jalur logika kritis, didukung **Alirridlo, dkk. (2025)** (*Jurnal RESTI, SINTA 2*) mengenai korelasi *Cyclomatic Complexity* dengan mutu modularitas ISO/IEC 25010.
2. **Alasan Memakai Black Box (*EP & Boundary Value Analysis*):**
   - Form booking memiliki batasan nilai kritis yang rawan salah: panjang digit WhatsApp (`628` + 8–11 digit = 11–14 digit), batas jam tutup `00:00` (`startHour + duration <= 24`), dan input wajib nama.
   - *Rujukan SINTA:* **Yulistina, dkk. (2020)** & **Nurudin, dkk. (2019)** (*JIUP, SINTA 3*) serta **Putri & Susanto (2024)** (*Sinkron, SINTA 3*) menunjukkan BVA memfokuskan uji pada nilai minimum, maksimum, dan batas luar (*out of boundary*) input aplikasi penjualan/website agar cacat validasi cepat tertangkap tanpa menebak input acak.
3. **Alasan Mengombinasikan White Box + Black Box + Automation Testing:**
   - **Seputra, dkk. (2024)** (*Jurnal RESTI, SINTA 2*) menunjukkan kombinasi *White Box* dan *Black Box* saling melengkapi dalam memvalidasi struktur kode sekaligus fungsionalitas antarmuka. Untuk uji regresi berulang yang aman di portal booking, **Fhonna, dkk. (2026)** (*Sisfo, SINTA 3*) memvalidasi efektivitas otomasi berbasis browser (*Cypress / Playwright*) untuk menguji konsistensi E2E.
4. **Alasan Memakai Model Kualitas ISO/IEC 25010:2023:**
   - Selain fungsionalitas, portal web UMKM wajib dinilai dari sisi keamanan header, efisiensi waktu muat, dan pencegahan kesalahan pengguna (*Interaction Capability* & *Safety*) sebagaimana diterapkan pada **Zahra & Kraugusteeliana (2023)** (*JTIIK, SINTA 2*).

---

## 5. Kriteria Masuk & Keluar (*Entry & Exit Criteria*)
- **Entry Criteria:** URL target `https://gorpermatabadminton.com` aktif (`HTTP 200 OK`), struktur *Test Plan* dan aturan etika non-destruktif telah disepakati tim.
- **Exit Criteria:** Seluruh *Test Case* non-destruktif pada folder `03-hasil-pengujian/` telah dieksekusi beserta bukti tangkapan layar, temuan *defect* tercatat mengacu ISO/IEC/IEEE 29119-3, skrip otomasi menghasilkan *log* bebas error eksekusi, dan siap sebelum tahap wawancara praktisi QA.

---

## 6. Manajemen Risiko & Kendala Khusus Objek
| Risiko | Dampak | Rencana Mitigasi |
| :--- | :--- | :--- |
| **Pengujian berulang memicu kunci jadwal di database** | Merugikan operasional UMKM dan membuat jadwal uji tidak bisa diulang | Pengujian hanya menyentuh validasi negatif sisi klien (`nama`/`WA` kosong, format WA salah, jam melewati `24:00`) yang langsung dihentikan `alert()` sebelum `fetch('/bookings/store')` berjalan, ditambah *route abort* di skrip otomasi. |
| **Token CSRF & konten jadwal berubah harian** | Skrip otomasi atau selector tanggal kadaluarsa | Gunakan tanggal dinamis (`date.today() + 1 day`) dan pilih tombol slot kosong secara dinamis di DOM pada skrip otomasi. |
| **Belum ada akses akun admin/penjaga** | Alur `approveBooking` / `rejectBooking` tidak bisa diuji secara end-to-end | Analisis alur tetap didokumentasikan pada kajian *White Box* dan dicatat sebagai batasan ruang lingkup (*Out of Scope*). |
