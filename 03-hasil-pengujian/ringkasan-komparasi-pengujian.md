# Ringkasan Komparasi Hasil Pengujian Dua Objek UMKM

Dokumen ini merangkum perbandingan hasil observasi, pengujian manual/non-fungsional, serta eksekusi *Automation Testing* (Playwright Python) antara **Objek 1 (GOR Permata Badminton Hall)** dan **Objek 2 (Kolam Renang TASA Pamulang)** per **14 November 2026**.

---

## 1. Tabel Perbandingan Teknis & Hasil Eksekusi

| Dimensi Uji | Objek 1: GOR Permata Badminton Hall | Objek 2: Kolam Renang TASA Pamulang |
| :--- | :--- | :--- |
| **Tautan Portal** | https://gorpermatabadminton.com | https://www.kolamtasa.com/ |
| **Stack & Hosting** | Server web + JS inline klien terbuka (`~7,4 KB` di `/booking`), token CSRF `_token` | Next.js (App Router) + Vercel (`_next/static/chunks/*.js` *minified*) |
| **Sistem Transaksi** | Booking grid + `POST /bookings/store` -> mengunci slot di database + link WA | **Tanpa checkout/cart**; seluruh pemesanan diarahkan via WhatsApp / pendaftaran wizard |
| **Kekuatan Utama untuk Tugas QA** | **White Box** sangat jelas (`normPhone()` $V(G)=4$, `submitBooking()` terbuka dibedah); sesuai 100% analogi lapangan bulu tangkis Pak Ahmad Fauzi. | **Bebas checkout permanen**, uji berulang pada validasi wizard **20/21 langkah** `/lesrenang`, dan kaya temuan bug nyata di berbagai lapisan. |
| **Hasil Eksekusi Playwright Non-Destruktif** | **9 / 9 Check PASS** (`0` `POST` booking terkirim; 397 slot terdeteksi pada `2026-11-15`) | **8 / 8 Check PASS** (`0` `POST` form terkirim; memverifikasi 14 rute `200`, 6 rute `404`, header, DOM, dan wizard Step 1–2) |
| **Jumlah Defect Awal Terverifikasi** | **4 Temuan (`BUG-GOR-01` s.d. `04`)** | **6 Temuan (`BUG-TASA-01` s.d. `06`)** |

---

## 2. Rekapitulasi Temuan Defect Utama Kedua Objek

### Objek 1 — `BUG-GOR-01` s.d. `04` ([Detail lengkap](../objek-1-gor-permata/test-cases-dan-laporan-bug.md))
1. **`BUG-GOR-01` (Major):** Halaman `/register` mengembalikan **HTTP `404 Not Found`**.
2. **`BUG-GOR-02` (Minor / White Box):** `normPhone()` gagal menormalkan nomor berawalan `+62 08...` menjadi `628...` sehingga ditolak regex.
3. **`BUG-GOR-03` (Minor):** Input `#custName` di modal booking belum memakai `.trim()` atau batas panjang karakter minimum.
4. **`BUG-GOR-04` (Info):** Pesan operasional internal (`Hubungi Koko atau Aan.`) dan path manajemen ikut dimuat di JS publik halaman `/booking`.

### Objek 2 — `BUG-TASA-01` s.d. `06` ([Detail lengkap](../objek-2-kolam-renang-tasa/test-cases-dan-laporan-bug.md))
1. **`BUG-TASA-01` (Critical / Functional):** Form di `/kontak` tidak memiliki atribut `action`, `method`, `onSubmit`, maupun *Server Action* (`$ACTION` kosong), sehingga klik *"Kirim pesan"* tidak mengirim pesan ke server/WhatsApp.
2. **`BUG-TASA-02` (Major / UI):** Item footer `Privacy`, `Terms`, `Settings` hanya tag `<span>` mati; rute `/privacy`, `/terms`, `/settings`, `/kerjasama` mengembalikan **HTTP `404`**.
3. **`BUG-TASA-03` (Minor / Content):** Footer masih bertuliskan `Hak Cipta 2023 - Kolam Renang TASA` padahal konten blog diperbarui November 2026.
4. **`BUG-TASA-04` (Major / Security):** 5 HTTP security header tidak terpasang (`Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`), `X-Powered-By: Next.js` terbuka, dan `robots.txt` mencantumkan path internal.
5. **`BUG-TASA-05` (Minor / Accessibility):** 7 dari 50 tag `<img>` di beranda kehilangan/kosong atribut `alt`.
6. **`BUG-TASA-06` (Major / Validation & UX):** Field `whatsapp` di wizard `/lesrenang` menerima string sembarang selain kosong (mis. `"abc"`), sementara `/blog` belum memiliki fitur pencarian dan pagination di luar rentang (`0`, `5`) mengembalikan `404`.
