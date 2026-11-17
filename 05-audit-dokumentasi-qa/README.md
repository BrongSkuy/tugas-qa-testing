# Audit Dokumentasi QA (`05-audit-dokumentasi-qa/`)

Folder ini berisi rencana implementasi audit, skrip verifikasi otomatis, dan laporan hasil audit menyeluruh terhadap seluruh dokumentasi, desain uji, bukti eksekusi, serta laporan Word/PDF pada repositori `tugas-qa-testing`.

---

## Daftar Berkas

| Berkas | Fungsi |
| :--- | :--- |
| [`implementation-plan-audit.md`](./implementation-plan-audit.md) | Rencana implementasi audit dokumentasi (`AUD-01` s.d. `AUD-06`), kriteria kelulusan, dan tahapan remediasi. |
| [`audit_dokumentasi.py`](./audit_dokumentasi.py) | Skrip Python otomatis untuk mengaudit kelengkapan artefak ISO 29119-2:2021, *bidirectional traceability*, akurasi angka & keamanan non-PII, integritas tautan Markdown, ketentuan Poin 1–7, serta sinkronisasi Word/PDF & `README.md`. |
| [`audit-results.json`](./audit-results.json) | Luaran terstruktur hasil eksekusi audit otomatis terbaru. |
| [`laporan-audit-dokumentasi.md`](./laporan-audit-dokumentasi.md) | Laporan resmi hasil audit dokumentasi, temuan awal, tindakan remediasi, catatan ketergantungan eksternal, dan keputusan kelayakan akhir. |

## Menjalankan Audit Ulang Secara Lokal

```bash
python 05-audit-dokumentasi-qa/audit_dokumentasi.py
```
