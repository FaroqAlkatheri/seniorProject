import machine
import time

# Setup UART communication
uart = machine.UART(1, baudrate=9600, tx=17, rx=18)  # UART 2, adjust pins and UART number as necessary

def read_gps():
    buffer = bytearray(128)  # Create a buffer to store data
    while True:
        if uart.any():  # Check if there is data waiting on UART
            gps_data = uart.readinto(buffer)  # Read data into buffer
            print('Raw GPS data:', buffer[:gps_data].decode().strip())  # Decode and print GPS data

            # Here, you could add parsing logic to extract specific details like latitude, longitude, etc.
            # For a full implementation, you would parse the NMEA sentences here.

        time.sleep(0.1)  # Sleep to allow other tasks to run

try:
    read_gps()
except KeyboardInterrupt:
    print("Stopped by User")

# Note: Handling NMEA sentences parsing for extracting specific information like coordinates, time, etc., would require additional logic.

