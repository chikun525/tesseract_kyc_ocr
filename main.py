import cv2
import pytesseract
from extractors import extract_fields, extract_address_from_back
import re

def ocr_image(img_path, lang='eng+ori+hin'):
    img = cv2.imread(img_path)
    if img is None:
        return ""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, lang=lang)
    return text

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Aadhaar OCR KYC Extraction (handles scenario logic)')
    parser.add_argument('images', nargs='+', help='Aadhaar image path(s): front [back]')
    args = parser.parse_args()

    front_ocr = ""
    back_ocr = ""

    if len(args.images) == 2:
        front_ocr = ocr_image(args.images[0])
        back_ocr = ocr_image(args.images[1])
    elif len(args.images) == 1:
        temp_ocr = ocr_image(args.images[0])
        # Try extracting address first
        address = extract_address_from_back(temp_ocr)
        if address and address != "NA":
            back_ocr = temp_ocr
            front_ocr = ""
        else:
            front_ocr = temp_ocr
            back_ocr = ""

    print('--- OCR RAW OUTPUT (FRONT) ---\n', front_ocr)
    print('\n--- OCR RAW OUTPUT (BACK) ---\n', back_ocr)

    fields = extract_fields(front_ocr, back_ocr)
    print('\n--- EXTRACTED FIELDS ---')
    for k, v in fields.items():
        print(f"{k}: {v}")

if __name__ == '__main__':
    main()