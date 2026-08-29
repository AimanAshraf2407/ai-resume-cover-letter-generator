import os
import re
from pathlib import Path
from fpdf import FPDF


class DocumentPDF(FPDF):
    """Custom PDF class with clean margins and headers."""
    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, "Generated via AI Resume & Cover Letter Generator", align="R")
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def clean_markdown_for_plain_text(markdown_text: str) -> str:
    """Strips Markdown syntax (headers, bold, italics, links) for clean text rendering."""
    text = re.sub(r"#+\s*", "", markdown_text)          # Strip # headers
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)       # Strip bold
    text = re.sub(r"\*([^*]+)\*", r"\1", text)           # Strip italics
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text) # Strip links [text](url) -> text
    text = re.sub(r"`([^`]+)`", r"\1", text)             # Strip inline code
    return text.strip()


def export_to_text(content: str, output_path: str | Path) -> Path:
    """Exports raw content or Markdown as clean plain text."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    cleaned = clean_markdown_for_plain_text(content)
    with open(path, "w", encoding="utf-8") as f:
        f.write(cleaned)
    return path


def export_to_markdown(content: str, output_path: str | Path) -> Path:
    """Exports content directly as a Markdown (.md) file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def export_to_pdf(content: str, output_path: str | Path, title: str = "Document") -> Path:
    """Converts text content into a formatted, downloadable PDF."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    cleaned_text = clean_markdown_for_plain_text(content)

    pdf = DocumentPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(left=15, top=15, right=15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Document Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(w=0, h=10, text=title, align="L")
    pdf.ln(12)

    # Document Body
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    
    # Usable width on A4 page with 15mm margins
    usable_width = pdf.epw 

    for raw_line in cleaned_text.split("\n"):
        safe_line = raw_line.encode("latin-1", "replace").decode("latin-1")
        if not safe_line.strip():
            pdf.ln(3)
        else:
            pdf.multi_cell(w=usable_width, h=6, text=safe_line)

    pdf.output(str(path))
    return path