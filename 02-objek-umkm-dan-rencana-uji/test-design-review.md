# Test Design Review — Black Box Testing

**Objek:** Portal Booking GOR Permata Badminton Hall  
**Reviewer:** Dzikri Attariq Samayaki (@meongasli) — Test Design  
**Status:** Draf usulan untuk review tim; belum dieksekusi.

## 1. Tujuan dan ruang lingkup

Meninjau kesesuaian antara test model (TD1–TD2) dan test case (TD3–TD4), mengidentifikasi celah cakupan eksplisit, serta mengusulkan perbaikan tanpa mengubah hasil pengujian sebelumnya.

Acuan internal: [Test Model](test-model-blackbox.md), khususnya bagian 1, 2 dan 3; [Test Case](../03-hasil-pengujian/test-case-blackbox.md), khususnya bagian 1–3. Review terbatas pada kedua dokumen tersebut; kode otomasi, test data, log, dan kebutuhan pemilik sistem belum diperiksa.

## 2. Hasil review

Seluruh 23 TCI pada model memiliki pasangan TC pada spesifikasi. Namun, pemetaan 23/23 tidak membuktikan bahwa seluruh kombinasi kondisi atau transisi telah diuji, maupun bahwa seluruh pengujian telah lulus.

| ID | Acuan | Temuan | Rekomendasi | Prioritas usulan |
|---|---|---|---|---|
| REV-01 | TM-BB-02 R1; TC-BB-08 | Nama dan WA diuji kosong bersamaan; nama kosong dengan WA valid tidak eksplisit. | Tambahkan TC-BB-24. | Tinggi |
| REV-02 | TM-BB-02 R2; TC-BB-08 | R2 (nama terisi, WA kosong) belum memiliki kasus eksplisit. | Tambahkan TC-BB-25. | Tinggi |
| REV-03 | TB-BB-02; TC-BB-05 | Format rusak diuji, tetapi tanggal kalender mustahil dengan format YYYY-MM-DD belum eksplisit. | Tambahkan TC-BB-26. | Tinggi |
| REV-04 | TM-BB-01; TC-BB-17/18 | Batas tutup diuji dari 22.00 dengan durasi 2 dan 3 jam; variasi mulai 23.00 belum eksplisit. | Tambahkan TC-BB-27/28 jika slot tersedia. Ini perluasan variasi, bukan bukti bahwa batas awal tidak diuji. | Sedang |
| REV-05 | TB-BB-04; TC-BB-07 | Durasi diuji naik 1–5; perubahan 5 kembali ke 1 belum eksplisit. | Tambahkan TC-BB-29. | Sedang |
| REV-06 | TM-BB-03; TC-BB-08/10/12 | Transisi ValidationAlert ke ModalOpen telah dimodelkan; pemulihan setelah input diperbaiki belum eksplisit sebagai satu alur. | Tambahkan TC-BB-30. | Tinggi |
| REV-07 | TB-BB-07; TC-BB-21 | Hanya viewport 390×844 dan 1280×800. | Tambahkan TC-BB-31 untuk viewport 360×800. | Sedang |
| REV-08 | TM-BB-03; TC-BB-19 | Reset saat modal ditutup sudah diuji; pembukaan ulang belum eksplisit. | Tambahkan TC-BB-32. | Sedang |
| REV-09 | TB-BB-05; TM-BB-01; TC-BB-09 | Penolakan nama satu karakter belum didukung batas minimal yang eksplisit pada test basis. | Pisahkan nama spasi dan nama satu karakter; konfirmasi aturan minimum kepada pemilik sistem sebelum menetapkan verdict untuk nama satu karakter. | Sedang |
| REV-10 | TC-BB-17; bagian 1 dan PROC-BB-03 | Prasyarat TC-BB-17 tidak menyebut interceptor secara eksplisit, walaupun kebijakan umum dan prosedur sudah mengharuskannya. | Tegaskan interceptor wajib sebelum setiap submit, termasuk input yang diperkirakan ditolak. | Tinggi |

## 3. Rekomendasi tindak lanjut

Rancangan tambahan tersedia pada [Additional Black Box Test Cases](../03-hasil-pengujian/test-case-additional.md). ID dan prioritas merupakan usulan; tim perlu memastikan tidak terjadi benturan dengan perubahan terbaru. Tester memeriksa script dan data uji untuk menghindari duplikasi, mengonfirmasi kebutuhan yang belum jelas, lalu menjalankan kasus hanya pada lingkungan yang diizinkan dengan pemblokiran request transaksi yang telah diverifikasi.

## 4. Kesimpulan

Pemetaan awal sudah terstruktur. Review ini mengusulkan perluasan cakupan kondisi input, pemulihan state, variasi batas waktu, kalkulasi dan kompatibilitas. Temuan review bukan temuan defect baru. Tidak ada perubahan pada hasil Pass/Fail awal atau klaim eksekusi tambahan.
