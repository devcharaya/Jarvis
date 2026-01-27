import pytesseract
import pyautogui
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def read_screen():
    # Capture center region instead of full screen
    width, height = pyautogui.size()
    
    region = (
        width // 6,         # x start
        height // 4,        # y start
        width // 1.5,       # width
        height // 2         # height
    )

    screenshot = pyautogui.screenshot(region=region)

    gray = screenshot.convert("L")
    bw = gray.point(lambda x: 0 if x < 150 else 255, '1')

    text = pytesseract.image_to_string(bw)
    return text.strip()