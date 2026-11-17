"""
Generator Laporan Resmi Pengujian QA (Word .docx & PDF)
Sesuai ISO/IEC/IEEE 29119-2:2021(E) & ISO/IEC 25010:2023
Objek: Portal Booking GOR Permata Badminton Hall (https://gorpermatabadminton.com)

Membaca langsung hasil empiris dari:
  - 03-hasil-pengujian/evidence/blackbox-results.json
  - 03-hasil-pengujian/evidence/performance-metrics.json
  - 03-hasil-pengujian/evidence/screenshots/*.png

Penggunaan:
    python 03-hasil-pengujian/generate_laporan_pengujian.py
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Sequence

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Pt, RGBColor

SCRIPT_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = SCRIPT_DIR / "evidence"
SCREENSHOT_DIR = EVIDENCE_DIR / "screenshots"
BB_JSON_PATH = EVIDENCE_DIR / "blackbox-results.json"
PERF_JSON_PATH = EVIDENCE_DIR / "performance-metrics.json"

OUT_DOCX = SCRIPT_DIR / "Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.docx"
OUT_PDF = SCRIPT_DIR / "Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.pdf"

# Palet warna konsisten dengan dokumen perkuliahan
NAVY = RGBColor(0x1B, 0x36, 0x5D)
ACCENT_BLUE = RGBColor(0x2B, 0x6C, 0xB0)
DARK_TEXT = RGBColor(0x1A, 0x20, 0x2C)
MUTED_TEXT = RGBColor(0x4A, 0x55, 0x68)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREEN_TEXT = RGBColor(0x15, 0x80, 0x3D)
RED_TEXT = RGBColor(0xB9, 0x1C, 0x1C)
AMBER_TEXT = RGBColor(0xB4, 0x53, 0x09)

HEX_NAVY = "1B365D"
HEX_ACCENT = "2B6CB0"
HEX_CALLOUT_BG = "EBF4FF"
HEX_WARN_BG = "FFFBEB"
HEX_WARN_BORDER = "D97706"
HEX_ALT_ROW = "F7FAFC"
HEX_BORDER = "CBD5E0"


def set_cell_shading(cell, fill_hex: str) -> None:
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_margins(cell, top=85, bottom=85, left=110, right=110) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement("w:tcMar")
    for side, val in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tc_mar.append(node)
    tc_pr.append(tc_mar)


def set_table_borders(table, border_hex: str = HEX_BORDER, sz: str = "4") -> None:
    tbl_pr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{border_hex}"/>'
        f'  <w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{border_hex}"/>'
        f'  <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{border_hex}"/>'
        f'  <w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{border_hex}"/>'
        f'  <w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{border_hex}"/>'
        f'  <w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{border_hex}"/>'
        f"</w:tblBorders>"
    )
    tbl_pr.append(borders)


def prevent_row_split(row) -> None:
    row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))


def repeat_header_row(row) -> None:
    row._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))


def add_bottom_border_to_paragraph(paragraph, color_hex: str = HEX_ACCENT, sz: str = "10") -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="{sz}" w:space="4" w:color="{color_hex}"/>'
        f"</w:pBdr>"
    )
    p_pr.append(p_bdr)


def add_field(paragraph, field_name: str, font_size: int = 8.5, color: RGBColor = MUTED_TEXT) -> None:
    run_begin = paragraph.add_run()
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    run_begin._r.append(fld_begin)

    run_instr = paragraph.add_run()
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = f" {field_name} "
    run_instr._r.append(instr)

    run_sep = paragraph.add_run()
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    run_sep._r.append(fld_sep)

    run_val = paragraph.add_run("1")
    run_val.font.name = "Calibri"
    run_val.font.size = Pt(font_size)
    run_val.font.color.rgb = color

    run_end = paragraph.add_run()
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run_end._r.append(fld_end)


def configure_styles(doc: Document) -> None:
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10)
    normal.font.color.rgb = DARK_TEXT
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(4)

    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(1.8)
        section.bottom_margin = Cm(1.8)
        section.left_margin = Cm(1.9)
        section.right_margin = Cm(1.9)
        section.different_first_page_header_footer = True

        hdr = section.header
        hp = hdr.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Laporan Pengujian QA (ISO/IEC/IEEE 29119-2:2021)  |  GOR Permata Badminton Hall")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = MUTED_TEXT
        add_bottom_border_to_paragraph(hp, color_hex=HEX_BORDER, sz="4")

        for ftr in (section.footer, section.first_page_footer):
            fp = ftr.paragraphs[0]
            fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r_left = fp.add_run("Universitas Pamulang • Teknik Informatika S1 (07TPLE001)     |     Halaman ")
            r_left.font.name = "Calibri"
            r_left.font.size = Pt(8.5)
            r_left.font.color.rgb = MUTED_TEXT
            add_field(fp, "PAGE")
            r_mid = fp.add_run(" dari ")
            r_mid.font.name = "Calibri"
            r_mid.font.size = Pt(8.5)
            r_mid.font.color.rgb = MUTED_TEXT
            add_field(fp, "NUMPAGES")


def add_section_heading(doc: Document, number_label: str, title: str, page_break_before: bool = False) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.page_break_before = page_break_before
    r_num = p.add_run(f"{number_label}  ")
    r_num.bold = True
    r_num.font.name = "Calibri"
    r_num.font.size = Pt(12.5)
    r_num.font.color.rgb = ACCENT_BLUE

    r_title = p.add_run(title)
    r_title.bold = True
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(12.5)
    r_title.font.color.rgb = NAVY
    add_bottom_border_to_paragraph(p, color_hex=HEX_ACCENT, sz="8")


def add_sub_heading(doc: Document, title: str) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title)
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)
    r.font.color.rgb = ACCENT_BLUE


def add_callout_box(
    doc: Document,
    title: str,
    paragraphs: Sequence[str],
    bg_hex: str = HEX_CALLOUT_BG,
    border_hex: str = HEX_ACCENT,
) -> None:
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Cm(17.2)
    set_cell_shading(cell, bg_hex)
    set_cell_margins(cell, top=100, bottom=100, left=160, right=140)
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>'
        f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>'
        f"</w:tcBorders>"
    )
    tc_pr.append(borders)
    prevent_row_split(tbl.rows[0])

    p0 = cell.paragraphs[0]
    p0.paragraph_format.space_after = Pt(3)
    rt = p0.add_run(title)
    rt.bold = True
    rt.font.name = "Calibri"
    rt.font.size = Pt(10)
    rt.font.color.rgb = NAVY

    for idx, text in enumerate(paragraphs):
        p = cell.add_paragraph()
        p.paragraph_format.space_after = Pt(2 if idx < len(paragraphs) - 1 else 0)
        p.paragraph_format.line_spacing = 1.12
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = DARK_TEXT

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(3)


def add_bullet(doc: Document, lead_bold: str | None, body: str) -> None:
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.line_spacing = 1.12
    if lead_bold:
        rb = p.add_run(lead_bold)
        rb.bold = True
        rb.font.name = "Calibri"
        rb.font.size = Pt(9.5)
        rb.font.color.rgb = DARK_TEXT
    r = p.add_run(body)
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    r.font.color.rgb = DARK_TEXT


def add_styled_table(
    doc: Document,
    headers: Sequence[str],
    rows: Iterable[Sequence[str]],
    col_widths_cm: Sequence[float],
    center_cols: Sequence[int] = (),
    font_size: float = 8.8,
) -> None:
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, border_hex=HEX_BORDER, sz="4")

    hdr_row = tbl.rows[0]
    repeat_header_row(hdr_row)
    prevent_row_split(hdr_row)

    for idx, text in enumerate(headers):
        cell = hdr_row.cells[idx]
        cell.width = Cm(col_widths_cm[idx])
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_shading(cell, HEX_NAVY)
        set_cell_margins(cell, top=90, bottom=90, left=95, right=95)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if idx in center_cols else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(text)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(font_size)
        r.font.color.rgb = WHITE

    for r_idx, row_data in enumerate(rows):
        row = tbl.add_row()
        prevent_row_split(row)
        bg = HEX_ALT_ROW if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = Cm(col_widths_cm[c_idx])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            set_cell_shading(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=95, right=95)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.12
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in center_cols else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(font_size)
            upper_val = val.strip().upper()
            if upper_val in ("PASS", "TERPENUHI", "DISETUJUI", "BAIK", "DITERAPKAN & PASS"):
                r.bold = True
                r.font.color.rgb = GREEN_TEXT
            elif upper_val.startswith("FAIL") or upper_val in ("OPEN", "MAJOR / HIGH", "ADA DEFECT"):
                r.bold = True
                r.font.color.rgb = RED_TEXT
            elif "PERLU" in upper_val or "CUKUP" in upper_val or "PROSES" in upper_val:
                r.bold = True
                r.font.color.rgb = AMBER_TEXT
            else:
                r.font.color.rgb = DARK_TEXT
            if c_idx == 0 and c_idx in center_cols:
                r.bold = True

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(3)


def add_title_banner(doc: Document, bb_ts: str, perf_ts: str) -> None:
    banner = doc.add_table(rows=1, cols=1)
    banner.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = banner.cell(0, 0)
    cell.width = Cm(17.2)
    set_cell_shading(cell, HEX_NAVY)
    set_cell_margins(cell, top=160, bottom=160, left=180, right=180)
    prevent_row_split(banner.rows[0])

    p_k = cell.paragraphs[0]
    p_k.paragraph_format.space_after = Pt(3)
    rk = p_k.add_run("LAPORAN HASIL PENGUJIAN PERANGKAT LUNAK • ISO/IEC/IEEE 29119-2:2021 & ISO/IEC 25010:2023")
    rk.bold = True
    rk.font.name = "Calibri"
    rk.font.size = Pt(8.5)
    rk.font.color.rgb = RGBColor(0x90, 0xCD, 0xF4)

    p_t = cell.add_paragraph()
    p_t.paragraph_format.space_after = Pt(4)
    rt = p_t.add_run("Portal Booking GOR Permata Badminton Hall")
    rt.bold = True
    rt.font.name = "Calibri"
    rt.font.size = Pt(17)
    rt.font.color.rgb = WHITE

    p_s = cell.add_paragraph()
    p_s.paragraph_format.space_after = Pt(0)
    rs = p_s.add_run(
        "Dokumentasi Lengkap Black Box Testing, Performance Testing, Pelaporan Insiden, Audit Mutu, & Penutupan Uji"
    )
    rs.font.name = "Calibri"
    rs.font.size = Pt(9.8)
    rs.font.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)

    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(3)

    meta_rows = [
        ("Program Studi / Universitas", "Teknik Informatika (S1) — Universitas Pamulang"),
        ("Mata Kuliah & Dosen", "Testing dan QA Perangkat Lunak — Bapak Ahmad Fauzi"),
        ("Kelas / Repositori GitHub", "07TPLE001 / Reguler C  |  https://github.com/BrongSkuy/tugas-qa-testing"),
        ("Tim Penyusun", "1. Muhammad Faiz Rabbani (231011402539)   2. Robi Farhan Anshori (231011401468)   3–4. [Menunggu Pengisian]"),
        ("Objek Uji (SUT)", "https://gorpermatabadminton.com (Kp. Cipari, Desa Ciakar, Kec. Panongan, Kab. Tangerang)"),
        ("Standar Acuan Resmi", "ISO/IEC/IEEE 29119-2:2021(E) (Test Processes), 29119-3/4/5, & ISO/IEC 25010:2023"),
        ("Waktu Eksekusi Terakhir", f"Black Box: {bb_ts}   |   Performance: {perf_ts}"),
    ]
    tbl = doc.add_table(rows=len(meta_rows), cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, border_hex=HEX_BORDER, sz="4")
    for idx, (k, v) in enumerate(meta_rows):
        row = tbl.rows[idx]
        prevent_row_split(row)
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Cm(5.0)
        c1.width = Cm(12.2)
        set_cell_shading(c0, HEX_ALT_ROW)
        set_cell_shading(c1, "FFFFFF")
        set_cell_margins(c0, top=60, bottom=60, left=100, right=100)
        set_cell_margins(c1, top=60, bottom=60, left=100, right=100)
        r0 = c0.paragraphs[0].add_run(k)
        c0.paragraphs[0].paragraph_format.space_after = Pt(0)
        r0.bold = True
        r0.font.name = "Calibri"
        r0.font.size = Pt(9)
        r0.font.color.rgb = NAVY

        r1 = c1.paragraphs[0].add_run(v)
        c1.paragraphs[0].paragraph_format.space_after = Pt(0)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9)
        r1.font.color.rgb = DARK_TEXT

    sp2 = doc.add_paragraph()
    sp2.paragraph_format.space_after = Pt(3)


def add_screenshot_gallery(doc: Document) -> None:
    items = [
        ("01_home_desktop.png", "Gambar 1. Beranda Portal (Desktop 1280x800, TC-BB-01 / TC-PERF-01)", 8.0),
        ("02_booking_grid_desktop.png", "Gambar 2. Grid Jadwal /booking (Label Pelanggan Dimasking [TERISI], TC-BB-03)", 8.0),
        ("03_booking_modal_desktop.png", "Gambar 3. Modal #bookingModal Desktop (TC-BB-06)", 5.6),
        ("06_login_page.png", "Gambar 4. Halaman Admin Login /login & Token CSRF (TC-BB-20)", 8.0),
        ("04_register_404.png", "Gambar 5. Bukti Insiden IR-GOR-01: Endpoint /register HTTP 404 (TC-BB-02)", 8.0),
        ("05_invalid_date_500.png", "Gambar 6. Bukti Insiden IR-GOR-06: ?start_date=invalid-date HTTP 500 (TC-BB-05)", 8.0),
        ("07_home_mobile.png", "Gambar 7. Bukti Insiden IR-GOR-10: Navbar Mobile 390x844 Terpotong (TC-BB-21)", 4.6),
        ("08_booking_modal_mobile.png", "Gambar 8. Modal #bookingModal pada Viewport Mobile 390x844 (TC-BB-21)", 4.6),
    ]

    for i in range(0, len(items), 2):
        pair = items[i : i + 2]
        tbl = doc.add_table(rows=2, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, border_hex=HEX_BORDER, sz="4")
        prevent_row_split(tbl.rows[0])
        prevent_row_split(tbl.rows[1])
        for col_idx, (fname, caption, width_cm) in enumerate(pair):
            img_path = SCREENSHOT_DIR / fname
            c_img = tbl.cell(0, col_idx)
            c_cap = tbl.cell(1, col_idx)
            c_img.width = Cm(8.6)
            c_cap.width = Cm(8.6)
            c_img.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(c_img, top=80, bottom=60, left=80, right=80)
            set_cell_margins(c_cap, top=60, bottom=60, left=80, right=80)
            set_cell_shading(c_cap, HEX_ALT_ROW)

            p_img = c_img.paragraphs[0]
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_after = Pt(0)
            if img_path.exists():
                p_img.add_run().add_picture(str(img_path), width=Cm(width_cm))
            else:
                p_img.add_run(f"[Gambar tidak ditemukan: {fname}]")

            p_cap = c_cap.paragraphs[0]
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(0)
            rc = p_cap.add_run(caption)
            rc.bold = True
            rc.font.name = "Calibri"
            rc.font.size = Pt(8.2)
            rc.font.color.rgb = NAVY

        sp = doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(3)


def build_report() -> tuple[Path, Path]:
    bb = json.loads(BB_JSON_PATH.read_text(encoding="utf-8"))
    perf = json.loads(PERF_JSON_PATH.read_text(encoding="utf-8"))

    doc = Document()
    configure_styles(doc)
    add_title_banner(doc, bb["timestamp"], perf["metadata"]["timestamp"])

    # BAB I
    add_section_heading(doc, "I.", "Ringkasan Eksekutif & Kepatuhan ISO/IEC/IEEE 29119-2:2021 (Clause 4 & 6)")
    add_callout_box(
        doc,
        "Intisari Hasil Pengujian Non-Destruktif (17 November 2026)",
        [
            f"1. Black Box Testing (Playwright Python): {bb['total_cases']} kasus uji dieksekusi -> "
            f"{bb['passed']} PASS dan {bb['failed_or_defect_repro']} FAIL (konfirmasi cacat aktual), "
            f"0 error konsol JS, serta network_posts_sent_to_server = {bb['network_posts_sent_to_server']} "
            f"({bb['intercepted_post_attempts_inside_browser']} percobaan fetch dicegat aman di browser).",
            f"2. Performance Testing (Web Vitals + HTTP 1/5/10 VUs GET-only): {len(perf['test_cases'])} kasus uji dieksekusi -> "
            f"{sum(1 for c in perf['test_cases'] if c['status'] == 'PASS')} PASS dan "
            f"{sum(1 for c in perf['test_cases'] if c['status'] == 'FAIL')} FAIL (pelanggaran SLA 10 VUs / payload / cold-TTFB), "
            f"dengan 0,0% HTTP error di seluruh 104 request konkuren.",
            "3. Pelaporan Insiden & Kepatuhan: Total 10 insiden tervalidasi (IR-GOR-01 s.d. IR-GOR-10) telah didokumentasikan "
            "mengikuti seluruh layer proses ISO/IEC/IEEE 29119-2:2021 (Organizational -> Test Management -> Dynamic Test Processes).",
        ],
    )

    add_sub_heading(doc, "1.1 Deklarasi Tailored Conformance (Clause 4.1.3) & Peta Artefak Repo")
    add_bullet(
        doc,
        "Klaim Kepatuhan: ",
        "Tailored Conformance terhadap ISO/IEC/IEEE 29119-2:2021 mencakup Clause 6, Clause 7 (7.2–7.4), dan Clause 8 (8.2–8.5). "
        "Pengecualian terbatas hanya pada pengiriman booking nyata (POST /bookings/store), panel admin internal, dan uji beban > 10 VUs demi melindungi jadwal dan ketersediaan layanan UMKM.",
    )
    iso_rows = [
        ("Clause 4 & 6 (OT1–OT3)", "Organizational Test Specification", "01-standar-ieee-iso/organizational-test-specification.md"),
        ("Clause 7.2 (TP1–TP9)", "Master Test Plan & Performance Test Plan", "02-.../test-plan-gor-permata.md & performance-test-plan.md"),
        ("Clause 8.2 (TD1–TD2)", "Test Model Spec & Test Coverage Items (2021)", "02-.../test-model-blackbox.md & test-model-performance.md"),
        ("Clause 8.2 (TD3–TD4)", "Test Case, Test Procedure, & Automation Scripts", "03-.../test-case-blackbox.md, test-case-performance.md, automation-scripts/"),
        ("Clause 8.3 (ED1–ED4)", "Environment & Data Readiness Reports", "03-.../test-environment-dan-data.md & test-data/*.json"),
        ("Clause 8.4 (TE1–TE3)", "Test Execution Log, JSON Metrik, & Screenshot", "03-.../test-execution-log.md & evidence/"),
        ("Clause 8.5 (IR1–IR2)", "Incident / Defect Reports (IR-GOR-01..10)", "03-.../incident-reports.md"),
        ("Clause 7.3 & 7.4", "Test Status/Control & Test Completion Report", "03-.../test-status-and-control-report.md & test-completion-report.md"),
    ]
    add_styled_table(
        doc,
        headers=("Klausul ISO 29119-2", "Information Item Wajib", "Berkas di Repositori tugas-qa-testing"),
        rows=iso_rows,
        col_widths_cm=(3.8, 6.2, 7.2),
    )

    # BAB II
    add_section_heading(doc, "II.", "Perencanaan Uji, Manajemen Risiko, & Landasan SINTA 1–3 (Clause 7.2)")
    add_bullet(
        doc,
        "Test Basis & Strategi: ",
        "Mencakup halaman publik (/ , /booking, /login, /register, /fasilitas/*), logika JS klien (7.473 karakter pada /booking), "
        "teknik Black Box ISO 29119-4 (EP, BVA, Decision Table, State Transition, Use Case), Performance Testing 3-tier, serta White/Gray Box.",
    )
    add_bullet(
        doc,
        "Justifikasi Ilmiah SINTA 2–3 (Poin 7): ",
        "Didukung 7 PDF full-paper dan 2 rujukan DOI SINTA 2–3: Alirridlo, dkk. (2025, RESTI SINTA 2) & Pratala, dkk. (2020, JIUP SINTA 3) untuk White Box V(G); "
        "Yulistina, dkk. (2020), Nurudin, dkk. (2019), & Putri & Susanto (2024) untuk Black Box EP/BVA; Seputra, dkk. (2024, RESTI SINTA 2) & Fhonna, dkk. (2026, Sisfo SINTA 3) untuk integrasi & otomasi E2E; "
        "serta Zahra & Kraugusteeliana (2023, JTIIK SINTA 2) & Putra, dkk. (2026, JAIC SINTA 3) untuk Performance ISO 25010 & pemilihan Playwright.",
    )

    risk_rows = [
        ("PR-01 (Product)", "normPhone() gagal di +62 08... & batas digit WA", "9 (Tinggi)", "EP/BVA panjang digit (10/11/14/15) + Basis Path V(G)=4"),
        ("PR-02 (Product)", "Query ?start_date= rusak picu 500 atau tanggal lampau aktif", "9 (Tinggi)", "Uji ?start_date=2020-01-01 & invalid-date -> catat IR"),
        ("PR-03 (Product)", "HTML /booking (~535 KB) lambat saat diakses konkuren", "6 (Sedang-Tinggi)", "Uji Web Vitals & beban GET 1/5/10 VUs (TP-GOR-PERF-01)"),
        ("PR-04 / PR-05 (Product)", "#custName tanpa .trim(), /register 404, & eksposur DOM PII", "6 (Sedang)", "Uji BVA spasi, rute /register, & audit atribut data-phone"),
        ("PJ-01 / PJ-02 (Project)", "Risiko transaksi fiktif atau beban berlebih ke DB/server UMKM", "8 / 6 (Terkendali)", "Blokir POST via page.route (0 terkirim) & GET max 10 VUs + circuit breaker"),
    ]
    add_styled_table(
        doc,
        headers=("ID & Kelas Risiko", "Deskripsi Risiko Utama", "Exposure", "Risk Treatment & Verifikasi"),
        rows=risk_rows,
        col_widths_cm=(3.2, 5.5, 2.5, 6.0),
        center_cols=(2,),
    )

    # BAB III
    add_section_heading(doc, "III.", "Lingkungan Uji, Data Uji, & Readiness Report (Clause 8.3)")
    env_rows = [
        ("Host & Runtime", "Windows-10-10.0.26300-SP0 | Python 3.9.10 | Playwright 1.60.0 (Chromium) | aiohttp 3.13.5", "SIAP (READY)"),
        ("Node / Cypress", "Node.js v24.14.0 & npm 11.13.0 terpasang; biner cypress tidak terpasang lokal (eksekusi E2E via Playwright)", "Alternatif Playwright"),
        ("Dataset Non-PII", "blackbox-testdata.json (TD-BB-GOR-01) & performance-profiles.json (TD-PERF-GOR-01)", "SIAP (READY)"),
        ("Beda Test vs Ops (8.3.4.2 c)", "POST /bookings/store dicegat lokal di browser (tidak menyentuh DB nyata); beban dibatasi GET max 10 VUs", "Terdokumentasi"),
    ]
    add_styled_table(
        doc,
        headers=("Aspek Lingkungan/Data", "Spesifikasi & Catatan Kesiapan", "Status"),
        rows=env_rows,
        col_widths_cm=(4.0, 10.4, 2.8),
        center_cols=(2,),
    )

    # BAB IV
    add_section_heading(doc, "IV.", "Hasil Eksekusi Black Box Testing (Clause 8.2 & 8.4 — 22 Test Cases)", page_break_before=True)
    p_bb = doc.add_paragraph(
        f"Eksekusi penuh dijalankan melalui test_gor_permata.py pada {bb['timestamp']} dengan hasil "
        f"{bb['passed']}/{bb['total_cases']} PASS dan {bb['failed_or_defect_repro']} FAIL (temuan cacat nyata). "
        f"Total percobaan POST yang dicegat di dalam browser: {bb['intercepted_post_attempts_inside_browser']}, "
        f"dan total POST terkirim ke server: {bb['network_posts_sent_to_server']}."
    )
    p_bb.paragraph_format.space_after = Pt(4)

    bb_rows = [
        (c["tc_id"], c["name"], c["expected"], c["actual"], c["status"])
        for c in bb["cases"]
    ]
    add_styled_table(
        doc,
        headers=("ID TC", "Skenario Uji Black Box", "Expected Result", "Actual Result Teramati", "Status"),
        rows=bb_rows,
        col_widths_cm=(1.8, 4.1, 4.1, 5.7, 1.5),
        center_cols=(0, 4),
        font_size=8.2,
    )

    # BAB V
    add_section_heading(doc, "V.", "Hasil Eksekusi Performance Testing (Clause 8.2 & 8.4 — 10 Test Cases)", page_break_before=True)
    p_pf = doc.add_paragraph(
        f"Pengujian performa dijalankan pada {perf['metadata']['timestamp']} menggunakan Playwright Chromium Headless "
        f"(Navigation/Resource Timing & Web Vitals) serta aiohttp asinkron (GET-only 1, 5, dan 10 VUs; jeda 500 ms)."
    )
    p_pf.paragraph_format.space_after = Pt(4)

    perf_tc_rows = [
        (c["tc_id"], c["name"], c["expected"], c["actual"], c["status"])
        for c in perf["test_cases"]
    ]
    add_styled_table(
        doc,
        headers=("ID TC", "Skenario Uji Performance", "Target SLA", "Actual Result Terukur", "Status"),
        rows=perf_tc_rows,
        col_widths_cm=(2.0, 4.0, 3.8, 5.9, 1.5),
        center_cols=(0, 4),
        font_size=8.2,
    )

    add_sub_heading(doc, "5.1 Rincian Browser Web Vitals (Cold vs Warm Desktop & Cold Mobile)")
    cd = perf["browser"]["cold_desktop"]
    wd = perf["browser"]["warm_desktop"]
    cm = perf["browser"]["cold_mobile"]
    vitals_rows = []
    for label, d in [
        ("Cold Desktop /", cd["/"]),
        ("Cold Desktop /booking", cd["/booking"]),
        ("Cold Desktop /login", cd["/login"]),
        ("Cold Desktop /fasilitas/lapangan", cd["/fasilitas/lapangan"]),
        ("Warm Desktop /", wd["/"]),
        ("Warm Desktop /booking", wd["/booking"]),
        ("Cold Mobile / (390x844)", cm["/"]),
        ("Cold Mobile /booking (390x844)", cm["/booking"]),
    ]:
        vitals_rows.append(
            (
                label,
                f"{d['ttfb_ms']} ms",
                f"{d['dcl_ms']} ms",
                f"{d['load_ms']} ms",
                f"{d['fcp_ms']} ms",
                f"{d['cls']}",
                f"{round(d['doc_decoded_bytes']/1024, 1)} KB / {round(d['doc_encoded_bytes']/1024, 1)} KB",
            )
        )
    add_styled_table(
        doc,
        headers=("Kondisi & Rute", "TTFB", "DCL", "Load", "FCP", "CLS", "HTML Raw / Encoded"),
        rows=vitals_rows,
        col_widths_cm=(4.8, 1.8, 1.8, 1.8, 1.8, 1.4, 3.8),
        center_cols=(1, 2, 3, 4, 5, 6),
        font_size=8.3,
    )

    inter = perf["browser"]["client_interactions"]
    add_bullet(
        doc,
        "Client DOM Interaction Latency (/booking): ",
        f"openBooking() = {inter['openBooking_ms']} ms | updateTotal() rata-rata = {inter['updateTotal_avg_ms']} ms "
        f"(maks = {inter['updateTotal_max_ms']} ms) | changeDate() trigger = {inter['changeDate_reload_ms']} ms (Seluruhnya PASS <= 250 ms).",
    )

    add_sub_heading(doc, "5.2 Rincian Tiered Concurrent HTTP GET Benchmark (1, 5, 10 VUs)")
    conc_rows = []
    for tier in perf["http_concurrency"]["tiers"]:
        for route, st in tier["per_route"].items():
            short_r = "/booking" if route.startswith("/booking") else route
            conc_rows.append(
                (
                    f"{tier['vus']} VU ({tier['rps']} req/s)",
                    short_r,
                    str(st["count"]),
                    f"{st['errors']} ({tier['error_rate_pct']}%)",
                    f"{st['mean_ms']} ms",
                    f"{st['p50_ms']} ms",
                    f"{st['p95_ms']} ms",
                    f"{st['max_ms']} ms",
                )
            )
    add_styled_table(
        doc,
        headers=("Level Beban", "Rute", "Req", "Err", "Mean", "p50", "p95", "Max"),
        rows=conc_rows,
        col_widths_cm=(3.2, 2.8, 1.1, 1.8, 2.0, 2.0, 2.2, 2.1),
        center_cols=(2, 3, 4, 5, 6, 7),
        font_size=8.2,
    )

    # BAB VI
    add_section_heading(doc, "VI.", "Laporan Insiden / Defect Terverifikasi (Clause 8.5 — IR-GOR-01 s.d. IR-GOR-10)", page_break_before=True)
    ir_rows = [
        ("IR-GOR-01 (BUG-01)", "TC-BB-02", "Functional", "Major / Medium", "Open", "Endpoint /register mengembalikan HTTP 404 Not Found."),
        ("IR-GOR-02 (BUG-02)", "TC-BB-16", "Validation / WB", "Minor / Medium", "Open", "normPhone('+62 08...') menghasilkan 6208... dan gagal regex."),
        ("IR-GOR-03 (BUG-03)", "TC-BB-09", "Validation / UX", "Minor / Low", "Open", "#custName tanpa .trim() meloloskan spasi '   ' & 1 huruf 'A'."),
        ("IR-GOR-04 (BUG-04)", "TC-BB-22", "Security / Privacy", "Major / High", "Open", "205 slot publik memuat atribut data-phone & data-name + skrip admin."),
        ("IR-GOR-05", "TC-BB-04", "Functional", "Major / High", "Open", "?start_date=2020-01-01 merender 612 slot openBooking() aktif."),
        ("IR-GOR-06", "TC-BB-05", "Error Handling", "Major / High", "Open", "?start_date=invalid-date menyebabkan crash HTTP 500 Server Error."),
        ("IR-GOR-07", "TC-PERF-10", "Performance", "Major / High", "Open", "Di 10 VUs, p95 /booking melonjak ke 5314,28 ms (> SLA 3000 ms)."),
        ("IR-GOR-08", "TC-PERF-06", "Performance", "Minor / Medium", "Open", "HTML mentah /booking mencapai 535,37 KB (> batas 500 KB)."),
        ("IR-GOR-09", "TC-PERF-01", "Performance", "Minor / Medium", "Open", "Cold-start TTFB / spike 2618,3 ms (FCP 3028 ms) vs warm 289,3 ms."),
        ("IR-GOR-10", "TC-BB-21", "Compatibility UI", "Minor / Medium", "Open", "Navbar mobile 390x844 memotong LOGIN & mendorong BOOKING ke x=489 px."),
    ]
    add_styled_table(
        doc,
        headers=("ID Insiden", "TC Pemicu", "Kategori", "Severity / Priority", "Status", "Ringkasan Temuan & Dampak"),
        rows=ir_rows,
        col_widths_cm=(2.6, 1.8, 2.3, 2.5, 1.3, 6.7),
        center_cols=(1, 4),
        font_size=8.2,
    )

    add_sub_heading(doc, "6.1 Galeri Bukti Tangkapan Layar Pengujian (8 Bukti Terverifikasi)")
    add_screenshot_gallery(doc)

    # BAB VII
    add_section_heading(doc, "VII.", "Audit Mutu ISO/IEC 25010:2023, Monitoring/Control, & Penutupan Uji (Clause 7.3–7.4)", page_break_before=True)
    iso25_rows = [
        ("1. Functional Suitability", "7 rute 200 OK & tarif 1..5 jam tepat; cacat pada /register 404, +62 08..., tanggal lampau & ?start_date=invalid 500.", "Ada Defect"),
        ("2. Performance Efficiency", "DOM instan (62,93 ms), 0% error 104 req, namun HTML /booking 535 KB & 10 VUs p95 = 5314,28 ms.", "Perlu Optimasi"),
        ("3. Compatibility", "Desktop & modal mobile 390px baik; cacat navbar mobile terpotong pada beranda / (IR-GOR-10).", "Perlu Perbaikan"),
        ("4. Interaction Capability", "Alur modal & reset form baik; kurangnya .trim() #custName & crash 500 pada query tanggal rusak.", "Cukup"),
        ("5. Reliability", "0% error pada uji beban 1–10 VUs; #btnSubmit nonaktif saat kirim & ditangani .catch().", "Baik"),
        ("6. Security", "X-CSRF-TOKEN & CSP upgrade-insecure-requests ada; 4 header hilang (HSTS/XFO/XCTO/RP) + 205 slot ekspos data-phone.", "Perlu Hardening"),
        ("7. Maintainability", "Skrip 7.473 karakter masih inline di /booking bersama tabel HTML 535 KB.", "Cukup"),
        ("8. Flexibility", "Berbasis web standar lintas OS/perangkat di balik CDN hcdn.", "Memadai"),
        ("9. Safety (Baru 2023)", "Batas jam tutup 00:00 (22:00 + 2 vs 3 jam) teruji akurat menolak di klien sebelum fetch.", "Diterapkan & PASS"),
    ]
    add_styled_table(
        doc,
        headers=("Karakteristik ISO/IEC 25010:2023", "Hasil Observasi & Pengujian Empiris", "Status"),
        rows=iso25_rows,
        col_widths_cm=(4.4, 9.8, 3.0),
        center_cols=(2,),
        font_size=8.4,
    )

    add_sub_heading(doc, "7.1 Ringkasan Test Monitoring, Control (7.3), & Test Completion (7.4)")
    add_bullet(
        doc,
        "Control Directives (CD-01..04): ",
        "(1) Penyesuaian Accept-Encoding: gzip, deflate pada aiohttp; (2) Penambahan jeda animasi 350 ms & masking [TERISI] pada screenshot grid; "
        "(3) Perluasan cek bounding box navbar mobile pada TC-BB-21; (4) Penambahan TC BVA/EP query start_date lampau & invalid.",
    )
    add_bullet(
        doc,
        "Evaluasi Completion Criteria & Cleanup (TC1–TC4): ",
        "100% TCI Black Box (22/22) dan Performance (10/10) telah dieksekusi dengan 0 request POST terkirim ke produksi; "
        "seluruh sesi Playwright/aiohttp telah ditutup bersih; seluruh aset uji (skrip, dataset JSON, bukti, & dokumen ISO) diarsipkan pada GitHub main.",
    )
    add_bullet(
        doc,
        "Lessons Learned & Langkah Lanjut: ",
        "Integrasi BVA otomatis + inspeksi visual tangkapan layar efektif menemukan cacat yang tidak terlihat lewat scrollWidth saja. "
        "Setelah fase 01–03 tuntas dan terarsip, kelompok siap melaksanakan tahap wawancara praktisi QA pada folder 04-wawancara-praktisi-qa/.",
    )

    sign_rows = [
        ("Muhammad Faiz Rabbani (231011402539)", "Koordinator QA & Lead Tester", "DISETUJUI", "17 Nov 2026"),
        ("Robi Farhan Anshori (231011401468)", "Anggota Tim QA & Standar ISO", "Sinkronisasi Repo", "17 Nov 2026"),
        ("Bapak Ahmad Fauzi", "Dosen Pengampu (Reviewer)", "Menunggu Asesmen", "—"),
    ]
    add_styled_table(
        doc,
        headers=("Nama / NIM", "Peran", "Status Persetujuan", "Tanggal"),
        rows=sign_rows,
        col_widths_cm=(6.2, 5.0, 3.6, 2.4),
        center_cols=(2, 3),
        font_size=8.8,
    )

    doc.save(str(OUT_DOCX))

    # Ekspor ke PDF identik melalui Microsoft Word COM
    import win32com.client  # type: ignore

    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        wdoc = word.Documents.Open(str(OUT_DOCX.resolve()))
        try:
            # Update semua field (PAGE / NUMPAGES) sebelum ekspor PDF
            wdoc.Fields.Update()
            # 17 = wdFormatPDF
            wdoc.SaveAs2(str(OUT_PDF.resolve()), FileFormat=17)
        finally:
            wdoc.Close(False)
    finally:
        word.Quit()

    return OUT_DOCX, OUT_PDF


if __name__ == "__main__":
    docx_p, pdf_p = build_report()
    print(f"Berhasil membuat DOCX: {docx_p} ({docx_p.stat().st_size} bytes)")
    print(f"Berhasil membuat PDF : {pdf_p} ({pdf_p.stat().st_size} bytes)")
