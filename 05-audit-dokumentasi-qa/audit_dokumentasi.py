"""
Automated QA Documentation Audit Script (AUD-01 s.d. AUD-06)
Mengaudit kelengkapan ISO/IEC/IEEE 29119-2:2021, traceability ID, konsistensi angka
empiris, keamanan non-PII, integritas tautan Markdown, ketentuan Poin 1-7, serta
sinkronisasi laporan Word/PDF dan README.md pada repositori tugas-qa-testing.

Penggunaan:
    python 05-audit-dokumentasi-qa/audit_dokumentasi.py
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

AUDIT_DIR = Path(__file__).resolve().parent
REPO_ROOT = AUDIT_DIR.parent
OUT_JSON = AUDIT_DIR / "audit-results.json"


def check_iso_artifacts() -> dict[str, Any]:
    """AUD-01: Cek keberadaan seluruh Information Items wajib ISO/IEC/IEEE 29119-2:2021."""
    required_files = [
        "01-standar-ieee-iso/organizational-test-specification.md",
        "01-standar-ieee-iso/standar-dokumentasi-qa.md",
        "01-standar-ieee-iso/evaluasi-iso-25010-gor-permata.md",
        "01-standar-ieee-iso/pdf-standar/10.1109@IEEESTD.2021.9591508.pdf",
        "02-objek-umkm-dan-rencana-uji/test-plan-gor-permata.md",
        "02-objek-umkm-dan-rencana-uji/performance-test-plan.md",
        "02-objek-umkm-dan-rencana-uji/test-model-blackbox.md",
        "02-objek-umkm-dan-rencana-uji/test-model-performance.md",
        "02-objek-umkm-dan-rencana-uji/analisis-white-black-gray-box.md",
        "02-objek-umkm-dan-rencana-uji/referensi-sinta-1-3.md",
        "03-hasil-pengujian/test-environment-dan-data.md",
        "03-hasil-pengujian/test-case-blackbox.md",
        "03-hasil-pengujian/test-case-performance.md",
        "03-hasil-pengujian/test-execution-log.md",
        "03-hasil-pengujian/incident-reports.md",
        "03-hasil-pengujian/test-status-and-control-report.md",
        "03-hasil-pengujian/test-completion-report.md",
        "03-hasil-pengujian/test-data/blackbox-testdata.json",
        "03-hasil-pengujian/test-data/performance-profiles.json",
        "03-hasil-pengujian/evidence/blackbox-results.json",
        "03-hasil-pengujian/evidence/performance-metrics.json",
        "03-hasil-pengujian/evidence/performance-summary.md",
        "03-hasil-pengujian/automation-scripts/test_gor_permata.py",
        "03-hasil-pengujian/automation-scripts/test_performance_gor_permata.py",
        "03-hasil-pengujian/automation-scripts/gor-permata.cy.js",
        "03-hasil-pengujian/automation-scripts/execution-log.txt",
        "03-hasil-pengujian/automation-scripts/performance-log.txt",
    ]
    missing = [rel for rel in required_files if not (REPO_ROOT / rel).exists()]
    return {
        "id": "AUD-01",
        "name": "Kelengkapan Information Items ISO/IEC/IEEE 29119-2:2021",
        "status": "PASS" if not missing else "FAIL",
        "checked_count": len(required_files),
        "missing": missing,
    }


def check_traceability() -> dict[str, Any]:
    """AUD-02: Cek keterhubungan dua arah TCI -> TC -> Log/JSON & Incident IDs."""
    bb_model = (REPO_ROOT / "02-objek-umkm-dan-rencana-uji/test-model-blackbox.md").read_text(encoding="utf-8")
    bb_spec = (REPO_ROOT / "03-hasil-pengujian/test-case-blackbox.md").read_text(encoding="utf-8")
    perf_model = (REPO_ROOT / "02-objek-umkm-dan-rencana-uji/test-model-performance.md").read_text(encoding="utf-8")
    perf_spec = (REPO_ROOT / "03-hasil-pengujian/test-case-performance.md").read_text(encoding="utf-8")
    exec_log = (REPO_ROOT / "03-hasil-pengujian/test-execution-log.md").read_text(encoding="utf-8")
    ir_doc = (REPO_ROOT / "03-hasil-pengujian/incident-reports.md").read_text(encoding="utf-8")

    bb_json = json.loads((REPO_ROOT / "03-hasil-pengujian/evidence/blackbox-results.json").read_text(encoding="utf-8"))
    perf_json = json.loads((REPO_ROOT / "03-hasil-pengujian/evidence/performance-metrics.json").read_text(encoding="utf-8"))

    missing_items: list[str] = []

    for i in range(1, 23):
        tci = f"TCI-BB-{i:02d}"
        tc = f"TC-BB-{i:02d}"
        if tci not in bb_model:
            missing_items.append(f"{tci} missing in test-model-blackbox.md")
        if tci not in bb_spec:
            missing_items.append(f"{tci} missing in test-case-blackbox.md")
        if tc not in bb_spec:
            missing_items.append(f"{tc} missing in test-case-blackbox.md")
        if tc not in exec_log:
            missing_items.append(f"{tc} missing in test-execution-log.md")

    bb_json_ids = {c["tc_id"] for c in bb_json["cases"]}
    for i in range(1, 23):
        tc = f"TC-BB-{i:02d}"
        if tc not in bb_json_ids:
            missing_items.append(f"{tc} missing in blackbox-results.json")

    for i in range(1, 11):
        tci = f"TCI-PERF-{i:02d}"
        tc = f"TC-PERF-{i:02d}"
        if tci not in perf_model:
            missing_items.append(f"{tci} missing in test-model-performance.md")
        if tci not in perf_spec:
            missing_items.append(f"{tci} missing in test-case-performance.md")
        if tc not in perf_spec:
            missing_items.append(f"{tc} missing in test-case-performance.md")
        if tc not in exec_log:
            missing_items.append(f"{tc} missing in test-execution-log.md")

    perf_json_ids = {c["tc_id"] for c in perf_json["test_cases"]}
    for i in range(1, 11):
        tc = f"TC-PERF-{i:02d}"
        if tc not in perf_json_ids:
            missing_items.append(f"{tc} missing in performance-metrics.json")

    for i in range(1, 11):
        ir = f"IR-GOR-{i:02d}"
        if ir not in ir_doc:
            missing_items.append(f"{ir} missing in incident-reports.md")

    return {
        "id": "AUD-02",
        "name": "Bidirectional Traceability (22 TCI/TC Black Box, 10 TCI/TC Performance, 10 IR)",
        "status": "PASS" if not missing_items else "FAIL",
        "missing_mappings": missing_items,
    }


def check_empirical_and_privacy() -> dict[str, Any]:
    """AUD-03: Cek konsistensi hasil empiris, guardrail POST=0, dan zero kebocoran PII."""
    bb_json = json.loads((REPO_ROOT / "03-hasil-pengujian/evidence/blackbox-results.json").read_text(encoding="utf-8"))
    perf_json = json.loads((REPO_ROOT / "03-hasil-pengujian/evidence/performance-metrics.json").read_text(encoding="utf-8"))
    exec_log_md = (REPO_ROOT / "03-hasil-pengujian/test-execution-log.md").read_text(encoding="utf-8")
    comp_md = (REPO_ROOT / "03-hasil-pengujian/test-completion-report.md").read_text(encoding="utf-8")

    issues: list[str] = []

    if bb_json.get("network_posts_sent_to_server") != 0:
        issues.append(f"network_posts_sent_to_server != 0 ({bb_json.get('network_posts_sent_to_server')})")
    if bb_json.get("total_cases") != 22 or bb_json.get("passed") != 15 or bb_json.get("failed_or_defect_repro") != 7:
        issues.append("Mismatch pada ringkasan hitungan Black Box JSON")

    perf_pass = sum(1 for c in perf_json["test_cases"] if c["status"] == "PASS")
    perf_fail = sum(1 for c in perf_json["test_cases"] if c["status"] == "FAIL")
    if len(perf_json["test_cases"]) != 10 or perf_pass != 7 or perf_fail != 3:
        issues.append("Mismatch pada ringkasan hitungan Performance JSON")

    for expected_snippet in ("15 / 22 PASS", "7 / 10 PASS", "network_posts_sent_to_server = 0"):
        if expected_snippet not in exec_log_md:
            issues.append(f"'{expected_snippet}' tidak ditemukan di test-execution-log.md")

    if "22/22" not in comp_md or "10/10" not in comp_md:
        issues.append("Ringkasan cakupan 22/22 & 10/10 tidak lengkap di test-completion-report.md")

    # Scan seluruh berkas teks hasil uji untuk memastikan tidak ada nomor telepon asli (>10 digit selain data sintetik uji)
    allowed_synthetic = {
        "081234567",
        "0812345678",
        "08123456789",
        "081234567890",
        "0812345678901",
        "08123456789012",
        "628123456789",
        "6281234567890",
        "6208123456789",
        "6281234567",
        "62812345678",
        "62812345678901",
        "628123456789012",
        "81234567890",
        "6282260003750",  # Nomor resmi admin publik pada halaman beranda/login portal
    }
    pii_hits: list[str] = []
    for p in list((REPO_ROOT / "03-hasil-pengujian").rglob("*.md")) + list((REPO_ROOT / "03-hasil-pengujian").rglob("*.json")) + list((REPO_ROOT / "03-hasil-pengujian").rglob("*.txt")):
        txt = p.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"(?:\+?62|0)8\d{7,12}", txt):
            num = m.group(0).lstrip("+")
            if num not in allowed_synthetic:
                pii_hits.append(f"{p.relative_to(REPO_ROOT)}: {m.group(0)}")
    if pii_hits:
        issues.append(f"Potensi nomor non-sintetik terdeteksi: {pii_hits}")

    return {
        "id": "AUD-03",
        "name": "Konsistensi Data Empiris, Guardrail POST=0, & Zero PII Leakage",
        "status": "PASS" if not issues else "FAIL",
        "bb_summary": f"{bb_json['passed']}/{bb_json['total_cases']} PASS, network_posts_sent={bb_json['network_posts_sent_to_server']}",
        "perf_summary": f"{perf_pass}/{len(perf_json['test_cases'])} PASS, aborted={perf_json['http_concurrency']['aborted_reason']}",
        "issues": issues,
    }


def check_links_and_assets() -> dict[str, Any]:
    """AUD-04: Validasi seluruh tautan relatif Markdown dan keberadaan aset PDF/gambar."""
    broken_links: list[dict[str, str]] = []
    checked_links = 0
    for md in REPO_ROOT.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        for m in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = m.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = target.split("#")[0]
            if not target_path:
                continue
            checked_links += 1
            if not (md.parent / target_path).resolve().exists():
                broken_links.append({"file": str(md.relative_to(REPO_ROOT)), "link": target})

    pdfs_standar = list((REPO_ROOT / "01-standar-ieee-iso/pdf-standar").glob("*.pdf"))
    pdfs_jurnal = list((REPO_ROOT / "02-objek-umkm-dan-rencana-uji/pdf-jurnal").glob("*.pdf"))
    screenshots = list((REPO_ROOT / "03-hasil-pengujian/evidence/screenshots").glob("*.png"))

    asset_issues: list[str] = []
    if len(pdfs_standar) < 3:
        asset_issues.append(f"Jumlah PDF standar kurang dari 3 ({len(pdfs_standar)})")
    if len(pdfs_jurnal) < 7:
        asset_issues.append(f"Jumlah PDF jurnal SINTA kurang dari 7 ({len(pdfs_jurnal)})")
    if len(screenshots) < 8:
        asset_issues.append(f"Jumlah screenshot bukti kurang dari 8 ({len(screenshots)})")

    return {
        "id": "AUD-04",
        "name": "Integritas Tautan Markdown & Kelengkapan Berkas PDF/Screenshot",
        "status": "PASS" if not broken_links and not asset_issues else "FAIL",
        "markdown_links_checked": checked_links,
        "broken_links": broken_links,
        "pdf_standar_count": len(pdfs_standar),
        "pdf_jurnal_count": len(pdfs_jurnal),
        "screenshot_count": len(screenshots),
        "asset_issues": asset_issues,
    }


def check_academic_requirements() -> dict[str, Any]:
    """AUD-05: Cek kepatuhan Poin 1-7 dan catatan status item yang memang masih menunggu."""
    pptx_files = list((REPO_ROOT / "00-materi-perkuliahan").glob("*.pptx"))
    wawancara = (REPO_ROOT / "04-wawancara-praktisi-qa/panduan-wawancara.md").read_text(encoding="utf-8")
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    sinta = (REPO_ROOT / "02-objek-umkm-dan-rencana-uji/referensi-sinta-1-3.md").read_text(encoding="utf-8")

    issues: list[str] = []
    if len(pptx_files) < 7:
        issues.append(f"Modul PPTX di 00-materi-perkuliahan kurang dari 7 ({len(pptx_files)})")
    if "gorpermatabadminton.com" not in readme:
        issues.append("Objek final GOR Permata tidak tercantum di README.md")
    if "SINTA 2" not in sinta or "SINTA 3" not in sinta:
        issues.append("Sitasi SINTA 2/3 tidak terdeteksi di referensi-sinta-1-3.md")
    if "*[Diisi]*" not in wawancara:
        issues.append("Format panduan wawancara berubah tak terduga")

    pending_notes = [
        "Anggota kelompok ke-3 dan ke-4 di README.md masih placeholder *[Diisi]* menunggu konfirmasi anggota.",
        "Modul perkuliahan Pertemuan 8-akhir di 00-materi-perkuliahan/ menunggu distribusi dari Ketua Kelas.",
        "Wawancara praktisi QA (04-wawancara-praktisi-qa/) berstatus Siap Dilaksanakan setelah proyek 01-03 selesai.",
        "Skrip Cypress gor-permata.cy.js disinkronkan namun tidak dieksekusi lokal karena biner cypress tidak terpasang.",
    ]

    return {
        "id": "AUD-05",
        "name": "Kepatuhan Ketentuan Akademik Perkuliahan (Poin 1-7)",
        "status": "PASS" if not issues else "FAIL",
        "pptx_count": len(pptx_files),
        "issues": issues,
        "pending_external_dependencies": pending_notes,
    }


def check_reports_and_readme() -> dict[str, Any]:
    """AUD-06: Cek keberadaan laporan Word/PDF serta kelengkapan README.md mencakup folder 00-05."""
    docx_p = REPO_ROOT / "03-hasil-pengujian/Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.docx"
    pdf_p = REPO_ROOT / "03-hasil-pengujian/Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.pdf"
    bb_p = REPO_ROOT / "03-hasil-pengujian/evidence/blackbox-results.json"
    perf_p = REPO_ROOT / "03-hasil-pengujian/evidence/performance-metrics.json"
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    issues: list[str] = []
    if not docx_p.exists() or docx_p.stat().st_size == 0:
        issues.append("File Word laporan hasil pengujian tidak ada atau kosong")
    if not pdf_p.exists() or pdf_p.stat().st_size == 0:
        issues.append("File PDF laporan hasil pengujian tidak ada atau kosong")
    if docx_p.exists() and pdf_p.exists():
        latest_json_mtime = max(bb_p.stat().st_mtime, perf_p.stat().st_mtime)
        if docx_p.stat().st_mtime < latest_json_mtime or pdf_p.stat().st_mtime < latest_json_mtime:
            issues.append("File Word/PDF lebih lama dari hasil JSON terbaru (perlu regenerasi)")

    for folder_ref in (
        "00-materi-perkuliahan",
        "01-standar-ieee-iso",
        "02-objek-umkm-dan-rencana-uji",
        "03-hasil-pengujian",
        "04-wawancara-praktisi-qa",
        "05-audit-dokumentasi-qa",
        "Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.docx",
        "Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.pdf",
    ):
        if folder_ref not in readme:
            issues.append(f"Referensi '{folder_ref}' belum tercantum di README.md root")

    return {
        "id": "AUD-06",
        "name": "Sinkronisasi Word/PDF & Kelengkapan Indeks README.md (00-05)",
        "status": "PASS" if not issues else "FAIL",
        "docx_bytes": docx_p.stat().st_size if docx_p.exists() else 0,
        "pdf_bytes": pdf_p.stat().st_size if pdf_p.exists() else 0,
        "issues": issues,
    }


def main() -> None:
    started = datetime.now().astimezone().isoformat(timespec="seconds")
    checks = [
        check_iso_artifacts(),
        check_traceability(),
        check_empirical_and_privacy(),
        check_links_and_assets(),
        check_academic_requirements(),
        check_reports_and_readme(),
    ]
    passed = sum(1 for c in checks if c["status"] == "PASS")
    overall = "PASS" if passed == len(checks) else "FAIL"

    report = {
        "audit_timestamp": started,
        "repository": str(REPO_ROOT),
        "overall_status": overall,
        "passed_checks": passed,
        "total_checks": len(checks),
        "checks": checks,
    }
    OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"=== AUDIT DOKUMENTASI QA: {started} | OVERALL: {overall} ({passed}/{len(checks)}) ===")
    for c in checks:
        print(f"[{c['status']}] {c['id']} - {c['name']}")
        for key in ("missing", "missing_mappings", "issues", "broken_links", "asset_issues"):
            if key in c and c[key]:
                print(f"    -> {key}: {c[key]}")
    print(f"Output JSON disimpan ke: {OUT_JSON}")


if __name__ == "__main__":
    main()
