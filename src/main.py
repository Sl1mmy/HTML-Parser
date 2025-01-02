from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QLabel, QTabWidget, QPushButton, QHBoxLayout, QFileDialog
from PySide6.QtCore import Qt
import sys
from parser import parse_file
import csv
import os
from openpyxl import Workbook

class DropArea(QLabel):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setText("Drag and Drop Files Here")
        self.setFixedHeight(100)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px dashed #aaa;")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
        print("Dropped files:", file_paths)  # Debugging line
        self.main_window.process_files(file_paths)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop File Parser")
        self.setGeometry(100, 100, 700, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        self.drop_area = DropArea(self)
        self.layout.addWidget(self.drop_area)
        
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)
        
        self.button_layout = QHBoxLayout()
        self.delete_button = QPushButton("Delete Tab")
        self.delete_button.clicked.connect(self.delete_current_tab)
        self.button_layout.addWidget(self.delete_button)

        self.save_button = QPushButton("Save to CSV")
        self.save_button.clicked.connect(self.save_to_csv)
        self.button_layout.addWidget(self.save_button)

        self.save_excel_button = QPushButton("Save to Excel")
        self.save_excel_button.clicked.connect(self.save_to_excel)
        self.button_layout.addWidget(self.save_excel_button)
        
        self.layout.addLayout(self.button_layout)


    def process_files(self, file_paths):
        for file_path in file_paths:
            print(f"Processing: {file_path}")
            try:
                content = parse_file(file_path)
                text_edit = QTextEdit()
                for each in content:
                    text_edit.append(str(each))
                    text_edit.append("")  # Add a new line after each append
                self.tab_widget.addTab(text_edit, file_path)
            except FileNotFoundError as e:
                error_tab = QTextEdit()
                error_tab.append(f"Error: {e}")
                self.tab_widget.addTab(error_tab, f"Error: {file_path}")

    def delete_current_tab(self):
        current_index = self.tab_widget.currentIndex()
        if current_index != -1:
            self.tab_widget.removeTab(current_index)

    def save_to_csv(self):
        current_index = self.tab_widget.currentIndex()
        if current_index != -1:
            tab_text = self.tab_widget.tabText(current_index)
            default_name = os.path.splitext(os.path.basename(tab_text))[0] + ".csv"
            file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", default_name, "CSV Files (*.csv)")
            if file_path:
                with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    text_edit = self.tab_widget.widget(current_index)
                    content = text_edit.toPlainText().strip()
                    rows = content.split("\n\n")
                    for row in rows:
                        csvwriter.writerow([row.replace("\n", ", ")])

    def save_to_excel(self):
        current_index = self.tab_widget.currentIndex()
        if current_index != -1:
            tab_text = self.tab_widget.tabText(current_index)
            default_name = os.path.splitext(os.path.basename(tab_text))[0] + ".xlsx"
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Excel", default_name, "Excel Files (*.xlsx)")
            if file_path:
                workbook = Workbook()
                sheet = workbook.active
                text_edit = self.tab_widget.widget(current_index)
                content = text_edit.toPlainText().strip()
                rows = content.split("\n\n")
                for row_index, row in enumerate(rows, start=1):
                    cells = row.split("\n")
                    for col_index, cell in enumerate(cells, start=1):
                        sheet.cell(row=row_index, column=col_index, value=cell)
                workbook.save(file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())