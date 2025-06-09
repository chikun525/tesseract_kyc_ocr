import yaml
import re

def load_field_map(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def extract_english_address_from_back(ocr_text):
    lines = ocr_text.split('\n')
    address_lines = []
    found = False

    # 1. Try to find by 'Address' label first
    for idx, line in enumerate(lines):
        if not found and "address" in line.lower():
            found = True
            continue
        if found:
            for l in lines[idx:idx+5]:
                only_eng = ''.join(c for c in l if ord(c) < 128)
                if len(only_eng.strip()) > 5 and (len(only_eng) / max(len(l), 1)) > 0.6:
                    address_lines.append(only_eng.strip())
            break

    # 2. If not found, fallback: lines after 'Unique Identification Authority'
    if not address_lines:
        for idx, line in enumerate(lines):
            if "unique identification authority" in line.lower():
                for l in lines[idx+1:idx+10]:  # next 10 lines is usually plenty
                    only_eng = ''.join(c for c in l if ord(c) < 128)
                    if len(only_eng.strip()) > 5 and (len(only_eng) / max(len(l), 1)) > 0.5:
                        address_lines.append(only_eng.strip())
                break

    # Combine, clean up
    raw_addr = ' '.join(address_lines) if address_lines else 'NA'
    # Remove stray pipes, underscores, and duplicate commas/spaces
    cleaned = re.sub(r'[,|_]+', ',', raw_addr)
    cleaned = re.sub(r',+', ',', cleaned)
    cleaned = re.sub(r' +', ' ', cleaned)
    cleaned = cleaned.replace(' ,', ',').replace(' ,', ',').strip(' ,|-_')
    # Remove Aadhaar number from address if accidentally included
    cleaned = re.sub(r'\b\d{4}\s?\d{4}\s?\d{4}\b', '', cleaned)
    cleaned = cleaned.strip(' ,|-_')
    return cleaned if cleaned else 'NA'

def extract_address_from_back(ocr_text):
    lines = [l.strip() for l in ocr_text.split('\n')]
    address_lines = []
    start_idx = None

    # 1. Try to find "Address" label
    for idx, line in enumerate(lines):
        if "address" in line.lower():
            start_idx = idx + 1
            break

    # 2. If not found, fallback to UIDAI header
    if start_idx is None:
        for idx, line in enumerate(lines):
            if "unique identification authority of india" in line.lower():
                start_idx = idx + 1
                break

    # 3. If found, collect address lines, skipping initial blanks after label
    if start_idx is not None:
        # Skip leading blanks after label
        while start_idx < len(lines) and not lines[start_idx]:
            start_idx += 1
        # Now grab lines until stop condition
        for l in lines[start_idx:]:
            # Stop if line is blank (after block started), Aadhaar number, or junk/footer
            if not l or re.search(r'\b\d{4}\s?\d{4}\s?\d{4}\b', l) or 'uidai' in l.lower() or 'www' in l.lower() or 'VID' in l:
                break
            address_lines.append(l)
    else:
        address_lines = []

    raw_addr = '\n'.join(address_lines) if address_lines else 'NA'
    return raw_addr.strip()



def extract_fields(front_ocr, back_ocr):
    # Aadhaar number
    aadhaar_number = re.search(r'\b\d{4}\s?\d{4}\s?\d{4}\b', front_ocr)
    aadhaar_number = aadhaar_number.group(0) if aadhaar_number else 'NA'

    # Full name
    name = 'NA'
    front_lines = [l.strip() for l in front_ocr.split('\n') if l.strip()]
    for i, line in enumerate(front_lines):
        if "government of india" in line.lower():
            for l in front_lines[i+1:i+4]:
                if l.replace(" ", "").isalpha() and len(l.split()) > 1:
                    name = l.strip()
                    break
            break
    # Fallback: first line (after removing Hindi/Odia/Marathi) with 2+ words
    if name == 'NA':
        for l in front_lines:
            if l.replace(" ", "").isalpha() and len(l.split()) > 1 and not any('\u0900' <= c <= '\u097F' for c in l):
                name = l.strip()
                break

    # DOB
    dob = re.search(r'\d{2}/\d{2}/\d{4}', front_ocr)
    dob = dob.group(0) if dob else 'NA'

    # Gender
    gender = 'NA'
    for g in ['FEMALE', 'MALE', 'Female', 'Male']:
        if g in front_ocr:
            gender = g.upper()
            break
    
    print("=== DEBUG: BACK OCR LINES ===")
    for i, line in enumerate(back_ocr.split('\n')):
        print(f"{i}: {repr(line)}")

    # Address
    address = extract_address_from_back(back_ocr)

    return {
        "aadhaar_number": aadhaar_number,
        "full_name": name,
        "dob": dob,
        "gender": gender,
        "address": address
    }