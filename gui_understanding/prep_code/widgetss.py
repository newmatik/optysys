import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import * 



# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widgets App")

        layout = QVBoxLayout()
        widgets = [
            QCheckBox,
            QComboBox, #drop down 
            QDateEdit,
            QDateTimeEdit,
            QDial,  #rotatable dial 
            QDoubleSpinBox, #A number spinner for floats
            QFontComboBox,   # list of fonts
            QLCDNumber,
            QLabel,         # non interactive label
            QLineEdit,         # enter a line of text
            QProgressBar,
            QPushButton,
            QRadioButton, #A toggle set, with only one active item
            QSlider,
            QSpinBox,
            QTimeEdit,
        ]

        for w in widgets:
            layout.addWidget(w())

        widget = QWidget()
        widget.setLayout(layout)
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()