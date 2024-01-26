from utils.motor_interface import motor_interface
from utils.camera import camera_interface
import pygame
from colorama import init, Fore, Style
import time
import cv2
import depthai as dai


'''
Motor Camera  are controlled using PS4 controller. 
Camera is openCV camera. The images from this camera can be saved. 

Vishaka Srinivasan, Newmatik GmBH
'''

def map_decimal_to_integer(decimal_value):
    # Scale the decimal value to the range 0 to 1
    scaled_value = (decimal_value + 1) / 2.0

    # Map the scaled value to the range 0 to 7
    mapped_integer = int(scaled_value * 8)

    # Ensure the mapped value stays within the range [0, 7]
    mapped_integer = max(0, min(mapped_integer, 7))

    return mapped_integer

pygame.init()
clock = pygame.time.Clock()
# Initialize the joysticks
pygame.joystick.init()
# print(pygame.joystick.Joystick.get_power_level)
done = False


C = camera_interface()
# C = camera_interface()
M = motor_interface()

X = 0
Y = 0
Flag_controller_power = 0
Zoom_in = -1 
Zoom_out = -1

focus_near = 0
focus_far = 0

flag_zoom_focus = True # True for zoom, False for focus
flag_stop_focus = True


#### other camera 
# Create pipeline
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


device = dai.Device(pipeline)
video = device.getOutputQueue('video')
preview = device.getOutputQueue('preview')
img_number = 0

while not done:
    # EVENT PROCESSING STEP
    time.sleep(0.01)
    videoFrame = video.get()
    previewFrame = preview.get()

    # Get BGR frame from NV12 encoded video frame to show with opencv
    cv2.imshow("video", videoFrame.getCvFrame())
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

        # Motor Commands
        if joystick.get_button(5) == 1:
            # print('DISCONNECTED')
            print(Fore.BLUE + ' ← Receive: [SETUP] Disconnecting Everything ' + Style.RESET_ALL )
            M.close_connection()
            time.sleep(1)
            C.close_connection()
            done = True
            

        
        if joystick.get_button(15) == 1:
            print('centre')  
            movement_command = b"G0 X100 Y100 Z0 F10\n"
            M.send_gcode(movement_command)

        # step left
        if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(13) == 1:
            print(Fore.GREEN + f' ← Receive: [OK] step left '+ Style.RESET_ALL )
            M.step_left()

        # step right
        if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(14) == 1:
            print(Fore.GREEN + f' ← Receive: [OK] step right '+ Style.RESET_ALL )
            M.step_right()


        # step up
        if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(11) == 1:
            print(Fore.GREEN + f' ← Receive: [OK] step up '+ Style.RESET_ALL )
            M.step_up()


        # step down
        if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(12) == 1:
            print(Fore.GREEN + f' ← Receive: [OK] step down '+ Style.RESET_ALL )
            M.step_down()


        # get values for jogging
        if abs(joystick.get_axis(0))>=0.1:#or joystick.get_axis(0)<-0.1) :
            X = round(joystick.get_axis(0),1)*2
        else :
            X = 0
        if abs(joystick.get_axis(1))>=0.1: # or joystick.get_axis(1)<-0.1) :
            Y = round(joystick.get_axis(1)*(-1),1)*2 #(-20)
        else :
            Y = 0



        # Camera commands
        if flag_zoom_focus:
            # ZOOM MODE
            focus_near = 0
            focus_far = 0

            if event.type == pygame.JOYAXISMOTION:
                if joystick.get_axis(5)> -0.9:#or joystick.get_axis(0)<-0.1) :
                    val = round(joystick.get_axis(5),1)
                    Zoom_in = map_decimal_to_integer(val)#1
                    
                else :
                    Zoom_in = -1

                if joystick.get_axis(4)>-0.9: # or joystick.get_axis(1)<-0.1) :
                    val = round(joystick.get_axis(4),1)
                    Zoom_out = map_decimal_to_integer(val)
                else: 
                    Zoom_out = -1

                
        else :
            # FOCUS MODE 
            Zoom_out = -1
            Zoom_in = -1

            if joystick.get_axis(4)> -0.9:
                focus_far = 1
            else :
                focus_far = 0

            if joystick.get_axis(5)>-0.9: 
                focus_near = 1
            else :
                focus_near = 0

        # Zoom in max 
        if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(10) == 1:
            print(Fore.BLUE + f' ← Received: [Zooming IN]'+ Style.RESET_ALL )
            C.zoom_in_max()

        # Zoom out max
        if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(9) == 1:
            print(Fore.BLUE + f' ← Received: [Zooming OUT]'+ Style.RESET_ALL )
            C.zoom_out_max()
        
        # toggle modes between focus and zoom
        if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(6) == 1:
            flag_zoom_focus = not flag_zoom_focus
            if flag_zoom_focus:
                print(Fore.BLUE + f' ← Received: [ZOOMING MODE]'+ Style.RESET_ALL )
            else:
                print(Fore.BLUE + f' ← Received: [FOCUS MODE]'+ Style.RESET_ALL )

        # autofocus
        if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(4) == 1:
            print(Fore.BLUE + f' ← Received: [Auto Focus] '+ Style.RESET_ALL )
            C.autofocus()

        if  event.type == pygame.JOYBUTTONDOWN and joystick.get_button(2) == 1:
            print('SAVE')
            img_number +=1
            image_save_path = f'saved_img/video_{img_number}.png'
            cv2.imwrite(image_save_path, videoFrame.getCvFrame())

    # jog move 
    if X!=0 or Y != 0:
        M.big_move(X,Y)
        # print(Fore.BLUE + f' ← Receiv
        # ed: jogging X:{X} Y:{Y} '+ Style.RESET_ALL )


    if Zoom_in > 0:
        print(Fore.BLUE + f' ← Received: [ZOOMING In Step]'+ Style.RESET_ALL )
        C.zoom_in(Zoom_in)
    elif Zoom_out >0:
        print(Fore.BLUE + f' ← Received: [ZOOMING Out Step]'+ Style.RESET_ALL )
        C.zoom_out(Zoom_out)
    

    if focus_near !=0:
        print('Focus near')
        C.focus_near()
    elif focus_far !=0:
        print('Focus far')
        C.focus_far() 
            
            
