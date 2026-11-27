# Audit Kualitas Perangkat Lunak Berbasis ISO/IEC 25010:2023, 25019:2023 & 40500:2025 - GOR Permata Badminton Hall

Dokumen ini memetakan kualitas **Portal Booking GOR Permata Badminton Hall** (`https://gorpermatabadminton.com`) menggunakan model mutu terbaru **ISO/IEC 25010:2023** (*Product quality model* — 9 karakteristik), **ISO/IEC 25019:2023** (*Quality-in-use model*), **ISO/IEC 25002:2024** (*Quality model overview*), serta kompatibilitas tampilan **ISO/IEC 40500:2025 (W3C WCAG 2.2)**. Hasil berikut menggabungkan observasi pasif awal (14 November 2026) **dan hasil eksekusi aktual Black Box ([`23 TC`](../03-hasil-pengujian/test-case-blackbox.md)) serta Performance Testing ([`10 TC`](../03-hasil-pengujian/test-case-performance.md)) pada 17 November 2026**.

---

## 0. Ringkasan Hasil Audit Kualitas

- **Cakupan Audit:** Memetakan seluruh hasil **Black Box Testing (`23` kasus uji: `16 Pass, 7 Fail`)** dan **Performance Testing (`10` kasus uji: `7 Pass, 3 Fail`)** ke dalam **`9` aspek mutu `ISO/IEC 25010:2023`** serta evaluasi penggunaan nyata (`ISO/IEC 25019:2023`) dan kerapian tampilan (`ISO/IEC 40500:2025 / WCAG 2.2`).
- **Aspek yang Sudah Baik:** Kestabilan server saat uji beban (`0%` error pada `104` kali akses `GET`), kepatuhan aturan batas jam tutup `00:00`, kecepatan klik tombol (`62,93 ms`), serta kemudahan akses langsung lewat browser laptop maupun HP tanpa instalasi aplikasi.
- **Aspek Prioritas Perbaikan:** Keamanan & privasi data (penghapusan `205` nomor WA pelanggan dari HTML publik `/booking` dan penambahan `4` header keamanan HTTP), penanganan tanggal (`HTTP 500` & tanggal lampau), validasi input nama/nomor `+62 08...`, kerapian menu atas di layar HP (`390×844`), serta optimasi kecepatan halaman `/booking` saat diakses `10` orang bersamaan (`5,31` detik).
- **Laporan Resmi Lengkap (Word & PDF):** [`05-dokumentasi-laporan/`](../05-dokumentasi-laporan/) | **Daftar 10 Temuan:** [`incident-reports.md`](../03-hasil-pengujian/incident-reports.md)

---

## 1. Matriks Evaluasi 9 Karakteristik ISO/IEC 25010:2023

