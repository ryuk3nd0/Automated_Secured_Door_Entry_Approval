import numpy as np
import cv2
import time
import requests
import csv
import random
import string

# Camera and detection setup
cap = cv2.VideoCapture(1)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# File setup
file_path = 'guest_requests.csv'
initial_rows = sum(1 for _ in open(file_path))
last_face = None

# Functions
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_image_through_telegram(image_path):
    files = {'photo': open(image_path, 'rb')}
    resp = requests.post('https://api.telegram.org/bot6740801322:AAHZLBdCxTn_71_gX33VxLrVVhcZXa5CEkc/sendPhoto?chat_id=-4017828034', files=files)
    print("Telegram response status code:", resp.status_code)
    files['photo'].close()  # Closing the file after sending

# Main loop
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)
        last_face = frame # Update last_face with the current frame having final detections

    # Check on the CSV updates
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

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()