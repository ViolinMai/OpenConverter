#This function uses libreoffice with subprocess
import subprocess
from pathlib import Path
from utils import get_libreoffice_path

def office_to_pdf_fun(file_path, output_path):
    soffice = get_libreoffice_path()
    if soffice is None:
        raise RuntimeError ("You don't have LibreOfiice installed on your system, consider installing it from https://www.libreoffice.org/download/ if you need this feature.")
    try:
        result = subprocess.run([
            soffice,
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_path,
            file_path
        ], capture_output=True,
            text=True,
            timeout=30
            )
        if result.returncode != 0:
            print(f"The proccess failed: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        raise RuntimeError("The proccess took too long...")
        
    except Exception as e:
        raise RuntimeError(f"An error happend: {e}")        
    output_path = str(Path(output_path).with_suffix(".pdf"))
   