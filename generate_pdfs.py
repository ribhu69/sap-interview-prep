#!/usr/bin/env python3
"""Generate SAP interview prep PDFs from markdown study guides."""

import re
from pathlib import Path
from fpdf import FPDF
from fpdf.enums import XPos, YPos

GUIDES = [
    {
        "input": "study_guides/sap_mm_guide.md",
        "output": "pdfs/SAP_MM_Study_Guide.pdf",
        "title": "SAP MM - Materials Management",
        "subtitle": "Comprehensive Interview Preparation Guide",
        "color": (0, 112, 184),
    },
    {
        "input": "study_guides/sap_ecc_guide.md",
        "output": "pdfs/SAP_ECC_Study_Guide.pdf",
        "title": "SAP ECC - ERP Central Component",
        "subtitle": "Architecture, Configuration & Technical Concepts",
        "color": (0, 150, 90),
    },
    {
        "input": "study_guides/sap_hana_guide.md",
        "output": "pdfs/SAP_HANA_Study_Guide.pdf",
        "title": "SAP HANA & S/4HANA",
        "subtitle": "Migration, Architecture & New Features Guide",
        "color": (220, 80, 30),
    },
]


class SAPGuide(FPDF):
    def __init__(self, title: str, color: tuple):
        super().__init__()
        self.guide_title = title
        self.header_color = color
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(20, 20, 20)

    def header(self):
        r, g, b = self.header_color
        self.set_fill_color(r, g, b)
        self.rect(0, 0, 210, 12, "F")
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 8)
        self.set_xy(0, 2)
        self.cell(0, 8, f"  {self.guide_title}", align="L")
        self.set_text_color(0, 0, 0)
        self.ln(10)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"SAP Interview Prep Guide  |  Page {self.page_no()}", align="C")
        self.set_text_color(0, 0, 0)

    def cover_page(self, title: str, subtitle: str):
        r, g, b = self.header_color
        self.add_page()
        # Background band
        self.set_fill_color(r, g, b)
        self.rect(0, 60, 210, 80, "F")
        # Title
        self.set_font("Helvetica", "B", 26)
        self.set_text_color(255, 255, 255)
        self.set_xy(15, 75)
        self.multi_cell(180, 12, title, align="C")
        # Subtitle
        self.set_font("Helvetica", "", 13)
        self.set_text_color(230, 230, 230)
        self.set_xy(15, 115)
        self.multi_cell(180, 8, subtitle, align="C")
        # Badge
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(r, g, b)
        self.set_fill_color(255, 255, 255)
        self.rect(55, 150, 100, 14, "F")
        self.set_xy(55, 153)
        self.cell(100, 8, "5+ Years Experience | ECC & S/4HANA", align="C")
        # Footer note
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.set_xy(15, 270)
        self.cell(0, 8, "Version 2025  |  Covers SAP ECC 6.0 and S/4HANA 2023/2024", align="C")
        self.set_text_color(0, 0, 0)


def clean_line(line: str) -> str:
    """Strip markdown formatting for PDF rendering and normalize to latin-1."""
    line = re.sub(r"\*\*(.+?)\*\*", r"\1", line)
    line = re.sub(r"\*(.+?)\*", r"\1", line)
    line = re.sub(r"`(.+?)`", r"\1", line)
    line = re.sub(r"_{1,2}(.+?)_{1,2}", r"\1", line)
    line = line.strip()
    # Replace common Unicode chars with ASCII equivalents
    replacements = {
        "—": "-",   # em dash
        "–": "-",   # en dash
        "‘": "'",   # left single quote
        "’": "'",   # right single quote
        "“": '"',   # left double quote
        "”": '"',   # right double quote
        "…": "...", # ellipsis
        "•": "*",   # bullet
        " ": " ",   # non-breaking space
        "→": "->",  # right arrow
        "←": "<-",  # left arrow
        "²": "2",   # superscript 2
        "³": "3",   # superscript 3
        "α": "alpha",
        "β": "beta",
    }
    for uni, asc in replacements.items():
        line = line.replace(uni, asc)
    # Final fallback: encode to latin-1, replacing anything else
    return line.encode("latin-1", errors="replace").decode("latin-1")


