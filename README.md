# 📄 Aadhaar OCR KYC Extractor

This project performs OCR (Optical Character Recognition) on scanned Aadhaar card images (front/back) to extract key KYC fields like name, gender, date of birth, Aadhaar number, and address — using **Tesseract OCR** and **OpenCV**, with support for Hindi, Odia, and English languages.

---

## 📁 Directory Structure

```
tesseract_kyc_ocr/
├── main.py                         # Entry point of the program
├── extractors.py                  # Logic to extract fields from OCR
├── crop_utils.py                 # (optional) image cropping utils
├── config/
│   ├── aadhaar.yaml              # Optional regex configs
│   └── birth_certificate_fields.yaml
├── templates/
│   └── aadhaar_uidai_template.png
├── test_images/                  # Aadhaar card samples
├── requirements.txt              # Python dependencies
```

---

## ✅ Prerequisites

1. Python 3.10+
2. Tesseract OCR (version 5+ strongly recommended)

### 🔧 Install Tesseract OCR

**Windows:**
Download from [here](https://github.com/UB-Mannheim/tesseract/wiki)

Set the path in your script if needed:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

**Linux (Ubuntu):**
```bash
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-eng tesseract-ocr-hin tesseract-ocr-ori
```

---

## 📦 Installation

```bash
cd tesseract_kyc_ocr
pip install -r requirements.txt
```

---

## ▶️ How to Run

### Scenario 1: Only **Front** image
```bash
python main.py test_images/JP_ADHAR_FRONT.jpg
```

### Scenario 2: Only **Back** image
```bash
python main.py test_images/JP_ADHAR_BACK.jpg
```

### Scenario 3: **Both** front and back
```bash
python main.py test_images/JP_ADHAR_FRONT.jpg test_images/JP_ADHAR_BACK.jpg
```

---

## 🧠 Output

```txt
--- OCR RAW OUTPUT (FRONT) ---
[...raw text...]

--- OCR RAW OUTPUT (BACK) ---
[...raw text...]

--- EXTRACTED FIELDS ---
aadhaar_number: 3181 9058 7376
full_name: Sipra Mohanty
dob: 17/09/1994
gender: FEMALE
address: The Nest, A - wing ,1008, Asha Nagar, Nandanvan, Mulund West, Mumbai...
```

---

## 📝 Notes

- OCR language used: `eng+ori+hin`
- Custom logic is used to intelligently detect front/back based on address patterns
- YAML configs are present for future enhancements but not required to run
