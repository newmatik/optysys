import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.button = QPushButton("Press Me!")


        # initalizing a flag
        self.button_is_checked = True

        # make the button checkable
        self.button.setCheckable(True) 


        # connect the button to a function when clicked
        self.button.clicked.connect(self.the_button_was_clicked)

        # # creates flag for state of button
        # self.button.clicked.connect(self.the_button_was_toggled)
        # # button.setChecked(self.button_is_checked)

        # # connect the button to a function when released after clicking
        # self.button.released.connect(self.the_button_was_released)
        # self.button.setChecked(self.button_is_checked)

        # resize the widget 
        self.setFixedSize(QSize(400, 300))

        # Set the central widget of the Window.
        self.setCentralWidget(self.button)



        self.label = QLabel()

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)


        self.label = QLabel("Click in this window")
        self.setCentralWidget(self.label)

    def mouseMoveEvent(self, e):
        self.label.setText("mouseMoveEvent")

    def mousePressEvent(self, e):
        self.label.setText("mousePressEvent")

    def mouseReleaseEvent(self, e):
        self.label.setText("mouseReleaseEvent")

    def mouseDoubleClickEvent(self, e):
        self.label.setText("mouseDoubleClickEvent")


    def the_button_was_clicked(self):
        # print("Clicked!")
        
        self.button.setText("You already clicked me.")
        #disable the button
        self.button.setEnabled(False)

        # Also change the window title.
        self.setWindowTitle("My Oneshot App")


    def the_button_was_toggled(self, checked):
        self.button_is_checked = checked
        print("Checked?", checked)


    def the_button_was_released(self):
        self.button_is_checked = self.button.isChecked()

        print(self.button_is_checked)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()