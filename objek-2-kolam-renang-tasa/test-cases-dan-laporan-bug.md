# Test Cases Manual & Laporan Temuan Bug: Kolam Renang TASA

Mengacu pada format **ISO/IEC/IEEE 29119-3** (*Test Case Specification* & *Defect Report*). Seluruh eksekusi pada `https://www.kolamtasa.com/` bersifat **non-destruktif** (memblokir `POST` pada skrip otomasi dan menghentikan pengujian wizard sebelum tombol `Kirim pendaftaran` / `Kirim ajuan`).

---

## A. Daftar Test Case Utama (`TC-TASA-01` s.d. `TC-TASA-11`)

| ID TC | Modul / Fitur | Teknik | Input / Langkah Uji | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| `TC-TASA-01` | Navigasi Halaman Utama | Functional | Akses `/`, `/berenang`, `/lesrenang`, `/kontak`, `/event`, `/blog`, `/club`, `/hidroterapi`, `/gelombang`, `/restoran`, `/sekolah-cita-pelangi` | Seluruh rute utama mengembalikan HTTP `200 OK` dan konten tampil normal. |
| `TC-TASA-02` | Tautan Footer (`Privacy`, `Terms`, `Settings`) & `/kerjasama` | Functional / UI | Klik item footer `Privacy`, `Terms`, `Settings` atau akses langsung `/privacy`, `/terms`, `/settings`, `/kerjasama` | Halaman kebijakan/menu tampil (`200 OK`) — *(Saat ini tercatat defect `BUG-TASA-02`: span mati & HTTP `404`)*. |
| `TC-TASA-03` | Pengiriman Form `/kontak` | Functional | Inspeksi & uji alur form `#name`, `#email`, `#phone`, `#subject`, `#message` pada `/kontak` | Form memiliki action/handler untuk mengirim pesan — *(Saat ini tercatat defect `BUG-TASA-01`: `<form>` tanpa action/handler)*. |
| `TC-TASA-04` | Validasi Kosong Step 1 `/lesrenang` | Black Box / State | Buka `/lesrenang` (`1 / 20`), langsung klik tombol `Lanjut` tanpa mengisi nama | Tetap di Step 1 dan tampil pesan error `"Nama muridnya belum diisi."`. |
| `TC-TASA-05` | Transisi Step 1 -> Step 2 `/lesrenang` | State Transition | Isi `Nama sesuai akta`, klik `Lanjut`; lalu uji `Lanjut` kosong pada Step 2 | Step berpindah ke `2 / 20` (`Nama panggilannya?`), dan error `"Nama panggilannya belum diisi."` tampil saat kosong. |
| `TC-TASA-06` | Batas Usia Step `lahir` & `kelas` | Black Box (BVA) | Pilih tanggal lahir usia `< 1` tahun vs `1–3` tahun vs `4–10` tahun vs `> 10` tahun | Usia `< 1` tahun ditolak di step `lahir`; `1–3` sesuai *Rumbul Club*; `4–10` sesuai *Kids Swimming*; `> 10` diarahkan ke kelas privat. |
| `TC-TASA-07` | Cabang Motivasi `"Lain-lain"` | White/Black Box | Pada step `motivasi`, pilih selain `"Lain-lain"` vs pilih `"Lain-lain"` | Memilih `"Lain-lain"` menambah 1 langkah `motivasi_lain` (total step berubah `20` -> `21`). |
| `TC-TASA-08` | Validasi Email & WhatsApp `/lesrenang` | Black Box (EP) | Uji email `"abc@gmail"` (tanpa TLD) dan WhatsApp `"abc"` | Email salah format ditolak; WA seharusnya ikut divalidasi format angka — *(Tercatat `BUG-TASA-06`: WA menerima `"abc"`)*. |
| `TC-TASA-09` | Filter & Pagination `/blog` | Black Box (BVA) | Akses `/blog/les-renang`, `/blog/halaman/2`, lalu batas luar `/blog/halaman/0` dan `/blog/halaman/5` | Kategori & halaman `1..4` tampil (`200 OK`); halaman di luar batas mengembalikan `404`. |
| `TC-TASA-10` | Audit Security Headers & `robots.txt` | Non-Functional (Gray Box) | Inspeksi header respons HTTPS `/` dan file `/robots.txt` | Header keamanan standar terpasang lengkap — *(Tercatat `BUG-TASA-04`: 5 header hilang & path internal tercantum di `robots.txt`)*. |
| `TC-TASA-11` | Audit Aksesibilitas Gambar (`alt`) | Non-Functional | Hitung seluruh elemen `<img>` pada `/` yang tidak memiliki teks `alt` | Seluruh gambar informatif memiliki `alt` — *(Tercatat `BUG-TASA-05`: 7 dari 50 gambar `alt` kosong/hilang)*. |

