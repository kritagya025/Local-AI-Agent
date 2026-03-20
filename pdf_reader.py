import pdfplumber

def extract_text(file_path):
    """
    Extracts all text from a PDF file using pdfplumber.
    """
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
    
    return text.strip()
