This project is a Smart Waste Management System that combines Deep Learning, Arduino-based hardware, and servo motors to create an intelligent, automated waste-sorting solution. The system is designed to identify and categorize waste (e.g., plastic, metal, paper, organic) using a trained machine learning model and perform sorting actions in real-time through servo-controlled bins.

Technologies Used:

Deep Learning (TensorFlow/Keras): For image classification of waste types.
Arduino Uno: Microcontroller to control the hardware components.
Servo Motors: To automatically open/close the correct waste bin based on prediction.
Python: For training the deep learning model and interfacing with Arduino.
OpenCV: For image processing and camera feed handling.
Serial Communication (PySerial): To send commands from the Python server to the Arduino.
Wires & Sensors: Used to connect and control the physical components.
Features

Waste is classified into multiple categories using a trained CNN model.
Real-time camera input for detecting waste.
Servo motors automatically sort detected waste into the correct bins.
Easy to retrain or update the model with new categories.
Modular design for easy hardware integration.
How to Run

Clone the repo: git clone https://github.com/nandyalanaveen13/Smart-Waste-Management-System.git cd Smart-Waste-Management-System

Create and activate a virtual environment: python -m venv venv venv\Scripts\activate # Windows

Install Python dependencies: pip install -r requirements.txt

Upload the Arduino code: Open arduino/sorter.ino in the Arduino IDE and upload it to your board.

Run the server (camera + classification): python server/main.py

Demo video:https://drive.google.com/file/d/1OMCCgW3Zf90VtszEfsAMC3CnPSmyIqSV/view?usp=sharing
