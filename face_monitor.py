import face_recognition
import cv2
import os

def load_known_faces(image_paths, names):
    known_face_encodings = []
    known_names = []
    for image_path, name in zip(image_paths, names):
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:
            known_face_encodings.extend(face_encodings)
            known_names.extend([name] * len(face_encodings))
        else:
            print(f"No faces found in the image: {image_path}")
    return known_face_encodings, known_names

def recognize_faces(video_capture, known_face_encodings, known_names):
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (frame_width, frame_height))

    unknown_face_detected_duration = 0
    max_duration = 3  # Time in seconds before turning off the screen if an unknown face is detected
    fps = 3

    screen_off = False

    try:
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            unknown_face_detected = False
            known_face_detected = False

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_names[first_match_index]
                    known_face_detected = True
                else:
                    unknown_face_detected = True

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            if unknown_face_detected and not known_face_detected and not screen_off:
                unknown_face_detected_duration += 1
                if unknown_face_detected_duration > max_duration * fps:
                    turn_off_screen()
                    screen_off = True
            elif known_face_detected:
                if screen_off:
                    turn_on_screen()
                    screen_off = False
                unknown_face_detected_duration = 0
            else:
                unknown_face_detected_duration = 0

            out.write(frame)
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        video_capture.release()
        out.release()
        cv2.destroyAllWindows()

def turn_off_screen():
    print("Turning off the screen...")
    os.system("xset dpms force off")

def turn_on_screen():
    print("Turning on the screen...")
    os.system("xset dpms force on")

person_image_paths = ["/home/force-4/Desktop/System_monitor_track_OG/vi.jpg"]
person_names = ["vishnu"]

known_face_encodings, known_names = load_known_faces(person_image_paths, person_names)
video_capture = cv2.VideoCapture(0)
recognize_faces(video_capture, known_face_encodings, known_names)
