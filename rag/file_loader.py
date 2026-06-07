from pypdf import PdfReader

def load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():  # skip blank/scanned pages silently
            pages.append(f"[Page {i+1}]\n{text}")
    return "\n\n".join(pages)

import hashlib

def get_file_hash(file_bytes: bytes) -> str:
    # FIX: use SHA-256 — MD5 has collision issues for security-sensitive dedup
    return hashlib.sha256(file_bytes).hexdigest()