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

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Function to send image to Telegram with inline keyboard
def send_image_telegram(image_path):
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_Approve = telebot.types.InlineKeyboardButton(text='Approve', callback_data='Approve')
    button_Decline = telebot.types.InlineKeyboardButton(text='Decline', callback_data='Decline') 
    keyboard.add(button_Approve, button_Decline)
    with open(image_path, 'rb') as photo:
        bot.send_photo(chat_id, photo, reply_markup=keyboard)

# Function to detect faces and process CSV updates
def detect_faces_and_process():
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
            last_face = frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

# Callback handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'Approve':
        bot.send_message(chat_id, "You've approved the entry ✅")
    elif call.data == 'Decline':
        bot.send_message(chat_id, "Entry declined ❌")
    bot.edit_message_reply_markup(chat_id, call.message.message_id)

# Function to handle button press event
def button_pressed(channel):
    global cap
    ret, frame = cap.read()
    if ret:
        image_path = os.path.join('detected_faces', f'last_face_{int(time.time())}.png')
        cv2.imwrite(image_path, frame)
        send_image_telegram(image_path)

# Setup event listener for button press
GPIO.add_event_detect(10, GPIO.RISING, callback=button_pressed, bouncetime=200)

# Start the face detection thread
thread = threading.Thread(target=detect_faces_and_process)
thread.start()

# Run until someone presses enter
message = input("Press enter to quit\n\n")

# Release resources and cleanup GPIO
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
