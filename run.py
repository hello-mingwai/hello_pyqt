#!/usr/bin/env python3

from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QPushButton, 
    QVBoxLayout,
    QTextEdit
    )
import sys
 
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 250)
        self.setWindowTitle("Hello PyQt6")
 
        label = QLabel("Copy and paste an Amazon URL here:", self)

        # button = QPushButton("Hello World", self)
        # button.setCheckable(True)
        # button.clicked.connect(self.button_was_clicked)

        # button2 = QPushButton("Fish", self)

        self.text_edit_in = QTextEdit()
        self.text_edit_in.textChanged.connect(self.update_out)

        self.text_edit_out = QTextEdit()
        self.text_edit_out.setPlainText("Shortened Amazon URL will appear here, and be copied to clipboard.")

        vbox = QVBoxLayout()
        vbox.addWidget(label)
        # vbox.addWidget(button)
        # vbox.addWidget(button2)
        vbox.addWidget(self.text_edit_in)
        vbox.addWidget(self.text_edit_out)

        self.setLayout(vbox)
        self.setGeometry(500, 500, 550, 100)
        # self.show()
    
    def button_was_clicked(self):
        print("Clicked")

    def update_out(self):
        input_str = self.text_edit_in.toPlainText()
        try:
            _, after_dp = input_str.split("/dp/", 1)
            before_slash, _ = after_dp.split("/", 1)
        except ValueError:
            self.text_edit_out.setPlainText("ValueError")
            return

        url = f"https://www.amazon.com/dp/{before_slash}"
        self.text_edit_out.setPlainText(url)
        self.text_edit_out.selectAll()
        self.text_edit_out.copy()

 
app = QApplication(sys.argv)
window = Window()
# window = QPushButton("Push Me")
window.show()
sys.exit(app.exec())