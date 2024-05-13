import cv2
import numpy as np
import socket
import tkinter as tk
from tkinter import Button, Label, Tk
from PIL import Image, ImageTk

def display_image_with_buttons(image_np):
    root = Tk()
    root.title("Drop or No Drop")

    # Convert the image from OpenCV format to PIL format
    image_pil = Image.fromarray(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
    # Resize the image to fit the window if necessary
    max_width = 800
    if image_pil.width > max_width:
        image_pil.thumbnail((max_width, max_width), Image.ANTIALIAS)

    # Convert the PIL image to Tkinter format and display it
    image_tk = ImageTk.PhotoImage(image_pil)
    label = Label(root, image=image_tk)
    label.image = image_tk
    label.pack()

    # Function to send the choice back to the client
    def send_choice(choice):
        root.destroy()
        conn.send(choice.encode())

    # Button for "Drop"
    button_drop = Button(root, text="Drop", command=lambda: send_choice("drop"))
    button_drop.pack(side=tk.LEFT)

    # Button for "No Drop"
    button_no_drop = Button(root, text="No Drop", command=lambda: send_choice("no drop"))
    button_no_drop.pack(side=tk.RIGHT)

    root.mainloop()

# Set up socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

print("Server started. Listening for connections...")

while True:
    conn, addr = server_socket.accept()
    print("Connected to", addr)

    # Receive image from client
    data = b""
    while True:
        packet = conn.recv(4096)
        if not packet:
            break
        data += packet
    image_np = np.frombuffer(data, dtype=np.uint8)
    image_np = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    # Display the image in a GUI with "Drop" and "No Drop" buttons
    display_image_with_buttons(image_np)

    conn.close()
