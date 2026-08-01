import easyocr 
reader = easyocr.Reader(['en'], gpu=False)


def extract_text(image_path: str) -> str:
    """
    Extracts text from an image using EasyOCR.
    """

    result = reader.readtext(image_path, detail=0)

    extracted_text= "\n".join(result)
    
    return extracted_text