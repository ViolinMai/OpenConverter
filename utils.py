import shutil
import sys
from pathlib import Path
    
def get_libreoffice_path():
    system_path = shutil.which("soffice")
    if system_path:
        return system_path
    return None

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).resolve().parent / relative_path

def get_poppler_path():
    embedded = resource_path("Assets/poppler/bin")
    if embedded.exists():
        return str(embedded)
    
    pdfinfo_path = shutil.which("pdfinfo")
    pdftoppm_path = shutil.which("pdftoppm")
    if pdfinfo_path and pdftoppm_path:
        return None
    
    return None

def check_is_poppler_exists():
    return shutil.which("pdftoppm") is not None and shutil.which("pdfinfo") is not None
    