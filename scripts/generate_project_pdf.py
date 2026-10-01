"""Generate a self-contained PDF from MaxxLoop's current documentation.

This uses only Python's standard library so contributors do not need a PDF
converter installed. Run from the repository root:
    python scripts/generate_project_pdf.py
"""

from __future__ import annotations

import re
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "MaxxLoop_Project_Documentation.pdf"

DOCUMENTS = [
    ("Project Overview", "docs/PROJECT_OVERVIEW.md"),
    ("Product", "docs/PRODUCT.md"),
    ("User Flow", "docs/USER_FLOW.md"),
    ("Architecture", "docs/ARCHITECTURE.md"),
    ("Technical Architecture", "docs/TECHNICAL_ARCHITECTURE.md"),
    ("Frontend", "docs/FRONTEND.md"),
    ("Backend", "docs/BACKEND.md"),
    ("API Reference", "docs/API.md"),
    ("Database", "docs/DATABASE.md"),
    ("Data Model", "docs/DATA_MODEL.md"),
    ("Authentication", "docs/AUTHENTICATION.md"),
    ("The MaxxLoop Loop", "docs/MAXXLOOP_LOOP.md"),
    ("Recommender", "docs/RECOMMENDER.md"),
    ("Insights", "docs/INSIGHTS.md"),
    ("Security", "docs/SECURITY.md"),
    ("Privacy", "docs/PRIVACY.md"),
    ("Testing", "docs/TESTING.md"),
    ("Development", "docs/DEVELOPMENT.md"),
    ("Environment", "docs/ENVIRONMENT.md"),
    ("Deployment", "docs/DEPLOYMENT.md"),
    ("Troubleshooting", "docs/TROUBLESHOOTING.md"),
    ("Hackathon Guide", "docs/HACKATHON_GUIDE.md"),
    ("Demo Script", "docs/DEMO_SCRIPT.md"),
    ("Judge Q&A", "docs/JUDGE_QA.md"),
    ("Limitations", "docs/LIMITATIONS.md"),
    ("Roadmap", "docs/ROADMAP.md"),
]

PAGE_WIDTH, PAGE_HEIGHT = 612, 792  # US Letter points
MARGIN_X, TOP, BOTTOM = 54, 54, 48
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_X * 2
NORMAL_SIZE, LEADING = 9.5, 13


