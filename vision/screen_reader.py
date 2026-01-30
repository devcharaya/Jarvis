import pytesseract
import pyautogui
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def read_screen():
    try:
        screenshot = pyautogui.screenshot()
        img = np.array(screenshot)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Enhance UI text
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray = cv2.convertScaleAbs(gray, alpha=1.6, beta=15)

        # Get OCR data with positions
        data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT, config='--oem 3 --psm 11')

        words = []

        for i in range(len(data['text'])):
            text = data['text'][i].strip()
            conf = int(data['conf'][i])

            if conf > 40 and len(text) > 1:  # ignore junk
                x = data['left'][i]
                y = data['top'][i]
                words.append((y, x, text))

        # Sort like human reading order
        words.sort(key=lambda k: (k[0], k[1]))

        # Combine into lines
        lines = []
        current_line_y = -1
        line = []

        for y, x, text in words:
            if current_line_y == -1 or abs(y - current_line_y) < 20:
                line.append(text)
                current_line_y = y
            else:
                lines.append(" ".join(line))
                line = [text]
                current_line_y = y

        if line:
            lines.append(" ".join(line))

        return "\n".join(lines)

    except Exception as e:
        return f"OCR error: {e}"
