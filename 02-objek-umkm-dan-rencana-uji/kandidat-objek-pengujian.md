# Kandidat Objek Pengujian UMKM (Tugas 1)

Dokumen ini merangkum hasil penelusuran dan verifikasi kandidat objek pengujian skala **UMKM / lembaga lokal (medium ke bawah)** dari dua jalur—**Website/Portal UMKM sekitar Cluster Agung Indah, Panongan, Tangerang, Banten** dan **Aplikasi Android di Google Play Store**—untuk dibahas dan dipilih bersama kelompok.

> **Batasan Etika Pengujian:** Seluruh observasi awal dan rencana pengujian bersifat **pasif serta non-destruktif** (fokus pada pengujian fungsional, validasi input wajar, UI/UX, *broken link*, responsivitas, *automation testing*, dan analisis skrip sisi klien publik tanpa melakukan *spam*, *brute force*, atau eksploitasi keamanan aktif tanpa izin pemilik).

---

## A. Jalur 1 — Website / Portal UMKM & Sekolah Lokal Sekitar Panongan, Tangerang

*Konteks lokasi acuan:* **Cluster Agung Indah** berada di wilayah **Serdang Kulon, Kecamatan Panongan, Kabupaten Tangerang, Banten** (sekitar Jl. Raya PLP Curug / Jl. Raya Serdang Kulon–Korelet).

### 1. GOR Permata Badminton Hall *(Rekomendasi Utama #1)*
- **URL Portal:** https://gorpermatabadminton.com
- **Alamat:** Kp. Cipari, Desa Ciakar, Kecamatan Panongan, Kabupaten Tangerang, Banten
- **Kategori / Skala:** UMKM fasilitas olahraga lokal (4 lapangan karpet standar BWF)
- **Status Verifikasi Teknis (8 Nov 2026):** **HTTP 200 OK** (waktu muat halaman utama ~0,36 detik, HTTPS aktif, viewport mobile tersedia)
- **Fitur & Halaman Teramati:**
  - Beranda + monitor ketersediaan slot berikutnya (`https://gorpermatabadminton.com`)
  - Grid jadwal & booking slot per tanggal/jam/lapangan (`https://gorpermatabadminton.com/booking?date=...&time=...&court=...`) dengan status slot nyata (`Menunggu`, `Terisi`, `Member`, `RTBC`, tombol `+` untuk booking)
  - Halaman login pengelola/member (`https://gorpermatabadminton.com/login` dengan `_token`, `email`, `password`)
  - Halaman informasi fasilitas (`/fasilitas/lapangan`, `/fasilitas/umum`, `/fasilitas/tunggu`, `/fasilitas/parkir`) dan integrasi WhatsApp admin (`wa.me`)
  - **Temuan Awal:** Rute `/register` menghasilkan **404 Not Found**; halaman `/booking` memuat skrip JavaScript sisi klien (~7,4 KB) berisi fungsi `rupiah`, `changeDate`, `updateTotal`, `openBooking`, `closeModal`, `submitBooking`, `manageBooking`, `approveBooking`, `rejectBooking`, `sendAction`.
- **Kelebihan untuk Tugas:**
  - **Sesuai 100% dengan analogi dosen** (*lapangan bulu tangkis lokal dengan portal booking sendiri*).
  - Mendukung **seluruh strategi pengujian**: *Black Box* (EP/BVA pada parameter tanggal/jam/court dan form booking/login, *State Transition* pada status slot, *Use Case*), *Gray Box* (struktur DOM, parameter URL, CSRF token), *White Box / Cyclomatic Complexity* (menganalisis alur logika fungsi JS publik di `/booking`), dan *Automation Testing* (Cypress / Katalon Studio).
  - Lokasinya di Kecamatan Panongan memudahkan observasi langsung atau meminta izin pengelola untuk *Acceptance Testing*.
- **Kekurangan / Catatan:** Bukan APK Play Store; pengujian pengiriman form booking harus hati-hati agar tidak membuat data booking palsu pada jadwal nyata GOR (uji cukup sampai validasi sisi klien/UI atau minta izin admin terlebih dahulu).

