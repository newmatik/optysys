from utils.motor_interface import motor_interface
import pygame
from colorama import init, Fore, Style
import time



'''

This is just the interface of  the controller with the motors. 

VIshaka Srinivasan, Newmatik GmBh
'''
pygame.init()
clock = pygame.time.Clock()
# Initialize the joysticks
pygame.joystick.init()
# print(pygame.joystick.Joystick.get_power_level)
done = False

M = motor_interface()
X = 0
Y = 0
Flag_controller_power = 0

while not done:
    # EVENT PROCESSING STEP
    time.sleep(0.01)
    for event in pygame.event.get():
        # print(event)
        try :
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            if Flag_controller_power < 10:
                power_level = joystick.get_power_level()
                print(Fore.BLUE + ' ← Receive: [SETUP] Controller Battery level: '+ str(power_level) + Style.RESET_ALL )
                Flag_controller_power += 1
        except:
            print(Fore.RED + ' ← Receive: [ERROR] in Controller. Connect to charge or change to wired mode '+ Style.RESET_ALL )

        # Motor Commands
        if joystick.get_button(5) == 1:
            print('DISCONNECTED')
            M.close_connection()
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

    # jog move 
    if X!=0 or Y != 0:
        M.big_move(X,Y)
        print(Fore.GREEN + f' ← Receive: [OK] jogging X:{X} Y:{Y} '+ Style.RESET_ALL )
            
            
                
                
        