"""
Generator Laporan Resmi Pengujian QA (Word .docx & PDF) — Bahasa Sederhana & Mudah Dipahami
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
import re
from pathlib import Path
from typing import Any, Iterable, Sequence

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Pt, RGBColor
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
EVIDENCE_DIR = SCRIPT_DIR / "evidence"
SCREENSHOT_DIR = EVIDENCE_DIR / "screenshots"
BB_JSON_PATH = EVIDENCE_DIR / "blackbox-results.json"
PERF_JSON_PATH = EVIDENCE_DIR / "performance-metrics.json"

OUT_DIR = REPO_ROOT / "05-dokumentasi-laporan"
OUT_DOCX = OUT_DIR / "Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.docx"
OUT_PDF = OUT_DIR / "Laporan_Hasil_Pengujian_GOR_Permata_ISO29119.pdf"

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


def set_cell_margins(cell, top=80, bottom=80, left=105, right=105) -> None:
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
        section.top_margin = Cm(1.7)
        section.bottom_margin = Cm(1.7)
        section.left_margin = Cm(1.9)
        section.right_margin = Cm(1.9)
        section.different_first_page_header_footer = True

        hdr = section.header
        hp = hdr.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Laporan Hasil Pengujian Website (ISO/IEC/IEEE 29119-2:2021)  |  GOR Permata Badminton Hall")
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
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.page_break_before = page_break_before
    r_num = p.add_run(f"{number_label}  ")
    r_num.bold = True
    r_num.font.name = "Calibri"
    r_num.font.size = Pt(12)
    r_num.font.color.rgb = ACCENT_BLUE

    r_title = p.add_run(title)
    r_title.bold = True
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(12)
    r_title.font.color.rgb = NAVY
    add_bottom_border_to_paragraph(p, color_hex=HEX_ACCENT, sz="8")


def add_sub_heading(doc: Document, title: str) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(7)
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
    set_cell_margins(cell, top=90, bottom=90, left=150, right=140)
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
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(9.4)
        r.font.color.rgb = DARK_TEXT

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(2)


def add_bullet(doc: Document, lead_bold: str | None, body: str) -> None:
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.line_spacing = 1.14
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
        set_cell_margins(cell, top=80, bottom=80, left=90, right=90)
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
            set_cell_margins(cell, top=65, bottom=65, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.12
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in center_cols else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(font_size)
            upper_val = val.strip().upper()
            if upper_val in ("PASS", "TERPENUHI", "DISETUJUI", "BAIK", "DITERAPKAN & PASS", "SIAP (READY)", "TERKENDALI"):
                r.bold = True
                r.font.color.rgb = GREEN_TEXT
            elif upper_val.startswith("FAIL") or upper_val in ("OPEN", "MAJOR / HIGH", "ADA DEFECT", "PERLU PERBAIKAN", "TINGGI / KRITIS", "SEDANG / CEPAT"):
                r.bold = True
                r.font.color.rgb = RED_TEXT if upper_val != "SEDANG / CEPAT" else AMBER_TEXT
            elif "PERLU" in upper_val or "CUKUP" in upper_val or "PROSES" in upper_val or "SEDANG" in upper_val:
                r.bold = True
                r.font.color.rgb = AMBER_TEXT
            else:
                r.font.color.rgb = DARK_TEXT
            if c_idx == 0 and c_idx in center_cols:
                r.bold = True

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(2)


def add_title_banner(doc: Document, bb_ts: str, perf_ts: str) -> None:
    banner = doc.add_table(rows=1, cols=1)
    banner.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = banner.cell(0, 0)
    cell.width = Cm(17.2)
    set_cell_shading(cell, HEX_NAVY)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    prevent_row_split(banner.rows[0])

    p_k = cell.paragraphs[0]
    p_k.paragraph_format.space_after = Pt(2)
    rk = p_k.add_run("LAPORAN HASIL PENGUJIAN PERANGKAT LUNAK • ISO/IEC/IEEE 29119-2:2021 & ISO/IEC 25010:2023")
    rk.bold = True
    rk.font.name = "Calibri"
    rk.font.size = Pt(8.5)
    rk.font.color.rgb = RGBColor(0x90, 0xCD, 0xF4)

    p_t = cell.add_paragraph()
    p_t.paragraph_format.space_after = Pt(3)
    rt = p_t.add_run("Website Booking GOR Permata Badminton Hall")
    rt.bold = True
    rt.font.name = "Calibri"
    rt.font.size = Pt(17)
    rt.font.color.rgb = WHITE

    p_s = cell.add_paragraph()
    p_s.paragraph_format.space_after = Pt(0)
    rs = p_s.add_run(
        "Laporan Terpadu Pengujian Fungsi (Black Box), Kecepatan Akses (Performance), Daftar Temuan Masalah (Bug), Penilaian Kualitas, & Bukti Uji"
    )
    rs.font.name = "Calibri"
    rs.font.size = Pt(9.5)
    rs.font.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)

    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(2)

    meta_rows = [
        ("Program Studi / Kampus", "Teknik Informatika (S1) — Universitas Pamulang"),
        ("Mata Kuliah & Dosen", "Testing dan QA Perangkat Lunak — Asep Erlan Maulana, S.Kom., M.Kom"),
        ("Kelas / Link GitHub", "07TPLE001 / Reguler C  |  https://github.com/BrongSkuy/tugas-qa-testing"),
        ("Tim Penyusun", "1. Muhammad Faiz Rabbani (231011402539)  |  2. Robi Farhan Anshori (231011401468)\n3. Dzikri Attariq Samayaki (221011401148)  |  4. Nurlaelasari (231011403531)"),
        ("Website yang Diuji", "https://gorpermatabadminton.com (Kp. Cipari, Desa Ciakar, Kec. Panongan, Kab. Tangerang)"),
        ("Standar Acuan Resmi", "ISO/IEC/IEEE 29119-2:2021(E) (Proses Pengujian), 29119-3/4/5, & ISO/IEC 25010:2023 (Kualitas Produk)"),
        ("Waktu Uji Terakhir", f"Uji Fungsi (Black Box): {bb_ts}   |   Uji Kecepatan (Performance): {perf_ts}"),
    ]
    tbl = doc.add_table(rows=len(meta_rows), cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, border_hex=HEX_BORDER, sz="4")
    for idx, (k, v) in enumerate(meta_rows):
        row = tbl.rows[idx]
        prevent_row_split(row)
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Cm(4.8)
        c1.width = Cm(12.4)
        set_cell_shading(c0, HEX_ALT_ROW)
        set_cell_shading(c1, "FFFFFF")
        set_cell_margins(c0, top=55, bottom=55, left=95, right=95)
        set_cell_margins(c1, top=55, bottom=55, left=95, right=95)
        r0 = c0.paragraphs[0].add_run(k)
        c0.paragraphs[0].paragraph_format.space_after = Pt(0)
        r0.bold = True
        r0.font.name = "Calibri"
        r0.font.size = Pt(8.8)
        r0.font.color.rgb = NAVY

        r1 = c1.paragraphs[0].add_run(v)
        c1.paragraphs[0].paragraph_format.space_after = Pt(0)
        r1.font.name = "Calibri"
        r1.font.size = Pt(8.8)
        r1.font.color.rgb = DARK_TEXT

    sp2 = doc.add_paragraph()
    sp2.paragraph_format.space_after = Pt(2)


def _load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = (
        [r"C:\Windows\Fonts\calibrib.ttf", r"C:\Windows\Fonts\arialbd.ttf"]
        if bold
        else [r"C:\Windows\Fonts\calibri.ttf", r"C:\Windows\Fonts\arial.ttf"]
    )
    for fp in candidates:
        if Path(fp).exists():
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def render_performance_chart(perf: dict, out_path: Path) -> None:
    """Bangkitkan grafik batang latensi p95 (1/5/10 pengunjung bersamaan) vs SLA langsung dari JSON."""
    w, h = 1400, 760
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = _load_font(28, bold=True)
    f_sub = _load_font(18, bold=False)
    f_axis = _load_font(17, bold=True)
    f_tick = _load_font(16, bold=False)
    f_val = _load_font(16, bold=True)
    f_leg = _load_font(18, bold=True)

    draw.rectangle([(0, 0), (w, 96)], fill=(27, 54, 93))
    draw.text((40, 22), "Simulasi Beban Pengunjung (1, 5, & 10 Orang Bersamaan) — Kecepatan Halaman", fill=(255, 255, 255), font=f_title)
    draw.text(
        (40, 58),
        "Target: https://gorpermatabadminton.com  |  104 Kali Akses Total  |  0% Gagal Muat  |  Sumber: performance-metrics.json",
        fill=(203, 213, 224),
        font=f_sub,
    )

    left, top, right, bottom = 120, 165, 1330, 620
    y_max = 6000.0

    def y_px(val: float) -> int:
        return int(bottom - (val / y_max) * (bottom - top))

    for tick in range(0, 6001, 1000):
        yp = y_px(tick)
        draw.line([(left, yp), (right, yp)], fill=(226, 232, 240), width=1)
        draw.text((left - 14, yp), f"{tick:,}".replace(",", "."), fill=(74, 85, 104), font=f_tick, anchor="rm")
    draw.line([(left, top), (left, bottom), (right, bottom)], fill=(100, 116, 139), width=2)
    draw.text((left - 14, top - 22), "Waktu Muat 95% Akses (ms)", fill=(27, 54, 93), font=f_axis, anchor="lb")

    for threshold, label_txt, col in [
        (3000.0, "Batas Ideal Jadwal /booking (3.000 ms / 3 detik)", (185, 28, 28)),
        (1500.0, "Batas Ideal Halaman Lain (1.500 ms / 1,5 detik)", (217, 119, 6)),
    ]:
        yt = y_px(threshold)
        for x0 in range(left, right, 22):
            draw.line([(x0, yt), (min(x0 + 12, right), yt)], fill=col, width=3)
        draw.text((left + 14, yt - 8), label_txt, fill=col, font=f_val, anchor="lb")

    tiers = perf["http_concurrency"]["tiers"]
    routes_meta = [
        ("/", "Beranda (/)", (59, 130, 246)),
        ("/booking", "Jadwal (/booking)", (220, 38, 38)),
        ("/login", "Login (/login)", (22, 163, 74)),
        ("/fasilitas/lapangan", "Fasilitas", (124, 58, 237)),
    ]

    group_w = (right - left) / len(tiers)
    bar_w = 52
    gap = 16

    for g_idx, tier in enumerate(tiers):
        cx = left + group_w * (g_idx + 0.5)
        draw.text((cx, bottom + 22), f"Tahap {chr(65+g_idx)}: {tier['vus']} Pengunjung ({tier['rps']} req/s)", fill=(27, 54, 93), font=f_axis, anchor="mt")
        total_w = len(routes_meta) * bar_w + (len(routes_meta) - 1) * gap
        x_start = cx - total_w / 2

        for r_idx, (r_key, _, col) in enumerate(routes_meta):
            matched_key = next(k for k in tier["per_route"] if (k == r_key or (r_key == "/booking" and k.startswith("/booking"))))
            p95_val = float(tier["per_route"][matched_key]["p95_ms"])
            x1 = int(x_start + r_idx * (bar_w + gap))
            x2 = x1 + bar_w
            y1 = y_px(p95_val)
            draw.rectangle([(x1, y1), (x2, bottom)], fill=col)

            txt_col = (185, 28, 28) if (r_key == "/booking" and p95_val > 3000) else (30, 41, 59)
            draw.text(((x1 + x2) // 2, y1 - 8), f"{p95_val:.0f}", fill=txt_col, font=f_val, anchor="mb")

    draw.rounded_rectangle([(820, 118), (1325, 160)], radius=8, fill=(254, 242, 242), outline=(185, 28, 28), width=2)
    draw.text((1072, 139), "IR-GOR-07: Saat 10 orang bersamaan, /booking = 5.314 ms (5,3 detik)", fill=(185, 28, 28), font=f_val, anchor="mm")

    lx = 260
    ly = 695
    for _, r_label, col in routes_meta:
        draw.rectangle([(lx, ly - 10), (lx + 24, ly + 10)], fill=col)
        draw.text((lx + 34, ly), r_label, fill=(30, 41, 59), font=f_leg, anchor="lm")
        lx += 245

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out_path), format="PNG", optimize=True)


def add_screenshot_gallery(doc: Document) -> None:
    items = [
        ("01_home_desktop.png", "Gambar 1. Halaman Utama Website di Layar Laptop (TC-BB-01)", 8.0),
        ("02_booking_grid_desktop.png", "Gambar 2. Tabel Jadwal Lapangan — Nama Pelanggan Lain Disamarkan [TERISI] (TC-BB-03)", 8.0),
        ("03_booking_modal_desktop.png", "Gambar 3. Formulir Pop-Up Pesan Lapangan di Layar Laptop (TC-BB-06)", 5.6),
        ("06_login_page.png", "Gambar 4. Halaman Login Pengurus & Pengaman Form CSRF (TC-BB-20)", 8.0),
        ("04_register_404.png", "Gambar 5. Bukti Bug IR-GOR-01: Halaman Daftar (/register) Rusak 404 Not Found (TC-BB-02)", 8.0),
        ("05_invalid_date_500.png", "Gambar 6. Bukti Bug IR-GOR-06: Input Tanggal Rusak Menyebabkan Server Error 500 (TC-BB-05)", 8.0),
        ("07_home_mobile.png", "Gambar 7. Bukti Bug IR-GOR-10: Menu Atas di Layar HP (390px) Terpotong ke Kanan (TC-BB-21)", 4.6),
        ("08_booking_modal_mobile.png", "Gambar 8. Formulir Pesan Lapangan Tampil Rapi di Layar HP 390px (TC-BB-21)", 4.6),
        ("09_slot_confirmed_rtbc.png", "Gambar 9. Tampilan Kotak Biru 'RTBC' Setelah Status Pesanan Dikonfirmasi Admin (TC-BB-23)", 8.0),
        ("10_popup_booking_confirmed_rtbc.png", "Gambar 10. Pop-Up Pesan 'SUDAH DIKONFIRMASI' Saat Kotak 'RTBC' Diklik (TC-BB-23)", 8.0),
        ("11_past_date_2020_bug.png", "Gambar 11. Bukti Bug IR-GOR-05: Tanggal Masa Lalu (1 Jan 2020) Masih Bisa Dibooking (TC-BB-04)", 8.0),
        ("12_performance_latency_chart.png", "Gambar 12. Grafik Bukti IR-GOR-07: Lonjakan Waktu Muat /booking Saat 10 Orang Bersamaan (TC-PERF-10)", 8.0),
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
            set_cell_margins(c_img, top=75, bottom=55, left=75, right=75)
            set_cell_margins(c_cap, top=55, bottom=55, left=75, right=75)
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
            rc.font.size = Pt(8.1)
            rc.font.color.rgb = NAVY

        sp = doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(2)


def _extract_int(text: str, pattern: str, default: str = "?") -> str:
    m = re.search(pattern, text)
    return m.group(1) if m else default


def format_bb_row(case: dict[str, Any]) -> tuple[str, str, str, str, str]:
    """Terjemahkan log JSON test case Black Box menjadi kalimat Indonesia yang jelas bagi pembaca."""
    tc = case["tc_id"]
    actual = case["actual"]
    status = case["status"]

    if tc == "TC-BB-01":
        return (
            tc,
            "Membuka 7 halaman utama website (Beranda, Jadwal, Login, & 4 halaman Fasilitas)",
            "Semua 7 halaman bisa dibuka normal (status 200 OK) tanpa error program.",
            "Semua 7 halaman berhasil dibuka normal dan tidak ada error.",
            status,
        )
    if tc == "TC-BB-02":
        return (
            tc,
            "Membuka halaman pendaftaran anggota (/register)",
            "Halaman registrasi tampil normal atau mengarahkan ke informasi pendaftaran.",
            "Muncul error 404 Not Found (halaman tidak ditemukan). Dicatat sebagai Bug IR-GOR-01.",
            status,
        )
    if tc == "TC-BB-03":
        slots = _extract_int(actual, r"slot_count=(\d+)")
        dt = _extract_int(actual, r"jumpDate=(\d{4}-\d{2}-\d{2})")
        return (
            tc,
            f"Memilih jadwal tanggal besok ({dt})",
            "Kolom tanggal menampilkan tanggal besok & tombol pesan '+' tersedia.",
            f"Tanggal cocok ({dt}) dan tersedia {slots} slot kosong siap dipesan.",
            status,
        )
    if tc == "TC-BB-04":
        slots = _extract_int(actual, r"^(\d+)\s+slot")
        return (
            tc,
            "Membuka jadwal tanggal masa lalu (1 Januari 2020)",
            "Slot tanggal yang sudah lewat seharusnya terkunci (0 slot aktif).",
            f"Masih ada {slots} tombol pesan '+' yang aktif dan bisa diklik. Dicatat sebagai Bug IR-GOR-05.",
            status,
        )
    if tc == "TC-BB-05":
        return (
            tc,
            "Memasukkan format tanggal rusak (?start_date=invalid-date)",
            "Website menolak dengan rapi atau kembali ke tanggal hari ini (bukan crash).",
            "Website mengalami crash dengan layar error 500 Server Error. Dicatat sebagai Bug IR-GOR-06.",
            status,
        )
    if tc == "TC-BB-06":
        return (
            tc,
            "Klik slot kosong '+' untuk membuka formulir pemesanan",
            "Formulir muncul dengan durasi awal 1 jam dan harga Rp 40.000.",
            "Formulir terbuka rapi, durasi otomatis 1 jam, dan total harga tepat Rp 40.000.",
            status,
        )
    if tc == "TC-BB-07":
        return (
            tc,
            "Mengubah pilihan durasi main dari 1 sampai 5 jam",
            "Total harga otomatis bertambah kelipatan Rp 40.000 per jam.",
            "Harga tampil akurat: Rp 40.000 (1 jam) hingga Rp 200.000 (5 jam).",
            status,
        )
    if tc == "TC-BB-08":
        return (
            tc,
            "Klik 'Booking Sekarang' saat Nama dan No. WA kosong",
            "Sistem menolak sebelum mengirim dan memunculkan pesan peringatan.",
            "Muncul peringatan wajib isi lengkap dan tidak ada data yang dikirim ke server.",
            status,
        )
    if tc == "TC-BB-09":
        return (
            tc,
            "Mengisi Nama hanya spasi ('   ') atau 1 huruf ('A')",
            "Sistem seharusnya menolak nama yang hanya berisi spasi atau terlalu singkat.",
            "Nama spasi & 1 huruf malah lolos pengecekan formulir (berhasil dicegat pengaman uji). Bug IR-GOR-03.",
            status,
        )
    if tc == "TC-BB-10":
        return (
            tc,
            "Mengisi No. WA sembarangan ('12345' dan huruf 'abc')",
            "Sistem menolak dengan peringatan format nomor WhatsApp salah.",
            "Kedua input salah ditolak langsung dengan pesan perbaikan format nomor WA.",
            status,
        )
    if tc == "TC-BB-11":
        return (
            tc,
            "Uji batas minimal: No. WA kurang dari 11 digit (10 digit: 081234567)",
            "Nomor terlalu pendek ditolak sebelum dikirim.",
            "Ditolak dengan peringatan format WA belum benar (tidak mengirim ke server).",
            status,
        )
    if tc == "TC-BB-12":
        return (
            tc,
            "Uji batas minimal sah: No. WA tepat 11 digit (0812345678)",
            "Nomor 11 digit diterima oleh validasi formulir.",
            "Lolos validasi formulir dan berhenti aman di pencegat uji (0 masuk ke server).",
            status,
        )
    if tc == "TC-BB-13":
        return (
            tc,
            "Uji batas maksimal sah: No. WA tepat 14 digit (0812345678901)",
            "Nomor 14 digit diterima oleh validasi formulir.",
            "Lolos validasi formulir dan berhenti aman di pencegat uji (0 masuk ke server).",
            status,
        )
    if tc == "TC-BB-14":
        return (
            tc,
            "Uji batas maksimal: No. WA lebih dari 14 digit (15 digit)",
            "Nomor terlalu panjang ditolak sebelum dikirim.",
            "Ditolak dengan peringatan format WA belum benar (tidak mengirim ke server).",
            status,
        )
    if tc == "TC-BB-15":
        return (
            tc,
            "Memasukkan No. WA diawali '8...' dan '628...'",
            "Keduanya otomatis dirapikan menjadi format 628... dan lolos.",
            "Kedua format awalan '8...' dan '628...' berhasil lolos validasi (dicegat aman sebelum server).",
            status,
        )
    if tc == "TC-BB-16":
        return (
            tc,
            "Memasukkan No. WA umum '+62 08123456789' (ada angka 0 setelah +62)",
            "Sistem semestinya merapikan menjadi 628123456789 agar bisa dipakai.",
            "Gagal dirapikan (menjadi 6208...) sehingga nomor valid ditolak. Dicatat sebagai Bug IR-GOR-02.",
            status,
        )
    if tc == "TC-BB-17":
        return (
            tc,
            "Memilih jam 22:00 dengan durasi 3 jam (selesai pukul 01:00 dini hari)",
            "Sistem menolak karena GOR tutup pukul 00:00 (24:00).",
            "Muncul peringatan penolakan 'GOR Permata tutup jam 00.00' dan tidak dikirim.",
            status,
        )
    if tc == "TC-BB-18":
        return (
            tc,
            "Memilih jam 22:00 dengan durasi 2 jam (selesai tepat pukul 00:00)",
            "Batas jam tutup tepat 00:00 diperbolehkan.",
            "Diizinkan lolos oleh aturan jam operasional (berhenti aman di pencegat uji).",
            status,
        )
    if tc == "TC-BB-19":
        return (
            tc,
            "Menutup formulir pesan lapangan lalu membukanya kembali",
            "Formulir tertutup dan isian nama/nomor WA sebelumnya terhapus bersih.",
            "Formulir tertutup normal dan seluruh kolom input kembali kosong.",
            status,
        )
    if tc == "TC-BB-20":
        return (
            tc,
            "Memeriksa halaman login pengurus (/login) dengan input kosong/format salah",
            "Ada pengaman token formulir (CSRF) dan email kosong/salah ditolak browser.",
            "Token pengaman aktif dan validasi browser menolak email kosong, salah format, maupun password kosong.",
            status,
        )
    if tc == "TC-BB-21":
        return (
            tc,
            "Memeriksa tampilan website pada ukuran layar HP (390 x 844 pixel)",
            "Semua tombol menu atas & formulir pesan muat penuh tanpa terpotong layar HP.",
            "Formulir pesan di HP muat rapi (lebar 350 px), tetapi menu atas di beranda memotong tulisan LOGIN & mendorong tombol BOOKING keluar layar (posisi 489 px). Bug IR-GOR-10.",
            status,
        )
    if tc == "TC-BB-22":
        total = _extract_int(actual, r"total_slot_terisi=(\d+)")
        return (
            tc,
            "Memeriksa keamanan kode HTML publik halaman jadwal (/booking)",
            "Nomor HP dan nama lengkap pemesan tidak boleh disimpan di kode halaman publik.",
            f"Ditemukan {total} kotak jadwal menyisipkan atribut data nomor HP & nama pemesan di kode halaman publik. Dicatat sebagai Bug IR-GOR-04.",
            status,
        )
    if tc == "TC-BB-23":
        cnt = _extract_int(actual, r"rtbc_count=(\d+)")
        return (
            tc,
            "Klik kotak biru jadwal yang sudah dikonfirmasi (sampel klub 'RTBC')",
            "Muncul kotak pesan dialog bahwa pesanan sudah dikonfirmasi oleh admin.",
            f"Ditemukan {cnt} slot 'RTBC'; saat diklik muncul pop-up bertuliskan 'Halo Kak [MEMBER] RTBC, bookingan Anda SUDAH DIKONFIRMASI...'.",
            status,
        )
    return tc, case["name"], case["expected"], actual, status


def format_perf_row(case: dict[str, Any]) -> tuple[str, str, str, str, str]:
    """Terjemahkan log JSON test case Performance menjadi kalimat Indonesia mudah dibaca."""
    tc = case["tc_id"]
    status = case["status"]

    mapping = {
        "TC-PERF-01": (
            "Kecepatan buka Halaman Utama pertama kali di laptop",
            "Respon awal server <= 800 ms (0,8 detik), mulai tampil <= 3.000 ms (3 detik).",
            "Respon awal server sempat melonjak ke 2.618,3 ms (2,6 detik) dan halaman baru mulai tampil di 3.028 ms (3 detik). Dicatat sebagai IR-GOR-09.",
        ),
        "TC-PERF-02": (
            "Kecepatan buka Halaman Jadwal (/booking) pertama kali di laptop",
            "Respon awal server <= 1.800 ms, mulai tampil <= 3.000 ms.",
            "Respon awal server 1.213 ms (1,2 detik), mulai tampil di 1.712 ms, dan selesai muat penuh dalam 1,83 detik.",
        ),
        "TC-PERF-03": (
            "Kecepatan buka halaman Login dan Fasilitas di laptop",
            "Respon awal server <= 800 ms, mulai tampil <= 3.000 ms.",
            "Sangat cepat: Login merespons dalam 98,9 ms (selesai 0,69 detik) dan Fasilitas dalam 95,9 ms (selesai 0,71 detik).",
        ),
        "TC-PERF-04": (
            "Perbandingan buka pertama kali vs buka ulang (cache browser aktif)",
            "Kunjungan kedua harus jauh lebih cepat dan tidak ada gambar/aset gagal muat.",
            "Halaman utama membaik drastis dari 3,34 detik menjadi 0,29 detik; halaman jadwal dari 1,83 detik menjadi 1,16 detik (0 aset gagal).",
        ),
        "TC-PERF-05": (
            "Kecepatan buka Halaman Utama & Jadwal melalui layar HP (390 x 844)",
            "Beranda <= 800 ms, Jadwal <= 1.800 ms, dan pergeseran tata letak minimal (CLS <= 0,25).",
            "Di HP, Beranda merespons dalam 108,2 ms (tampil 0,71 detik) dan Jadwal 1.016,5 ms (tampil 1,58 detik) tanpa pergeseran layar (CLS = 0).",
        ),
        "TC-PERF-06": (
            "Pemeriksaan berat ukuran halaman & kompresi data (/booking)",
            "Ukuran kode HTML halaman sebelum dikompresi idealnya <= 500 KB.",
            "Ukuran HTML mentah /booking mencapai 535,37 KB (sedikit di atas 500 KB karena jadwal 7 hari dimuat sekaligus), walau kompresi jaringan menekan jadi 34,78 KB. Dicatat sebagai IR-GOR-08.",
        ),
        "TC-PERF-07": (
            "Kecepatan respons klik tombol di layar (buka modal, ubah durasi, pilih tanggal)",
            "Setiap interaksi tombol di browser terasa instan (<= 250 ms).",
            "Sangat responsif: buka formulir hanya 62,93 ms dan hitung ulang total harga hanya 8,11 ms rata-rata.",
        ),
        "TC-PERF-08": (
            "Simulasi 1 orang mengakses 4 halaman berulang kali (24 kali akses)",
            "0% gagal muat; 95% akses beranda <= 1,5 detik dan /booking <= 3 detik.",
            "Semua 24 akses berhasil (0% error); 95% akses /booking selesai dalam 1,03 detik.",
        ),
        "TC-PERF-09": (
            "Simulasi 5 orang membuka bersamaan (40 kali akses)",
            "0% gagal muat; 95% akses beranda <= 1,5 detik dan /booking <= 3 detik.",
            "Semua 40 akses berhasil (0% error); halaman /booking masih aman di 2,25 detik (2.249,31 ms).",
        ),
        "TC-PERF-10": (
            "Simulasi 10 orang membuka bersamaan saat jam ramai (40 kali akses)",
            "0% gagal muat; 95% akses /booking tidak melebihi batas 3 detik (3.000 ms).",
            "Semua 40 akses tetap berhasil (0% error), tetapi halaman /booking melambat drastis menjadi 5,31 detik (p95 = 5.314,28 ms). Dicatat sebagai IR-GOR-07.",
        ),
    }
    scen, exp, act = mapping[tc]
    return tc, scen, exp, act, status


def build_report() -> tuple[Path, Path]:
    bb = json.loads(BB_JSON_PATH.read_text(encoding="utf-8"))
    perf = json.loads(PERF_JSON_PATH.read_text(encoding="utf-8"))
    render_performance_chart(perf, SCREENSHOT_DIR / "12_performance_latency_chart.png")

    doc = Document()
    configure_styles(doc)
    add_title_banner(doc, bb["timestamp"], perf["metadata"]["timestamp"])

    # BAB I
    add_section_heading(doc, "I.", "Ringkasan Mudah & Kepatuhan Standar ISO/IEC/IEEE 29119-2:2021")
    add_callout_box(
        doc,
        "Kesimpulan Utama Pengujian Non-Destruktif (17 November 2026)",
        [
            f"1. Uji Fungsi Fitur Website (Black Box Testing): Dari {bb['total_cases']} skenario yang diuji otomatis, "
            f"{bb['passed']} skenario berjalan normal (PASS) dan {bb['failed_or_defect_repro']} skenario berhasil mengungkap cacat/kelemahan nyata (FAIL), "
            f"dengan 0 error pemrograman konsol serta {bb['network_posts_sent_to_server']} data uji masuk ke server "
            f"(seluruh {bb['intercepted_post_attempts_inside_browser']} simulasi klik kirim ditahan aman di browser).",
            f"2. Uji Kecepatan & Kapasitas (Performance Testing): Dari {len(perf['test_cases'])} pengujian kecepatan dan beban pengunjung (1, 5, hingga 10 orang bersamaan), "
            f"{sum(1 for c in perf['test_cases'] if c['status'] == 'PASS')} skenario memenuhi batas nyaman (PASS) dan "
            f"{sum(1 for c in perf['test_cases'] if c['status'] == 'FAIL')} skenario melambat/kelebihan ukuran dokumen, "
            "namun seluruh 104 kali akses tetap stabil dengan 0,0% kegagalan server.",
            "3. Ringkasan Temuan Masalah: Sebanyak 10 temuan resmi (kode IR-GOR-01 s.d. IR-GOR-10) telah dicatat lengkap bersama bukti visual "
            "(12 gambar/grafik) agar mudah ditindaklanjuti pengelola maupun developer website.",
        ],
    )

    add_callout_box(
        doc,
        "Panduan Singkat Membaca Istilah di Laporan Ini",
        [
            "• Kenapa ada hasil tertulis FAIL? Dalam dokumen QA, skenario uji ditulis mengharapkan perilaku website yang sempurna. Jika ditemukan bug (misalnya menu terpotong di HP atau halaman error), statusnya ditulis FAIL sebagai tanda bahwa tim penguji berhasil membuktikan adanya masalah di website.",
            "• Black Box vs Performance Testing: Black Box menguji fungsi tombol, formulir, dan aturan jam tutup dari sisi pengguna; Performance Testing mengukur seberapa cepat halaman muncul saat diakses normal maupun saat ramai bersamaan (hingga 10 pengunjung serentak / VUs).",
            "• Istilah Kecepatan: TTFB = waktu tunggu sampai server mulai merespons; FCP = waktu tampilan pertama muncul di layar; p95 = kecepatan terburuk yang dialami oleh 95% pengunjung tercepat.",
        ],
        bg_hex=HEX_WARN_BG,
        border_hex=HEX_WARN_BORDER,
    )

    doc.add_page_break()
    add_sub_heading(doc, "1.1 Batasan Ruang Lingkup Aman & Peta Kelengkapan Dokumen (ISO 29119-2)")
    add_bullet(
        doc,
        "Kepatuhan Standar dengan Batasan Aman (Tailored Conformance — Clause 4.1.3): ",
        "Seluruh tahapan kerja mengikuti ISO/IEC/IEEE 29119-2:2021 (Clause 6, 7.2–7.4, dan 8.2–8.5). Pengecualian disengaja hanya pada pemesanan beneran (POST /bookings/store), panel admin internal, dan uji beban di atas 10 pengguna agar jadwal usaha UMKM GOR Permata tidak terganggu.",
    )
    iso_rows = [
        ("Clause 4 & 6", "Kebijakan & Aturan Uji Tim", "01-standar-ieee-iso/organizational-test-specification.md"),
        ("Clause 7.2", "Rencana Uji Utama & Rencana Uji Kecepatan", "02-.../test-plan-gor-permata.md & performance-test-plan.md"),
        ("Clause 8.2 (Model)", "Peta Skenario & Hal yang Harus Diuji (Edisi 2021)", "02-.../test-model-blackbox.md & test-model-performance.md"),
        ("Clause 8.2 (Kasus)", "Daftar Lengkap Kasus Uji & Langkah Otomasi", "03-.../test-case-blackbox.md, test-case-performance.md, automation-scripts/"),
        ("Clause 8.3", "Catatan Kesiapan Komputer & Data Uji Bebas Privasi", "03-.../test-environment-dan-data.md & test-data/*.json"),
        ("Clause 8.4", "Rekaman Hasil Uji Mentah, JSON, & 12 Gambar Bukti", "03-.../test-execution-log.md & evidence/"),
        ("Clause 8.5", "Laporan Resmi 10 Masalah / Bug (IR-GOR-01..10)", "03-.../incident-reports.md"),
        ("Clause 7.3 & 7.4", "Laporan Kontrol Progres & Penutupan Pengujian", "03-.../test-status-and-control-report.md & test-completion-report.md"),
    ]
    add_styled_table(
        doc,
        headers=("Bagian ISO 29119-2", "Penjelasan Isi Dokumen (Bahasa Sederhana)", "Lokasi Berkas di Repositori GitHub"),
        rows=iso_rows,
        col_widths_cm=(3.2, 6.8, 7.2),
        font_size=8.5,
    )

    # BAB II
    add_section_heading(doc, "II.", "Perencanaan Uji, Hal Paling Berisiko, & Referensi Ilmiah (Clause 7.2)")
    add_bullet(
        doc,
        "Bagian Website yang Diuji: ",
        "Mencakup seluruh halaman publik (/, /booking, /login, /register, /fasilitas/*), aturan perhitungan harga & validasi nomor WhatsApp di dalam halaman /booking, kekuatan kecepatan saat diakses ramai, serta kerapian tampilan Laptop vs HP.",
    )
    add_bullet(
        doc,
        "Landasan Jurnal Terakreditasi SINTA 2–3: ",
        "Seluruh metode uji didukung 7 berkas PDF jurnal ilmiah SINTA 2–3 (Alirridlo dkk. 2025, Pratala dkk. 2020 untuk alur percabangan kode; Yulistina dkk. 2020, Nurudin dkk. 2019, Putri & Susanto 2024 untuk teknik Black Box BVA/EP; Seputra dkk. 2024, Fhonna dkk. 2026 untuk integrasi & otomasi E2E; serta Zahra & Kraugusteeliana 2023, Putra dkk. 2026 untuk uji kecepatan & Playwright).",
    )

    risk_rows = [
        ("PR-01 (Fungsi)", "Nomor WhatsApp salah tolak (misal +62 08...) atau panjang digit keliru", "Tinggi (9)", "Uji batas panjang digit 10/11/14/15 & variasi awalan nomor"),
        ("PR-02 (Fungsi)", "Alamat tanggal jadwal dimanipulasi menjadi tanggal rusak atau masa lalu", "Tinggi (9)", "Uji tanggal 2020-01-01 dan format invalid-date lalu catat efeknya"),
        ("PR-03 (Performa)", "Halaman jadwal berat & melambat saat dibuka banyak pelanggan bersamaan", "Sedang-Tinggi (6)", "Ukur kecepatan muat browser & simulasi 1, 5, dan 10 pengunjung"),
        ("PR-04 / PR-05 (Data)", "Nama diisi spasi saja, link /register rusak, & nomor WA terlihat di kode HTML", "Sedang (6)", "Uji spasi kosong, buka /register, & cek atribut data-phone di HTML"),
        ("PJ-01 / PJ-02 (Aman)", "Uji coba merusak jadwal asli pemilik GOR Permata atau membebani server", "Terkendali (8/6)", "Cegat pengiriman form di browser (0 masuk server) & batasi maks 10 VUs"),
    ]
    add_styled_table(
        doc,
        headers=("Kode & Jenis Risiko", "Hal yang Dikhawatirkan Terjadi", "Tingkat Risiko", "Cara Tim Menguji & Mencegah Dampak"),
        rows=risk_rows,
        col_widths_cm=(3.2, 6.2, 2.4, 5.4),
        center_cols=(2,),
    )

    # BAB III
    add_section_heading(doc, "III.", "Kondisi Komputer Penguji & Keamanan Privasi Pelanggan (Clause 8.3)")
    env_rows = [
        ("Perangkat & Alat Uji", "Windows 10/11 x64, Python 3.9.10, Chrome Otomatis (Playwright 1.60.0), dan aiohttp 3.13.5", "SIAP (READY)"),
        ("Dukungan Cypress", "Node.js v24.14.0 terpasang; biner Cypress tidak terpasang lokal sehingga seluruh skrip dijalankan via Playwright", "Alternatif Playwright"),
        ("Data Uji Buatan (Non-PII)", "Memakai data fiktif (seperti nama 'Test QA' & WA buatan) agar bebas kebocoran data pribadi", "SIAP (READY)"),
        ("Beda Uji vs Asli (8.3.4.2 c)", "Pengguna asli menyimpan pesanan ke database; pada pengujian ini pengiriman diblokir pengaman uji agar jadwal asli aman", "Terdokumentasi"),
    ]
    add_styled_table(
        doc,
        headers=("Komponen Uji", "Penjelasan Kondisi Saat Pengujian Berjalan", "Status"),
        rows=env_rows,
        col_widths_cm=(4.0, 10.4, 2.8),
        center_cols=(2,),
    )

    # BAB IV
    add_section_heading(
        doc,
        "IV.",
        f"Hasil Uji Fungsi Website — {bb['total_cases']} Skenario Black Box (Clause 8.2 & 8.4)",
        page_break_before=True,
    )
    p_bb = doc.add_paragraph(
        f"Sebanyak {bb['total_cases']} kasus uji dijalankan otomatis lewat skrip test_gor_permata.py pada {bb['timestamp']}. "
        f"Hasilnya tercatat {bb['passed']} PASS dan {bb['failed_or_defect_repro']} FAIL "
        f"(FAIL di sini menandakan skenario berhasil membuktikan adanya bug/cacat pada website). Total simulasi pengiriman form yang ditahan di browser adalah "
        f"{bb['intercepted_post_attempts_inside_browser']} kali, sehingga data uji yang benar-benar masuk ke server GOR Permata adalah {bb['network_posts_sent_to_server']}."
    )
    p_bb.paragraph_format.space_after = Pt(4)

    bb_rows = [format_bb_row(c) for c in bb["cases"]]
    add_styled_table(
        doc,
        headers=("Kode Uji", "Apa yang Diuji di Website", "Seharusnya Bagaimana?", "Kenyataan yang Terlihat di Website", "Status"),
        rows=bb_rows,
        col_widths_cm=(1.8, 4.1, 4.2, 5.7, 1.4),
        center_cols=(0, 4),
        font_size=8.2,
    )

    # BAB V
    add_section_heading(doc, "V.", "Hasil Uji Kecepatan & Beban Pengunjung — 10 Skenario Performance", page_break_before=True)
    p_pf = doc.add_paragraph(
        f"Pengujian kecepatan dilakukan pada {perf['metadata']['timestamp']} memakai dua cara: mengukur langsung waktu tampil halaman di Chrome "
        "pada laptop & HP, serta melakukan simulasi pengunjung serentak (1, 5, dan 10 orang membuka halaman bersamaan, hanya membaca halaman / GET-only)."
    )
    p_pf.paragraph_format.space_after = Pt(4)

    perf_tc_rows = [format_perf_row(c) for c in perf["test_cases"]]
    add_styled_table(
        doc,
        headers=("Kode Uji", "Pengujian Kecepatan yang Dilakukan", "Target Batas Nyaman", "Hasil Terukur di Lapangan", "Status"),
        rows=perf_tc_rows,
        col_widths_cm=(2.0, 4.1, 3.8, 5.9, 1.4),
        center_cols=(0, 4),
        font_size=8.2,
    )

    add_sub_heading(doc, "5.1 Perbandingan Kecepatan Tampil di Browser Laptop vs HP (dalam milidetik / ms)")
    cd = perf["browser"]["cold_desktop"]
    wd = perf["browser"]["warm_desktop"]
    cm = perf["browser"]["cold_mobile"]
    vitals_rows = []
    for label, d in [
        ("Laptop - Buka Pertama / (Beranda)", cd["/"]),
        ("Laptop - Buka Pertama /booking (Jadwal)", cd["/booking"]),
        ("Laptop - Buka Pertama /login", cd["/login"]),
        ("Laptop - Buka Pertama /fasilitas/lapangan", cd["/fasilitas/lapangan"]),
        ("Laptop - Buka Ulang / (Cache Aktif)", wd["/"]),
        ("Laptop - Buka Ulang /booking (Cache Aktif)", wd["/booking"]),
        ("HP (390x844) - Buka Pertama / (Beranda)", cm["/"]),
        ("HP (390x844) - Buka Pertama /booking", cm["/booking"]),
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
        headers=("Kondisi & Halaman", "Respon Awal", "Siap DOM", "Selesai Muat", "Tampil Awal", "Geser Layar", "Ukuran Asli / Kompresi"),
        rows=vitals_rows,
        col_widths_cm=(5.2, 1.8, 1.7, 1.8, 1.8, 1.4, 3.5),
        center_cols=(1, 2, 3, 4, 5, 6),
        font_size=8.2,
    )

    inter = perf["browser"]["client_interactions"]
    add_bullet(
        doc,
        "Kecepatan Respon Klik Tombol di Browser (/booking): ",
        f"Membuka formulir pesan butuh {inter['openBooking_ms']} ms (0,06 detik), hitung ulang harga butuh rata-rata {inter['updateTotal_avg_ms']} ms "
        f"(maksimal {inter['updateTotal_max_ms']} ms), dan memilih tanggal hanya {inter['changeDate_reload_ms']} ms — semuanya jauh lebih cepat dari batas 250 ms.",
    )

    add_sub_heading(doc, "5.2 Simulasi Banyak Pengunjung Membuka Halaman Secara Bersamaan (1, 5, & 10 Orang)")
    conc_rows = []
    for tier in perf["http_concurrency"]["tiers"]:
        for route, st in tier["per_route"].items():
            short_r = "/booking" if route.startswith("/booking") else route
            conc_rows.append(
                (
                    f"{tier['vus']} Pengunjung ({tier['rps']} akses/detik)",
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
        headers=("Jumlah Pengunjung", "Halaman", "Akses", "Gagal", "Rata-rata", "Tengah (p50)", "95% Akses (p95)", "Terlama"),
        rows=conc_rows,
        col_widths_cm=(3.8, 2.5, 1.0, 1.6, 2.0, 2.0, 2.2, 2.1),
        center_cols=(2, 3, 4, 5, 6, 7),
        font_size=8.1,
    )

    # BAB VI
    add_section_heading(doc, "VI.", "Daftar 10 Masalah Ditemukan & Saran Perbaikannya (Clause 8.5)", page_break_before=True)
    ir_rows = [
        ("IR-GOR-01 (BUG-01)", "TC-BB-02", "Major / Medium", "Open", "Halaman /register menampilkan error 404 (tidak ada).", "Buat halaman pendaftaran anggota atau arahkan tombol daftar langsung ke Admin WA."),
        ("IR-GOR-02 (BUG-02)", "TC-BB-16", "Minor / Medium", "Open", "Nomor WA format '+62 08...' ditolak sistem karena menjadi 6208...", "Hapus angka '0' setelah '62' secara otomatis sebelum sistem memeriksa format nomor."),
        ("IR-GOR-03 (BUG-03)", "TC-BB-09", "Minor / Low", "Open", "Nama pemesan bisa diisi spasi kosong '   ' atau hanya 1 huruf.", "Tambahkan pembersih spasi (.trim()) dan wajibkan minimal 2 huruf untuk nama pemesan."),
        ("IR-GOR-04 (BUG-04)", "TC-BB-22", "Major / High", "Open", "Kode halaman publik menyertakan 205 data nomor HP & nama pemesan.", "Hapus nomor HP & data pribadi dari tampilan publik; tampilkan hanya status 'Terisi'."),
        ("IR-GOR-05", "TC-BB-04", "Major / High", "Open", "Tanggal masa lalu (2020-01-01) masih memunculkan 612 slot bisa dipesan.", "Kunci pilihan tanggal agar hanya hari ini dan ke depan yang tombol pesannya aktif."),
        ("IR-GOR-06", "TC-BB-05", "Major / High", "Open", "Menulis format tanggal rusak di alamat URL memicu error server 500.", "Tangani tanggal tidak valid dengan aman agar otomatis kembali ke jadwal hari ini."),
        ("IR-GOR-07", "TC-PERF-10", "Major / High", "Open", "Saat 10 orang membuka bersamaan, /booking melambat hingga 5,31 detik.", "Pasang indeks database dan cache singkat (15–30 detik) pada tabel jadwal publik."),
        ("IR-GOR-08", "TC-PERF-06", "Minor / Medium", "Open", "Ukuran kode HTML mentah /booking mencapai 535,37 KB (memuat banyak hari).", "Tampilkan maksimal 1–3 hari terlebih dahulu atau muat jadwal lewat API ringan."),
        ("IR-GOR-09", "TC-PERF-01", "Minor / Medium", "Open", "Akses awal ke Beranda sempat lambat (2,62 detik) sebelum cache tersimpan.", "Aktifkan caching halaman beranda di server atau CDN agar buka awal selalu cepat."),
        ("IR-GOR-10", "TC-BB-21", "Minor / Medium", "Open", "Di layar HP (390 px), menu LOGIN terpotong dan tombol BOOKING tergeser keluar.", "Gunakan menu lipat (hamburger menu) untuk tampilan layar kecil/smartphone."),
    ]
    add_styled_table(
        doc,
        headers=("ID Masalah", "Uji Pemicu", "Dampak / Prioritas", "Status", "Penjelasan Masalah yang Ditemukan", "Saran Perbaikan Sederhana"),
        rows=ir_rows,
        col_widths_cm=(2.5, 1.7, 2.2, 1.2, 4.9, 4.7),
        center_cols=(1, 3),
        font_size=8.0,
    )

    add_sub_heading(doc, "6.1 Galeri Bukti Visual Pengujian (12 Gambar & Grafik Terverifikasi)")
    add_screenshot_gallery(doc)

    # BAB VII
    add_section_heading(doc, "VII.", "Penilaian Kualitas Keseluruhan (ISO 25010:2023) & Penutupan Uji", page_break_before=True)
    iso25_rows = [
        ("1. Ketepatan Fungsi (Functional Suitability)", "7 halaman utama & hitungan tarif 1–5 jam akurat; kendala ada di /register 404, format WA +62 08..., tanggal lampau, dan tanggal rusak error 500.", "Ada Defect"),
        ("2. Kecepatan & Efisiensi (Performance Efficiency)", "Klik tombol sangat cepat (62,93 ms) & 0% gagal di 104 akses, namun ukuran HTML /booking besar (535 KB) & melambat di 10 orang bersamaan (5,31 detik).", "Perlu Optimasi"),
        ("3. Kesesuaian Perangkat (Compatibility)", "Tampilan di laptop dan pop-up booking di HP sudah rapi; perbaikan diperlukan di bar menu atas beranda saat dibuka di HP.", "Perlu Perbaikan"),
        ("4. Kemudahan Pakai (Interaction Capability)", "Alur pesan lapangan simpel & otomatis mengosongkan kolom saat ditutup; tinggal tambahkan tolakan untuk nama kosong spasi.", "Cukup"),
        ("5. Keandalan (Reliability)", "Website tidak pernah down (0% error saat uji beban 1–10 orang) dan tombol kirim aman menonaktifkan klik ganda saat memproses.", "Baik"),
        ("6. Keamanan & Privasi (Security)", "Token pengaman form (CSRF) aktif, tetapi 4 header pengaman standar masih absen dan 205 data nomor WA terlihat di HTML publik.", "Perlu Hardening"),
        ("7. Kemudahan Perawatan (Maintainability)", "Kode JavaScript (7.473 karakter) masih digabung langsung di satu file halaman /booking; lebih baik dipisah.", "Cukup"),
        ("8. Fleksibilitas Akses (Flexibility)", "Langsung berjalan di browser HP dan laptop tanpa perlu instalasi aplikasi tambahan.", "Memadai"),
        ("9. Keamanan Aturan (Safety — Baru 2023)", "Batasan jam operasional hingga 00:00 malam terbukti bekerja akurat mencegah pesanan yang melebihi jam tutup.", "Diterapkan & PASS"),
    ]
    add_styled_table(
        doc,
        headers=("Aspek Kualitas ISO/IEC 25010:2023", "Penilaian Praktis Berdasarkan Hasil Pengujian", "Status"),
        rows=iso25_rows,
        col_widths_cm=(4.8, 9.5, 2.9),
        center_cols=(2,),
        font_size=8.3,
    )

    add_sub_heading(doc, "7.1 Ringkasan Kontrol Pengujian & Persetujuan Penutupan (Clause 7.3–7.4)")
    add_bullet(
        doc,
        "Penyesuaian Selama Pengujian (Control Directives CD-01..04): ",
        "(1) Menyesuaikan kompresi HTTP agar uji beban berjalan lancar; (2) Menambahkan jeda animasi 350 ms & sensor nama pelanggan [TERISI] sebelum screenshot; "
        "(3) Memperluas pemeriksaan posisi tombol menu HP sehingga bug kepotong terdeteksi otomatis; (4) Menambah uji tanggal masa lalu dan tanggal rusak.",
    )
    add_bullet(
        doc,
        "Pemenuhan Syarat Selesai & Kebersihan Sistem (TC1–TC4): ",
        f"Seluruh rencana Black Box ({bb['total_cases']}/{bb['total_cases']}) dan Performance ({len(perf['test_cases'])}/{len(perf['test_cases'])}) selesai dijalankan "
        f"dengan {bb['network_posts_sent_to_server']} pesanan palsu masuk ke database asli GOR Permata. Seluruh 12 gambar bukti, log hasil, dan laporan resmi sudah tersimpan rapi di GitHub main.",
    )
    add_bullet(
        doc,
        "Langkah Akademik Berikutnya: ",
        "Setelah seluruh pengujian teknis (Folder 01–03 & Laporan Folder 05) selesai dan terdokumentasi lengkap, kelompok siap melanjutkan tahap wawancara 1 praktisi QA pada Folder 04.",
    )

    sign_rows = [
        ("Muhammad Faiz Rabbani (231011402539)", "Anggota Tim QA", "Disetujui & Sinkron", "18 Nov 2026"),
        ("Robi Farhan Anshori (231011401468)", "Anggota Tim QA", "Disetujui & Sinkron", "18 Nov 2026"),
        ("Dzikri Attariq Samayaki (221011401148)", "Anggota Tim QA", "Disetujui & Sinkron", "18 Nov 2026"),
        ("Nurlaelasari (231011403531)", "Anggota Tim QA", "Disetujui & Sinkron", "18 Nov 2026"),
        ("Asep Erlan Maulana, S.Kom., M.Kom", "Dosen Pengampu Mata Kuliah", "Menunggu Asesmen", "—"),
    ]
    add_styled_table(
        doc,
        headers=("Nama / NIM", "Peran dalam Kelompok", "Status", "Tanggal"),
        rows=sign_rows,
        col_widths_cm=(6.2, 5.2, 3.4, 2.4),
        center_cols=(2, 3),
        font_size=8.7,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT_DOCX))

    import win32com.client  # type: ignore

    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        wdoc = word.Documents.Open(str(OUT_DOCX.resolve()))
        try:
            wdoc.Fields.Update()
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