---

## B. Laporan Temuan Bug Terverifikasi (*Defect Report*)

### `BUG-TASA-01`: Form `/kontak` Statis Tanpa `action`, `onSubmit`, ataupun Server Action
- **Kategori / Severity / Priority:** Functional / **Critical** / **High**
- **URL:** `https://www.kolamtasa.com/kontak`
- **Steps to Reproduce:**
  1. Buka `https://www.kolamtasa.com/kontak`.
  2. Periksa elemen `<form>` dan seluruh bundel JS halaman tersebut.
  3. Isi seluruh field wajib lalu tekan **"Kirim pesan"**.
- **Expected Result:** Pesan dikirimkan ke server/email admin atau diarahkan otomatis ke WhatsApp admin dengan konfirmasi pengiriman.
- **Actual Result:** Elemen `<form>` tidak memiliki atribut `action` maupun `method`, string `"Kirim pesan"` tidak ada dalam JS client bundle mana pun, dan `$ACTION` di RSC payload kosong (`[]`). Klik tombol hanya memicu *GET reload* browser tanpa mengirim data ke mana pun.

### `BUG-TASA-02`: Teks Footer `Privacy`, `Terms`, `Settings` Tidak Dapat Diklik & Rute `/kerjasama` `404`
- **Kategori / Severity / Priority:** UI & Navigation / **Major** / **Medium**
- **URL:** Seluruh halaman (footer) serta `/privacy`, `/terms`, `/settings`, `/kerjasama`
- **Expected Result:** Item kebijakan di footer merupakan tautan (`<a>`) menuju halaman aktif (`HTTP 200`).
- **Actual Result:** Footer hanya merender `<span>Privacy</span><span>Terms</span><span>Settings</span>` tanpa `href`, dan akses ke `/privacy`, `/terms`, `/settings`, serta `/kerjasama` mengembalikan **HTTP `404 Not Found`**.

### `BUG-TASA-03`: Tahun Hak Cipta di Footer Tidak Mutakhir (`Hak Cipta 2023`)
- **Kategori / Severity / Priority:** Content / **Minor** / **Low**
- **Actual Result:** Footer di seluruh halaman masih menampilkan `Hak Cipta 2023 - Kolam Renang TASA`, sementara blog aktif menerbitkan artikel bertanggal `14 November 2026`.

### `BUG-TASA-04`: Lima HTTP Security Header Hilang, `X-Powered-By` Terbuka, & Path Disclosure di `robots.txt`
- **Kategori / Severity / Priority:** Security (Non-Functional) / **Major** / **Medium**
- **Actual Result:** Header `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, dan `Permissions-Policy` tidak ada di respons `https://www.kolamtasa.com/`, header `X-Powered-By: Next.js` terekspos, dan `/robots.txt` mencantumkan path internal (`/club/`, `/auth/`, `/setoran/`, `/lapangan/`, `/internal/`, `/tagihan/`, `/dapur/`, `/api/`, `/loket/`, `/air/`).

### `BUG-TASA-05`: 7 dari 50 Gambar di Beranda Tidak Memiliki Atribut `alt` Deskriptif
- **Kategori / Severity / Priority:** Accessibility / **Minor** / **Medium**
- **Actual Result:** Audit DOM pada `/` menemukan 7 tag `<img>` memiliki `alt=""` atau tanpa nilai deskriptif.

### `BUG-TASA-06`: Validasi Field `whatsapp` di `/lesrenang` Terlalu Longgar & `/blog` Tanpa Search Bar
- **Kategori / Severity / Priority:** Functional Validation & UX / **Major** / **Medium**
- **Actual Result:** Fungsi `whatsapp.sah()` pada `/lesrenang` hanya memeriksa string tidak kosong (`.trim()`), tidak memvalidasi format angka/awalan `08`/`62` sebagaimana `email.sah` memakai regex. Selain itu, `/blog` dengan puluhan artikel belum memiliki kolom pencarian.

