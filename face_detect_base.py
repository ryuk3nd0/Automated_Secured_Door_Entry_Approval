import numpy as np
import cv2
import time
import requests


cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

run_duration = 30
start_time = time.time()


i=0
while True:
    
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
        roi_gray = gray[y:y+w, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)

        cv2.imwrite('output_frame.jpg', frame)
        i=i+1  # of detection

    cv2.imshow('frame', frame)


    current_time = time.time()
    
    if current_time - start_time > run_duration:
        break
    
    if cv2.waitKey(1) == ord('q'):
        break
    if (i==200):
        break

#files={'photo': open('output_frame.jpg','rb')}

#resp=requests.post('https://api.telegram.org/bot6740801322:AAHZLBdCxTn_71_gX33VxLrVVhcZXa5CEkc/sendPhoto?chat_id=-4017828034',files=files)

#print(resp.status_code)
#ei 3 line comment out korle telegram server e direct captured image chole jabe...comment out korle further permission chara image up hobe...
print(i)


cap.release()
cv2.destroyAllWindows()