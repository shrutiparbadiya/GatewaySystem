from ultralytics import YOLO
import cv2
# from sort.sort import *
from .util import read_license_plate
from .models import Vehicle
import numpy as np
from PIL import Image
import io


results = {}



# Load YOLO models
coco_model = YOLO('../../yolov8n.pt')
license_plate_detector = YOLO('../../models/license_plate_detector.pt')

def plate_detection(image_path):
    # image = cv2.imread("./car1.jpg")
    # Read the uploaded file into OpenCV
    image = cv2.imread(image_path)
    # image_bytes = image.read()
    # np_arr = np.frombuffer(image_bytes, np.uint8)
    # image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if image is None:
        return "❌ Failed to decode uploaded image."
    image = cv2.resize(image, (640, 480))
    vehicles = [2, 3, 5, 7]

    detections = coco_model(image)[0]
    detections_ = []

    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = detection
        if class_id in vehicles:
            detections_.append([x1, y1, x2, y2, score, class_id])
            print(detections_)
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

    license_plates = license_plate_detector(image)[0]
    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

        # Crop the license plate region
        license_plate_crop = image[y1:y2, x1:x2]
        license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
        # _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 120, 255, cv2.THRESH_BINARY_INV)
        # Optionally display or run OCR
        license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_gray)
        # cv2.imshow("License Plate", license_plate_crop_thresh)
        # print(license_plate_text)
        plate = ''.join(filter(str.isalnum, license_plate_text)).upper()
        matched = Vehicle.objects.filter(number_plate=plate).first()
    if matched:
        return f"Access Granted to {matched.owner_name} - {matched.number_plate}"
    return f"Access Denied: No match found. Detected Text: {license_plate_text.strip()}"
    # cv2.imshow("image", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()