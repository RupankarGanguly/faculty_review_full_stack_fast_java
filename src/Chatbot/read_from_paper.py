"""
OCR text extraction from images using EasyOCR.

Note: First run downloads the model (~100MB). Keep gpu=False for CPU machines.
"""

_reader = None


def _get_reader():
    global _reader
    if _reader is None:
        import easyocr
        _reader = easyocr.Reader(["en"], gpu=False)
    return _reader


def extract_text(image_path: str) -> str:
    """Extracts text from an image using EasyOCR."""
    reader = _get_reader()
    result = reader.readtext(image_path, detail=0)
    return "\n".join(result)
