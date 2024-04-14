import serial

# Replace with the port name of your USB-to-UART adapter on Windows
serial_port = 'COM4'  # Replace 'x' with the assigned port number (e.g., COM3)

# Set the baud rate to match the MicroPython code
baud_rate = 115200


# Open the serial connection
ser = serial.Serial(serial_port, baud_rate)

# Prepare the call data/command string
call_data = 'initiate_call'  # Replace with your specific command or data

# Send the data over UART
ser.write(call_data.encode())

# Optionally receive a response
response = ser.readline().decode()
print(response)
ser.close()
