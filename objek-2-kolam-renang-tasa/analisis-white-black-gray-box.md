# Analisis White Box, Black Box, dan Gray Box: Kolam Renang TASA

Seluruh hasil analisis bersumber langsung dari inspeksi DOM, header HTTP, RSC payload, serta chunk JavaScript publik `https://www.kolamtasa.com/` (diobservasi 14 November 2026).

---

## 1. Black Box Testing

### A. Equivalence Partitioning (EP) & Boundary Value Analysis (BVA)

| Modul / Field | Partisi Valid | Partisi Tidak Valid | Nilai Batas (*BVA*) |
| :--- | :--- | :--- | :--- |
| **Wizard `/lesrenang` Step `nama` & `panggilan`** | Teks non-kosong setelah `.trim()` | Kosong `""` atau spasi saja `"   "` | Panjang `0` (error `"Nama muridnya belum diisi."`) vs `1` karakter non-spasi (diterima) |
| **Wizard `/lesrenang` Step `lahir` & `kelas` (Usia)** | Tanggal lahir menghasilkan usia `U >= 1` tahun (`1–3`: *Rumbul Club*, `4–10`: *Kids Swimming*, `>10`: hanya *Privat*) | Kosong `""`, atau `U < 1` tahun | • `U = 0` (`< 1` th): ditolak pada step `lahir` (*"mulai usia 1 tahun"*)<br>• `U = 1..3`: lolos ke *Rumbul Club*<br>• `U = 4..10`: lolos ke *Kids Swimming*<br>• `U = 11`: lolos step `lahir`, lalu ditolak jika memilih *Kids Swimming/Rumbul Club* di step `kelas` |
| **Wizard `/lesrenang` Step `whatsapp`** | Nomor WA aktif (`08...`) | *(Celah ditemukan)* Hanya menolak kosong `""` — huruf `"abc"` ikut lolos! | Panjang `0` (ditolak) vs `"a"` (diterima oleh JS karena hanya cek `.trim()`) |
| **Wizard `/lesrenang` Step `email`** | Sesuai regex `/^[^@\s]+@[^@\s]+\.[^@\s]+$/` | Kosong `""`, tanpa `@`, tanpa domain/titik (mis. `"faiz@gmail"`) | `"a@b.c"` (valid minimal) vs `"a@b"` (error *"Format emailnya belum benar."*) |
| **Pagination `/blog/halaman/{n}`** | `n = 1` (`/blog`), `2`, `3`, `4` (`HTTP 200`) | `n <= 0` atau `n >= 5` (`HTTP 404`) | Batas bawah: `0` (`404`) vs `1` (`200`); Batas atas: `4` (`200`) vs `5` (`404`) |
| **Form `/kontak`** | Seluruh field `required` terisi | Field wajib kosong (ditahan validasi HTML5 browser) | Saat semua valid -> **bug sistem**: form melakukan submit GET tanpa mengirim pesan |

### B. State Transition Testing (Wizard `/lesrenang`)
- **State Awal (`Step 1 / 20`)** -> klik `Lanjut` dengan input kosong -> **Tetap di `Step 1 / 20` + pesan error tampil**.
- **State `Step 1 / 20` (`nama` terisi)** -> klik `Lanjut` -> **Berpindah ke `Step 2 / 20` (`panggilan`)**.
- **State `Step 6` (`motivasi`)**:
  - Jika pilih selain `"Lain-lain"` -> total langkah tetap **`20`** (`Step 7 = kesehatan`).
  - Jika pilih `"Lain-lain"` -> array langkah bertambah secara dinamis menjadi **`21`** (`Step 7 = motivasi_lain`).

### C. Use Case Testing
- **UC-01:** Calon orang tua murid mengisi pendaftaran les renang langkah demi langkah hingga penentuan kelas sesuai usia anak.
- **UC-02:** Pengunjung membuka menu `/kontak` untuk mengirim pertanyaan via form web (berujung defect karena form tidak memiliki backend handler).
- **UC-03:** Pengunjung membaca artikel di `/blog`, memfilter kategori, dan berpindah halaman.

