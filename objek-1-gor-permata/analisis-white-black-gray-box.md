# Analisis White Box, Black Box, dan Gray Box: GOR Permata Badminton Hall

Analisis disusun langsung dari pengamatan halaman publik `https://gorpermatabadminton.com/booking` dan `/login` (diverifikasi 14 November 2026).

---

## 1. White Box Testing & Perhitungan Cyclomatic Complexity ($V(G)$)

Pada `/booking`, terdapat skrip JavaScript klien terbuka sepanjang `7.456` karakter yang mengatur interaksi pemesanan. Berikut analisis alur logika pada fungsi inti `normPhone()` dan `submitBooking()`:

### A. Fungsi `normPhone(p)`
```javascript
const normPhone = (p) => {
    let d = String(p).replace(/\D+/g, '');
    if (d.startsWith('62')) return d;
    if (d.startsWith('0'))  return '62' + d.slice(1);
    if (d.startsWith('8'))  return '62' + d;
    return d;
};
```
- **Jumlah keputusan predikat ($P$):** 3 buah pernyataan `if` (`startsWith('62')`, `startsWith('0')`, `startsWith('8')`).
- **Cyclomatic Complexity:** $V(G) = P + 1 = 3 + 1 = 4$.
- **4 Basis Path Minimal:**
  1. Path 1: Input berawalan `62` (mis. `628123456789`) -> langsung dikembalikan.
  2. Path 2: Input berawalan `0` (mis. `08123456789`) -> dikonversi menjadi `628123456789`.
  3. Path 3: Input berawalan `8` (mis. `8123456789`) -> diawali `62` menjadi `628123456789`.
  4. Path 4: Input tidak diawali `62`, `0`, atau `8` (mis. `12345` atau `+62 0812...` yang menjadi `620812...`) -> dikembalikan apa adanya.
- **Temuan Logika (*White Box Defect*):** Jika pengguna mengetik `+62 08123456789`, fungsi menghapus non-digit menjadi `6208123456789`, memenuhi branch pertama `startsWith('62')`, lalu gagal di regex `/^628\d{8,11}$/` tanpa koreksi `620` -> `62`.

### B. Fungsi `submitBooking()`
Struktur cabang keputusan teramati pada `submitBooking()`:
1. `if (!name || !phone)` — mengecek input wajib kosong (*2 kondisi atomik:* `!name`, `!phone`).
2. `if (!/^628\d{8,11}$/.test(phoneNorm))` — validasi format dan panjang nomor WA Indonesia (`628` + 8 s.d. 11 digit = total 11–14 digit).
3. `if (startHour + duration > 24)` — validasi batas jam tutup operasional `00:00`.
4. `.then(...) if (res.ok && data.success)` — percabangan keberhasilan API (*2 kondisi atomik:* `res.ok`, `data.success`).
5. `if (data.wa_link)` — percabangan redirect ke WhatsApp vs reload halaman.
6. `.catch(...)` — jalur penanganan kegagalan jaringan.

- **Kompleksitas Siklomatik ($V(G)$):**
  - Menghitung blok keputusan utama (*5 percabangan `if` + 1 jalur `catch` jaringan*): $V(G) = 6 + 1 = 7$ jalur independen.
  - Jika kondisi majemuk (`!name || !phone` dan `res.ok && data.success`) dipecah menjadi predikat atomik (7 kondisi + 1 catch): $V(G) = 8 + 1 = 9$ jalur uji basis kondisi.
- **Jalur Uji Non-Destruktif yang Aman Dijalankan Berulang (Path 1–4):**
  - Path A: `name == ""` atau `phone == ""` -> `alert('⚠️Halo kak! Nama dan Nomor WA harus diisi lengkap!')` (berhenti sebelum `fetch`).
  - Path B: `name != ""` dan `phone` tidak lolos `/^628\d{8,11}$/` -> `alert('⚠️ Nomor WA belum benar...')` (berhenti sebelum `fetch`).
  - Path C: `name != ""`, `phone` valid, dan `startHour + duration > 24` -> `alert('🚨 GAGAL! GOR Permata tutup jam 00:00...')` (berhenti sebelum `fetch`).

