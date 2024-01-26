from utils.motor_interface import motor_interface
from utils.camera import camera_interface
import pygame
from colorama import init, Fore, Style
import time

'''
Camera is controlled with the PS5 controller
Here the camera is the "good camera" with the zoom and focus functions.

Vishaka Srinivasan,Newmatik GmBh
'''
pygame.init()
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
done = False

C = camera_interface()



Flag_controller_power = 0
Zoom_in = 0 
Zoom_out = 0

focus_near = 0
focus_far = 0

flag_zoom_focus = True # True for zoom, False for focus
flag_stop_focus = True

while not done:
    # EVENT PROCESSING STEP
    # print('waiting for event')
    time.sleep(0.01)
    for event in pygame.event.get():
        # print(event)
        try :
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            if Flag_controller_power == 3:
                power_level = joystick.get_power_level()
                print(Fore.BLUE + ' ← Receive: [SETUP] Controller Battery level: '+ str(power_level) + Style.RESET_ALL )
            Flag_controller_power += 1
        except:
            print(Fore.RED + ' ← Receive: [ERROR] in Controller. Connect to charge or change to wired mode '+ Style.RESET_ALL )


        # Camera commands
        if joystick.get_button(5) == 1:
            try:
                print('DISCONNECTED')
                C.close_connection()
                done = True
            except:
                pass


        if flag_zoom_focus:
            # ZOOM MODE
            focus_near = 0
            focus_far = 0

            if event.type == pygame.JOYAXISMOTION:
                if joystick.get_axis(4)> -0.9:#or joystick.get_axis(0)<-0.1) :
                    Zoom_in = 1
                else :
                    Zoom_in = 0

                if joystick.get_axis(5)>-0.9: # or joystick.get_axis(1)<-0.1) :
                    Zoom_out = 1
                else: 
                    Zoom_out = 0

                
        else :
            # FOCUS MODE 
            Zoom_out = 0
            Zoom_in = 0

            if joystick.get_axis(4)> -0.9:
                focus_far = 1
            else :
                focus_far = 0

            if joystick.get_axis(5)>-0.9: 
                focus_near = 1
            else :
                focus_near = 0

        # Zoom in max 
        if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(9) == 1:
            print('zoom in max')
            print('Zoom in max')
            C.zoom_in_max()

        # Zoom out max
        if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(10) == 1:
            print('zoom out max')
            print('Zoom out max')
            C.zoom_out_max()
        
        # toggle modes between focus and zoom
        if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(6) == 1:
            flag_zoom_focus = not flag_zoom_focus
            if flag_zoom_focus:
                print('zooming mode')
            else:
                print('focus mode')

        # autofocus
        if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(4) == 1:
            print('autofocus')
            C.autofocus()

    if Zoom_in !=0:
        # print('Zoom in')
        C.zoom_in()
    elif Zoom_out !=0:
        # print('Zoom out')
        C.zoom_out()
    

    if focus_near !=0:
        # print('Focus near')
        C.focus_near()
    elif focus_far !=0:
        # print('Focus far')
        C.focus_far()
    # else: 
    #     C.stop_focus()
        
            
                
                
        