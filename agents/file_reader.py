import fitz  # PyMuPDF
import re

def extract_data_from_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = " ".join([page.get_text() for page in doc])
        doc.close()

        # Example regex-based extraction
        name = re.search(r"Name[:\-]\s*(.+)", text)
        parent = re.search(r"Parent[:\-]\s*(.+)", text)
        address = re.search(r"Address[:\-]\s*(.+)", text)
        uid = re.search(r"\b\d{12}\b", text)
        dob = re.search(r"(?:DOB|Date of Birth)[:\-]\s*([\d\-\/]+)", text)

        return {
            "name": name.group(1).strip() if name else "",
            "parent": parent.group(1).strip() if parent else "",
            "address": address.group(1).strip() if address else "",
            "uid": uid.group(0).strip() if uid else "",
            "dob": dob.group(1).strip() if dob else ""
        }
    except Exception as e:
        print(f"PDF Parsing Error: {e}")
        return None
