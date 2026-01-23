import pytesseract
import pyautogui
from PIL import Image

# SAFETY: hardcode path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def read_screen():
    screenshot = pyautogui.screenshot()
    text = pytesseract.image_to_string(screenshot)
    return text.strip()
