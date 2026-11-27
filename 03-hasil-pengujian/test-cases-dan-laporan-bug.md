# Indeks Hasil Pengujian, Test Cases, & Laporan Bug — GOR Permata Badminton Hall

Dokumen ini menjadi ringkasan indeks untuk folder `03-hasil-pengujian/` agar kompatibel dengan tautan lama sekaligus mengarahkan ke seluruh artefak resmi sesuai standar **`>= 2022`** (**ISO/IEC/IEEE 29119-1:2022**, **29119-5:2024**, & **ISTQB CTFL v4.0.1 2024**).

---

## 0. Ringkasan Dokumen & Cara Pakai Script

- **Dokumen ini isinya apa?** Ini adalah **"Peta Indeks Cepat Folder Hasil Pengujian (`03-hasil-pengujian/`)"** yang merangkum daftar seluruh dokumen uji dari Tahap 1 sampai Tahap 7 serta ringkasan hasil akhir (**Black Box:** `16/23 Pass, 7 Fail`; **Performance:** `7/10 Pass, 3 Fail`) dan `10` bug yang ditemukan (`IR-GOR-01` s.d. `IR-GOR-10`).
- **Panduan pemula & cara menjalankan script di Terminal:** Baca [`panduan-uji-aman-dan-jalankan-script.md`](./panduan-uji-aman-dan-jalankan-script.md) untuk penjelasan bahasa sehari-hari serta perintah siap copy-paste ke **Terminal / CMD / PowerShell** (`python 03-hasil-pengujian/automation-scripts/test_gor_permata.py`, `test_performance_gor_permata.py`, dan `generate_laporan_pengujian.py`).

---

## 1. Peta Artefak Pengujian (`Flow Testing STLC — >= 2022`)

Seluruh artefak hasil uji disusun berurutan mengimplementasikan kerangka **Software Testing Life Cycle (STLC)** dan **Fundamental Test Process** (**ISO/IEC/IEEE 29119-1:2022**, **29119-5:2024**, **ISO/IEC 25010:2023**, dan **ISTQB CTFL v4.0.1**):

| No | Tahapan STLC | Dokumen / Berkas | Klausul ISO / Acuan Perkuliahan | Ringkasan Isi & Status Terverifikasi |
| :-: | :--- | :--- | :--- | :--- |
| 1 | **Requirements & Risk Analysis** | [`organizational-test-specification.md`](../01-standar-ieee-iso/organizational-test-specification.md) | `ISO 29119-1` (`OT1–OT3`) & Kuliah P1–P3 | Kebijakan uji non-destruktif, lingkup uji *In/Out of Scope*, dan kalkulasi *Risk Exposure* produk/proyek. |
| 2 | **Test Planning** | [`test-plan-gor-permata.md`](../02-objek-umkm-dan-rencana-uji/test-plan-gor-permata.md) & [`performance-test-plan.md`](../02-objek-umkm-dan-rencana-uji/performance-test-plan.md) | `ISO 29119-1` (`TP1–TP9`) & ISTQB §1.4.1 | Rencana uji utama, profil SLA *Core Web Vitals*, dan penurunan metode dari 9 jurnal SINTA 2–3 (`2022–2026`). |
| 3 | **Test Design** | [`test-case-blackbox.md`](./test-case-blackbox.md) & [`test-case-performance.md`](./test-case-performance.md) | `ISO 29119-1` (`TD1–TD4`) & Kuliah P6–P7 | `23` *Test Case* Black Box (EP, BVA, Decision Table, STT, Use Case) & `10` *Test Case* Performance (Web Vitals + 1/5/10 VUs) beserta matriks ketertelusuran penuh. |
| 4 | **Test Implementation & Environment** | [`test-environment-dan-data.md`](./test-environment-dan-data.md) & [`test-data/`](./test-data/) | `ISO 29119-1` (`ED1–ED4`) & `29119-5:2024` | Kesiapan runner (`Python Playwright`, `aiohttp`), dataset JSON fiktif terpisah, serta guardrail pencegat `POST` ke server DB produksi. |
| 5 | **Test Execution** | [`test-execution-log.md`](./test-execution-log.md), log TXT, & metrik JSON | `ISO 29119-1` (`TE1–TE3`) & Otomasi | Rekaman hasil eksekusi aktual: **Black Box `16/23 PASS` (`7` temuan defect, `0` POST terkirim)** & **Performance `7/10 PASS` (`3` temuan SLA/payload, `0%` error pada `104` request)**. |
| 6 | **Incident / Defect Reporting** | [`incident-reports.md`](./incident-reports.md) & [`evidence/screenshots/`](./evidence/screenshots/) | `ISO 29119-1` (`IR1–IR2`) & ISTQB §5.5 | `10` laporan insiden terstandar (`IR-GOR-01` s.d. `IR-GOR-10`), penentuan *Severity/Priority*, dan masking nama pemesan lain menjadi `[TERISI]`. |
| 7 | **Test Reporting & Completion** | [`test-status-and-control-report.md`](./test-status-and-control-report.md), [`test-completion-report.md`](./test-completion-report.md), [`evaluasi-iso-25010-gor-permata.md`](../01-standar-ieee-iso/evaluasi-iso-25010-gor-permata.md), & [`05-dokumentasi-laporan/`](../05-dokumentasi-laporan/) | `ISO 29119-1` (`TC1–TC4`) & `ISO 25010:2023` | Evaluasi 100% *Completion Criteria*, audit 9 dimensi mutu produk ISO 25010, pengarsipan Git, dan penerbitan **Laporan Resmi Word & PDF**. |

