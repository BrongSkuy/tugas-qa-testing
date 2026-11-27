# Test Environment & Data Management Report (`ED1`–`ED4`)

Dokumen ini mengimplementasikan proses **Test Environment and Data Management (`ED1–ED4`)** sesuai **ISO/IEC/IEEE 29119-1:2022** & **29119-5:2024** (*Keyword-Driven Testing* dengan pemisahan data uji JSON) untuk mendukung pengujian **Black Box** dan **Performance Testing** pada **Portal Booking GOR Permata Badminton Hall** (`https://gorpermatabadminton.com`).

---

## 0. Ringkasan Dokumen & Cara Pakai Script

- **Dokumen ini isinya apa?** Menjelaskan **persiapan komputer, aplikasi bantu, dan data contoh palsu** sebelum pengujian dijalankan, serta bagaimana **Prinsip Pengujian Aman (Non-Destruktif)** bekerja secara teknis supaya skrip otomatis tidak pernah mengisi jadwal booking asli GOR Permata.
- **Bagaimana rem pengaman kerjanya?** Di dalam skrip otomatis (`test_gor_permata.py`), baris kode `page.route("**/bookings/store", route.abort())` bekerja seperti **penjaga di dalam browser uji**: form tetap diisi data contoh (`"Test QA"`, `"0812..."`), tetapi begitu tombol kirim ditekan oleh skrip, pengiriman dibatalkan otomatis sebelum keluar ke server website.
- **Script & datanya di-copy-paste ke mana?**
  - File data uji JSON ([`test-data/blackbox-testdata.json`](./test-data/blackbox-testdata.json) & [`test-data/performance-profiles.json`](./test-data/performance-profiles.json)) dan skrip `.py` **sudah siap pakai di foldernya**, jadi **jangan di-copy isinya ke Terminal**.
  - Untuk menyiapkan alat bantu dan menjalankan tes, buka **Terminal / CMD / PowerShell** dari folder utama `tugas-qa-testing`, lalu **copy-paste perintah ini ke Terminal**:
    ```bash
    # Instal alat uji (cukup 1 kali di komputer baru)
    pip install playwright aiohttp python-docx pillow
    playwright install chromium

    # Jalankan tes fungsi & tes kecepatan
    python 03-hasil-pengujian/automation-scripts/test_gor_permata.py
    python 03-hasil-pengujian/automation-scripts/test_performance_gor_permata.py
    ```
  - Panduan lengkap pemula tersedia di [`panduan-uji-aman-dan-jalankan-script.md`](./panduan-uji-aman-dan-jalankan-script.md).

---

## 1. Spesifikasi Lingkungan Uji (`ED1 — Establish Test Environment`)

| Komponen Lingkungan Uji | Spesifikasi Terverifikasi | Peran dalam Pengujian |
| :--- | :--- | :--- |
| **Sistem Operasi Klien Uji** | `Windows-10-10.0.26300-SP0` (Windows 11/10 x64) | Host eksekusi skrip Python, browser headless, dan pengukuran metrik |
| **Runtime Python** | `Python 3.9.10` | Menjalankan suite otomasi Black Box & Performance |
| **Browser Automation** | `Playwright 1.60.0` (Chromium Headless) | Eksekusi UI Black Box, viewport Desktop (`1280×800`) & Mobile (`390×844`), tangkapan layar, & Web Vitals (`Navigation/Resource Timing`) |
| **Async HTTP Benchmark Engine** | `aiohttp 3.13.5` + `asyncio` | Menjalankan benchmark `GET`-only bertingkat (`1`, `5`, `10 VUs`) dengan kompresi `br`/`gzip` |
| **Runtime JS Tambahan** | `Node.js v24.14.0`, `npm 11.13.0` | Lingkungan pendukung untuk [`gor-permata.cy.js`](./automation-scripts/gor-permata.cy.js) *(catatan: biner `cypress` tidak terpasang lokal)* |
| **Guardrail Jaringan Non-Destruktif** | `page.route("**/bookings/store", ...)` & `GET`-only enforcement | Mencegah seluruh request tulis mencapai server produksi UMKM |
| **Target Lingkungan Operasional** | `https://gorpermatabadminton.com` di balik `Server: hcdn` (HTTPS aktif) | Sistem produksi UMKM yang diamati secara pasif & non-destruktif |

