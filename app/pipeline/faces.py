import cv2
import os

import shutil


video_path = "vid01.mp4"

output_dir = "faces"

if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

os.makedirs(output_dir, exist_ok=True)

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

video = cv2.VideoCapture(video_path)

frame_count = 0
saved_count = 0

saved_faces=[]


while True:

    success, frame = video.read()

    if not success:
        break

    frame_count += 1

    # skip frames
    if frame_count % 30 != 0:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(180, 180)
    )

    for (x, y, w, h) in faces:

        ratio = w / h

        if ratio < 0.7 or ratio > 1.3:
            continue

        face = frame[y:y+h, x:x+w]

        small_face = cv2.resize(face, (100, 100))

        is_new = True

        for old_face in saved_faces:

            difference = cv2.absdiff(small_face, old_face)

            score = difference.mean()

            if score < 40:
                is_new = False
                break

        if not is_new:
            continue

        saved_faces.append(small_face)

        filename = f"{output_dir}/face_{saved_count}.jpg"

        cv2.imwrite(filename, face)

        print(f"saved {filename}")

        saved_count += 1


video.release()

print("\nface extraction complete!")