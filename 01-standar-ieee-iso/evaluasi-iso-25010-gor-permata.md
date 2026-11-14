# Audit Kualitas Perangkat Lunak Berbasis ISO/IEC 25010:2023 — GOR Permata Badminton Hall

Dokumen ini memetakan kualitas **Portal Booking GOR Permata Badminton Hall** (`https://gorpermatabadminton.com`) menggunakan model mutu terbaru **ISO/IEC 25010:2023** (*Systems and software Quality Requirements and Evaluation / SQuaRE*), yang memperluas model 2011 menjadi **9 karakteristik utama** (*Functional Suitability, Performance Efficiency, Compatibility, Interaction Capability, Reliability, Security, Maintainability, Flexibility,* dan *Safety*).

> **Catatan Metodologi:** Seluruh temuan berasal dari observasi langsung, pengujian *HTTP GET* pasif, pembacaan respons *header* server (`hcdn`), serta analisis skrip JavaScript sisi klien pada `/booking` tanggal **14 November 2026** tanpa mengirim transaksi palsu ke basis data UMKM.

---

## 1. Matriks Evaluasi 9 Karakteristik ISO/IEC 25010:2023

| No | Karakteristik (2023) | Sub-Karakteristik Relevan | Hasil Observasi Aktual pada Portal GOR Permata | Status Penilaian |
| :-: | :--- | :--- | :--- | :---: |
| 1 | **Functional Suitability** | *Functional completeness, Functional correctness, Functional appropriateness* | Rute inti (`/`, `/booking`, `/login`, `/fasilitas/*`) merespons `HTTP 200 OK` dan kalkulasi tarif `updateTotal()` (`Rp 40.000`/jam) tepat. Namun endpoint `/register` mengembalikan **`HTTP 404 Not Found`** (`BUG-GOR-01`) dan `normPhone()` gagal menormalisasi format nomor `+62 08...` (`BUG-GOR-02`). | **Cukup — Ada Defect** |
| 2 | **Performance Efficiency** | *Time behaviour, Resource utilization, Capacity* | Waktu muat HTML langsung relatif cepat: `/` (`0,34s`, `37.947` karakter), `/login` (`0,25s`, `13.145` karakter), `/booking` (`1,36s`, `570.436` karakter). Ukuran HTML halaman `/booking` cukup besar karena seluruh grid jadwal mingguan & skrip dirender sekaligus. | **Baik *(Catatan Ukuran `/booking`)*** |
| 3 | **Compatibility** | *Co-existence, Interoperability* | Aplikasi mengarahkan konfirmasi pemesanan ke tautan WhatsApp (`data.wa_link`) melalui peramban standar. Pengujian lintas ukuran layar (*desktop vs mobile*) dan peramban tambahan dijadwalkan lengkap pada Tahap 2. | **Dalam Pengujian Lanjut** |
| 4 | **Interaction Capability** *(pengganti Usability pada edisi 2023)* | *Appropriateness recognizability, Learnability, Operability, User error protection, User engagement, Inclusivity, User assistance, Self-descriptiveness* | Alur pilih tanggal (`#jumpDate`), pilih slot grid, serta buka/tutup modal `#bookingModal` mudah dipahami. Celah pada **User error protection**: input `#custName` menerima spasi `"   "` atau 1 karakter karena tidak ada `.trim()` maupun batas panjang minimal (`BUG-GOR-03`), dan pesan error WA belum menjelaskan kegagalan awalan `+62 08...`. | **Cukup — Perlu Perbaikan Validasi** |
| 5 | **Reliability** | *Maturity, Availability, Fault tolerance, Recoverability* | Seluruh rute layanan utama aktif. Pada `submitBooking()`, tombol `#btnSubmit` langsung di-nonaktifkan (`btn.disabled = true`) saat pengiriman untuk mencegah *double submit*, dan blok `.catch(...)` menampilkan pesan gangguan jaringan jika koneksi terputus. | **Baik** |
| 6 | **Security** | *Confidentiality, Integrity, Non-repudiation, Accountability, Authenticity, Resistance* | Pengambilan *HTTP response headers* pada `/`, `/booking`, dan `/login` mendapati header `Content-Security-Policy: upgrade-insecure-requests` terpasang, namun **4 header keamanan web penting belum aktif (*MISSING*)**: `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`, dan `Referrer-Policy`. Selain itu, skrip manajemen internal (`manageBooking()`, pesan `"Hubungi Koko atau Aan."`, dan endpoint `/bookings/confirm\|reject\|delete`) ikut dimuat pada halaman pengunjung publik (`BUG-GOR-04`), meski otorisasi akhir berada di server dan pengiriman dilindungi `X-CSRF-TOKEN`. | **Perlu Peningkatan Header & Pemisahan Skrip** |
| 7 | **Maintainability** | *Modularity, Reusability, Analysability, Modifiability, Testability* | Kode CSS/JS interaksi (`/booking`) sepanjang `7.456` karakter disematkan langsung (*inline script*) di dalam file HTML alih-alih dipecah ke modul terpisah, sehingga kurang modular jika aplikasi membesar (*namun mempermudah inspeksi White Box mahasiswa*). | **Cukup** |
| 8 | **Flexibility** *(pengganti Portability pada edisi 2023)* | *Adaptability, Installability, Replaceability, Scalability* | Berbasis web standar di balik server/CDN `hcdn`, dapat diakses lintas sistem operasi tanpa instalasi aplikasi klien; aspek *scalability* infrastruktur server berada di luar ruang lingkup uji publik. | **Memadai *(Scope Terbatas)*** |
| 9 | **Safety** *(Karakteristik Baru Edisi 2023)* | *Operational constraints, Risk identification, Fail-safe, Hazard warning, Safe integration* | Pada konteks operasional bisnis UMKM, portal menerapkan **Operational constraints** & **Hazard warning** di fungsi `submitBooking()` dengan memeriksa `if (startHour + duration > 24)` sehingga pemesanan melewati jam tutup `00:00` ditolak di klien sebelum menyentuh jadwal produksi. | **Diterapkan pada Aturan Jam Tutup** |

