# Test Plan: Website Kolam Renang TASA (`https://www.kolamtasa.com/`)

Disusun mengikuti kerangka **ISO/IEC/IEEE 29119-3 (*Test Plan*)** serta materi *Automation Testing* (14 November 2026).

---

## 1. Identifikasi & Tujuan Pengujian
- **ID Test Plan:** `TP-TASA-01`
- **Target Sistem:** Aplikasi Web Publik **Kolam Renang TASA** (`https://www.kolamtasa.com/`)
- **Tujuan:** Mengevaluasi fungsionalitas antarmuka publik, ketepatan validasi input, konsistensi navigasi, mutu non-fungsional (keamanan header HTTP, aksesibilitas gambar, respons waktu), serta keandalan pengujian otomatis berulang tanpa mengganggu operasional admin UMKM.

---

## 2. Ruang Lingkup (*Scope*)

### A. In Scope (Diuji)
1. **Navigasi & Integritas Rute:** Seluruh halaman publik pada `sitemap-pages.xml`, tautan navbar/footer (`Privacy`, `Terms`, `Settings`), serta artikel dan redirect WhatsApp.
2. **Wizard Pendaftaran `/lesrenang`:** Interaksi 20/21 langkah (`1 / 20` hingga `21`), logika cabang `"Lain-lain"` pada alasan motivasi, validasi input kosong/salah format, kalkulasi umur dari tanggal lahir (`1–10` tahun vs di bawah 1 tahun), dan validasi `email` serta `whatsapp`.
3. **Form `/kontak` & `/event`:** Inspeksi atribut HTML, kelengkapan field wajib, dan perilaku tombol submit (`Kirim pesan` / `Kirim ajuan`).
4. **Modul Blog (`/blog`):** Filter kategori, *pagination* batas bawah & atas (`/blog/halaman/0`, `1`, `2`, `4`, `5`), serta ketersediaan fitur pencarian.
5. **Pengujian Non-Fungsional:** Pemeriksaan *HTTP Security Headers*, konfigurasi `robots.txt`, kelengkapan atribut `alt` pada `<img>`, dan waktu respons halaman.

### B. Out of Scope (Tidak Diuji Secara Aktif)
1. **Submit Berhasil Form `/lesrenang` (Langkah Akhir) & `/event`:** Karena memicu *Next.js Server Action* yang mengirim data ke sistem internal/admin TASA, pengujian berhenti pada langkah sebelum pengiriman akhir agar tidak membanjiri admin dengan data fiktif.
2. **Rute Terlarang di `robots.txt`:** Path `/club/`, `/auth/`, `/setoran/`, `/lapangan/`, `/internal/`, `/tagihan/`, `/dapur/`, `/api/`, `/loket/`, `/air/` **tidak diakses/di-probe** demi kepatuhan etika pengujian pasif.
3. **Uji Beban Skala Besar (*Flooding / Stress Test*):** Tidak mengirim trafik masif ke server produksi Vercel/UMKM.

---

## 3. Strategi Pengujian
1. **Black Box Testing:** *EP*, *BVA*, *State Transition*, dan *Use Case* pada wizard `/lesrenang`, pagination `/blog`, dan input form `/kontak`.
2. **White Box Testing:** Analisis logika keputusan (*branch/decision analysis*) pada fungsi validasi `sah()` tiap langkah wizard `/lesrenang` dan struktur percabangan dinamis array langkah `W` (dengan catatan teknis keterbatasan kode *minified* Next.js).
3. **Gray Box Testing:** Kombinasi inspeksi respons HTTP/header keamanan, payload React Server Components (`__next_f`, cek `$ACTION`), serta perilaku UI di browser.
4. **Automation Testing (Playwright Python & skrip contoh Cypress):** Skrip dijalankan berulang untuk memvalidasi status halaman, deteksi error form kosong `/lesrenang`, pemeriksaan 404 footer/pagination, dan audit atribut DOM (`POST` diblokir pada skrip otomasi sebagai pengaman).

---

## 4. Kriteria Masuk & Keluar
- **Entry Criteria:** Domain `https://www.kolamtasa.com/` dapat diakses (`HTTP 200`), perangkat uji dilengkapi Playwright/Chromium, dan aturan blokir `POST` pada skrip otomasi telah aktif.
- **Exit Criteria:** Seluruh *Test Case* `TC-TASA-01..12` terevaluasi, 6 temuan awal terverifikasi lengkap, skrip otomasi menghasilkan `execution-log.txt` tanpa error skrip, dan seluruh artefak teknis rampung sebelum wawancara praktisi QA.

---

## 5. Penanganan Risiko Proyek
| Risiko | Dampak | Mitigasi |
| :--- | :--- | :--- |
| **Form `/event` atau langkah akhir `/lesrenang` mengirim data fiktif** | Mengganggu administrasi Kolam TASA | Skrip otomasi memasang interceptor memblokir `POST`, dan uji manual dihentikan sebelum tombol `Kirim pendaftaran` / `Kirim ajuan`. |
| **Hash nama file JS chunk Next.js berubah saat deploy ulang** | Pemetaan kode White Box versi lama perlu penyesuaian | Mencantumkan ID deployment yang diamati (`dpl_GhpthfZjz43gzqmDcFfQHcBZpiJe`) dan memakai selector berbasis role/placeholder stabil pada skrip otomasi. |
| **Pertanyaan dosen terkait jumlah ulasan Google (`2.146 reviews`)** | Kemungkinan dinilai terlalu besar dibanding warung mikro | Menekankan fokus pengujian pada cacat fungsional kritis yang masih ditemukan (`/kontak` mati, validasi WA `/lesrenang` lolos teks non-angka, 404 footer, header keamanan kosong). |

