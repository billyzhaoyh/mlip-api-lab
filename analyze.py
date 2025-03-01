try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import time


def read_image(uri):
    maxRetries = 10
    res_text = pytesseract.image_to_string(Image.open(uri))
    if res_text:
        return res_text
    else:
        return "error"
    