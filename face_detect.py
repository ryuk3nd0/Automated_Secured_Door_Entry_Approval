import os
import cv2
from mtcnn import MTCNN
import dlib  # Import dlib for face recognition
import time

# Ensure the "detected_faces" folder exists
output_folder = 'detected_faces'
os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(2)
mtcnn_detector = MTCNN()

# Initialize the face recognition model
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

run_duration = 120  # seconds
start_time = time.time()

save_interval = 10  # Save a frame every 10 seconds
last_save_time = time.time()

current_face_descriptor = None
previous_face_descriptor = None
i = 0

while True:
    ret, frame = cap.read()

    # Resize the frame for faster processing (optional)
    # frame = cv2.resize(frame, (640, 480))

    # Perform face detection using MTCNN
    faces = mtcnn_detector.detect_faces(frame)

    if faces:
        x, y, w, h = faces[0]['box']
        face = frame[y:y + h, x:x + w]

        # Perform face recognition using dlib
        shape = predictor(frame, dlib.rectangle(left=x, top=y, right=x + w, bottom=y + h))
        current_face_descriptor = face_rec_model.compute_face_descriptor(frame, shape)

        # Save the initial frames if a new face is detected
        if previous_face_descriptor is None or (w > 0 and h > 0 and
                                                dlib.distance(current_face_descriptor, previous_face_descriptor) > 0.6):
            output_path = os.path.join(output_folder, f'output_frame_{i}.jpg')
            cv2.imwrite(output_path, frame)
            i += 1

    cv2.imshow('frame', frame)

    current_time = time.time()

    if current_time - start_time > run_duration:
        break

    if cv2.waitKey(1) == ord('q'):
        break

    previous_face_descriptor = current_face_descriptor

cap.release()
cv2.destroyAllWindows()
