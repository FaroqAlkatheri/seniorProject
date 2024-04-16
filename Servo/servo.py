from machine import Pin, PWM
import time

# Define the GPIO pins where the servos are connected
SERVO_PIN1 = 5  # Replace with the actual GPIO pin you're using
SERVO_PIN2 = 6  # Replace with the actual GPIO pin you're using

# Initialize PWM objects for both servos
servo1 = PWM(Pin(SERVO_PIN1), freq=50)
servo2 = PWM(Pin(SERVO_PIN2), freq=50)

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

# Call the function to release the payload
release_payload()

