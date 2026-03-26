#This function uses pdf2image
from pdf2image import convert_from_path
from pdf2image.exceptions import (PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError)
from utils import check_is_poppler_exists, get_poppler_path
from pathlib import Path
import fitz
def pdf_to_image_fun(input_path, output_folder, combo_choice):
    
    try:
        formats = {
            "jpg": ("JPEG", "jpg"),
            "png": ("PNG", "png"),
            "jpeg": ("JPEG", "jpeg")
        }
        pil_format, extension = formats[combo_choice] 
        paths = []
        poppler_path = get_poppler_path()
        if poppler_path is None and not check_is_poppler_exists():
           raise RuntimeError("Poppler is not installed. It's necessary for PDF to images covertions, if you want help with that consider reviewing the README file.") 
        pdf = fitz.open(input_path)
        pages_count = len(pdf)
        pdf.close()    
        for i, page_number in enumerate(range(1, pages_count + 1), start=1):
            image = convert_from_path(
                input_path,
                first_page=page_number,
                last_page=page_number,
                poppler_path=poppler_path
            )[0]
            path = Path(output_folder) / f"page_{i:03}.{extension}" 
            image.save(path, pil_format)  
            paths.append(str(path))
            print(paths)
        return paths           
    except PDFInfoNotInstalledError:
        raise RuntimeError("Poppler is not installed on your system")            
    except PDFPageCountError:
        raise RuntimeError("Cannot read PDF pages (file may be corrupted)")
    except PDFSyntaxError:
        raise RuntimeError("Invalid or corrupted PDF file")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")  