### 2. Sekolah Alam Tangerang Mekar Bakti (SATMERBAK) *(Rekomendasi Runner-Up #2)*
- **URL Portal:** https://sekolahalammekarbakti.sch.id
- **Alamat:** Jl. Kp. Jawaringan, Kelurahan Mekar Bakti, Kecamatan Panongan, Kabupaten Tangerang, Banten
- **Kategori / Skala:** Sekolah swasta lokal (KB, TK, SD, SMP–SMA di bawah Yayasan Pesona Alam Citra)
- **Status Verifikasi Teknis (8 Nov 2026):** **HTTP 200 OK** (~1,3 detik, HTTPS aktif)
- **Fitur & Halaman Teramati:**
  - Halaman profil sekolah, fasilitas, galeri, kontak, dan tautan ke **7 portal login modul PHP terpisah**:
    - PPDB Online (`/ppdb/login.php` — input `username`, `password`, `remember`)
    - Sistem Kantin Sekolah (`/e-warung/login.php` — input `username`, `password`)
    - LMS SD, Siswa, Orang Tua, Katering, & TK/PAUD (`/lmssd/login.php`, `/lmssd/siswa/login.php`, `/lmssd/login_ortu.php`, `/lmssd/katering/login.php`, `/lmstkpaud/login.php`)
  - **Temuan Awal:** Di halaman beranda terdapat kesalahan ketik (*typo*) alamat (`Kelurhana Mekar Bakti`) serta teks *placeholder/dummy* yang tertinggal (`PPDB Online sdssd Daftar Sekarang`).
- **Kelebihan untuk Tugas:** Sangat sesuai dengan analogi kedua dosen (*sekolah/madrasah lokal*), memiliki banyak halaman login/form untuk diuji dengan *EP, BVA, Use Case*, *UI/Usability*, dan *Automation Testing*, serta sudah tampak cacat konten nyata di beranda.
- **Kekurangan / Catatan:** Modul internal PPDB/LMS/e-Warung memerlukan akun siswa/admin untuk masuk lebih dalam (tanpa izin sekolah, pengujian berhenti pada halaman publik, navigasi, form login, dan UI).

### 3. SMKS Citra Nusantara Panongan
- **URL Portal:** https://smkscitranusantara.sch.id
- **Alamat:** Kecamatan Panongan, Kabupaten Tangerang, Banten
- **Kategori / Skala:** Sekolah kejuruan swasta lokal
- **Status Verifikasi Teknis (8 Nov 2026):** **HTTP 200 OK** (~1,0 detik, HTTPS aktif, 81 tautan, 25 skrip)
- **Fitur & Halaman Teramati:** Portal informasi lengkap (Berita, Pengumuman, Agenda, Jadwal Pelajaran, Jadwal Ujian, Unduhan, Kelulusan, SPMB 2026/2027, Testonline, Kuisioner, Login). Rute langsung `/kontak` dan `/ppdb` mengembalikan **404**.
- **Kelebihan / Kekurangan:** Kaya menu untuk uji fungsional & navigasi web (*broken link*, *usability*, *responsive*), tetapi fitur ujian/SPMB memerlukan akses akun siswa dan skalanya sedikit lebih besar dibanding sekolah/madrasah kecil.

### 4. Toko 8 Plastik *(UMKM Ritel/Kemasan)*
- **URL Portal:** https://toko8plastik.wixsite.com/toko8
- **Alamat:** Ruko The Boulevard VD05/80, Jl. Ecopolis Citra Raya, Mekar Bakti, Kecamatan Panongan, Kabupaten Tangerang, Banten
- **Kategori / Skala:** UMKM toko perlengkapan plastik & kemasan
- **Status Verifikasi Teknis (8 Nov 2026):** **HTTP 200 OK** (~1,5 detik, menggunakan platform **Wix** gratis)
- **Fitur & Halaman Teramati:** Halaman Home, Galeri, Contact, Customer Kami, serta tautan ke toko Shopee/Tokopedia/Blibli. Masih terlihat teks bawaan template Wix (`Home: Welcome`, `Anchor 1`).
- **Kelebihan / Kekurangan:** Jelas berskala UMKM lokal dan banyak temuan *usability*/desain; namun karena berbasis website statis Wix tanpa fitur transaksi/form booking kompleks, skenario *White Box* dan *State Transition* lebih terbatas.

