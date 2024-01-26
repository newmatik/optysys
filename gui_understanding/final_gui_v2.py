from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *# QApplication, QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import *# QPixmap

'''
The following UI displays images from the webcam of the laptop. 


Vishaka Srinivasan, Newmatik GmBh
'''

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                cv_img = cv2.flip(cv_img, 1)
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Optysys")
        self.disply_width = 500
        self.display_height = 1000
        # create the label that holds the image
        self.image_label = QLabel(self)
        # self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        
        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        disp_camera1_frame = QFrame()
        vbox.addWidget(self.image_label)
        disp_camera1_frame.setLayout(vbox)
        

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()


        rightFrame = QFrame()
        rightLayout = QVBoxLayout() #QHBoxLayout()


        # Project details
        project_layout = QGridLayout()
        project_frame = QFrame()
        project_label = QLabel('Project Details')
        project_layout.addWidget(project_label, 0,0)
        project_name = QLabel('ABC')
        project_layout.addWidget(project_name, 0,1)
        inspection_label = QLabel('Inspection Details')
        project_layout.addWidget(inspection_label, 1,0)
        inspection_name = QLabel('ABC')
        project_layout.addWidget(inspection_name, 1,1)
        project_frame.setLayout(project_layout)




        camera_layout = QHBoxLayout()
        camera_frame = QFrame()
        # Zoom in 
        zoom_in_button = QPushButton()
        icon = QIcon(QPixmap('images/zoom_in.jpg'))
        zoom_in_button.setIcon(icon)
        zoom_in_button.setIconSize(QSize(32, 32))
        zoom_in_button.setFlat(False)
        # rightLayout.addWidget(zoom_in_button)
        camera_layout.addWidget(zoom_in_button)
        zoom_in_button.clicked.connect(lambda: self.on_button_clicked('Zoom In'))        
        


        # Zoom out
        zoom_out_button = QPushButton()
        icon = QIcon(QPixmap('images/zoom_out.png'))
        zoom_out_button.setIcon(icon)
        zoom_out_button.setIconSize(QSize(32, 32))
        zoom_out_button.setFlat(False)
        # rightLayout.addWidget(zoom_out_button)
        camera_layout.addWidget(zoom_out_button)
        zoom_out_button.clicked.connect(lambda: self.on_button_clicked('Zoom Out'))


        # Zoom to fit
        zoom_to_fit_button = QPushButton()
        icon = QIcon(QPixmap('images/zoom_to_fit.png'))
        zoom_to_fit_button.setIcon(icon)
        zoom_to_fit_button.setIconSize(QSize(32, 32))
        zoom_to_fit_button.setFlat(False)
        # rightLayout.addWidget(zoom_to_fit_button)
        camera_layout.addWidget(zoom_to_fit_button) 
        zoom_to_fit_button.clicked.connect(lambda: self.on_button_clicked('Zoom to Fit'))

        # Zoom to 100%
        zoom_to_100_button = QPushButton()
        icon = QIcon(QPixmap('images/zoom_in_max.png'))
        zoom_to_100_button.setIcon(icon)
        zoom_to_100_button.setIconSize(QSize(32, 32))
        zoom_to_100_button.setFlat(False)
        # rightLayout.addWidget(zoom_to_100_button)
        camera_layout.addWidget(zoom_to_100_button)
        zoom_to_100_button.clicked.connect(lambda: self.on_button_clicked('Zoom to 100%'))


        # Capture Image
        capture_image_button = QPushButton()
        icon = QIcon(QPixmap('images/capture_image.jpg'))
        capture_image_button.setIcon(icon)
        capture_image_button.setIconSize(QSize(32, 32))
        capture_image_button.setFlat(False)
        # rightLayout.addWidget(zoom_to_100_button)
        camera_layout.addWidget(capture_image_button)
        zoom_to_100_button.clicked.connect(lambda: self.on_button_clicked('Image Capture'))



        camera_frame.setLayout(camera_layout)
        
        # Add motor controls
        motor_layout = QGridLayout()
        motor_frame = QFrame()




        # move up 
        move_up_button = QPushButton()
        icon = QIcon(QPixmap('images/up-arrow.svg'))
        move_up_button.setIcon(icon)
        move_up_button.setIconSize(QSize(32, 32))
        move_up_button.setFlat(False)
        motor_layout.addWidget(move_up_button, 0,1)
        move_up_button.clicked.connect(lambda: self.on_button_clicked('Move Up'))

        # move left
        move_left_button = QPushButton()
        icon = QIcon(QPixmap('images/left-arrow.svg'))
        move_left_button.setIcon(icon)
        move_left_button.setIconSize(QSize(32, 32))
        move_left_button.setFlat(False)
        motor_layout.addWidget(move_left_button, 1,0)
        move_left_button.clicked.connect(lambda: self.on_button_clicked('Move Left'))	

        # move right
        move_right_button = QPushButton()
        icon = QIcon(QPixmap('images/right-arrow.png'))
        move_right_button.setIcon(icon)
        move_right_button.setIconSize(QSize(32, 32))
        move_right_button.setFlat(False)
        motor_layout.addWidget(move_right_button, 1,2)
        move_right_button.clicked.connect(lambda: self.on_button_clicked('Move Right'))   

        # move down
        move_down_button = QPushButton()
        icon = QIcon(QPixmap('images/down-arrow.png'))
        move_down_button.setIcon(icon)
        move_down_button.setIconSize(QSize(32, 32))
        move_down_button.setFlat(False)
        motor_layout.addWidget(move_down_button, 2,1) 
        move_down_button.clicked.connect(lambda: self.on_button_clicked('Move Down'))

        # Center motor
        center_motor_button = QPushButton()
        icon = QIcon(QPixmap('images/centre.png'))
        center_motor_button.setIcon(icon)
        center_motor_button.setIconSize(QSize(32, 32))
        center_motor_button.setFlat(False)
        motor_layout.addWidget(center_motor_button, 1,1)
        center_motor_button.clicked.connect(lambda: self.on_button_clicked('Center Motor'))

        # stop motor
        stop_motor_button = QPushButton()
        icon = QIcon(QPixmap('images/stop.png'))
        stop_motor_button.setIcon(icon)
        stop_motor_button.setIconSize(QSize(32, 32))
        stop_motor_button.setFlat(False)
        motor_layout.addWidget(stop_motor_button, 0,5)
        stop_motor_button.clicked.connect(lambda: self.on_button_clicked('Stop Motor'))

        # Homing motor
        home_motor_button = QPushButton()
        icon = QIcon(QPixmap('images/home.png'))
        home_motor_button.setIcon(icon)
        home_motor_button.setIconSize(QSize(32, 32))
        home_motor_button.setFlat(False)
        motor_layout.addWidget(home_motor_button, 2,5)
        home_motor_button.clicked.connect(lambda: self.on_button_clicked('Homing'))
    

        motor_frame.setLayout(motor_layout)

        ## Show Zoom overview
        zoom_overivew_layout = QHBoxLayout()
        zoom_overivew_frame = QFrame()
        zoom_overview_imglabel = QLabel()
        zoom_overview_image = QPixmap('images/overview.jpg')
        zoom_overview_imglabel.setPixmap(zoom_overview_image)
        zoom_overivew_layout.addWidget(zoom_overview_imglabel)
        zoom_overivew_frame.setLayout(zoom_overivew_layout)

        
        
        # console frame
        console_frame = QFrame()
        console_layout = QGridLayout()
        self.console = QTextEdit()

        # self.console.textChanged.connect(self.tracking)
        self.console.setFixedHeight(80)

        console_layout.addWidget(self.console,0,0,1,3)
        
        # add enter button 
        enter_button = QPushButton()
        icon = QIcon(QPixmap('images/enter.png'))
        enter_button.setIcon(icon)
        enter_button.setIconSize(QSize(32, 32))
        enter_button.setFlat(False)
        enter_button.setFixedHeight(50)
        console_layout.addWidget(enter_button,0,4)
        enter_button.clicked.connect(lambda: self.on_button_clicked('Enter'))
        # Add print text 
        self.op_text = QTextEdit()
        self.op_text.setReadOnly(True)
        console_layout.addWidget(self.op_text,1,0,1,4)


        console_frame.setLayout(console_layout)



        # Device Status
        Device_status_layout = QGridLayout()
        Device_status_frame = QFrame()
        
        controller_label = QLabel()
        controller_pixmap = QPixmap('images/controller.png')
        controller_pixmap = controller_pixmap.scaled(64, 64, Qt.KeepAspectRatio)
        controller_label.setPixmap(controller_pixmap)
        Device_status_layout.addWidget(controller_label,0,0)

        idx = np.random.randint(3, size = 1)
        Batt = ["empty", "medium", "full"]
        
        Battery_percentage = Batt[idx[0]]#"empty"
        if Battery_percentage  == "empty":
            controller_status_label = QLabel(f'WARNING Battery LOW!', styleSheet='color: red')
            
        elif Battery_percentage == "medium":
            controller_status_label = QLabel(f'Battery OK!', styleSheet='color: orange')
        else:
            controller_status_label = QLabel(f'Battery OK!', styleSheet='color: green')
        
        controller_status_label.setWordWrap(True)
        Device_status_layout.addWidget(controller_status_label,1,0)


        Camera1_label = QLabel()
        Camera1_pixmap = QPixmap('images/camera1.png')
        Camera1_pixmap = Camera1_pixmap.scaled(64, 64, Qt.KeepAspectRatio)
        Camera1_label.setPixmap(Camera1_pixmap)
        Device_status_layout.addWidget(Camera1_label,0,1)

        camera1_status_label = QLabel('Camera 1 Status: Connected', styleSheet='color: green')
        camera1_status_label.setWordWrap(True)
        Device_status_layout.addWidget(camera1_status_label,1,1)


        Camera2_label = QLabel()
        Camera2_pixmap = QPixmap('images/camera2.png')
        Camera2_pixmap = Camera2_pixmap.scaled(64, 64, Qt.KeepAspectRatio)
        Camera2_label.setPixmap(Camera2_pixmap)
        Device_status_layout.addWidget(Camera2_label,0,2)

        camera2_status_label = QLabel('Camera 2 Status: Connected', styleSheet='color: green')
        camera2_status_label.setWordWrap(True)
        Device_status_layout.addWidget(camera2_status_label,1,2)


        mouse_label = QLabel()
        mouse_pixmap = QPixmap('images/mouse.png')
        mouse_pixmap = mouse_pixmap.scaled(64, 64, Qt.KeepAspectRatio)
        mouse_label.setPixmap(mouse_pixmap)
        Device_status_layout.addWidget(mouse_label,0,3)

        mouse_status_label = QLabel('Mouse Status: Connected', styleSheet='color: green')
        mouse_status_label.setWordWrap(True)
        Device_status_layout.addWidget(mouse_status_label,1,3)
        
        Device_status_frame.setLayout(Device_status_layout)






        

        rightLayout.addWidget(project_frame)
        rightLayout.addWidget(camera_frame)
        rightLayout.addWidget(motor_frame)
        rightLayout.addWidget(zoom_overivew_frame)
        rightLayout.addWidget(console_frame)
        rightLayout.addWidget(Device_status_frame)


        rightFrame.setLayout(rightLayout)



        mainLayout = QHBoxLayout()
        mainLayout.addWidget(disp_camera1_frame)
        mainLayout.addWidget(rightFrame)
        self.setLayout(mainLayout)



    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        # p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        p = convert_to_Qt_format
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())