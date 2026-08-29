import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

from src.exporter import export_to_text, export_to_markdown, export_to_pdf, clean_markdown_for_plain_text


def test_clean_markdown():
    sample_md = "## Experience\n**Software Engineer** at *Company*\n- Built [API](https://api.com)"
    cleaned = clean_markdown_for_plain_text(sample_md)
    assert "##" not in cleaned
    assert "**" not in cleaned
    assert "https://api.com" not in cleaned
    assert "Software Engineer at Company" in cleaned


def test_export_to_markdown(tmp_path):
    output_file = tmp_path / "resume.md"
    sample_text = "# Alex Chen\nBackend Developer"
    
    saved_path = export_to_markdown(sample_text, output_file)
    assert saved_path.exists()
    assert saved_path.read_text(encoding="utf-8") == sample_text


def test_export_to_text(tmp_path):
    output_file = tmp_path / "resume.txt"
    sample_text = "# Alex Chen\n**Skills**: Python"
    
    saved_path = export_to_text(sample_text, output_file)
    assert saved_path.exists()
    content = saved_path.read_text(encoding="utf-8")
    assert "#" not in content
    assert "**" not in content


def test_export_to_pdf(tmp_path):
    output_file = tmp_path / "cover_letter.pdf"
    sample_text = "Dear Hiring Manager,\nI am excited to apply for the role."
    
    saved_path = export_to_pdf(sample_text, output_file, title="Cover Letter")
    assert saved_path.exists()
    assert saved_path.stat().st_size > 0