> *Catatan Domain Tidak Aktif Saat Penelusuran:* `http://sekolahmandiri.sch.id` (SMP Mandiri Serdang Kulon) dan `http://www.mafatihaqiqah.com` (Mafatih Aqiqah Panongan) tercatat di direktori publik tetapi gagal resolusi DNS (`getaddrinfo failed`) pada 8 November 2026. Tidak dipilih sebagai objek utama karena tidak dapat diakses/diuji fitur interaktifnya.

---

## B. Jalur 2 — Aplikasi Android (Google Play Store)

Seluruh kandidat di bawah ini telah diverifikasi langsung status aktifnya (**HTTP 200 OK** pada halaman Play Store per 8 November 2026), berasal dari pengembang independen/UMKM/lokal (bukan raksasa teknologi), serta memiliki jumlah unduhan **< 20.000**.

### 1. Waroengkoe Kasir Offline UMKM (`com.paksyaffak.waroengkoepos`) *(Terpilih Kelompok: Download Literal Tier 10+ [< 20] & Khusus Warung UMKM)*
- **Package ID / Link:** `com.paksyaffak.waroengkoepos` — https://play.google.com/store/apps/details?id=com.paksyaffak.waroengkoepos
- **Developer:** Pak Syaffak *(pengembang independen/perorangan)*
- **Statistik Play Store (Terverifikasi):** **10+ unduhan** (secara harfiah < 20 download) | Rating: Belum ada agregat rating karena aplikasi baru rilis
- **Deskripsi & Fitur:** Didesain khusus warung mikro & toko kelontong. Fitur lengkap:
  - Transaksi kasir offline (tanpa internet & QRIS lokal)
  - Modul Stok & Kulakan barang dagangan
  - Laporan laba rugi & analitik tren penjualan
  - Pemisahan hak akses Akun Admin vs Pegawai
  - Ekspor/Impor (backup/restore) database lokal
  - Cetak & kirim screenshot nota via WhatsApp
- **Kelebihan:** Memenuhi syarat literal download di bawah 20 (`10+`), target UMKM sangat pas (warung kelontong/UMKM mikro), dan 100% aman untuk pengujian ekstrem (boundary value harga minus, stok habis, otorisasi akun) secara lokal di HP.
- **Kekurangan / Catatan:** Rating bintang agregat belum muncul di Play Store karena jumlah pengunduh masih di bawah ambang batas minimal review Google.

### 2. Kasir Toko - POS Offline (`com.paksyaffak.kasirtoko`) *(Alternatif: Unduhan 1K+ & Rating Jelek 3,6)*
- **Package ID / Link:** `com.paksyaffak.kasirtoko` — https://play.google.com/store/apps/details?id=com.paksyaffak.kasirtoko
- **Developer:** Pak Syaffak *(pengembang independen/perorangan)*
- **Statistik Play Store (Terverifikasi):** **1K+ unduhan** | Rating **3,6 bintang** (15 ulasan) | Update: 25 Agustus 2026
- **Deskripsi:** Aplikasi kasir POS offline sederhana untuk toko & UMKM (catat penjualan, stok, dan utang).
- **Kelebihan:** Memenuhi syarat rating kurang baik (`3,6`) dengan 15 ulasan yang memuat komplain nyata dari pengguna.
- **Kekurangan / Catatan:** Unduhan berada di tier `1K+` (di bawah 20 ribu, tapi bukan di bawah 20 satuan).

### 3. Simpan Pinjam Koperasi (`com.snr.ksp`) *(Download Sedikit & Rating Rendah)*
- **Package ID / Link:** `com.snr.ksp` — https://play.google.com/store/apps/details?id=com.snr.ksp
- **Developer:** PT Sinar Teknologi Retailindo
- **Statistik Play Store (Terverifikasi):** **500+ unduhan** | Rating **3,2 bintang** | Update: 21 September 2026
- **Deskripsi:** Sistem manajemen koperasi simpan pinjam lengkap dengan jurnal otomatis.
- **Kelebihan:** Unduhan sangat kecil (`500+`) dan rating rendah (`3,2`), relevan untuk koperasi/UMKM.
- **Kekurangan / Risiko:** Perlu dicek apakah membutuhkan pendaftaran/login server terlebih dahulu sebelum menu transaksi terbuka.

