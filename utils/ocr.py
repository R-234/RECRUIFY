import os

def setup_tesseract():
    tessdata = os.getenv("TESSDATA_PREFIX")
    if tessdata:
        os.environ['TESSDATA_PREFIX'] = tessdata