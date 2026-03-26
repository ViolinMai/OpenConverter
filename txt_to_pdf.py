#This function uses fpdf
from fpdf import FPDF
from pathlib import Path

def txt_to_pdf_fun(file_path, output_path):
    try:
        with open(f"{file_path}", "r", encoding="utf-8") as file:
            text = file.read()
    except Exception as e:
        return False, f"Error reading file {e}", None        
    try:    
        lines = text.splitlines()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        BASE_DIR = Path(__file__).resolve().parent
        font_path = BASE_DIR / "Assets" / "DejaVuSans.ttf"
        pdf.add_font("DejaVuSans", fname=font_path)
        pdf.set_font("DejaVuSans", size=12)
        for line in lines:
            clean_line = (line.encode("utf-8", "ignore").decode("utf-8")).strip()
            pdf.cell(0,10,clean_line,new_x="LMARGIN",new_y="NEXT")
        output_path = str(Path(output_path).with_suffix(".pdf"))
        pdf.output(str(output_path))
        return True, "Convertion seccessful", output_path
    except Exception as e2:
        return False, f"Error writing file {e2}", None
