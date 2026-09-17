"""
ReaderAgent — Download e extração de texto de PDFs acadêmicos.

Pipeline:
  1. Tenta download do PDF (arXiv → Semantic Scholar → DOI)
  2. Extrai texto com pdfplumber
  3. Salva markdown em data/papers/markdown/
  4. Retorna texto estruturado
"""

import os
import re
import hashlib
from pathlib import Path

import requests
import pdfplumber


class ReaderAgent:
    """
    Baixa PDFs acadêmicos e extrai texto completo para markdown.
    """

    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent / "data" / "papers"
        self.pdf_dir = self.base_dir / "pdfs"
        self.md_dir = self.base_dir / "markdown"

        self.pdf_dir.mkdir(parents=True, exist_ok=True)
        self.md_dir.mkdir(parents=True, exist_ok=True)

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "OpenClaw/1.0 (Research Agent; mailto:research@openclaw.local)"
        })

    def read_paper(self, paper: dict) -> dict:
        """
        Pipeline completo: download → extração → texto estruturado.

        Args:
            paper: dict com ao menos 'url' ou 'doi'

        Returns:
            dict com 'text' (markdown), 'success', 'error', 'pdf_path', 'md_path'
        """
        url = paper.get("url", "")
        doi = paper.get("doi", "")
        title = paper.get("title", "untitled")

        pdf_path = self._download(url, doi)
        if not pdf_path:
            return {"text": "", "success": False, "error": "Download failed", "title": title}

        md_text = self._extract(pdf_path)
        if not md_text:
            return {"text": "", "success": False, "error": "Extraction failed", "title": title}

        # Salva markdown
        md_path = self.md_dir / f"{Path(pdf_path).stem}.md"
        with open(md_path, "w") as f:
            f.write(f"# {title}\n\n{md_text}")

        return {
            "text": md_text,
            "success": True,
            "pdf_path": str(pdf_path),
            "md_path": str(md_path),
            "title": title,
        }

    # ---- Download ----

    def _download(self, url: str, doi: str = "") -> Path | None:
        """Tenta baixar PDF de múltiplas fontes."""
        candidates = []

        if url and url.endswith(".pdf"):
            candidates.append(url)
        if "arxiv.org" in url:
            pdf_url = url.replace("/abs/", "/pdf/").replace("/html/", "/pdf/")
            if not pdf_url.endswith(".pdf"):
                pdf_url += ".pdf"
            candidates.append(pdf_url)
        elif "arxiv.org" in url:
            arxiv_id = self._extract_arxiv_id(url)
            if arxiv_id:
                candidates.append(f"https://arxiv.org/pdf/{arxiv_id}.pdf")
        if doi:
            candidates.append(f"https://doi.org/{doi}")

        for candidate in candidates:
            try:
                path = self._try_download(candidate)
                if path:
                    return path
            except Exception:
                continue

        return None

    def _try_download(self, url: str) -> Path | None:
        resp = self.session.get(url, timeout=30, stream=True)
        if resp.status_code != 200:
            return None

        content_type = resp.headers.get("Content-Type", "")
        if "text/html" in content_type and not url.endswith(".pdf"):
            return None

        # Gera nome único pelo hash da URL
        fname = hashlib.sha256(url.encode()).hexdigest()[:16] + ".pdf"
        path = self.pdf_dir / fname

        with open(path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)

        # Verifica se é PDF válido
        if path.stat().st_size < 1000:
            path.unlink(missing_ok=True)
            return None

        return path

    # ---- Extração ----

    def _extract(self, pdf_path: Path) -> str:
        """Extrai texto do PDF usando pdfplumber."""
        text_pages = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text() or ""
                    if page_text.strip():
                        text_pages.append(f"--- Page {i + 1} ---\n{page_text}")
        except Exception as e:
            print(f"[Reader] PDF extraction error: {e}")
            return ""

        return "\n\n".join(text_pages)

    # ---- Helpers ----

    @staticmethod
    def _extract_arxiv_id(url: str) -> str | None:
        match = re.search(r"arxiv\.org/(?:abs|pdf|html)/(\d+\.\d+)", url)
        return match.group(1) if match else None

    def stats(self) -> dict:
        return {
            "pdfs_cached": len(list(self.pdf_dir.glob("*.pdf"))),
            "markdown_cached": len(list(self.md_dir.glob("*.md"))),
            "pdf_dir": str(self.pdf_dir),
            "md_dir": str(self.md_dir),
        }
