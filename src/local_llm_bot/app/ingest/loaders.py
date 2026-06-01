# Version: 1.0.0
# Changelog: 1.0.0 — AIStudio_733: first version header on loaders.py.
#            AIStudio_817: table-aware HTML/iXBRL extraction. Data <table> elements are
#            normalized to GFM markdown pipe-tables (colspan/rowspan expanded into a
#            rectangular grid, empty gutter rows/cols pruned, lone currency-symbol cells
#            merged into the adjacent value) and spliced into the text in document order
#            before get_text() flattening. Layout/decorative tables (the majority) fail the
#            data-table test and fall through to get_text() exactly as before. Shared,
#            format-agnostic back-half (_grid_to_markdown / _grid_is_data_table) is reusable
#            by future per-format grid extractors (xlsx/docx/pptx/pdf) — see
#            NOTES - AIStudio - Table Extraction Strategy - 2026-05-31.
from __future__ import annotations

import fnmatch
import logging
import warnings
from dataclasses import dataclass
from pathlib import Path

# from ..config import DEFAULT_XLSX_MAX_CELLS
from local_llm_bot.app.config import CONFIG

SUPPORTED_EXTS = {".txt", ".md", ".pdf", ".docx", ".pptx", ".xlsx", ".htm", ".html", ".xhtml"}

# Silence noisy PDF parsing logs/warnings (common with imperfect PDFs)
logging.getLogger("pypdf").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", module="pypdf")


@dataclass(frozen=True)
class ExtractResult:
    ok: bool
    text: str = ""
    reason: str = ""  # empty if ok, otherwise a short failure label


def should_skip_filename(name: str) -> bool:
    return name.startswith("~$") or name == ".DS_Store"


def is_excluded(path: Path, patterns: list[str]) -> bool:
    s = str(path)
    return any(fnmatch.fnmatch(s, pat) for pat in patterns)


def extract_text(path: Path) -> ExtractResult:
    ext = path.suffix.lower()
    if ext in {".txt", ".md"}:
        return _extract_txt_md(path)
    if ext == ".docx":
        return _extract_docx(path)
    if ext == ".pptx":
        return _extract_pptx(path)
    if ext == ".xlsx":
        return _extract_xlsx(path, max_cells=CONFIG.ingest.xlsx_max_cells)
    if ext == ".pdf":
        return _extract_pdf(path)
    if ext in {".htm", ".html", ".xhtml"}:
        return _extract_html(path)
    return ExtractResult(ok=False, text="", reason="unsupported_ext")


def _extract_txt_md(path: Path) -> ExtractResult:
    try:
        t = path.read_text(encoding="utf-8", errors="ignore").strip()
        if not t:
            return ExtractResult(ok=False, text="", reason="empty")
        return ExtractResult(ok=True, text=t, reason="")
    except Exception as e:
        return ExtractResult(ok=False, text="", reason=f"read_error:{type(e).__name__}")


def _extract_docx(path: Path) -> ExtractResult:
    try:
        from docx import Document as DocxDocument  # type: ignore
    except Exception:
        return ExtractResult(ok=False, text="", reason="missing_dep:python-docx")

    try:
        doc = DocxDocument(str(path))
        parts: list[str] = []

        for p in doc.paragraphs:
            t = (p.text or "").strip()
            if t:
                parts.append(t)

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    t = (cell.text or "").strip()
                    if t:
                        parts.append(t)

        text = "\n".join(parts).strip()
        if not text:
            return ExtractResult(ok=False, text="", reason="empty")
        return ExtractResult(ok=True, text=text, reason="")
    except Exception as e:
        return ExtractResult(ok=False, text="", reason=f"parse_error:{type(e).__name__}")


def _extract_pptx(path: Path) -> ExtractResult:
    try:
        from pptx import Presentation  # type: ignore
    except Exception:
        return ExtractResult(ok=False, text="", reason="missing_dep:python-pptx")

    try:
        prs = Presentation(str(path))
        parts: list[str] = []

        for slide in prs.slides:
            for shape in slide.shapes:
                # Text frames
                if hasattr(shape, "text") and shape.text:
                    t = str(shape.text).strip()
                    if t:
                        parts.append(t)

                # Tables
                if hasattr(shape, "has_table") and shape.has_table:
                    tbl = shape.table
                    for row in tbl.rows:
                        for cell in row.cells:
                            t = (cell.text or "").strip()
                            if t:
                                parts.append(t)

        text = "\n".join(parts).strip()
        if not text:
            return ExtractResult(ok=False, text="", reason="empty")
        return ExtractResult(ok=True, text=text, reason="")
    except Exception as e:
        return ExtractResult(ok=False, text="", reason=f"parse_error:{type(e).__name__}")