---

## 2. Rincian Temuan Header Keamanan HTTP (Bukti Teknis *Passive Scan*)

Hasil pemeriksaan header HTTP `GET` pada tanggal 14 November 2026:

| Header HTTP | Status Teramati (`/`, `/booking`, `/login`) | Dampak Keamanan |
| :--- | :---: | :--- |
| `Content-Security-Policy` | `upgrade-insecure-requests` | Membantu mengalihkan aset HTTP ke HTTPS, namun belum membatasi sumber skrip (*script-src*). |
| `Strict-Transport-Security` | **TIDAK ADA** | Klien berisiko tidak memaksa HTTPS HSTS pada kunjungan awal tanpa redirect. |
| `X-Frame-Options` | **TIDAK ADA** | Situs rentan disematkan pada `<iframe>` pihak ketiga (*clickjacking risk*). |
| `X-Content-Type-Options` | **TIDAK ADA** | Peramban berisiko melakukan *MIME-type sniffing*. |
| `Referrer-Policy` | **TIDAK ADA** | Peramban memakai kebijakan default saat berpindah ke tautan eksternal/WhatsApp. |

---

## 3. Kesimpulan & Rekomendasi Prioritas dari Perspektif ISO/IEC 25010:2023
1. **Prioritas Tinggi (Functional & Interaction Capability):** Perbaiki tautan/rute `/register` (`HTTP 404`) atau hapus referensinya dari portal, benahi urutan normalisasi `normPhone()` agar menghapus `0` setelah kode negara `62` (`6208...` -> `628...`), serta tambahkan `.trim()` dan panjang minimum pada `#custName`.
2. **Prioritas Menengah (Security & Maintainability):** Tambahkan header keamanan HTTP (`Strict-Transport-Security`, `X-Frame-Options: SAMEORIGIN`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`), serta pisahkan berkas JavaScript manajemen internal admin/penjaga agar tidak ikut dimuat ke pengunjung biasa.
