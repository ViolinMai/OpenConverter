from pathlib import Path
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, QSettings, QThread
from PyQt6.QtGui import QIcon
from conversionthreading import ConverionsThreading
from utils import get_libreoffice_path, get_poppler_path, check_is_poppler_exists
from languages import translations
from convertions import conversion_types
from pdf_to_image import pdf_to_image_fun
from pdf_to_txt import pdf_to_txt_fun
from image_to_pdf import image_to_pdf_fun
from txt_to_pdf import txt_to_pdf_fun
from office_to_pdf import office_to_pdf_fun
from ocr import *



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        BASE_DIR = Path(__file__).resolve().parent
        ui_file = BASE_DIR / "Assets" / "OpenConverterGUI.ui"
        loadUi(str(ui_file), self)
        self.setWindowIcon(QIcon(str(self.resource_path("Assets/OpenConverter_icon.png"))))
        self.translations = translations
        self.settings = QSettings("ViolinMai", "OpenConverterGUI")
        saved_language = self.settings.value("language", "English")
        self.chosen_function = None
        self.files = []
        self.output_for_file_functions = ""
        self.output_for_folder_functions = ""
        self.thread = None
        self.worker = None
        if saved_language == "Arabic":
            self.radioButton_2.setChecked(True)
        else:
            self.radioButton.setChecked(True)
        self.change_language(saved_language) 
        self.acceptDrops()
        self.signals()
        self.Available_functions_list.hide()
    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            return Path(sys._MEIPASS) / relative_path
        return Path(__file__).resolve().parent / relative_path
            
    def handle_conversion_success(self, result):
        self.convert_button.setEnabled(True)
        self.show_success_message("Success", "Conversion completed successfully.")  
        self.thread = None
        self.worker = None 
    def handle_conversion_error(self, message):
        self.convert_button.setEnabled(True)
        self.show_error_message("Error", message) 
        self.thread = None
        self.worker = None       
    def show_error_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()    
    def show_success_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()
    def change_language(self, choice):   
        t = self.translations[choice]
        if choice == "Arabic":
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            self.settings.setValue("language", choice)

        else:
            self.setLayoutDirection(Qt.LayoutDirection.LeftToRight) 
            self.settings.setValue("language", choice)       
            

        self.input_label.setText(t["input_label"])
        self.output_label.setText(t["output_label"])
        self.drag_and_drop_label.setText(t["drag_and_drop_label"])
        self.input_browse_button.setText(t["input_browse_button"])
        self.output_browse_button.setText(t["output_browse_button"])
        self.convert_button.setText(t["convert_button"])
        self.language_label.setText(t["language_label"])
        self.input_line.setPlaceholderText(t["input_placeholder"])
        self.output_line.setPlaceholderText(t["output_placeholder"])

        self.radioButton.setText(t["radioButton"])
        self.radioButton_2.setText(t["radioButton_2"])

        self.about_label.setText(t["about_label"])

        self.converting_tab.setTabText(0, t["converting_tab"])
        self.converting_tab.setTabText(1, t["settings_tab"])
        self.converting_tab.setTabText(2, t["about_tab"])
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
            
    def dropEvent(self, event):

        if not event.mimeData().hasUrls():
            self.show_error_message("Error:", "Couldn't accept the file")
            event.ignore()
            return
   
        allowed_ext = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tiff", ".tif", ".j2k", ".pdf", ".pptx", ".docx", ".xlsx", ".txt")
        files = []

        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if not file_path:
                self.show_error_message("Error:", "Something's wrong with file path.")
                event.ignore()
                return
            if not any(file_path.lower().endswith(ext) for ext in allowed_ext):
                self.show_error_message("Error:", "Not a valid extension.") 
                event.ignore() 
                return     
            files.append(file_path)

        if not files:
            print("No valid files were dropped.") 
            event.ignore()
            return  
        self.handle_drop_input(files)
        event.acceptProposedAction()                          
            
    def signals(self):
        self.input_browse_button.clicked.connect(self.handle_button_input)
        self.output_browse_button.clicked.connect(self.proper_output)
        self.Available_functions_list.itemClicked.connect(self.proper_output)
        self.convert_button.clicked.connect(self.apply_convertions)
        self.radioButton.toggled.connect(lambda checked: checked and self.change_language("English"))
        self.radioButton_2.toggled.connect(lambda checked: checked and self.change_language("Arabic"))
        
    def display_input_line(self, files):
        i = len(files)
        if i > 1:
            i -= 1
            self.input_line.setText(f"{files[0]}, and {i} file/s.")
        else:
            if files:
                self.input_line.setText(files[0])
                       
    def handle_drop_input(self, files):
        self.input_line.clear()
        
        if not self.input_file_suffix_check(files):
            files.clear()
            return
        self.display_input_line(files)
        if files:
            self.routing_input_to_functions(files)    
    def handle_button_input(self):  
        self.input_line.clear()  
        try:
            files = QFileDialog.getOpenFileNames(parent=None, caption="Select files to convert", directory="", filter="Supported files (*.png *.jpg *.jpeg *.webp *.bmp *.gif *.tiff *.tif *.j2k *.pdf *.pptx *.docx *.xlsx *.txt)")
            files = (files[0])
            if not self.input_file_suffix_check(files):
                files.clear()
                return
            self.display_input_line(files)
            
        except ValueError as e2:
            self.show_error_message("Input Error:", str(e2))
            files.clear()
            return
        if files:
            self.routing_input_to_functions(files)    
            
    def clean(self,files):
        files.clear()
        self.input_line.clear()
        
    def file_validations(self, files):
        self.is_single_file = (len(files) == 1)
        self.is_multi_file = (len(files) >= 2)
        
    def input_file_suffix_check(self, files):
        self.file_suffix = [Path(file).suffix.lower() for file in files]   
        self.is_same_suffix = all(suffix == self.file_suffix[0] for suffix in self.file_suffix)
        if not self.is_same_suffix:
            self.show_error_message("Error:", "The files must have the same extension.")
            return False
        if not self.file_suffix:
            self.show_error_message("Error:", "No files were provided.") 
            return False
        return True
    def show_available_convertions(self, convertions):
        self.Available_functions_list.clear()
        
        if not convertions:
            self.Available_functions_list.hide()
            return
        
        for name, fun in convertions:
            self.Available_functions_list.addItem(name)
        self.Available_functions_list.show()  
        
        count = self.Available_functions_list.count()
        item_hieght = self.Available_functions_list.sizeHintForRow(0)
        total_hieght = item_hieght * count + 10
        self.Available_functions_list.setFixedHeight(total_hieght)  
         
    def routing_input_to_functions(self, files):
        self.chosen_function = None
        self.output_for_file_functions = ""
        self.output_for_folder_functions = ""
        self.output_line.clear()
        suffix = self.file_suffix[0]
        if suffix == ".pdf":
            if len(files) != 1:
                self.show_error_message("Error:", "Can't have more than one 'PDF' file at the same time")
                self.clean(files)
                return
            available_convertions = [
                ("PDF to TXT", pdf_to_txt_fun),
                ("PDF to Searchable PDF (OCR)", pdf_to_searchablepdf),
                ("PDF to Images (PNG)", pdf_to_image_fun),
                ("PDF to Images (JPEG)", pdf_to_image_fun),
                ("PDF to Images (JPG)", pdf_to_image_fun)
            ]
            self.show_available_convertions(available_convertions)
            
            
               
        elif suffix == ".txt": 
            if len(files) != 1:
                self.show_error_message("Error:", "Can't have more than one 'TXT' file at the same time")
                self.clean(files)
                return 
            available_convertions = [
                ("TXT to PDF", txt_to_pdf_fun)
            ]             
            self.show_available_convertions(available_convertions)
        elif suffix in [".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tiff", ".tif", ".j2k"]:
            available_convertions = [
                ("Images to PDF", image_to_pdf_fun),
                ("Images to Searchable PDF (OCR)", images_to_searchablepdf)
            ]
            self.show_available_convertions(available_convertions)      
        
        elif suffix in [".pptx", ".xlsx", ".docx"]:
            if len(files) != 1:
                self.show_error_message("Error:", "Can't have more than one 'Office' file at the same time")
                self.clean(files)
                return
            if get_libreoffice_path() is None:
                self.show_error_message("LibreOffice Missing", "You don't have LibreOfiice installed on your system, consider installing it from https://www.libreoffice.org/download/ if you need this feature.")
                self.Available_functions_list.clear()
                self.Available_functions_list.hide()
                self.clean(files)
                return
            available_convertions = [
                ("Office to PDF", office_to_pdf_fun)
            ]  
            self.show_available_convertions(available_convertions)             
        self.files = files
    def proper_output(self, item=None):
        self.output_line.clear()
        chosen_function = self.Available_functions_list.currentItem()
        if chosen_function is None:
            
            print("You haven't chosen a function yet")
            return
        self.chosen_function = chosen_function.text()
        if self.chosen_function in ["PDF to Images (PNG)", "PDF to Images (JPEG)","PDF to Images (JPG)"]:   
            if get_poppler_path() is None and not check_is_poppler_exists():
                self.show_error_message("Poppler Missing", "Poppler is not installed. It's necessary for PDF to images covertions, if you want help with that consider reviewing the README file.")
                return
            self.output_for_folder_functions = QFileDialog.getExistingDirectory(self, caption="Save file/s", directory="")
            if self.output_for_folder_functions == "":
                return
            self.output_line.setText(self.output_for_folder_functions)    
        elif self.chosen_function in ["Images to Searchable PDF (OCR)", "Images to PDF", "TXT to PDF", "PDF to Searchable PDF (OCR)", "PDF to TXT", "Office to PDF"]:
            self.output_for_file_functions = QFileDialog.getSaveFileName(self, caption="Save file/s", directory="")[0]
            if self.output_for_file_functions:
                self.output_line.setText(self.output_for_file_functions)            
            else:
                return            
    def apply_convertions(self):
        output_type = conversion_types.get(self.chosen_function)
        if not self.files:
            self.show_error_message("Error:", "You need to choose an input first.")
            return  
        elif not self.chosen_function:
            self.show_error_message("Error:", "You need to choose a function first.")
            return
        elif output_type == "file":
            if not self.output_for_file_functions:
                self.show_error_message("Error:", "You need to choose an output file.")
                return
        elif output_type == "folder":    
            if not self.output_for_folder_functions:
                self.show_error_message("Error:", "You need to choose an output folder.")
                return
        
        if self.chosen_function == "PDF to Images (PNG)":
            selected_function = pdf_to_image_fun
            args = (self.files[0], self.output_for_folder_functions, "png")
            
        elif self.chosen_function == "PDF to Images (JPEG)":
            selected_function = pdf_to_image_fun
            args = (self.files[0], self.output_for_folder_functions, "jpeg")

        elif self.chosen_function == "PDF to Images (JPG)":
            selected_function = pdf_to_image_fun
            args = (self.files[0], self.output_for_folder_functions, "jpg")

        elif self.chosen_function == "PDF to TXT":
            selected_function = pdf_to_txt_fun
            args = (self.files[0], self.output_for_file_functions)

            
        elif self.chosen_function == "PDF to Searchable PDF (OCR)":
            selected_function = pdf_to_searchablepdf
            args = (self.files[0], self.output_for_file_functions) 
         
        elif self.chosen_function == "TXT to PDF":
            selected_function = txt_to_pdf_fun
            args = (self.files[0], self.output_for_file_functions)

        elif self.chosen_function == "Images to Searchable PDF (OCR)":
            selected_function = images_to_searchablepdf
            args = (self.files, self.output_for_file_functions)  

        elif self.chosen_function == "Images to PDF":
            selected_function = image_to_pdf_fun
            args = (self.files, self.output_for_file_functions)

        elif self.chosen_function == "Office to PDF":
            selected_function = office_to_pdf_fun
            args = (self.files[0], self.output_for_file_functions)
        self.convert_button.setEnabled(False)
        self.thread = QThread()
        self.worker = ConverionsThreading(selected_function, *args)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.success.connect(self.handle_conversion_success)
        self.worker.error.connect(self.handle_conversion_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
                
                        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())