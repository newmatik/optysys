import cv2
import depthai as dai
import pygame
from colorama import init, Fore, Style
import time
# Create pipeline
'''
Viewing and saving images from openCV Camera. 
Everything is operated with PS5 controller. 
The following script has two functions: 
1. View the camera feed and save images with the 'X' button
2. Disconnect the camera with the 'O' button 



Vishaka Srinivasan, Newmatik GmBh
'''




## prep for reading camera 
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

# Connect to device and start pipeline


pygame.init()
clock = pygame.time.Clock()
# Initialize the joysticks
pygame.joystick.init()

done = False


Flag_controller_power = 0
device = dai.Device(pipeline) 

video = device.getOutputQueue('video')
preview = device.getOutputQueue('preview')
img_number = 0
while not done:
    videoFrame = video.get()
    previewFrame = preview.get()

    # Get BGR frame from NV12 encoded video frame to show with opencv
    cv2.imshow("video", videoFrame.getCvFrame())
    # Show 'preview' frame as is (already in correct format, no copy is made)
    # cv2.imshow("preview", previewFrame.getFrame())

    # time.sleep(0.01)
    for event in pygame.event.get():
        # print(event)
        try :
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            if Flag_controller_power ==3:
                power_level = joystick.get_power_level()
                print(Fore.BLUE + ' ← Receive: [SETUP] Controller Battery level: '+ str(power_level) + Style.RESET_ALL )
            Flag_controller_power += 1
        except:
            print(Fore.RED + ' ← Receive: [ERROR] in Controller. Connect to charge or change to wired mode '+ Style.RESET_ALL )


        if  event.type == pygame.JOYBUTTONDOWN and joystick.get_button(5) == 1:
            print(Fore.BLUE + ' ← Receive: [SETUP] Disconnecting '+ str(power_level) + Style.RESET_ALL )
            done = True


        if  event.type == pygame.JOYBUTTONDOWN and joystick.get_button(2) == 1:
            print('SAVE')
            img_number +=1
            image_save_path = f'saved_img/video_{img_number}.png'
            cv2.imwrite(image_save_path, videoFrame.getCvFrame())






    