def _extract_xlsx(path: Path, max_cells: int) -> ExtractResult:
    try:
        import openpyxl  # type: ignore
    except Exception:
        return ExtractResult(ok=False, text="", reason="missing_dep:openpyxl")

    try:
        wb = openpyxl.load_workbook(filename=str(path), read_only=True, data_only=True)
        parts: list[str] = []
        scanned = 0
        partial = False

        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                for v in row:
                    scanned += 1
                    if scanned > max_cells:
                        partial = True
                        break
                    if v is None:
                        continue
                    s = str(v).strip()
                    if s:
                        parts.append(s)
                if partial:
                    break
            if partial:
                break

        wb.close()
        text = "\n".join(parts).strip()
        if not text:
            return ExtractResult(ok=False, text="", reason="empty")
        if partial:
            return ExtractResult(ok=True, text=text, reason="partial:cell_cap")
        return ExtractResult(ok=True, text=text, reason="")
    except Exception as e:
        return ExtractResult(ok=False, text="", reason=f"parse_error:{type(e).__name__}")


def _extract_pdf(path: Path) -> ExtractResult:
    """
    Extract PDF text with page boundary markers using pdfplumber.
    Each page is prefixed with [PAGE_N] so downstream chunking can
    store page numbers in Qdrant payload for click-to-source citation.
    Falls back to pypdf if pdfplumber is unavailable.
    """
    try:
        import pdfplumber  # type: ignore

        parts: list[str] = []
        with pdfplumber.open(str(path)) as pdf:
            if not pdf.pages:
                return ExtractResult(ok=False, text="", reason="empty")
            for page_num, page in enumerate(pdf.pages, 1):
                t = (page.extract_text() or "").strip()
                if t:
                    parts.append(f"[PAGE_{page_num}]\n{t}")

        text = "\n\n".join(parts).strip()
        if not text:
            return ExtractResult(ok=False, text="", reason="empty")
        if text.lstrip().startswith("%PDF-"):
            return ExtractResult(ok=False, text="", reason="pdf_bytes_detected")
        return ExtractResult(ok=True, text=text, reason="")

    except ImportError:
        pass  # fall through to pypdf
    except Exception as e:
        return ExtractResult(ok=False, text="", reason=f"parse_error:{type(e).__name__}")

    # Fallback: pypdf (no page markers)
    try:
        from pypdf import PdfReader  # type: ignore
        from pypdf.errors import PdfReadError  # type: ignore
    except Exception:
        return ExtractResult(ok=False, text="", reason="missing_dep:pypdf")

    try:
        reader = PdfReader(str(path))
        if getattr(reader, "is_encrypted", False):
            return ExtractResult(ok=False, text="", reason="encrypted_pdf")

        parts = []
        for page in reader.pages:
            t = (page.extract_text() or "").strip()
            if t:
                parts.append(t)

        text = "\n".join(parts).strip()
        if not text:
            return ExtractResult(ok=False, text="", reason="empty")
        if text.lstrip().startswith("%PDF-"):
            return ExtractResult(ok=False, text="", reason="pdf_bytes_detected")
        return ExtractResult(ok=True, text=text, reason="")
    except PdfReadError:
        return ExtractResult(ok=False, text="", reason="pdf_read_error")
    except Exception as e:
        return ExtractResult(ok=False, text="", reason=f"parse_error:{type(e).__name__}")


# ── Table normalization (AIStudio_817) ───────────────────────────────────────
# Format-agnostic back-half: _grid_to_markdown / _grid_is_data_table operate on an
# abstract 2-D grid of cell strings and know nothing about HTML. The HTML-specific
# part is only _html_table_to_grid (colspan/rowspan expansion). Future per-format
# extractors (xlsx iter_rows, docx/pptx .rows[].cells[]) produce a grid and reuse the
# same back-half. See NOTES - AIStudio - Table Extraction Strategy - 2026-05-31 §3.

_CURRENCY_SYMBOLS = {"$", "€", "£", "¥"}


def _grid_put(matrix: list[list[str]], r: int, c: int, value: str) -> None:
    while len(matrix) <= r:
        matrix.append([])
    row = matrix[r]
    while len(row) <= c:
        row.append("")
    row[c] = value


def _grid_rectangularize(matrix: list[list[str]]) -> list[list[str]]:
    width = max((len(r) for r in matrix), default=0)
    for r in matrix:
        while len(r) < width:
            r.append("")
    return matrix