def ascii_text(value: str) -> str:
    replacements = {
        "→": "->", "–": "-", "—": "-", "’": "'", "“": '"', "”": '"',
        "…": "...", "×": "x", "θ": "theta", "α": "alpha", "β": "beta",
        "≥": ">=", "≤": "<=", "•": "*", "✓": "[x]", "⚠": "Note:",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value.encode("latin-1", "replace").decode("latin-1")


def pdf_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def markdown_lines(path: Path):
    in_code = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            in_code = not in_code
            yield ("code_toggle", "")
            continue
        if in_code:
            yield ("code", line)
            continue
        if not line or line == "---":
            yield ("space", "")
            continue
        match = re.match(r"^(#{1,3})\s+(.*)", line)
        if match:
            yield (f"heading{len(match.group(1))}", match.group(2))
            continue
        line = re.sub(r"!?(\[[^]]*\])\([^)]+\)", r"\1", line)
        line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
        line = re.sub(r"`([^`]*)`", r"\1", line)
        if line.startswith("| ") or line.startswith("|"):
            yield ("table", line.replace("|", " | "))
        elif re.match(r"^[-*]\s+", line):
            yield ("bullet", re.sub(r"^[-*]\s+", "", line))
        elif re.match(r"^\d+\.\s+", line):
            yield ("bullet", line)
        elif line.startswith("> "):
            yield ("quote", line[2:])
        else:
            yield ("body", line)


def wrap(text: str, kind: str):
    text = ascii_text(text)
    if kind == "code":
        return textwrap.wrap(text, width=79, replace_whitespace=False) or [""]
    if kind == "table":
        return textwrap.wrap(text, width=89) or [""]
    prefix = "  - " if kind == "bullet" and not re.match(r"^\d+\. ", text) else "  "
    width = 84 if kind in {"body", "bullet", "quote"} else 76
    parts = textwrap.wrap(text, width=width - len(prefix)) or [""]
    return [prefix + parts[0]] + [" " * len(prefix) + part for part in parts[1:]]


def make_stream(page_number: int, content, title: str):
    lines = ["BT", "/F1 8 Tf", "0.35 0.38 0.43 rg", f"{MARGIN_X} 24 Td", f"(MaxxLoop Project Documentation - {pdf_escape(title)}) Tj", "ET"]
    lines += ["BT", "/F1 8 Tf", "0.35 0.38 0.43 rg", f"{PAGE_WIDTH - 74} 24 Td", f"(Page {page_number}) Tj", "ET"]
    for font, size, x, y, color, text in content:
        lines += ["BT", f"/{font} {size} Tf", color, f"{x} {y} Td", f"({pdf_escape(text)}) Tj", "ET"]
    return "\n".join(lines).encode("latin-1")


def paginate():
    pages = []
    current = []
    y = PAGE_HEIGHT - TOP
    doc_title = ""

    def new_page():
        nonlocal current, y
        if current:
            pages.append((doc_title, current))
        current = []
        y = PAGE_HEIGHT - TOP

    def add(font, size, text, color="0 0 0", indent=0, line_height=None):
        nonlocal y
        height = line_height or (size + 4)
        if y - height < BOTTOM:
            new_page()
        current.append((font, size, MARGIN_X + indent, y, color, text))
        y -= height

    # Cover page
    doc_title = "Overview"
    add("F2", 28, "MaxxLoop", "0.03 0.32 0.28", 0, 38)
    add("F2", 16, "Complete Project Documentation", "0.06 0.12 0.20", 0, 28)
    add("F1", 11, "Focus & Recovery / Personal Capacity Learning Loop", "0.25 0.30 0.36", 0, 23)
    y -= 28
    for sentence in [
        "This document is generated from the current repository documentation.",
        "It covers product behavior, architecture, data, authentication, APIs,",
        "local development, deployment gaps, hackathon presentation, and limits.",
        "It describes MaxxLoop as a wellness/productivity prototype, not a medical device.",
    ]:
        add("F1", 11, sentence, "0.12 0.16 0.22", 0, 19)
    y -= 25
    add("F2", 12, "Contents", "0.03 0.32 0.28", 0, 22)
    for index, (name, _) in enumerate(DOCUMENTS, start=1):
        add("F1", 9, f"{index:02d}. {name}", "0.12 0.16 0.22", 12, 13)
    new_page()

    for section_name, relative in DOCUMENTS:
        doc_title = section_name
        path = ROOT / relative
        if not path.exists():
            continue
        for kind, value in markdown_lines(path):
            if kind == "space":
                y -= 5
                continue
            if kind == "code_toggle":
                continue
            if kind.startswith("heading"):
                sizes = {"heading1": 18, "heading2": 13, "heading3": 11}
                size = sizes[kind]
                if y - (size + 12) < BOTTOM:
                    new_page()
                add("F2", size, ascii_text(value), "0.03 0.32 0.28", 0, size + 7)
                continue
            font = "F3" if kind == "code" else "F1"
            size = 8.5 if kind in {"code", "table"} else NORMAL_SIZE
            color = "0.10 0.12 0.16 rg" if kind != "quote" else "0.24 0.30 0.36 rg"
            indent = 8 if kind in {"bullet", "quote"} else 0
            for item in wrap(value, kind):
                add(font, size, item, color, indent, 12 if kind == "code" else LEADING)
    if current:
        pages.append((doc_title, current))
    return pages


def build_pdf(pages):
    objects = []
    # 1 catalog, 2 page tree, 3/4/5 fonts; then page/content pairs
    objects.extend([
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [] /Count 0 >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>",
    ])
    page_ids = []
    for page_number, (section, content) in enumerate(pages, start=1):
        page_id = len(objects) + 1
        content_id = page_id + 1
        stream = make_stream(page_number, content, section)
        page = f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] /Resources << /Font << /F1 3 0 R /F2 4 0 R /F3 5 0 R >> >> /Contents {content_id} 0 R >>".encode("ascii")
        content_obj = b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream"
        objects.extend([page, content_obj])
        page_ids.append(page_id)
    objects[1] = f"<< /Type /Pages /Kids [{' '.join(f'{pid} 0 R' for pid in page_ids)}] /Count {len(page_ids)} >>".encode("ascii")

    result = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, obj in enumerate(objects, start=1):
        offsets.append(len(result))
        result.extend(f"{number} 0 obj\n".encode("ascii"))
        result.extend(obj)
        result.extend(b"\nendobj\n")
    xref = len(result)
    result.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("ascii"))
    for offset in offsets[1:]:
        result.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    result.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("ascii"))
    return bytes(result)


if __name__ == "__main__":
    generated_pages = paginate()
    OUTPUT.write_bytes(build_pdf(generated_pages))
    print(f"Created {OUTPUT} ({len(generated_pages)} pages)")
