import machine
from machine import Pin, PWM
import time

# Setup UART communication
gps_uart = machine.UART(1, baudrate=9600, tx=17, rx=18)  # UART 1
pc_uart = machine.UART(2, baudrate=9600, tx=10, rx=11)  # UART 2

SERVO_PIN1 = 5  # Replace with the actual GPIO pin you're using
SERVO_PIN2 = 6  # Replace with the actual GPIO pin you're using


servo1 = PWM(Pin(SERVO_PIN1), freq=50)
servo2 = PWM(Pin(SERVO_PIN2), freq=50)


# Define the duty for servo positions
MIN_DUTY = 30  # Typically the duty cycle for the 0-degree position
MAX_DUTY = 125  # Typically the duty cycle for the 180-degree position

#####################################################################################
#Servo motor
# Define the duty for servo positions
MIN_DUTY = 30  # Typically the duty cycle for the 0-degree position
MAX_DUTY = 125  # Typically the duty cycle for the 180-degree position

def map_range(x, in_min, in_max, out_min, out_max):
    # Maps a number from one range to another.
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def set_servo_angle(servo, angle):
    # Sets the servo to the specified angle.
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180
    duty = map_range(angle, 0, 180, MIN_DUTY, MAX_DUTY)
    servo.duty(duty)

def release_payload():
    # Move servos to release payload
    print("realeasing ........")
    set_servo_angle(servo1, 0)   # Adjust the angle to match the release mechanism
    set_servo_angle(servo2, 180) # Adjust the angle to be the opposite of servo1

    # Wait 3 seconds
    print("Sleep")
    time.sleep(3)

    # Move servos back to initial position
    print("Moving back")
    set_servo_angle(servo1, 90) # Adjust the angle as per your mechanism's "closed" position
    set_servo_angle(servo2, 90) # Adjust the angle to be the initial position (same as servo1)

#####################################################################################

def read_gps():
    #GPS Pinout
    # GPS     ESP32
    # VIN     3.3v
    # GND     GND
    # TX      RX
    # RX
    
    while True:
        buffer = bytearray(128)  # Create a buffer to store data
        if gps_uart.any():  # Check if there is data waiting on UART
            gps_data = gps_uart.readinto(buffer)  # Read data into buffer
            data = buffer[:gps_data].decode().strip()
            print('Raw GPS data:', data)  # Decode and print GPS
            return data
        
        

            # Here, you could add parsing logic to extract specific details like latitude, longitude, etc.
            # For a full implementation, you would parse the NMEA sentences here.

def read_pc():
    print("Waiting for mission Signal")
    while True:
        buffer = bytearray(128)  # Create a buffer to store data
        if pc_uart.any():  # Check if there is data waiting on UART
            pc_data = pc_uart.readinto(buffer)  # Read data into buffer
            print(pc_data)
            data = buffer[:pc_data].decode('utf-8').strip()
            if data == 'starting mission':
                read_gps()
                release_payload()
                break

                    
try:
    read_pc()
except KeyboardInterrupt:
    print("Stopped by User")




