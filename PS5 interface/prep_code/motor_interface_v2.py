import serial
import serial.tools.list_ports
import pprint
import time
import sys
import tty
import termios
import json
from colorama import init, Fore, Style


'''
Important code for motor interface testing
'''

# Load Grbl error codes from JSON file
with open('grbl_errorcodes.json') as f:
    error_codes = json.load(f)

# Pretty Print and Colorama for terminal printout
pp = pprint.PrettyPrinter(indent=4, width=80)
init() # Colorama init

# Welcome message
print(Fore.YELLOW + "\nGrbl Python Demo" + Style.RESET_ALL)
print(Fore.YELLOW + "----------------" + Style.RESET_ALL)

# Send gcode through serial write and readline
def send_gcode(gcode):
    try:
        read = ''
        s.flushInput() # Flush startup text in serial input
        s.write(str.encode(gcode + '\n'))
        print(Fore.CYAN + '→ Send: ' + str(str.encode(gcode)), end='')
        read = s.readline().strip().decode('utf-8').strip()
        if read.startswith('error:'):
            error_num = int(read.split(':')[1])
            error_msg = error_codes[str(error_num)]
            print(Fore.RED + ' ← Receive: [ERROR] ' + read + ' (' + error_msg + ')' 
                + Style.RESET_ALL)
        elif read != 'ok':
            print(Fore.MAGENTA + ' ← Receive: [INFO] ' + read + Style.RESET_ALL)
        else:
            print(Fore.GREEN + ' ← Receive: [OK]' + Style.RESET_ALL)
    except serial.SerialException as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
        exit(1)

# List all serial ports
def list_serial_ports():
    serial_ports = serial.tools.list_ports.comports(include_links=True)
    return serial_ports

# Print all available serial ports on console
print(Fore.YELLOW + 'Available serial ports:' + Style.RESET_ALL)
pp.pprint(list_serial_ports())

# Open grbl serial port
try:
    s = serial.Serial('/dev/tty.usbserial-AQ02Z8ND', 115200) # put your serial port here
    print(Fore.YELLOW + 'Connected to: ' + Style.RESET_ALL + s.name)
    # Print status of serial port
    print(Fore.YELLOW + 'Serial port open: ' + Style.RESET_ALL + str(s.is_open) +
        Style.RESET_ALL)
except (ValueError, serial.SerialException, FileNotFoundError) as e:
    print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
    exit(1)

# Initialize grbl
print(Fore.YELLOW + '\nInitializing: ' + Style.RESET_ALL)
print('[Wake up grbl] ', end='')
send_gcode('\r\n\r') # Wake up grbl
time.sleep(2)   # Wait for grbl to initialize
s.flushInput() # Flush startup text in serial input

print('[Resetting Errors] ', end='')
send_gcode('$X') # Reset errors
print('[Homing] ', end='')
send_gcode('$H') # Homing

def jog(x, y, f):
    # Send jog command in relative mode and millimeter units
    send_gcode(f'$J = G91 G21 X{x} Y{y} F{f}')

# Function to read arrow keys from keyboard
def read_arrow_keys():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch = sys.stdin.read(2)
            if ch == '[A':
                print('\r[Up arrow pressed] ', end='')
                jog(0, 10, 5000)
            elif ch == '[B':
                print('\r[Down arrow pressed] ', end='')
                jog(0, -10, 5000)
            elif ch == '[C':
                print('\r[Right arrow pressed] ', end='')
                jog(10, 0, 5000)
            elif ch == '[D':
                print('\r[Left arrow pressed] ', end='')
                jog(-10, 0, 5000)
        elif ch.upper() == 'Z':
            print('\r[Null Key Pressed] ', end='')
            send_gcode("G1 X0 Y0 Z0.0 F10000")
        elif ch.upper() == 'H':
            print('\r[Homing Key Pressed] ', end='')
            send_gcode("$H")
        elif ch.upper() == 'C':
            print('\r[Center Key Pressed] ', end='')
            send_gcode("G1 X390 Y150 Z0.0 F10000")
        elif ch.upper() == 'Q':
            print(Fore.YELLOW + "\n[Exit Key Pressed]" + Style.RESET_ALL)
            s.close()
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            exit() # Exit program
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# Wait for keyboard inputs
print(Fore.YELLOW + '\nENTERING JOG MODE' + Style.RESET_ALL)
print(Fore.YELLOW + '-----------------' + Style.RESET_ALL)
print(Fore.YELLOW + 'INFO: Press "Q" to exit, "H" for homing, ' 
    + '"C" to center or "Z" to go to zero.\n' + Style.RESET_ALL)
while True:
    read_arrow_keys()