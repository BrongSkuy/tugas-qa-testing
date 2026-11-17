# Audit Kualitas Perangkat Lunak Berbasis ISO/IEC 25010:2023 — GOR Permata Badminton Hall

Dokumen ini memetakan kualitas **Portal Booking GOR Permata Badminton Hall** (`https://gorpermatabadminton.com`) menggunakan model mutu terbaru **ISO/IEC 25010:2023** (*Systems and software Quality Requirements and Evaluation / SQuaRE*) dengan 9 karakteristik utama. Hasil berikut menggabungkan observasi pasif awal (14 November 2026) **dan hasil eksekusi aktual Black Box (`23 TC`) serta Performance Testing (`10 TC`) pada 17 November 2026**.

---

## 1. Matriks Evaluasi 9 Karakteristik ISO/IEC 25010:2023

| No | Karakteristik (2023) | Sub-Karakteristik Relevan | Hasil Observasi & Pengujian Terukur (17 Nov 2026) | Status Penilaian |
| :-: | :--- | :--- | :--- | :---: |
| 1 | **Functional Suitability** | *Functional completeness, correctness, appropriateness* | 7 rute publik utama aktif `HTTP 200 OK`, tarif `updateTotal()` (`1..5` jam = `Rp 40.000..Rp 200.000`) tepat, dan BVA panjang WA `11–14` digit akurat. **Cacat ditemukan:** `/register` mengembalikan `HTTP 404` (`IR-GOR-01`), `normPhone()` gagal pada `+62 08...` (`IR-GOR-02`), `?start_date=2020-01-01` masih merender `612` slot aktif (`IR-GOR-05`), dan `?start_date=invalid-date` memicu **`HTTP 500 Server Error`** (`IR-GOR-06`). | **Ada Defect Kritis/Major** |
| 2 | **Performance Efficiency** | *Time behaviour, Resource utilization, Capacity* | *Client interaction* instan (`openBooking=62,93 ms`, `updateTotal=8,11 ms`), kompresi Brotli/Gzip aktif, dan `0,0%` error pada `104` request `GET` (`1/5/10 VUs`). **Temuan bottleneck:** HTML mentah `/booking` mencapai `535,37 KB` (`IR-GOR-08`), spike *cold TTFB* `/` `2618,3 ms` (`IR-GOR-09`), dan pada `10 VUs` latensi `/booking` melonjak ke **`p95 = 5314,28 ms`** (`5,14x` dari baseline `1 VU = 1033,24 ms`, `IR-GOR-07`). | **Perlu Optimasi `/booking`** |
| 3 | **Compatibility** | *Co-existence, Interoperability* | Desktop (`1280×800`) dan `#bookingModal` mobile (`390×844`, lebar kartu `350 px`) tampil baik tanpa error JS konsol. **Temuan Mobile:** Pada halaman `/` viewport `390×844`, tautan navbar terpotong (`LOGIN` -> `LOGI`, tombol `BOOKING` terdorong ke `x=489 px`, `IR-GOR-10`). | **Cukup — Perlu Perbaikan Navbar Mobile** |
| 4 | **Interaction Capability** *(revisi Usability 2023)* | *User error protection, Operability, Self-descriptiveness* | Form `/login` memakai validasi HTML5 `required`/`email`, modal booking mudah dipakai & reset otomatis via `closeModal()`. Namun `#custName` meloloskan spasi `"   "` & 1 karakter (`IR-GOR-03`) dan pesan error invalid date langsung jatuh ke layar `500 Server Error`. | **Cukup — Perlu Perbaikan Validasi** |
| 5 | **Reliability** | *Maturity, Availability, Fault tolerance, Recoverability* | `104` request `GET` uji beban `1–10 VUs` mencatat `0%` error, dan `submitBooking()` menonaktifkan `#btnSubmit` serta memulihkannya melalui `.catch()`. Kekurangan pada *fault tolerance* parameter `?start_date=invalid-date` (`HTTP 500`). | **Baik *(Kecuali Validasi Query)*** |
| 6 | **Security** | *Confidentiality, Integrity, Resistance* | `X-CSRF-TOKEN` dan `Content-Security-Policy: upgrade-insecure-requests` aktif; **4 header keamanan HTTP hilang** (`HSTS`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`). Selain itu terverifikasi **`205` slot pada DOM publik `/booking` memuat `data-phone` & `data-name` non-kosong** serta kode `manageBooking()` (`IR-GOR-04`). | **Perlu Hardening & Pembersihan PII DOM** |
| 7 | **Maintainability** | *Modularity, Analysability, Testability* | Skrip JS interaksi (`/booking`) sepanjang `7.473` karakter ditanam *inline* di HTML bersama grid jadwal `535 KB`, mempermudah analisis statis *White Box* tetapi kurang modular untuk pengembangan jangka panjang. | **Cukup** |
| 8 | **Flexibility** *(revisi Portability 2023)* | *Adaptability, Installability* | Berbasis web standar di balik CDN `hcdn` tanpa instalasi klien dan responsif pada modal pemesanan mobile. | **Memadai** |
| 9 | **Safety** *(baru 2023)* | *Operational constraints, Hazard warning* | Batas operasional jam tutup `00:00` (`startHour + duration > 24`) terverifikasi akurat pada BVA `22:00 + 2 Jam` (lolos) vs `22:00 + 3 Jam` (ditolak alert jam tutup). | **Diterapkan & Terverifikasi PASS** |

---

## 2. Rincian Temuan Header Keamanan HTTP (*Passive Scan*)

| Header HTTP | Status Teramati (`/`, `/booking`, `/login`) | Dampak Keamanan |
| :--- | :---: | :--- |
| `Content-Security-Policy` | `upgrade-insecure-requests` | Memaksa aset HTTPS, namun belum membatasi `script-src` & `frame-ancestors`. |
| `Strict-Transport-Security` | **TIDAK ADA** | Klien berisiko tidak memaksa HSTS pada koneksi awal. |
| `X-Frame-Options` | **TIDAK ADA** | Rentan disematkan pada `<iframe>` pihak ketiga (*clickjacking*). |
| `X-Content-Type-Options` | **TIDAK ADA** | Berisiko *MIME-type sniffing*. |
| `Referrer-Policy` | **TIDAK ADA** | Menggunakan kebijakan default browser saat mengarah ke tautan WhatsApp. |

---

## 3. Rekomendasi Prioritas Perbaikan
1. **Prioritas Tinggi (Security/Privacy & Error Handling):** Hapus atribut `data-phone` dan PII dari HTML publik `/booking` (`IR-GOR-04`), tambahkan validasi/`try-catch` pada query `start_date` agar tidak crash `HTTP 500` (`IR-GOR-06`) serta nonaktifkan slot tanggal masa lalu (`IR-GOR-05`), dan lengkapi 4 *HTTP security headers*.
2. **Prioritas Tinggi (Performance `/booking`):** Terapkan caching jangka pendek atau pemuatan grid bertahap/JSON agar latensi `10 VUs` (`p95 = 5,31s`, `IR-GOR-07`) dan payload HTML (`535 KB`, `IR-GOR-08`) turun signifikan.
3. **Prioritas Menengah (Validation & Mobile UI):** Perbaiki urutan `normPhone()` untuk `+62 08...` (`IR-GOR-02`), tambahkan `.trim()` + panjang minimal `#custName` (`IR-GOR-03`), lengkapi atau hapus rute `/register` (`IR-GOR-01`), dan perbaiki tata letak navbar pada viewport `390 px` (`IR-GOR-10`).