def render_table(pdf: FPDF, rows: list[list[str]], color: tuple):
    r, g, b = color
    if not rows:
        return
    col_count = max(len(row) for row in rows)
    available = pdf.w - pdf.l_margin - pdf.r_margin
    col_w = available / col_count

    for i, row in enumerate(rows):
        # Strip | delimiters and separators
        cells = [c.strip() for c in row if not re.match(r"^[-:]+$", c.strip())]
        if not cells:
            continue
        if i == 0:  # Header row
            pdf.set_fill_color(r, g, b)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 8)
        else:
            pdf.set_fill_color(245, 245, 250) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(30, 30, 30)
            pdf.set_font("Helvetica", "", 8)

        x_start = pdf.get_x()
        y_start = pdf.get_y()
        row_h = 6
        # Calculate actual heights needed
        for j, cell in enumerate(cells[:col_count]):
            x = x_start + j * col_w
            text = clean_line(cell)
            lines_needed = max(1, int(len(text) / (col_w / 2.2)) + 1)
            row_h = max(row_h, lines_needed * 5)
        row_h = min(row_h, 20)

        if y_start + row_h > pdf.h - 25:
            pdf.add_page()
            x_start = pdf.get_x()
            y_start = pdf.get_y()

        for j, cell in enumerate(cells[:col_count]):
            x = x_start + j * col_w
            pdf.set_xy(x, y_start)
            fill = (i == 0) or (i % 2 == 0)
            pdf.rect(x, y_start, col_w, row_h, "FD" if fill else "D")
            pdf.set_xy(x + 1, y_start + 1)
            text = clean_line(cell)
            pdf.multi_cell(col_w - 2, 4.5, text, border=0, align="L" if j > 0 else "L")

        pdf.set_xy(x_start, y_start + row_h)
        pdf.set_text_color(0, 0, 0)

    pdf.ln(3)