### 3. SEKOLAH KITA INDONESIA - SKID *(Rating Sangat Rendah 1,8)*
- **Package ID / Link:** `com.sekolak` — https://play.google.com/store/apps/details?id=com.sekolak
- **Developer:** Fortis Teknologi Indonesia
- **Statistik Play Store (Terverifikasi):** **100+ unduhan** | Rating **1,8 bintang** | Update: 4 Juli 2026
- **Deskripsi:** Aplikasi ujian & aktivitas sekolah (`Persiapkan diri untuk ujian dengan aman dan mudah menggunakan aplikasi Sekolak!`).
- **Kelebihan:** Memenuhi dua syarat dosen sekaligus (**unduhan < 20rb dan rating sangat rendah 1,8**), sangat kuat untuk dianalisis penyebab keluhan pengguna (*Black Box*, *Usability*, kompatibilitas).
- **Kekurangan / Risiko:** Aplikasi ujian sekolah sering mengunci fitur utama di balik login akun/kode sekolah tertentu (perlu dicoba instal di HP untuk memastikan apakah ada mode demo/halaman uji tanpa akun sekolah).

### 4. Book Playgrounds: Futsal Court *(Alternatif Sport Booking)*
- **Package ID / Link:** `com.firefly.futsal` — https://play.google.com/store/apps/details?id=com.firefly.futsal
- **Developer:** FireFly I.T. Solutions
- **Statistik Play Store (Terverifikasi):** **1K+ unduhan** | Rating **3,8 bintang** | Update: 13 Oktober 2026
- **Deskripsi:** Aplikasi pemesanan lapangan dan arena olahraga secara langsung (*Pesan lapangan dan arena olahraga secara instan*).
- **Kelebihan:** Rating di bawah 4,0 (`3,8`), unduhan kecil (`1K+`), dan bertema *booking* lapangan sehingga kaya alur *State Transition* dan *Use Case Testing*.
- **Kekurangan / Risiko:** Perlu cek langsung di perangkat apakah ada venue aktif di Indonesia/Tangerang serta cek ukuran APK di aplikasi Play Store HP.

### 5. Kasir UMKM (`com.warung.umkm`) & Booking Futsal System (`mufa.dev.bfs`) *(Aplikasi Baru — Belum Ada Rating)*
- **Kasir UMKM:** `com.warung.umkm` — https://play.google.com/store/apps/details?id=com.warung.umkm (Dev: NVX Studio | **100+ unduhan** | Belum ada rating | Update: 1 September 2026)
- **Booking Futsal System:** `mufa.dev.bfs` — https://play.google.com/store/apps/details?id=mufa.dev.bfs (Dev: MUA Digital Technology | **100+ unduhan** | Belum ada rating | Update: 9 September 2026)
- **Catatan:** Sangat ringan/awal dan mudah dicoba, namun karena belum memiliki skor rating publik, tidak menunjukkan indikasi "rating jelek" secara langsung di Play Store.

> *Kandidat Cadangan Play Store (< 20K downloads, rating tinggi):* **Mituni POS - Kasir Laundry** (`id.mituni.laundry_mobile` — PT Mituni Teknologi Indonesia, `100+` downloads, ~24,1 MB di AppBrain, rating `5,0` dari 22 ulasan) dan **Laundry by Ketoko** (`com.inspirasi.ketokolnd` — Inspirasi Media Kreatif, `1K+` downloads, rating `4,6`–`4,7`). Kurang diprioritaskan karena ratingnya sudah tinggi.

---

## C. Matriks Perbandingan & Rekomendasi Final

