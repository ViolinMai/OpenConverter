#This function uses "img2pdf"
import img2pdf
def image_to_pdf_fun(pdf_name_output, image_paths):
    try:
        with open(f"{pdf_name_output}.pdf", "wb") as file:
            file.write(img2pdf.convert(image_paths))
    except Exception as e:
        raise RuntimeError(f"Failed to convert the file/s: {e}")
    