import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QComboBox, QWidget, QPushButton, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from pdf_to_image import pdf_to_image_fun
from image_to_pdf import image_to_pdf_fun
from pathlib import Path

class OpenConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenConverter")
        self.resize(1000,600)
        self.input_line = QLineEdit(self)
        self.input_button = QPushButton("Browse...", self)
        self.output_line = QLineEdit(self)
        self.output_button = QPushButton("Browse...", self)
        self.input_notice = QLabel("Input") 
        self.output_notice = QLabel("output")
        self.convert_button = QPushButton("Convert")
        self.photo_format_choice = QComboBox()
        self.file_input_path = []
        self.file_output_path = ""
        self.folder_output_path = ""
        self.is_single_pdf = False
        self.are_all_images = False 
        self.UI()
        
    def UI(self):
        self.photo_format_choice.addItems(["PNG", "JPEG", "JPG"])
        self.photo_format_choice.setVisible(False)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.input_line)
        hbox1.addWidget(self.input_button)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.output_line)
        hbox2.addWidget(self.output_button)
        vbox = QVBoxLayout()
        vbox_input = QVBoxLayout()
        vbox_output = QVBoxLayout()
        vbox_input.addWidget(self.input_notice)
        vbox_input.addLayout(hbox1)
        vbox_output.addWidget(self.output_notice)
        vbox_output.addLayout(hbox2)
        vbox.addLayout(vbox_input)
        vbox.addLayout(vbox_output)
        hbox_photo_output = QHBoxLayout()
        hbox_photo_output.addWidget(self.photo_format_choice)
        hbox_photo_output.addStretch()
        vbox.addLayout(hbox_photo_output)
        vbox.addWidget(self.convert_button)
        self.setLayout(vbox) 
        self.setStyleSheet("font-size: 25px;"
                           "font-family: Arial;")
        self.input_notice.setAlignment(Qt.AlignCenter)
        self.output_notice.setAlignment(Qt.AlignCenter)
        self.input_button.clicked.connect(self.input_open_file_manager)
        self.output_button.clicked.connect(self.output_open_file_manager)
        self.convert_button.clicked.connect(self.converting)
        
        
    #Here it takes the input file/s and clarify the suffix    
    def input_open_file_manager(self):
        self.file_input_path,_ = QtWidgets.QFileDialog.getOpenFileNames(self, caption="Open File", directory="", filter="images and PDF (*.jpeg *.png *.jpg *.pdf)", options=QtWidgets.QFileDialog.DontUseNativeDialog)
        self.file_output_path = ""
        self.folder_output_path = ""
        self.output_line.clear()
        if not self.file_input_path:
            return
        self.proper_suffix = [Path(file).suffix.lower() for file in self.file_input_path]
        self.is_single_pdf = (len(self.proper_suffix) == 1
                              and self.proper_suffix[0] == ".pdf")
        self.are_all_images = all(suffix in [".png", ".jpeg", '.jpg']
                               for suffix in self.proper_suffix)
        self.photo_format_choice.setVisible(self.is_single_pdf)
        
        
        if self.is_single_pdf:
            self.input_line.setText(self.file_input_path[0])
        elif self.are_all_images:
            self.input_line.setText(f"{len(self.file_input_path)} files selected")
    #Here it determines the output file dialog based on the suffix of the input file                 
    def output_open_file_manager(self):
        if self.is_single_pdf:
            self.folder_output_path = QtWidgets.QFileDialog.getExistingDirectory(self, caption="Save file", directory="", options=QtWidgets.QFileDialog.DontUseNativeDialog)
            self.output_line.setText(self.folder_output_path) 
        elif self.are_all_images:
            self.file_output_path = QtWidgets.QFileDialog.getSaveFileName(self, caption="Save file", directory="", filter="PDF Files (*.pdf)", options=QtWidgets.QFileDialog.DontUseNativeDialog)
            self.output_line.setText(self.file_output_path[0])           
    #Here it takes the converting button signal and calls the proper function depending on the input file
    def converting(self):
        try:
            if self.is_single_pdf:
                combo_choice = self.photo_format_choice.currentText().lower()
                pdf_to_image_fun(self.file_input_path[0], self.folder_output_path, combo_choice)
            elif self.are_all_images:
                image_to_pdf_fun(self.file_output_path[0], self.file_input_path)
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {e}")       
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OpenConverter()
    window.show()
    sys.exit(app.exec_())   