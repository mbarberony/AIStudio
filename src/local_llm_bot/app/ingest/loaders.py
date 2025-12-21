from __future__ import annotations

import fnmatch
import logging
import warnings
from dataclasses import dataclass
from pathlib import Path

from ..config import DEFAULT_XLSX_MAX_CELLS

SUPPORTED_EXTS = {".txt", ".md", ".pdf", ".docx", ".pptx", ".xlsx"}

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
        return _extract_xlsx(path, max_cells=DEFAULT_XLSX_MAX_CELLS)
    if ext == ".pdf":
        return _extract_pdf(path)
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
    try:
        from pypdf import PdfReader  # type: ignore
        from pypdf.errors import PdfReadError  # type: ignore
    except Exception:
        return ExtractResult(ok=False, text="", reason="missing_dep:pypdf")

    try:
        reader = PdfReader(str(path))
        if getattr(reader, "is_encrypted", False):
            # Skip encrypted PDFs by design
            return ExtractResult(ok=False, text="", reason="encrypted_pdf")

        parts: list[str] = []
        for page in reader.pages:
            t = (page.extract_text() or "").strip()
            if t:
                parts.append(t)

        text = "\n".join(parts).strip()
        if not text:
            return ExtractResult(ok=False, text="", reason="empty")

        # guardrail: avoid raw PDF bytes ever making it through
        if text.lstrip().startswith("%PDF-"):
            return ExtractResult(ok=False, text="", reason="pdf_bytes_detected")

        return ExtractResult(ok=True, text=text, reason="")
    except PdfReadError:
        return ExtractResult(ok=False, text="", reason="pdf_read_error")
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
