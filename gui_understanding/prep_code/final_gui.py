from PyQt5.QtCore import *
from PyQt5.QtWidgets import *# QApplication, QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import *# QPixmap

from colorama import init, Fore, Style
import time
import cv2
import depthai as dai
import numpy as np


class VideoThread(QThread):
    update_pixmap = pyqtSignal(QPixmap)

    def __init__(self):
        super().__init__()
        # self.cap = cv2.VideoCapture(2)  # Device 0 is the webcam
        pipeline = dai.Pipeline()

        # Define source and outputs
        camRgb = pipeline.create(dai.node.ColorCamera)
        xoutVideo = pipeline.create(dai.node.XLinkOut)
        # xoutPreview = pipeline.create(dai.node.XLinkOut)

        xoutVideo.setStreamName("video")
        # xoutPreview.setStreamName("preview")

        # Properties
        camRgb.setPreviewSize(300, 300)
        camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
        camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        camRgb.setInterleaved(True)
        camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

        # Linking
        camRgb.video.link(xoutVideo.input)
        # camRgb.preview.link(xoutPreview.input)
        self.device = dai.Device(pipeline) 

        # self.cap = device.getOutputQueue('video')
        # preview = device.getOutputQueue('preview')
        # img_number = 0
        # videoFrame = video.get()
        # previewFrame = preview.get()

    def run(self):
        # while True:
        # Capture frame-by-frame
        self.cap = self.device.getOutputQueue('video')
        frame = self.cap.get()#read()
        ret = True
        if ret:
            frame = self.cap.get()#read()
            # Convert frame to RGB format
            frame = frame.getCvFrame()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the RGB frame to a QImage
            image = QImage(rgb_frame.data, rgb_frame.shape[1], rgb_frame.shape[0], QImage.Format_RGB888)

            # Create a QPixmap from the QImage
            pixmap = QPixmap.fromImage(image)

            # Emit the update_pixmap signal with the QPixmap
            self.update_pixmap.emit(pixmap)

            # Wait a few milliseconds
            time.sleep(0.001)

    def stop(self):
        self.cap.release()
        self.exit()

    def update_label(self, pixmap):
        # Process the events in the queue
        self.app.processEvents()
        # Update the label with the new QPixmap
        self.ui.label.setPixmap(pixmap)



class gui_call():

    def __init__(self,):

        
        # initializing Qapplication
        app = QApplication([])
        window = QWidget()
        window.setGeometry(
            (QApplication.desktop().screenGeometry().center().x() - 400),
            (QApplication.desktop().screenGeometry().center().y() - 300),
            600,
            400,
            )



        self.imageLabel = QLabel()
        self.video_thread = VideoThread()

        # Connect the update_pixmap signal to the update_label slot
        self.video_thread.update_pixmap.connect(self.update_label)
        # image = QPixmap(videoFrame.getCvFrame())#'images/bus.jpg')
        # imageLabel.setPixmap(image)
        # self.video_thread.start()
        self.video_thread.run()
        

        
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

        camera1_status_label = QLabel('Camera 1 Status: Connected')
        camera1_status_label.setWordWrap(True)
        Device_status_layout.addWidget(camera1_status_label,1,1)


        Camera2_label = QLabel()
        Camera2_pixmap = QPixmap('images/camera2.png')
        Camera2_pixmap = Camera2_pixmap.scaled(64, 64, Qt.KeepAspectRatio)
        Camera2_label.setPixmap(Camera2_pixmap)
        Device_status_layout.addWidget(Camera2_label,0,2)

        camera2_status_label = QLabel('Camera 2 Status: Connected')
        camera2_status_label.setWordWrap(True)
        Device_status_layout.addWidget(camera2_status_label,1,2)


        mouse_label = QLabel()
        mouse_pixmap = QPixmap('images/mouse.png')
        mouse_pixmap = mouse_pixmap.scaled(64, 64, Qt.KeepAspectRatio)
        mouse_label.setPixmap(mouse_pixmap)
        Device_status_layout.addWidget(mouse_label,0,3)

        mouse_status_label = QLabel('Mouse Status: Connected')
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

        
        
        # rightFrame.setLayout(rightLayout)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.imageLabel)
        mainLayout.addWidget(rightFrame)
        window.setLayout(mainLayout)
        window.show()
        app.exec_()

    def on_button_clicked(self, button_name:str):
        print(button_name)
        self.op_text.append(button_name)

    def tracking(self,pos,rem,add):
        global prev_txt
        current_txt = self.console.toPlainText()
        if add>0: #if add
            print('What was added: ', current_txt[pos:pos+add])
        if rem>0: # if remove
            print('What was removed: ', prev_txt[pos:pos+rem])
        prev_txt = current_txt
    def update_label(self, pixmap):
        # Update the label with the new QPixmap
        self.imageLabel.setPixmap(pixmap)


if __name__ == '__main__':
    gui_call()