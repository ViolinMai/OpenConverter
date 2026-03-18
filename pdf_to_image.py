#This function uses pdf2image
from pdf2image import convert_from_path
from pdf2image.exceptions import (PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError)
def pdf_to_image_fun(input_path, output_folder, combo_choice):
    try:    
        images = convert_from_path(input_path)
        for i, image in enumerate(images):
            if combo_choice == "jpg":
                image.save(f"{output_folder}/page_{i+1}.jpg",  "JPEG")
            if combo_choice == "png":
                image.save(f"{output_folder}/page_{i+1}.png",  "PNG")
            if combo_choice == "jpeg":
                image.save(f"{output_folder}/page_{i+1}.jpeg",  "JPEG")    
    except PDFInfoNotInstalledError:
        raise RuntimeError("Poppler is not installed on your system")            
    except PDFPageCountError:
        raise RuntimeError("Cannot read PDF pages (file may be corrupted)")
    except PDFSyntaxError:
        raise RuntimeError("Invalid or corrupted PDF file")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")