import cv2

import serial
import serial.tools.list_ports
import time
from tensorflow.keras.models import load_model
import numpy as np
import os

# Load trained model
model_path = r"C:\Users\Dhiru\Music\new\new\waste_classification_model.keras"
if not os.path.exists(model_path):
    print(f"Error: Model file '{model_path}' not found!")
    exit()
model = load_model(model_path)

# Function to find and connect to Arduino
def find_arduino():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "Arduino" in port.description:
            try:
                arduino_conn = serial.Serial(port.device, 9600, timeout=1)
                time.sleep(2)  # Allow Arduino to initialize
                print(f"Connected to Arduino on {port.device}")
                return arduino_conn
            except serial.SerialException as e:
                print(f"Error connecting to Arduino: {e}")
    print("Arduino not found. Please check the connection.")
    return None

try:
    arduino = serial.Serial("COM10", 9600, timeout=1)  # Replace COM3 with your actual port
    time.sleep(2)
    print("Connected to Arduino.")
except Exception as e:
    print(f"Failed to connect to Arduino: {e}")
    arduino = None


# Open video capture (try webcam first, then IP camera)
cap = cv2.VideoCapture('http://192.168.137.246:8080/video')
if not cap.isOpened():
    print("Error: Could not open video source")
    exit()

# Define categories and angles
categories = {
    "Plastic": 0,
    "Glass": 45,
    "Metal": 90,
    "Paper": 135,
    "Cardboard": 180,
    "foodwaste": 180
}

# Create directories for categories
for category in categories.keys():
    os.makedirs(category, exist_ok=True)

# Function to preprocess the frame
def preprocess_frame(frame):
    img = cv2.resize(frame, (150, 150))
    img = img.astype('float32') / 255
    img = np.expand_dims(img, axis=0)
    return img

# Function to send data to Arduino
def send_to_arduino(letter, angle):
    if arduino:
        command = f"{letter},{angle}\n"
        try:
            arduino.flushOutput()
            arduino.write(command.encode())
            print(f"Sent to Arduino: '{command.strip()}'")
            time.sleep(0.5)
            response = arduino.readline().decode().strip()
            if response:
                print(f"Arduino response: {response}")
        except serial.SerialException as e:
            print(f"Serial error: {e}. Retrying...")
    else:
        print("Arduino is not connected. Skipping communication.")

# Main loop
image_counter = 0  # Counter for saved images
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        break

    frame_height, frame_width = frame.shape[:2]
    circle_radius = 300
    circle_center = (frame_width // 2, frame_height // 4)

    # Draw guiding circle
    cv2.circle(frame, circle_center, circle_radius, (0, 255, 0), 3)
    cv2.putText(frame, "Place object inside the circle. Press 'c' to classify. Press 'q' to quit.",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.imshow('Video Feed', frame)

    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('c'):  # Capture and classify
        mask = np.zeros_like(frame)
        cv2.circle(mask, circle_center, circle_radius, (255, 255, 255), -1)
        roi = cv2.bitwise_and(frame, mask)
        
        img = preprocess_frame(roi)
        prediction = model.predict(img)
        class_index = np.argmax(prediction, axis=1)[0]
        result = list(categories.keys())[class_index]
        angle = categories[result]
        
        print(f"Classification result: {result}")
        send_to_arduino(result[0], angle)
        
        image_path = os.path.join(result, f"{result}_{image_counter}.jpg")
        cv2.imwrite(image_path, roi)
        print(f"Image saved at {image_path}")
        image_counter += 1
    
    elif key == ord('q'):  # Quit
        print("Exiting program.")
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
if arduino and arduino.is_open:
    arduino.close()
    print("Arduino connection closed.")
