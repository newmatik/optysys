import time
import serial

'''
Sample code for motor interface

'''
# Open grbl serial port
serial_port = 'COM3' #'/dev/tty.usbserial-AQ02Z8ND'
s = serial.Serial(serial_port, baudrate=11520,timeout=1) # put your serial port here
print('Connected to: ', s.name)
print('Serial port open: ', str(s.is_open))

# Serial write and readline
def send_gcode(gcode):
    s.write(str.encode(gcode))
    print('Sending: ' + str(str.encode(gcode)))
    check = s.readline().strip()
    print(check)

# Wake up grbl
send_gcode('\r\n\r\n')
time.sleep(2)   # Wait for grbl to initialize
print('done initalization')
# s.flushInput()  # Flush startup text in serial input
# Flush input and output buffer
s.reset_input_buffer()
s.reset_output_buffer()
send_gcode('$X') # Reset errors
send_gcode('$H') # Homing
time.sleep(5)
send_gcode('G1 X100 Y100  F5000') # Go to X:100, Y:100, Z:0.0 at 5000 mm/min

# Close serial port
s.close()