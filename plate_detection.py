from ultralytics import YOLO
import cv2
from sort.sort import *
from util import get_car, read_license_plate, write_csv
import numpy as np

results = {}

mot_tracker = Sort()

# Load YOLO models
coco_model = YOLO('../../yolov8n.pt')
license_plate_detector = YOLO('../../models/license_plate_detector.pt')


# Load video
cap = cv2.VideoCapture("C:\\Users\\dell\\PycharmProjects\\Upwards-Downwards_Count\\Resources\\video3_cropped.mp4")

# Class IDs for vehicles (COCO)
vehicles = [2, 3, 5, 7]

frame_nmr = -1
ret = True
while ret:
    frame_nmr += 1
    ret, frame = cap.read()
    if not ret:
        break

    results[frame_nmr] = {}

    # Detect vehicles
    detections = coco_model(frame)[0]
    detections_ = []
    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = detection
        if int(class_id) in vehicles:
            detections_.append([x1, y1, x2, y2, score])

    # Track vehicles
    track_ids = mot_tracker.update(np.asarray(detections_))

    # Detect license plates
    license_plates = license_plate_detector(frame)[0]
    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate

        # Match license plate to a car
        xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

        if car_id != -1:
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])  # Ensure integer
            license_plate_crop = frame[y1:y2, x1:x2, :]

            # Preprocess
            license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
            _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

            # OCR
            license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)

            if license_plate_text is not None:
                print(f"✅ Frame {frame_nmr}, Car ID {car_id}, Plate: {license_plate_text}, Score: {license_plate_text_score}")
                results[frame_nmr][car_id] = {
                    'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                    'license_plate': {
                        'bbox': [x1, y1, x2, y2],
                        'text': license_plate_text,
                        'bbox_score': score,
                        'text_score': license_plate_text_score
                    }
                }

# Save to CSV
write_csv(results, r'/test.csv')
print("✅ Finished. Data saved to test.csv")
