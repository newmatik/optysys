import time
import serial
from colorama import init, Fore, Style
from pynput import keyboard
from pynput.keyboard import Key
import json


'''
This script contains all the functions to control the motors.

Vishaka Srinivasan, Newmatik GmBH
'''
class motor_interface():
    def __init__(self):
        # Open serial communication
        serial_port = 'COM3' # Example: 'COM1' for Windows or '/dev/ttyUSB0' for Linux
        ser = serial.Serial(serial_port, baudrate=115200, timeout=1)
        # Wake up GRBL
        self.ser = ser
        ser.write(b"\r\n\r\n")
        time.sleep(2) # Wait for the initialization to complete
        print(Fore.BLUE + ' ← Receive: [SETUP] Connecting Motors ' + Style.RESET_ALL )


        # get error codes 
        file_path = 'utils/grbl_errors.json'
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        self.error_grbl = data


        # Flush input and output buffer
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(b"$X\n")
        self.home()

        
    def send_gcode(self,movement_command):
            # Send a movement command  Example: Move X-axis 100mm at a speed of 200mm/min


            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()

            self.ser.write(movement_command)
            read = self.ser.readline().strip().decode('utf-8').strip()
            if read.startswith('error:'):
                error_num = int(read.split(':')[1])
                error_msg = self.error_grbl[str(error_num)]
                # error_msg = str(error_num)
                print(Fore.RED + ' ← Receive: [ERROR] ' + read + ' (' + error_msg + ')' 
                    + Style.RESET_ALL)
            elif read != 'ok':
                print(Fore.MAGENTA + ' ← Receive: [INFO] ' + read + Style.RESET_ALL)
            else:
                print(Fore.GREEN + ' ← Receive: [OK]' + Style.RESET_ALL)
            if read == b'OK':   
            
                print('Waiting for next command')
            # time.sleep(0.01)
            done = False
            # while not done:
            #     movement_command = b'?\n'
            #     self.ser.write(movement_command)
            #     read = self.ser.readline().strip().decode('utf-8').strip()
            #     read = read.split('|')
            #     # print(read[0])
            #     if read[0] =='<Idle': # or read[0] == '':
            #         done = True
            #         print('Idle')
            return True

    def close_connection(self):
        print(Fore.BLUE + ' ← Receive: [SETUP] Switching OFF communication with motors '+ Style.RESET_ALL )
        self.ser.close()
        

    def jog(self,x, y, f,t=5):
        # Send jog command in relative mode and millimeter units
        command = f'$J = G91 G21 X{x} Y{y} F{f}\n'
        # command = f'$J = $X{x} Y{y} F{f}\n'
        check = self.send_gcode(command.encode('utf-8'))
        return check

    def on_key_release(self,key):

        if key == Key.right:
            print("Right key clicked")
            self.jog(10, 0, 5000,1)
        elif key == Key.left:
            print("Left key clicked")
            self.jog(-10, 0, 5000,1)
        elif key == Key.up:
            print("Up key clicked")
            self.jog(0, 10, 5000,1)
        elif key == Key.down:
            print("Down key clicked")
            self.jog(0, -10, 5000,1)
        elif key == Key.esc:
            exit()
        elif key.char == 'h' or key.char == 'H':
            self.send_gcode(b"$H\n")

    def step_left(self,t=3):
        check = self.jog(-10, 0, 5000,t)
        return check

    def step_right(self,t=3):
        self.jog(10, 0, 5000,t)

    def step_up(self,t=3):
        self.jog(0, 10, 5000,t)
    
    def step_down(self,t=3):
        self.jog(0, -10, 5000,t)
    
    def big_move(self,x,y,t=5):
        check = self.jog(x, y, 5000,t)
        return check
    def stop(self):
        self.ser.write(b"$X\n")
        print('stopped')

    def home(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.ser.write(b"$X\n")
        # Send command to home the machine
        self.ser.write(b"$H\n") # Homing command for GRBL
        # Wait for response
        # while True:
        #     self.ser.flushInput()
        #     response = self.ser.readline().strip()
            
        #     if response == b'ok':
                
        #         break
        # time.sleep(10)
        time.sleep(0.01)
        done = False
        while not done:
            movement_command = b'?\n'
            self.ser.write(movement_command)
            read = self.ser.readline().strip().decode('utf-8').strip()
            read = read.split('|')
            # print(read[0])
            if read[0] =='<Idle': # or read[0] == '':
                done = True
                # print('Idle')
        print(Fore.BLUE + ' ← Receive: [SETUP] Done Homing ' + Style.RESET_ALL )

    

    
    # def controller_key(self,key,t=5):
    #     if key == 'right':
    #         print("Right key clicked")
    #         self.jog(10, 0, 5000,t)
    #     elif key == 'left':
    #         print("Left key clicked")
    #         self.jog(-10, 0, 5000,t)
    #     elif key == 'up':
    #         print("Up key clicked")
    #         self.jog(0, 10, 5000,t)
    #     elif key == 'down':
    #         print("Down key clicked")
    #         self.jog(0, -10, 5000,t)
    #     elif key == 'esc':
    #         self.close_connection()
    #     elif key == 'home':
    #         self.send_gcode(b"$H\n")
        

if __name__ == "__main__":

    M = motor_interface()
    # movement_command = b"G0 X10 Y10 Z0 F10\n"
    # M.send_gcode(movement_command)
    # movement_command = b"G0 X100 Y100 Z0 F10\n"
    # M.send_gcode(movement_command)





    with keyboard.Listener(on_release=M.on_key_release) as listener:
        listener.join()



    M.close_connection()