def parse_and_render(pdf: FPDF, md_path: str, color: tuple):
    content = Path(md_path).read_text(encoding="utf-8")
    lines = content.split("\n")

    in_table = False
    table_rows: list[list[str]] = []
    in_code = False
    code_lines: list[str] = []
    in_qa = False
    qa_text: list[str] = []

    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()

        # Code block
        if line.startswith("```"):
            if not in_code:
                in_code = True
                code_lines = []
            else:
                in_code = False
                r, g, b = color
                pdf.set_fill_color(245, 245, 245)
                pdf.set_draw_color(r, g, b)
                pdf.set_font("Courier", "", 7)
                pdf.set_text_color(30, 30, 60)
                block = "\n".join(code_lines[:30])
                x = pdf.get_x()
                y = pdf.get_y()
                w = pdf.w - pdf.l_margin - pdf.r_margin
                lines_h = min(len(code_lines), 25) * 4.2 + 4
                if y + lines_h > pdf.h - 25:
                    pdf.add_page()
                pdf.rect(pdf.get_x(), pdf.get_y(), w, lines_h, "FD")
                pdf.set_xy(pdf.l_margin + 2, pdf.get_y() + 2)
                for cl in code_lines[:25]:
                    pdf.set_x(pdf.l_margin + 2)
                    cl_safe = clean_line(cl[:90])
                    pdf.cell(w - 4, 4, cl_safe, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.ln(2)
                pdf.set_text_color(0, 0, 0)
                pdf.set_draw_color(0, 0, 0)
            i += 1
            continue

        if in_code:
            code_lines.append(raw)
            i += 1
            continue

        # Table detection
        if "|" in line and not line.startswith(">"):
            if not in_table:
                in_table = True
                table_rows = []
            cells = [c for c in line.split("|") if c.strip()]
            # Skip pure separator rows
            if not all(re.match(r"[-:]+$", c.strip()) for c in cells):
                table_rows.append(cells)
            i += 1
            continue
        else:
            if in_table and table_rows:
                render_table(pdf, table_rows, color)
                in_table = False
                table_rows = []

        # Q&A blockquote
        if line.startswith(">"):
            qa_text.append(line.lstrip("> ").strip())
            i += 1
            continue
        else:
            if qa_text:
                r, g, b = color
                pdf.set_fill_color(r + 200 if r < 56 else 240, 248, 255)
                pdf.set_draw_color(r, g, b)
                w = pdf.w - pdf.l_margin - pdf.r_margin
                block = " ".join(qa_text)
                n_lines = max(1, len(block) // 90) + len(qa_text)
                h = n_lines * 4.5 + 6
                if pdf.get_y() + h > pdf.h - 25:
                    pdf.add_page()
                pdf.rect(pdf.l_margin, pdf.get_y(), w, h, "FD")
                pdf.set_xy(pdf.l_margin + 3, pdf.get_y() + 3)
                pdf.set_font("Helvetica", "I", 8)
                pdf.set_text_color(30, 30, 80)
                for ql in qa_text:
                    ql = clean_line(ql)
                    if ql.startswith("Q:"):
                        pdf.set_font("Helvetica", "BI", 8)
                        pdf.set_text_color(r, g, b)
                        pdf.set_x(pdf.l_margin + 3)
                        pdf.multi_cell(w - 6, 4.5, ql, border=0)
                        pdf.set_font("Helvetica", "I", 8)
                        pdf.set_text_color(30, 30, 80)
                    elif ql.startswith("A:"):
                        pdf.set_x(pdf.l_margin + 3)
                        pdf.multi_cell(w - 6, 4.5, ql, border=0)
                    else:
                        pdf.set_x(pdf.l_margin + 3)
                        pdf.multi_cell(w - 6, 4.5, ql, border=0)
                pdf.ln(3)
                pdf.set_text_color(0, 0, 0)
                pdf.set_draw_color(0, 0, 0)
                qa_text = []

        # Headings
        if line.startswith("# ") and not line.startswith("## "):
            # Skip title line (already on cover)
            i += 1
            continue
        elif line.startswith("## "):
            text = clean_line(line[3:])
            pdf.add_page()
            r, g, b = color
            pdf.set_fill_color(r, g, b)
            pdf.rect(pdf.l_margin, pdf.get_y(), pdf.w - pdf.l_margin - pdf.r_margin, 10, "F")
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(255, 255, 255)
            pdf.set_x(pdf.l_margin + 2)
            pdf.cell(0, 10, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(3)
        elif line.startswith("### "):
            text = clean_line(line[4:])
            pdf.set_font("Helvetica", "B", 11)
            r, g, b = color
            pdf.set_text_color(r, g, b)
            if pdf.get_y() + 8 > pdf.h - 25:
                pdf.add_page()
            pdf.ln(2)
            pdf.cell(0, 7, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_text_color(0, 0, 0)
            # Underline
            y = pdf.get_y()
            pdf.set_draw_color(r, g, b)
            pdf.set_line_width(0.3)
            pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
            pdf.set_line_width(0.2)
            pdf.set_draw_color(0, 0, 0)
            pdf.ln(2)
        elif line.startswith("#### "):
            text = clean_line(line[5:])
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(60, 60, 60)
            pdf.ln(1)
            pdf.cell(0, 6, text, ln=True)
            pdf.set_text_color(0, 0, 0)
        elif line.startswith("- ") or line.startswith("* "):
            text = clean_line(line[2:])
            pdf.set_font("Helvetica", "", 9)
            x = pdf.get_x()
            if pdf.get_y() + 5 > pdf.h - 25:
                pdf.add_page()
            pdf.set_x(pdf.l_margin + 4)
            pdf.cell(4, 5, "*")
            pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 8, 5, text, border=0)
        elif line.startswith("  - ") or line.startswith("  * "):
            text = clean_line(line[4:])
            pdf.set_font("Helvetica", "", 8.5)
            pdf.set_text_color(60, 60, 60)
            if pdf.get_y() + 5 > pdf.h - 25:
                pdf.add_page()
            pdf.set_x(pdf.l_margin + 10)
            pdf.cell(4, 5, "-")
            pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 14, 5, text, border=0)
            pdf.set_text_color(0, 0, 0)
        elif line.startswith("---"):
            r, g, b = color
            pdf.set_draw_color(r, g, b)
            pdf.set_line_width(0.5)
            pdf.line(pdf.l_margin, pdf.get_y() + 3, pdf.w - pdf.r_margin, pdf.get_y() + 3)
            pdf.set_line_width(0.2)
            pdf.set_draw_color(0, 0, 0)
            pdf.ln(6)
        elif line == "":
            pdf.ln(2)
        else:
            text = clean_line(line)
            if text:
                pdf.set_font("Helvetica", "", 9)
                pdf.set_text_color(30, 30, 30)
                if pdf.get_y() + 5 > pdf.h - 25:
                    pdf.add_page()
                pdf.set_x(pdf.l_margin)
                w = pdf.w - pdf.l_margin - pdf.r_margin
                pdf.multi_cell(w, 5, text, border=0)
                pdf.set_text_color(0, 0, 0)

        i += 1

    # Flush any remaining table or qa
    if in_table and table_rows:
        render_table(pdf, table_rows, color)
    if qa_text:
        pdf.set_font("Helvetica", "I", 8)
        for ql in qa_text:
            pdf.multi_cell(0, 5, ql, border=0)


def generate_pdf(guide: dict, base_dir: Path):
    print(f"Generating: {guide['output']} ...")
    pdf = SAPGuide(guide["title"], guide["color"])
    pdf.set_title(guide["title"])
    pdf.set_author("SAP MM Interview Prep")
    pdf.set_creator("SAP Interview Prep Tool")

    pdf.cover_page(guide["title"], guide["subtitle"])

    md_path = base_dir / guide["input"]
    parse_and_render(pdf, str(md_path), guide["color"])

    out_path = base_dir / guide["output"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out_path))
    size_kb = out_path.stat().st_size // 1024
    print(f"  -> Saved {out_path}  ({size_kb} KB)")


if __name__ == "__main__":
    base = Path(__file__).parent
    for guide in GUIDES:
        generate_pdf(guide, base)
    print("\nAll 3 PDFs generated successfully.")
