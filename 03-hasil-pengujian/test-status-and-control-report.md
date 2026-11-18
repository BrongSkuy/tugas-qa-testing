# Test Status, Risk Updates & Control Directives Report (`TMC1`–`TMC4`)

Dokumen ini mengimplementasikan **Test Monitoring and Control Process (`7.3`, aktivitas `TMC1–TMC4`)** sesuai **ISO/IEC/IEEE 29119-2:2021(E)** dan mencakup keempat *Information Items* wajib pada **§7.3.5** (*Test Status Reports, Test Plan Updates, Control Directives,* serta *Project & Product Risk Information*) untuk periode pengujian **14–17 November 2026**.

---

## 1. *Test Status Report* (`7.3.5 a` — Periode 14–17 November 2026)

### 1.1 Metrik Cakupan & Hasil Eksekusi (`TMC1–TMC2`)
| Dimensi / Paket Uji | Target Cakupan (`TP-GOR-01`) | Realisasi Terukur | Progres |
| :--- | :--- | :--- | :---: |
| **Black Box Design (`TCI-BB`)** | `23` *Test Coverage Items* | `23 / 23 TCI-BB` diturunkan menjadi `TC-BB-01..23` | **100%** |
| **Black Box Execution (`TC-BB`)** | `23` *Test Cases* non-destruktif | **`23 / 23` dieksekusi** (`16 PASS`, `7 FAIL` konfirmasi defect, `0` console error) | **100%** |
| **Performance Design (`TCI-PERF`)** | `10` *Test Coverage Items* | `10 / 10 TCI-PERF` diturunkan menjadi `TC-PERF-01..10` | **100%** |
| **Performance Execution (`TC-PERF`)** | `10` *Test Cases* (`Web Vitals` + `1/5/10 VUs`) | **`10 / 10` dieksekusi** (`7 PASS`, `3 FAIL` pelanggaran SLA/payload, `0,0%` HTTP error pada `104` request) | **100%** |
| **Guardrail Non-Destruktif** | `0` request `POST /bookings/store` ke server | `7` percobaan `fetch` validasi dicegat lokal; **`network_posts_sent_to_server = 0`** | **100% Aman** |
| **Cypress Runner Lokal** | Referensi skrip E2E | Skrip `gor-permata.cy.js` disinkronkan; tidak dieksekusi lokal karena biner `cypress` absen (*lihat `ED1`*) | **Tailored / Alternatif Playwright** |

---

## 2. *Control Directives* yang Diterbitkan (`7.3.5 c` — `TMC3`)

Selama pemantauan eksekusi dinamis, Tim QA menerbitkan empat *control directives* untuk mengoreksi hambatan teknis dan memperluas deteksi cacat:

| ID Directive | Pemicu / Deviasi yang Teramati | Tindakan Kontrol yang Dilakukan | Dampak |
| :---: | :--- | :--- | :--- |
| **`CD-01`** | `aiohttp` gagal mendekode `Content-Encoding: br` karena pustaka `Brotli` tidak terpasang | Ubah header benchmark HTTP menjadi `Accept-Encoding: gzip, deflate` (didukung `zlib` bawaan Python), sambil tetap mencatat kompresi `br` lewat Playwright | Benchmark `1/5/10 VUs` berjalan sukses tanpa error (`0%` error) |
| **`CD-02`** | Tangkapan layar awal modal mobile (`08_booking_modal_mobile.png`) tertangkap saat transisi CSS fade masih berjalan & grid publik menampilkan nama | Tambahkan jeda `wait_for_timeout(350)` setelah modal tampil serta masker DOM `mask_grid_pii()` (`[TERISI]`) sebelum screenshot | Bukti visual jernih dan bebas 100% kebocoran PII pelanggan |
| **`CD-03`** | Inspeksi visual `07_home_mobile.png` mengungkap tombol navbar terpotong (`LOGI` / `BOOKING`) padahal `document.scrollWidth == 390` | Perluas asersi `TC-BB-21` pada `test_gor_permata.py` untuk memeriksa `getBoundingClientRect().right <= innerWidth` pada elemen `header a, nav a` | Mendeteksi `IR-GOR-10` secara otomatis (`right = 489 > 390`) |
| **`CD-04`** | Eksplorasi awal `?start_date=` menemukan crash `HTTP 500` pada format rusak & slot aktif pada tanggal `2020-01-01` | Tambahkan `TC-BB-04` dan `TC-BB-05` ke *Test Model*, *Test Case*, dan skrip otomasi | Mendokumentasikan `IR-GOR-05` dan `IR-GOR-06` beserta bukti screenshot |