---

## 2. Black Box Testing

### A. Equivalence Partitioning (EP) & Boundary Value Analysis (BVA)

| Parameter / Field | Partisi Valid | Partisi Tidak Valid | Nilai Batas (*BVA*) |
| :--- | :--- | :--- | :--- |
| **Nama Pemesan (`#custName`)** | String non-kosong (mis. `"Faiz"`) | String kosong `""` | Panjang `0` (ditolak) vs `1` karakter (diterima oleh JS; *catatan:* belum ada batas minimal panjang nama / filter karakter khusus) |
| **Nomor WhatsApp (`#custPhone`)** | `08xxxxxxxxxx`, `628xxxxxxxxxx`, `8xxxxxxxxxx` (setara `628` + 8–11 digit = 11–14 digit) | Kosong, huruf `"abc"`, nomor di bawah 11 digit, atau di atas 14 digit | **7 digit setelah `628`** (`081234567` -> ditolak), **8 digit setelah `628`** (`0812345678` -> valid), **11 digit setelah `628`** (`0812345678901` -> valid), **12 digit setelah `628`** (`08123456789012` -> ditolak) |
| **Durasi Main (`#custDuration`)** | Bilangan bulat positif di mana `startHour + duration <= 24` | Nilai di mana `startHour + duration > 24` | Slot jam `22:00`: durasi `2` jam (`24 <= 24` -> valid, total `Rp 80.000`) vs durasi `3` jam (`25 > 24` -> ditolak alert jam tutup) |
| **Parameter URL `start_date`** | Format `YYYY-MM-DD` valid (mis. `2026-11-14`) | Format salah / tanggal non-valid | Perubahan tanggal lewat `#jumpDate` memicu `changeDate(date)` |

### B. State Transition Testing (Status Slot di Grid `/booking`)
- `Kosong (tombol +)` -> klik slot -> `Modal Booking Terbuka` (`openBooking`)
- `Modal Booking Terbuka` -> klik Batal/Tutup (`closeModal`) -> `Modal Tertutup & Input Ter-reset`
- `Modal Booking Terbuka` -> input invalid -> `Alert Validasi Klien (Tetap di Modal)`
- `Modal Booking Terbuka` -> submit valid *(dibatasi di environment nyata)* -> `Status Slot: Menunggu` -> Admin konfirmasi -> `Status Slot: Terisi` / `Member`

### C. Use Case Testing
- **UC-01:** Pengunjung membuka beranda -> klik menu Booking -> memilih tanggal -> melihat tarif lapangan (`Rp 40.000`/jam -> `Rp 80.000`/2 jam -> dst.) -> membatalkan modal.
- **UC-02:** Pengunjung mencari halaman pendaftaran (`/register`) -> sistem gagal menemukan halaman (`404`).

---

## 3. Gray Box Testing
- **Struktur Token & Request Header:** Halaman `/booking` menyisipkan variabel global `const CSRF = '...'` di JS inline dan mengirimkannya pada header `X-CSRF-TOKEN` saat memanggil `https://gorpermatabadminton.com/bookings/store`.
- **Inspeksi Data Slot DOM:** Fungsi `manageBooking(el)` membaca atribut `data-status`, `data-name`, `data-phone`, `data-date`, `data-court`, `data-start`, `data-end`, `data-duration`, `data-price` langsung dari DOM, dan memiliki *flag* sisi klien `const isAdmin = false; const isGuard = false;`.
- **Risiko Privasi/Informasi Teramati:** Pesan hardcoded `Hubungi Koko atau Aan.` serta logika cabang admin/guard tercantum langsung pada skrip publik halaman `/booking` meskipun otorisasi dieksekusi di sisi server.

