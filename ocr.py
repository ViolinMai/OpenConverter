#This function uses pypdf and pytesseract
from pathlib import Path
from tempfile import TemporaryDirectory
from pdf_to_image import pdf_to_image_fun
from pypdf import PdfWriter
import pytesseract
import os
import sys
import platform

base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
if platform.system() == "Windows":
    tess_name = "tesseract.exe"
else:
    tess_name = "tesseract"    

tess_path = base_dir / "Assets" / "bin" / tess_name
tessdata_path = base_dir / "Assets" / "tessdata"

def setup_tess_engine():
    if not is_ocr_available():
        raise RuntimeError("Tesseract or tessdata not found.")
    pytesseract.pytesseract.tesseract_cmd = str(tess_path)
    os.environ["TESSDATA_PREFIX"] = str(tessdata_path)
    
def is_ocr_available():
    return tess_path.exists() and tessdata_path.exists()

def images_to_searchablepdf(images_list, output_path):
    setup_tess_engine()
    pdf_list = []
    with TemporaryDirectory() as tempdir:
        try:    
            for i, image in enumerate(images_list):
                pdf_bytes = pytesseract.image_to_pdf_or_hocr(image, extension="pdf", lang='ara+eng')
                file_name = f"{tempdir}/PDF{i+1:03}.pdf"
                with open(file_name, "wb") as file:
                    file.write(pdf_bytes)
                pdf_list.append(file_name)   
            merger = PdfWriter()
            for pdf in pdf_list:
                merger.append(pdf)       
            merger.write(f"{output_path}.pdf")
            merger.close()
        except Exception as e2:
            raise RuntimeError(f"An error happened: {e2}")
        
        
def pdf_to_searchablepdf(input_path, output_path):
    setup_tess_engine()
    with TemporaryDirectory() as tempdir:
        try:
            images_list = pdf_to_image_fun(input_path, tempdir, "png")
            pdf_list = []
            for i, image in enumerate(images_list):
                pdf_bytes = pytesseract.image_to_pdf_or_hocr(image, extension="pdf", lang='ara+eng')
                file_name = f"{tempdir}/PDF{i+1:03}.pdf"
                with open(file_name, "wb") as file:
                    file.write(pdf_bytes)
                pdf_list.append(file_name)   
            merger = PdfWriter()
            for pdf in pdf_list:
                merger.append(pdf)
            merger.write(f"{output_path}.pdf")
            merger.close()
        except Exception as e2:
            raise RuntimeError(f"An error happened: {e2}")