import serial
import time
from colorama import init, Fore, Style
from pynput import keyboard
from pynput.keyboard import Key

'''
Contains all the functions to control the camera

Vishaka Srinivasan, Newmatik GmBH
'''
class camera_interface():

    def __init__(self):
        # Define the serial port and baud rate
        self.ser = serial.Serial('COM4', 9600, timeout=1)
        print(Fore.BLUE + ' ← Receive: [SETUP] Switching Camera ON '+ Style.RESET_ALL )
        self.switch_on = "81 01 04 00 02 FF"
        self.send_visca_command(self.switch_on)


    def send_visca_command(self,command):
        # Convert the command to bytes
        command_bytes = bytes.fromhex(command)
        
        # Send the command
        self.ser.write(command_bytes)
        time.sleep(0.01)  # Wait for the command to be processed
        
        # Read response if needed
        response = self.ser.read()  # Adjust the number of bytes to read based on your device's response length
        return response#.decode('utf-8')

    # All zoom commands
    def zoom_in(self,speed=0):
        command= f"81 01 04 07 2{speed} FF" # 0 (3rd from right) can be changed to a value between 0 to 7
        response = self.send_visca_command(command)
        self.stop_zooming(t=0)
        return response
    
    def zoom_out(self,speed = 0):
        command= f"81 01 04 07 3{speed} FF" # 0 (3rd from right) can be changed to a value between 0 to 7
        response = self.send_visca_command(command)
        self.stop_zooming(0)
        return response
    
    def stop_zooming(self, t= 0.01):
        time.sleep(t)
        stop_zoom = "81 01 04 07 00 FF"
        self.send_visca_command(stop_zoom)
    
    
    def zoom_out_max(self):
        command= "81 01 04 07 37 FF" 
        response = self.send_visca_command(command)
        return response
    
    def zoom_in_max(self):
        command= "81 01 04 07 25 FF"#"81 01 04 47 0200 0200 0200 0200 FF" 
        response = self.send_visca_command(command)
        self.stop_zooming(t=1)

        return response

    # All focus commands
    def focus_near(self):
        # self.stop_focus()
        command = '81 01 04 08 35 FF'#'81 01 04 08 03 FF'
        response = self.send_visca_command(command)
        return response

    def focus_far(self):
        # self.stop_focus()
        command = '81 01 04 08 25 FF'#'81 01 04 08 02 FF'
        response = self.send_visca_command(command)
        return response

    def autofocus(self):
        command = '81 01 04 18 01 FF'#"81 01 04 57 00 FF" #"81 01 04 18 01 FF"
        
        response = self.send_visca_command(command)
        return response
    
    def stop_focus(self):
        command = "81 01 04 08 00 FF"
        response = self.send_visca_command(command)
        return response



    def close_connection(self):
        print(Fore.BLUE + ' ← Receive: [SETUP] Switching Camera OFF '+ Style.RESET_ALL )
        command = "81 01 04 00 03 FF"   
        response = self.send_visca_command(command)
        print('closing response',response)
        print(Fore.BLUE + ' ← Receive: [SETUP] Switching OFF communication with camera '+ Style.RESET_ALL )
        try:
            self.ser.close()
        except:
            pass
        return True




    def on_key_release(self,key):
        # print(key)
        if key == keyboard.Key.esc:
            self.close_connection()
            return False
        elif key == keyboard.Key.up:
            print('zoom in')
            self.zoom_in()
        elif key == keyboard.Key.down:
            print('zoom out')
            self.zoom_out()
        elif key == keyboard.Key.left:
            print('focus near')
            self.focus_near()
        elif key == keyboard.Key.right:
            print('focus far')
            self.focus_far()
        elif key == keyboard.Key.space:
            print('autofocus')
            self.autofocus()
        elif key.char == 'h' or key.char == 'H':
            print('zoom out completely')
            self.zoom_home()
        else:
            pass
            # stop_zoom = "81 01 04 07 00 FF"
            # self.send_visca_command(stop_zoom)


if __name__ == "__main__":
    C = camera_interface()

    with keyboard.Listener(on_release=C.on_key_release) as listener:
            listener.join()