---

## 2. Ringkasan Cepat Temuan Utama (`IR-GOR-01` s.d. `IR-GOR-10`)

1. **`IR-GOR-01` (`BUG-GOR-01` — Major):** Endpoint `/register` mengembalikan `HTTP 404 Not Found`.
2. **`IR-GOR-02` (`BUG-GOR-02` — Minor):** `normPhone()` gagal menormalisasi awalan `+62 08...`.
3. **`IR-GOR-03` (`BUG-GOR-03` — Minor):** `#custName` meloloskan spasi `"   "` dan `1` huruf karena tidak ada `.trim()` & batas panjang minimum.
4. **`IR-GOR-04` (`BUG-GOR-04` — Major/High):** `205` elemen slot publik `/booking` menyematkan `data-phone` & `data-name` pelanggan di HTML publik serta skrip `manageBooking()` internal.
5. **`IR-GOR-05` (Major/High):** Query `?start_date=2020-01-01` (tanggal lampau) tetap merender `612` tombol booking aktif.
6. **`IR-GOR-06` (Major/High):** Query `?start_date=invalid-date` menyebabkan crash **`HTTP 500 Server Error`**.
7. **`IR-GOR-07` (Major/High — Performance):** Pada beban `10 VUs`, latensi `p95` `/booking` melonjak ke **`5314,28 ms`** (> batas SLA `3000 ms`).
8. **`IR-GOR-08` (Minor/Medium — Performance):** Ukuran HTML mentah `/booking` mencapai **`535,37 KB`** (`> 500 KB`).
9. **`IR-GOR-09` (Minor/Medium — Performance):** Spike *Cold-Start TTFB* `/` mencapai **`2618,3 ms`** (`FCP = 3028 ms`) sebelum turun ke `89,4 ms` saat *Warm Reload*.
10. **`IR-GOR-10` (Minor/Medium — Compatibility):** Navbar halaman `/` pada viewport mobile `390×844` memotong teks `LOGIN` dan mendorong tombol `BOOKING` keluar viewport (`right = 489 px`).

Rincian langkah reproduksi dan rekomendasi perbaikan masing-masing insiden tersedia pada [`incident-reports.md`](./incident-reports.md).
