import PyPDF2
import docx
from PIL import Image
import pytesseract
from io import BytesIO

def extract_text(file_upload):
    file_type = file_upload.name.lower()
    content = file_upload.read()
    file_upload.seek(0)

    if file_type.endswith('.pdf'):
        reader = PyPDF2.PdfReader(BytesIO(content))
        return " ".join([page.extract_text() or "" for page in reader.pages])

    elif file_type.endswith('.docx'):
        doc = docx.Document(BytesIO(content))
        return "\n".join([p.text for p in doc.paragraphs])

    elif file_type.endswith(('.png', '.jpg', '.jpeg')):
        img = Image.open(BytesIO(content))
        lang = __import__('os').environ.get('OCR_LANG', 'eng')
        return pytesseract.image_to_string(img, lang=lang)

    else:
        return content.decode("utf-8", errors="ignore")