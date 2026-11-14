# Profil & Analisis Objek Uji: Website Kolam Renang TASA (`kolamtasa.com`)

Hasil observasi teknis langsung terhadap `https://www.kolamtasa.com/` dan seluruh rute publiknya pada **14 November 2026**.

---

## 1. Identitas & Gambaran Sistem
- **Nama Usaha:** Kolam Renang TASA (PT / kawasan rekreasi keluarga di Pamulang; berdiri sejak 1997)
- **Lokasi:** Jl. Salak Raya, Pd. Benda, Kec. Pamulang, Kota Tangerang Selatan, Banten 15416
- **Domain Resmi:** https://www.kolamtasa.com/ (juga menautkan sub-brand venue pernikahan `https://www.ruangtasa.com/`)
- **Arsitektur Teknis:** **Next.js** (App Router, React Server Components & Client Chunks) di-host di **Vercel**, HTTPS aktif (`Strict-Transport-Security: max-age=63072000`).
- **Model Transaksi:** **Tanpa fitur *checkout* / *cart* / pembayaran online.** Seluruh pertanyaan dan pembelian tiket/paket diarahkan ke **WhatsApp Admin (`+62 819-4437-1997`)** atau pendaftaran terstruktur.

---

## 2. Mengapa Tidak Cukup Menguji `/blog` Saja?
Pengamatan awal pada `https://www.kolamtasa.com/blog` menunjukkan:
- Jumlah tag `<form>`: **0** | Jumlah `<input>`: **0**
- Hanya menyediakan tombol filter 3 kategori, *pagination* (`1, 2, …, 4`), dan tautan artikel.
- Jika kelompok hanya membatasi pengujian pada `/blog`, teknik *Black Box* (*EP/BVA*), *State Transition*, *White Box*, dan *Automation Script* menjadi terlalu sempit. Oleh sebab itu, ruang lingkup resmi diperluas ke **seluruh situs publik `https://www.kolamtasa.com/`** agar mencakup modul interaktif `/lesrenang`, `/kontak`, `/event`, `/blog`, dan audit non-fungsional beranda.

---

## 3. Peta Rute Publik Terverifikasi (`sitemap-pages.xml` & Crawl Beranda)

| Rute / URL | Status HTTP (14 Nov 2026) | Fungsi Utama | Potensi Pengujian |
| :--- | :---: | :--- | :--- |
| `/` | `200 OK` (`~0,27s`) | Halaman beranda, ringkasan layanan, FAQ, artikel populer, footer | UI/UX, aksesibilitas (`alt` gambar), tautan eksternal, footer link, security headers |
| `/lesrenang` | `200 OK` | Wizard pendaftaran les renang anak **20/21 langkah** | *Black Box* (EP/BVA/State Transition), *White Box* logika `sah()`, Automation |
| `/kontak` | `200 OK` | Form hubungi kami (`name`, `email`, `phone`, `subject`, `message`) | Uji form & temuan bug kritis `<form>` tanpa handler/action |
| `/event` | `200 OK` | Form pengajuan kegiatan/komunitas (Next.js Server Action) | Validasi input form sebelum pengiriman akhir |
| `/blog` & kategori (`/blog/les-renang`, `/blog/perawatan-kolam`, `/blog/kesehatan-dan-hidroterapi`) | `200 OK` | Daftar artikel edukasi & *pagination* | Filter kategori, BVA pagination (`/blog/halaman/0..5`), ketiadaan search bar |
| `/berenang`, `/hidroterapi`, `/gelombang`, `/club`, `/restoran`, `/sekolah-cita-pelangi` | `200 OK` | Halaman profil layanan, harga, dan redirect WhatsApp spesifik | Navigasi menu, *broken link*, konsistensi format tautan `wa.me` / `api.whatsapp.com` |
| `/privacy`, `/terms`, `/settings`, `/kerjasama` | **`404 Not Found`** | Teks tercantum di footer (`Privacy`, `Terms`, `Settings`) atau label menu | Temuan bug link/halaman hilang (*Dead UI / Broken Route*) |
| `https://www.ruangtasa.com/?utm_...` | `200 OK` (`2,0–2,8s`) | Portal paket pernikahan rujukan | Pengujian performa *redirect* eksternal & *referral parameters* |

