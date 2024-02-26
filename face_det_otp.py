import numpy as np
import cv2
import time
import requests
import csv
import random
import string

# File handling and camera setup
cap = cv2.VideoCapture(1)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
file_path = 'guest_requests.csv'
initial_rows = sum(1 for _ in open(file_path))
last_face = None

# Function to generate an OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=4))

# Function to send the image via Telegram (pseudo-code)
def send_image_through_telegram(image_path):
    resp=requests.post('https://api.telegram.org/bot6740801322:AAHZLBdCxTn_71_gX33VxLrVVhcZXa5CEkc/sendPhoto?chat_id=-4017828034',files=image_path)

# Main loop
while True:
    # Face detection
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) > 0:
        x, y, w, h = faces[0] # Assuming we use the first detected face
        last_face = frame[y:y+h, x:x+w]
    
    # Check for new rows in the CSV file
    with open(file_path, 'r+', newline='') as file:
        rows = list(csv.reader(file))
        current_rows = len(rows)

        if current_rows > initial_rows:
            for new_row in rows[initial_rows:]:
                if len(new_row) < 4:
                    new_row.append('')

                # Generating and appending the OTP
                new_row[3] = generate_otp()

                # Saving the image of the last detected face
                if last_face is not None:
                    image_path = f'last_face_{int(time.time())}.png'
                    cv2.imwrite(image_path, last_face)

                    # Sending the image through Telegram
                    send_image_through_telegram(image_path)

            # Update the file with the OTP
            file.seek(0)
            csv.writer(file).writerows(rows)
            initial_rows = current_rows

    #Optional: Display the frame with detected faces (for testing purposes)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()