---

## 2. Test Environment Readiness Report (`8.3.4.2 b, c` & `8.3.5 b`)

- **Status Kesiapan Lingkungan:** **SIAP (`READY`)** untuk eksekusi Playwright Black Box dan Python `aiohttp` + Playwright Performance Testing.
- **Perbedaan Diketahui antara Lingkungan Uji dan Lingkungan Operasional (`8.3.4.2 c` — Wajib):**
  1. **Pemblokiran Endpoint Penulisan (`POST /bookings/store`):** Pada lingkungan operasional nyata, pengguna mengirimkan form hingga server memproses penyimpanan ke database dan mengembalikan tautan `wa_link`. Pada lingkungan uji, interceptor `page.route("**/bookings/store", route.abort())` memutus pengiriman di dalam browser sebelum menyentuh jaringan sehingga respons akhir `200 OK` server dan pembuatan order WhatsApp tidak dieksekusi (*Out of Scope*).
  2. **Peramban Headless & Jaringan Penguji:** Pengujian dijalankan melalui Chromium *headless* pada koneksi internet penguji (bukan variasi seluruh perangkat ponsel pelanggan di area Panongan), sehingga metrik `TTFB`, `FCP`, dan `LCP` mencerminkan kondisi rute jaringan dari lokasi penguji ke `Server: hcdn`.
  3. **Batas Beban Uji Performa:** Uji beban konkuren dibatasi `1–10 VUs` (`GET`-only + jeda `500 ms`), bukan lonjakan trafik ekstrem seperti uji *stress* lingkungan *staging* terisolasi.
  4. **Ketersediaan Cypress Runner:** Biner paket `cypress` belum terpasang di `node_modules` lokal; seluruh eksekusi E2E aktual dijalankan melalui **Playwright Python** (`test_gor_permata.py`), sementara [`gor-permata.cy.js`](./automation-scripts/gor-permata.cy.js) disinkronkan sebagai referensi skrip Cypress.

---

## 3. Kebutuhan Data Uji & Test Data Readiness Report (`ED2` — `8.3.4.3` & `8.3.5 e`)

### 3.1 Struktur & Sumber Data Uji
1. **Dataset Black Box ([`test-data/blackbox-testdata.json`](./test-data/blackbox-testdata.json)):**
   - Daftar rute publik (`/` s.d. `/fasilitas/parkir` dan `/register`), variasi parameter `?start_date=` (`tomorrow` dinamis, `2020-01-01`, `invalid-date`), variasi opsi durasi `1..5`, variasi nama (`""`, `"   "`, `"A"`, `"Test QA"`), batas digit WA (`10`, `11`, `14`, `15` digit & prefiks `8...`, `628...`, `+62 08...`), slot jam `22:00`, data negatif `/login`, serta konfigurasi viewport.
2. **Dataset Profil Performa ([`test-data/performance-profiles.json`](./test-data/performance-profiles.json)):**
   - Konfigurasi 4 rute uji, 3 level beban (`1 VU`, `5 VUs`, `10 VUs`), konfigurasi *circuit breaker* (`max_error_rate_pct = 5.0`), dan ambang batas SLA (`ms`).

### 3.2 Status Kesiapan Data Uji (*Test Data Readiness*)
- **Status Kesiapan Data:** **SIAP (`READY`)**.
- **Validasi Keamanan Data:** `100%` data uji bersifat **sintetik dan bebas informasi pribadi nyata (non-PII)**; tanggal slot booking dihitung secara dinamis relatif terhadap tanggal eksekusi (`date.today() + timedelta(days=1)`) agar tetap valid kapan pun skrip dijalankan ulang.

---

## 4. Pemeliharaan Lingkungan & Data Uji (`ED3` & `ED4`)
- Jika struktur DOM `/booking` atau jam operasional berubah pada pembaruan portal UMKM, dataset JSON pada `test-data/` diperbarui terlebih dahulu sebelum menjalankan ulang skrip (`ED3`/`ED4`).
- Seluruh bukti keluaran sementara disimpan terpisah di `evidence/` dan `automation-scripts/` agar data input di `test-data/` tetap bersih dan *reusable* untuk pengujian regresi.
