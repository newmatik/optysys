import sys
from PyQt5.QtWidgets import *#QApplication, QMainWindow, QLabel, QThread, QVBoxLayout
from PyQt5.QtGui import *#QPixmap
from PyQt5.QtCore import *#Qt
import cv2
import numpy as np
import time
import depthai as dai

from PyQt5.QtCore import pyqtSignal

class VideoThread(QThread):
    update_pixmap = pyqtSignal(QPixmap)

    def __init__(self):
        super().__init__()
        # self.cap = cv2.VideoCapture(2)  # Device 0 is the webcam
        pipeline = dai.Pipeline()

        # Define source and outputs
        camRgb = pipeline.create(dai.node.ColorCamera)
        xoutVideo = pipeline.create(dai.node.XLinkOut)
        xoutPreview = pipeline.create(dai.node.XLinkOut)

        xoutVideo.setStreamName("video")
        xoutPreview.setStreamName("preview")

        # Properties
        camRgb.setPreviewSize(300, 300)
        camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
        camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        camRgb.setInterleaved(True)
        camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

        # Linking
        camRgb.video.link(xoutVideo.input)
        camRgb.preview.link(xoutPreview.input)
        self.device = dai.Device(pipeline) 

        # self.cap = device.getOutputQueue('video')
        # preview = device.getOutputQueue('preview')
        img_number = 0
        # videoFrame = video.get()
        # previewFrame = preview.get()

    def run(self):
        while True:
            # Capture frame-by-frame
            self.cap = self.device.getOutputQueue('video')
            frame = self.cap.get()#read()
            ret = True
            if ret:
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
                time.sleep(0.01)

    def stop(self):
        self.cap.release()
        self.exit()

    def update_label(self, pixmap):
        # Process the events in the queue
        self.app.processEvents()
        # Update the label with the new QPixmap
        self.ui.label.setPixmap(pixmap)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Live Video')

        # Create a custom signal emitter object
        self.video_thread = VideoThread()

        # Connect the update_pixmap signal to the update_label slot
        self.video_thread.update_pixmap.connect(self.update_label)

        # Create the label and layout
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)

        # Start the video thread
        self.video_thread.start()

        # Set the central widget and show the window
        self.setCentralWidget(self.label)
        self.show()

    def update_label(self, pixmap):
        # Update the label with the new QPixmap
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    exit_code = app.exec_()
    sys.exit(exit_code)
