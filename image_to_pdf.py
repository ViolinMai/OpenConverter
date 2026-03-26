#This function uses "img2pdf"
import img2pdf
def image_to_pdf_fun(input_paths, pdf_name_output):
    try:
        with open(f"{pdf_name_output}.pdf", "wb") as file:
            file.write(img2pdf.convert(input_paths))
    except Exception as e:
        raise RuntimeError(f"Failed to convert the file/s: {e}")
     