---

## 2. White Box Testing (Analisis Struktur Keputusan Client-Side)

Berbeda dengan portal JS polos yang tidak ter-*minify*, `kolamtasa.com` memakai *production build* Next.js yang ter-*minify* (`/_next/static/chunks/app/(site)/lesrenang/page-68955bdddde0c5b0.js`). Namun, struktur logika aturan validasi (`sah`) dan alur fungsi `E()` pada wizard `/lesrenang` dapat dianalisis sebagai berikut:

### A. Analisis Alur Fungsi Submit/Next Wizard (`E()`)
1. `let n = z.sah?.() ?? null` -> evaluasi fungsi validasi step aktif.
2. `if (n) return void C(n)` -> *Path 1:* tampilkan pesan error dan hentikan perpindahan step.
3. `if (!K) return void A(a => a + 1)` -> *Path 2:* bila bukan step terakhir (`M < F - 1`), naikkan indeks step `M + 1`.
4. `else` (`K === true`) -> *Path 3:* susun `FormData`, pasang `__program = "les-renang"`, `__ph_distinct_id` (opsional `if (l.distinctId)`), `__ph_session_id` (opsional `if (l.sessionId)`), `__event_id`, dan panggil `startTransition(() => w(t))`.
- **Kompleksitas Siklomatik Inti Navigasi `E()`:** Terdapat 4 cabang keputusan utama (`z.sah`, `if (n)`, `if (!K)`, plus guard `distinctId`/`sessionId` & `try/catch crypto`) -> minimal **5 jalur independen** untuk alur perpindahan wizard.

### B. Analisis Fungsi Validasi `kelas.sah` & Percabangan Array `W`
- **Kondisi Percabangan Array `W`:** `..."Lain-lain" === N.motivasi ? [{kunci:"motivasi_lain",...}] : []` (2 cabang panjang wizard: `20` vs `21`).
- **Kondisi Validasi `kelas.sah`:**
  1. `if (!N.kelas)` -> error `"Pilih dulu programnya."`
  2. `a && "privat" !== a.kode && null !== U && null !== a.usiaMin && null !== a.usiaMaks && (U < a.usiaMin || U > a.usiaMaks)` -> tolak jika usia anak di luar rentang program reguler, arahkan ke program lain atau kelas privat.
- **Perbandingan Kondisi vs `whatsapp.sah`:** Pemeriksaan `whatsapp.sah` hanya berisi `(N.whatsapp?.trim()) ? null : "Nomor WhatsApp belum diisi."` — tidak ada validasi pola regex sebagaimana yang ada pada `email.sah` (`/^[^@\s]+@[^@\s]+\.[^@\s]+$/`).

---

## 3. Gray Box Testing
- **Inspeksi HTTP Headers (`/`):**
  - *Ada:* `Strict-Transport-Security: max-age=63072000`, `Server: Vercel`, `X-Powered-By: Next.js` *(membeberkan stack framework)*.
  - *Hilang:* `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`.
- **Inspeksi RSC Payload `/kontak` vs `/event`:**
  - `/event` memuat referensi *Next.js Server Action* (`createServerReference`) di bundel JS-nya.
  - `/kontak` memiliki `$ACTION` = `[]` (kosong), `<form>` tanpa `action`/`method`, dan string `"Kirim pesan"` tidak ada dalam JS client bundle mana pun — membuktikan secara teknis bahwa form `/kontak` bersifat statis tanpa logika kirim.
- **Inspeksi `robots.txt`:** Mengungkap daftar path internal pada blok `Disallow:` (`/club/`, `/auth/`, `/setoran/`, `/lapangan/`, `/internal/`, `/tagihan/`, `/dapur/`, `/api/`, `/loket/`, `/air/`).