---

## 3. *Test Plan Updates* (`7.3.5 b`)

Perubahan terhadap rencana awal (`TP-GOR-01 v1.0` tanggal 14 Nov 2026 -> `v2.0` tanggal 17 Nov 2026):
1. Penambahan dokumen **Organizational Test Specification** ([`organizational-test-specification.md`](../01-standar-ieee-iso/organizational-test-specification.md)) dan klaim *Tailored Conformance* sesuai Clause 4 & 6.
2. Pemisahan dan pendalaman **Performance Test Plan** ([`performance-test-plan.md`](../02-objek-umkm-dan-rencana-uji/performance-test-plan.md)) beserta model beban bertingkat (`1/5/10 VUs`).
3. Migrasi struktur desain uji dari *test conditions* menjadi **Test Model Specification (`TM-*`) -> Test Coverage Items (`TCI-*`) -> Test Cases (`TC-*`) -> Test Procedures (`PROC-*`)** sesuai revisi edisi 2021 `ISO/IEC/IEEE 29119-2`.

---

## 4. Pembaruan *Project & Product Risk Information* (`7.3.5 d`)

| ID Risiko | Status Awal (`TP3`) | Status Terkini Pasca-Eksekusi | Tindak Lanjut |
| :--- | :--- | :--- | :--- |
| **`PR-01`** (`normPhone`) | Exposure 9 (Tinggi) | **Terealisasi:** `IR-GOR-02` terkonfirmasi; batas `11–14` digit selain `+62 08...` lolos akurat | Dilaporkan pada `incident-reports.md` |
| **`PR-02`** (`start_date`) | Exposure 9 (Tinggi) | **Terealisasi Kritis:** Crash `HTTP 500` (`IR-GOR-06`) & `612` slot tanggal lampau aktif (`IR-GOR-05`) | Dilaporkan sebagai prioritas tinggi |
| **`PR-03`** (Payload & Latensi `/booking`) | Exposure 6 (Sedang-Tinggi) | **Terealisasi:** HTML `535,37 KB` (`IR-GOR-08`) dan `p95` `10 VUs = 5,31s` (`IR-GOR-07`) + spike `/` (`IR-GOR-09`) | Diangkat ke audit `ISO 25010` & `IR` |
| **`PR-04`** (`#custName` trim) | Exposure 6 (Sedang) | **Terealisasi:** Spasi `"   "` dan `"A"` lolos ke `fetch` (`IR-GOR-03`) | Dilaporkan pada `incident-reports.md` |
| **`PR-05`** (`/register` & DOM PII) | Exposure 6 (Sedang) | **Terealisasi Kritis:** `/register` `404` (`IR-GOR-01`) & `205` slot ekspos `data-phone` (`IR-GOR-04`) | Dilaporkan prioritas tinggi |
| **`PR-06`** (Tarif & Jam Tutup) | Exposure 3 | **Mitigasi Berhasil:** Tarif `1..5` jam & batas `22:00 + 2 vs 3 jam` seluruhnya **PASS** | Tidak ada insiden |
| **`PJ-01` & `PJ-02`** (Risiko Produksi UMKM) | Exposure 8 & 6 | **Terkendali Penuh:** `0` request `POST` terkirim ke server, `0%` error selama uji beban `1–10 VUs` | Guardrail dipertahankan |

---

## 5. Persetujuan Kesiapan Penutupan Uji (`7.3.4.4 g, h`)
Seluruh *Exit Criteria* pada [`test-plan-gor-permata.md`](../02-objek-umkm-dan-rencana-uji/test-plan-gor-permata.md#43-kriteria-masuk-penyelesaian-penangguhan--kelanjutan-7246-a-note-2) telah terpenuhi (`100%` TCI Black Box & Performance dieksekusi, `0` kebocoran POST produksi, seluruh insiden & bukti terekam). Keputusan untuk memasuki proses **Test Completion (`7.4`)** **DISETUJUI** pada `17 November 2026`.
