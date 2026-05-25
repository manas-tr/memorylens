import cv2
import os

video_path = "vid01.mp4"

faces_dir = "faces"

output_path = "vid01_out.mp4"

known_faces = []

for filename in os.listdir(faces_dir):

    path = os.path.join(faces_dir, filename)

    image = cv2.imread(path)

    if image is None:
        continue

    image = cv2.resize(image, (100, 100))

    known_faces.append(image)


print(f"loaded {len(known_faces)} faces")

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

video = cv2.VideoCapture(video_path)

width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video.get(cv2.CAP_PROP_FPS))

writer = cv2.VideoWriter(
    output_path,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height)
)

while True:

    success, frame = video.read()

    if not success:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(180, 180)
    )

    for (x, y, w, h) in faces:

        face = frame[y:y+h, x:x+w]

        if face.size == 0:
            continue

        small_face = cv2.resize(face, (100, 100))

        best_score = 999999
        best_id = None

        for i, known_face in enumerate(known_faces):

            difference = cv2.absdiff(
                small_face,
                known_face
            )

            score = difference.mean()

            if score < best_score:
                best_score = score
                best_id = i

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"PERSON_{best_id}",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    writer.write(frame)


video.release()
writer.release()

print("\nvideo saved!")