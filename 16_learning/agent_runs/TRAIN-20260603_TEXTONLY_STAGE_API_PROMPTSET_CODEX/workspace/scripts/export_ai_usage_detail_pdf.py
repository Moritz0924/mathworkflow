from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "10_ai_logs/ai_usage_detail.md"
PDF_PATHS = [ROOT / "10_ai_logs/ai_usage_detail.pdf", ROOT / "12_submission/ai_usage_detail.pdf"]


def build_story(text: str):
    styles = getSampleStyleSheet()
    styles["Normal"].fontName = "STSong-Light"
    styles["Heading1"].fontName = "STSong-Light"
    story = []
    for line in text.splitlines():
        if line.startswith("# "):
            story.append(Paragraph(line[2:], styles["Heading1"]))
        elif line.strip():
            story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 6))
    return story


def export_pdf():
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    text = MD_PATH.read_text(encoding="utf-8") if MD_PATH.exists() else "AI 工具使用详情"
    for path in PDF_PATHS:
        path.parent.mkdir(parents=True, exist_ok=True)
        doc = SimpleDocTemplate(str(path), pagesize=A4)
        doc.build(build_story(text))
        print(f"[OK] wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    export_pdf()
