#This function uses pymypdf
import fitz
from pathlib import Path

def pdf_to_txt_fun(pdf_path, output_path):
    try:
        pdf = fitz.open(pdf_path)
    except FileNotFoundError:
        raise RuntimeError("The file wasn't found")   
    except Exception as e:
        raise RuntimeError(f"Error opening file: {e}")      
    extracted_text = []
    output_path = str(Path(output_path).with_suffix(".txt"))
    try:
        for page in pdf:
            text = page.get_text().strip()
            if text:
                extracted_text.append(text)
        if not extracted_text:
            raise RuntimeError("No extractable text found, try OCR mode.")       
        with open(output_path , "w", encoding="utf-8") as file:
            for page in pdf:
                file.write(page.get_text() + "\n")                        
    except Exception as e2:
        raise RuntimeError(f"Error writing file: {e2}")
    finally:
        pdf.close()    
       