def _html_table_to_grid(table) -> list[list[str]]:
    """Expand an HTML <table> (with colspan/rowspan) into a rectangular cell matrix."""
    matrix: list[list[str]] = []
    carry: dict[tuple[int, int], str] = {}  # (row, col) -> text held by a rowspan
    for r, tr in enumerate(table.find_all("tr")):
        if len(matrix) <= r:
            matrix.append([])
        c = 0
        for cell in tr.find_all(["td", "th"], recursive=False):
            while (r, c) in carry:
                _grid_put(matrix, r, c, carry.pop((r, c)))
                c += 1
            style = (cell.get("style") or "").replace(" ", "").lower()
            text = "" if "display:none" in style else cell.get_text(" ", strip=True)
            colspan = int(cell.get("colspan", 1) or 1)
            rowspan = int(cell.get("rowspan", 1) or 1)
            for dc in range(colspan):
                val = text if dc == 0 else ""
                _grid_put(matrix, r, c + dc, val)
                for dr in range(1, rowspan):
                    carry[(r + dr, c + dc)] = val
            c += colspan
    return _grid_rectangularize(matrix)


def _grid_prune(grid: list[list[str]]) -> list[list[str]]:
    """Drop fully-empty rows and columns (spacer rows + gutter columns)."""
    grid = [r for r in grid if any(x.strip() for x in r)]
    if not grid:
        return grid
    keep = [c for c in range(len(grid[0])) if any(r[c].strip() for r in grid)]
    return [[r[c] for c in keep] for r in grid]


def _grid_merge_currency(grid: list[list[str]]) -> list[list[str]]:
    """Merge a lone currency-symbol cell into the next non-empty cell in its row."""
    out: list[list[str]] = []
    for r in grid:
        nr, i = [], 0
        while i < len(r):
            cur = r[i].strip()
            if cur in _CURRENCY_SYMBOLS and i + 1 < len(r) and r[i + 1].strip():
                nr.append(f"{cur}{r[i + 1].strip()}")
                i += 2
            else:
                nr.append(r[i])
                i += 1
        out.append(nr)
    return _grid_rectangularize(out)


def _grid_is_data_table(grid: list[list[str]]) -> bool:
    """True only for real data grids: >=2x2 non-empty with at least one numeric cell.
    Layout/decorative tables fail this and fall through to get_text()."""
    if len(grid) < 2 or (grid and len(grid[0]) < 2):
        return False
    nonempty = sum(1 for r in grid for x in r if x.strip())
    numeric = sum(1 for r in grid for x in r if any(ch.isdigit() for ch in x))
    return nonempty >= 4 and numeric >= 1


def _grid_to_markdown(grid: list[list[str]]) -> str:
    """Render a grid as a GFM pipe-table (first row = header). Emits all rows."""
    head = grid[0]
    lines = ["| " + " | ".join(head) + " |",
             "| " + " | ".join(["---"] * len(head)) + " |"]
    for r in grid[1:]:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def _table_to_markdown(table) -> str | None:
    """Normalize one HTML <table> to markdown, or None if it is not a data table."""
    grid = _grid_merge_currency(_grid_prune(_html_table_to_grid(table)))
    if not _grid_is_data_table(grid):
        return None
    return _grid_to_markdown(grid)


def _extract_html(path: Path) -> ExtractResult:
    try:
        from bs4 import BeautifulSoup  # type: ignore
    except Exception:
        return ExtractResult(ok=False, text="", reason="missing_dep:beautifulsoup4")

    try:
        raw = path.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(raw, "html.parser")
        # Remove scripts, styles, nav boilerplate
        for tag in soup(["script", "style", "nav", "header", "footer", "meta", "link"]):
            tag.decompose()
        # AIStudio_817: convert data tables to markdown IN DOCUMENT ORDER before the
        # get_text() flatten. Each <table> that normalizes to a data grid is replaced
        # in-place by its markdown (wrapped in blank lines so chunking sees one atomic
        # block); layout/decorative tables return None and flatten as before. The
        # parent-None guard skips tables already detached by an outer replacement
        # (nested-table case).
        for table in soup.find_all("table"):
            if table.parent is None:
                continue
            md = _table_to_markdown(table)
            if md:
                table.replace_with("\n\n" + md + "\n\n")
        text = soup.get_text(separator="\n").strip()
        # Collapse excessive blank lines
        import re

        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        if not text:
            return ExtractResult(ok=False, text="", reason="empty")
        return ExtractResult(ok=True, text=text, reason="")
    except Exception as e:
        return ExtractResult(ok=False, text="", reason=f"parse_error:{type(e).__name__}")


# Backward-compatible helper if you already import load_document elsewhere:
@dataclass(frozen=True)
class Document:
    doc_id: str
    source_path: str
    text: str


def load_document(path: Path) -> Document | None:
    if not path.is_file():
        return None
    if should_skip_filename(path.name):
        return None

    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTS:
        return None

    res = extract_text(path)
    if not res.ok or not res.text.strip():
        return None

    return Document(doc_id=str(path.resolve()), source_path=str(path), text=res.text)
