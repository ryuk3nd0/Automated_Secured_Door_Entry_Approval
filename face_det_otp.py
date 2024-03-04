import cv2
import time
import os
import telebot
import RPi.GPIO as GPIO
import threading

# Telegram bot setup
bot_api = "7092626455:AAFz5FkyHIu3dYzYIFwBswaS6kydL4afb8Q"
chat_id = "-4017828034"
bot = telebot.TeleBot(bot_api)

# Camera and detection setup
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# File setup
file_path = 'guest_requests.csv'
initial_rows = sum(1 for _ in open(file_path))

# Function to generate an OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=4))

# Function to send image to Telegram with inline keyboard
def send_image_telegram(image_path):
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_Approve = telebot.types.InlineKeyboardButton(text='Approve', callback_data='Approve')
    button_Decline = telebot.types.InlineKeyboardButton(text='Decline', callback_data='Decline') 
    keyboard.add(button_Approve, button_Decline)
    with open(image_path, 'rb') as photo:
        bot.send_photo(chat_id, photo, reply_markup=keyboard)

# Callback handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global initial_rows
    if call.data == 'Approve':
        bot.send_message(chat_id, "You've approved the entry ✅")
        print("User selected Approve") 
        # Generating and appending the OTP to the last non-empty row
        with open(file_path, 'r+', newline='') as file:
            rows = list(csv.reader(file))
            # Find the index of the last non-empty row
            last_non_empty_index = len(rows) - 1
            while last_non_empty_index >= 0 and not any(rows[last_non_empty_index]):
                last_non_empty_index -= 1
            if last_non_empty_index >= 0:
                last_row = rows[last_non_empty_index]
                last_row.extend([''] * (5 - len(last_row)))  # Ensure each row has at least 5 elements
                last_row[3] = generate_otp()
                last_row[4] = '1'  # Marking as verified
                file.seek(0)
                csv.writer(file).writerows(rows)
    elif call.data == 'Decline':
        bot.send_message(chat_id, "Entry declined ❌")
        print("User selected Decline")
        # Marking the last row as unverified
        with open(file_path, 'r+', newline='') as file:
            rows = list(csv.reader(file))
            # Find the index of the last non-empty row
            last_non_empty_index = len(rows) - 1
            while last_non_empty_index >= 0 and not any(rows[last_non_empty_index]):
                last_non_empty_index -= 1
            if last_non_empty_index >= 0:
                last_row = rows[last_non_empty_index]
                last_row.extend([''] * (5 - len(last_row)))  # Ensure each row has at least 5 elements
                last_row[4] = '0'  # Marking as unverified
                file.seek(0)
                csv.writer(file).writerows(rows)
    # Remove keyboard
    bot.edit_message_reply_markup(chat_id, call.message.message_id)


# Function to detect faces and process CSV updates
def detect_faces_and_process():
    global initial_rows
    last_face = None
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
        with open(file_path, 'r', newline='') as file:
            rows = list(csv.reader(file))
            current_rows = len(rows)
            if current_rows > initial_rows:
                #new_row = rows[-1]  # Get the last updated row
                # Saving the image of the last detected face
                if last_face is not None:
                    image_path = os.path.join('detected_faces', f'last_face_{int(time.time())}.png')
                    cv2.imwrite(image_path, last_face)
                    # Sending the image through Telegram
                    send_image_telegram(image_path)
                initial_rows = current_rows

        #cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break


# Start the face detection and CSV processing thread
thread = threading.Thread(target=detect_faces_and_process)
thread.start()

# Start bot polling
bot.polling()