| No | Karakteristik (2023) | Sub-Karakteristik Relevan | Hasil Observasi & Pengujian Terukur (17 Nov 2026) | Status Penilaian |
| :-: | :--- | :--- | :--- | :---: |
| 1 | **Functional Suitability** | *Functional completeness, correctness, appropriateness* | 7 rute publik utama aktif `HTTP 200 OK`, tarif `updateTotal()` (`1..5` jam = `Rp 40.000..Rp 200.000`) tepat, dan BVA panjang WA `11–14` digit akurat. **Cacat ditemukan:** `/register` mengembalikan `HTTP 404` ([`IR-GOR-01`](../03-hasil-pengujian/incident-reports.md)), `normPhone()` gagal pada `+62 08...` ([`IR-GOR-02`](../03-hasil-pengujian/incident-reports.md)), `?start_date=2020-01-01` masih merender `612` slot aktif ([`IR-GOR-05`](../03-hasil-pengujian/incident-reports.md)), dan `?start_date=invalid-date` memicu **`HTTP 500 Server Error`** ([`IR-GOR-06`](../03-hasil-pengujian/incident-reports.md)). | **Ada Defect Kritis/Major** |
| 2 | **Performance Efficiency** | *Time behaviour, Resource utilization, Capacity* | *Client interaction* instan (`openBooking=62,93 ms`, `updateTotal=8,11 ms`), kompresi Brotli/Gzip aktif, dan `0,0%` error pada `104` request `GET` (`1/5/10 VUs`). **Temuan bottleneck:** HTML mentah `/booking` mencapai `535,37 KB` ([`IR-GOR-08`](../03-hasil-pengujian/incident-reports.md)), spike *cold TTFB* `/` `2618,3 ms` ([`IR-GOR-09`](../03-hasil-pengujian/incident-reports.md)), dan pada `10 VUs` latensi `/booking` melonjak ke **`p95 = 5314,28 ms`** (`5,14x` dari baseline `1 VU = 1033,24 ms`, [`IR-GOR-07`](../03-hasil-pengujian/incident-reports.md)). | **Perlu Optimasi `/booking`** |
| 3 | **Compatibility** | *Co-existence, Interoperability* | Desktop (`1280×800`) dan `#bookingModal` mobile (`390×844`, lebar kartu `350 px`) tampil baik tanpa error JS konsol. **Temuan Mobile:** Pada halaman `/` viewport `390×844`, tautan navbar terpotong (`LOGIN` -> `LOGI`, tombol `BOOKING` terdorong ke `x=489 px`, [`IR-GOR-10`](../03-hasil-pengujian/incident-reports.md)). | **Cukup — Perlu Perbaikan Navbar Mobile** |
| 4 | **Interaction Capability** *(revisi Usability 2023)* | *User error protection, Operability, Self-descriptiveness* | Form `/login` memakai validasi HTML5 `required`/`email`, modal booking mudah dipakai & reset otomatis via `closeModal()`. Namun `#custName` meloloskan spasi `"   "` & 1 karakter ([`IR-GOR-03`](../03-hasil-pengujian/incident-reports.md)) dan pesan error invalid date langsung jatuh ke layar `500 Server Error`. | **Cukup — Perlu Perbaikan Validasi** |
| 5 | **Reliability** | *Maturity, Availability, Fault tolerance, Recoverability* | `104` request `GET` uji beban `1–10 VUs` mencatat `0%` error, dan `submitBooking()` menonaktifkan `#btnSubmit` serta memulihkannya melalui `.catch()`. Kekurangan pada *fault tolerance* parameter `?start_date=invalid-date` (`HTTP 500`). | **Baik *(Kecuali Validasi Query)*** |
| 6 | **Security** | *Confidentiality, Integrity, Resistance* | `X-CSRF-TOKEN` dan `Content-Security-Policy: upgrade-insecure-requests` aktif; **4 header keamanan HTTP hilang** (`HSTS`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`). Selain itu terverifikasi **`205` slot pada DOM publik `/booking` memuat `data-phone` & `data-name` non-kosong** serta kode `manageBooking()` ([`IR-GOR-04`](../03-hasil-pengujian/incident-reports.md)). | **Perlu Hardening & Pembersihan PII DOM** |
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

## 3. Evaluasi *Quality-in-Use* (`ISO/IEC 25019:2023`) & Aksesibilitas Tampilan (`ISO/IEC 40500:2025 / WCAG 2.2`)

| Dimensi `25019:2023` | Temuan & Dampak bagi Pemesan / Admin GOR Permata |
| :--- | :--- |
| **Effectiveness & Efficiency** | Pemesanan slot valid cepat di klien (`openBooking = 62,93 ms`), namun terhambat bagi pengguna yang mengetik format `+62 08...` ([`IR-GOR-02`](../03-hasil-pengujian/incident-reports.md)) atau ketika 10 pengguna bersamaan mengakses `/booking` (`p95 = 5,31 detik`, [`IR-GOR-07`](../03-hasil-pengujian/incident-reports.md)). |
| **Freedom from Risk** | Risiko privasi pelanggan tinggi akibat eksposur `data-phone` & `data-name` pada `205` slot publik ([`IR-GOR-04`](../03-hasil-pengujian/incident-reports.md)), ketiadaan 4 header keamanan HTTP, serta celah crash `HTTP 500` pada query `?start_date=` ([`IR-GOR-06`](../03-hasil-pengujian/incident-reports.md)). |
| **Acceptability & WCAG 2.2 Reflow** | Pada viewport mobile `390×844` (*W3C WCAG 2.2 Reflow / ISO 40500:2025*), navbar halaman `/` memotong tautan `LOGIN` -> `LOGI` dan mendorong `BOOKING` ke `x = 489 px` ([`IR-GOR-10`](../03-hasil-pengujian/incident-reports.md)), serta menu `/register` kembali `404` ([`IR-GOR-01`](../03-hasil-pengujian/incident-reports.md)). |

---

## 4. Rekomendasi Prioritas Perbaikan
1. **Prioritas Tinggi (Security/Privacy & Error Handling):** Hapus atribut `data-phone` dan PII dari HTML publik `/booking` ([`IR-GOR-04`](../03-hasil-pengujian/incident-reports.md)), tambahkan validasi/`try-catch` pada query `start_date` agar tidak crash `HTTP 500` ([`IR-GOR-06`](../03-hasil-pengujian/incident-reports.md)) serta nonaktifkan slot tanggal masa lalu ([`IR-GOR-05`](../03-hasil-pengujian/incident-reports.md)), dan lengkapi 4 *HTTP security headers*.
2. **Prioritas Tinggi (Performance `/booking`):** Terapkan caching jangka pendek atau pemuatan grid bertahap/JSON agar latensi `10 VUs` (`p95 = 5,31s`, [`IR-GOR-07`](../03-hasil-pengujian/incident-reports.md)) dan payload HTML (`535 KB`, [`IR-GOR-08`](../03-hasil-pengujian/incident-reports.md)) turun signifikan.
3. **Prioritas Menengah (Validation & Mobile UI):** Perbaiki urutan `normPhone()` untuk `+62 08...` ([`IR-GOR-02`](../03-hasil-pengujian/incident-reports.md)), tambahkan `.trim()` + panjang minimal `#custName` ([`IR-GOR-03`](../03-hasil-pengujian/incident-reports.md)), lengkapi atau hapus rute `/register` ([`IR-GOR-01`](../03-hasil-pengujian/incident-reports.md)), dan perbaiki tata letak navbar pada viewport `390 px` ([`IR-GOR-10`](../03-hasil-pengujian/incident-reports.md)).

---

## 5. Rujukan Standar Resmi (`>= 2023`)
- **ISO/IEC 25010:2023** — [`iso.org/standard/78176.html`](https://www.iso.org/standard/78176.html) | Ringkasan Audit: [`Audit-Mutu-ISO-IEC-25010-2023-GOR-Permata.pdf`](./pdf-standar/Audit-Mutu-ISO-IEC-25010-2023-GOR-Permata.pdf)
- **ISO/IEC 25019:2023** — [`iso.org/standard/78177.html`](https://www.iso.org/standard/78177.html)
- **ISO/IEC 25002:2024** — [`iso.org/standard/78175.html`](https://www.iso.org/standard/78175.html)
- **ISO/IEC 40500:2025 (W3C WCAG 2.2)** — [`iso.org/standard/91029.html`](https://www.iso.org/standard/91029.html) | PDF Lokal: [`W3C_WCAG_2.2_Accessibility_2023_ISO_40500_2025.pdf`](./pdf-standar/W3C_WCAG_2.2_Accessibility_2023_ISO_40500_2025.pdf)