| Kandidat | Jalur | Skala UMKM | Kelayakan Rating / Kondisi | White/Gray/Black Box | Automation Testing (Cypress/Katalon) | Kemudahan Akses Uji | Skor Kecocokan |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **GOR Permata Badminton Hall** (`gorpermatabadminton.com`) | Web Panongan | Sangat Sesuai | Ada temuan 404 `/register` & ruang uji UI/validasi | **Lengkap** (ada fungsi JS klien + parameter URL + status slot) | **Sangat Mudah** (Web/Cypress/Katalon) | Tinggi (web publik + dekat Panongan) | **9,5 / 10** |
| **Sekolah Alam Mekar Bakti** (`sekolahalammekarbakti.sch.id`) | Web Panongan | Sangat Sesuai | Ada typo & teks dummy `sdssd` di halaman utama | Cukup Lengkap (Black Box, Gray Box, UI, 7 portal login) | **Mudah** (Web/Cypress/Katalon) | Sedang–Tinggi (modul dalam perlu akun) | **8,5 / 10** |
| **Kasir Toko - POS Offline** (`com.paksyaffak.kasirtoko`) | Play Store | Sangat Sesuai | `1K+` unduhan, **rating 3,6** (dev perorangan) | Black Box & Gray Box baik; **White Box sulit** (tanpa source code) | Perlu setup Appium/Katalon Mobile | Tinggi (offline, langsung uji fitur penuh) | **8,2 / 10** |
| **Simpan Pinjam Koperasi** (`com.snr.ksp`) | Play Store | Sesuai (Koperasi/UMKM) | `500+` unduhan, **rating 3,2** | Black Box baik, **White Box sulit** | Perlu setup mobile | Sedang (perlu cek apakah butuh login server) | **7,6 / 10** |
| **SKID (`com.sekolak`)** | Play Store | Sesuai (Pendidikan) | `100+` unduhan, **rating 1,8** | Black Box baik, **White Box sulit** (tanpa source code) | Perlu setup mobile | Sedang–Rendah (berpotensi terkunci login sekolah) | **7,3 / 10** |
| **Book Playgrounds (`com.firefly.futsal`)** | Play Store | Sesuai | `1K+` unduhan, **rating 3,8** | Black Box baik, **White Box sulit** | Perlu setup mobile | Sedang (perlu cek ketersediaan venue lokal) | **7,5 / 10** |
| **Kasir UMKM** (`com.warung.umkm`) | Play Store | Sangat Sesuai | `100+` unduhan, belum ada rating | Black Box baik; **White Box sulit** | Perlu setup mobile | Tinggi (bisa dicoba langsung) | **7,4 / 10** |
| **Toko 8 Plastik** (`toko8plastik.wixsite.com/toko8`) | Web Panongan | Sangat Sesuai | Ada teks template Wix belum diganti | Terbatas (web statis Wix, minim form) | Mudah tapi skenario sedikit | Tinggi | **6,8 / 10** |

### Rekomendasi Pilihan untuk Kelompok
1. **Pilihan Utama yang Paling Direkomendasikan:** **`https://gorpermatabadminton.com` (GOR Permata Badminton Hall — Desa Ciakar, Panongan, Tangerang)**.
   - **Alasan:** Secara literal sesuai dengan contoh yang disampaikan Bapak Ahmad Fauzi (*portal lapangan bulu tangkis skala lokal*), berlokasi di Kecamatan Panongan (dekat dengan Cluster Agung Indah), seluruh teknik yang disyaratkan tugas (**White Box / Cyclomatic Complexity pada fungsi JS `/booking`, Black Box EP/BVA/State Transition/Use Case, Gray Box, Manual, dan Automation via Cypress/Katalon Studio**) dapat dijalankan secara lengkap dan terdokumentasi nyata tanpa terkendala kepemilikan source code APK tertutup.
2. **Alternatif #2 (Jika Kelompok Memilih Sekolah):** **`https://sekolahalammekarbakti.sch.id`** (Sekolah Alam Mekar Bakti, Panongan — banyak modul login & sudah tampak cacat konten di halaman depan).
3. **Alternatif #3 (Jika Kelompok Wajib Memilih APK Play Store):** **`com.paksyaffak.kasirtoko` (Kasir Toko - POS Offline)** karena memenuhi seluruh syarat APK dosen (`1K+` unduhan, rating rendah `3,6`, developer perorangan) sekaligus paling mudah diuji fitur penuh secara offline—atau **`com.snr.ksp`** (rating `3,2`, `500+` unduhan) / **`com.sekolak`** (rating `1,8`, `100+` unduhan) setelah dicek ukuran file `< 20 MB` di aplikasi Play Store HP.

