# # number_plate_detection.py
# import cv2
# import pytesseract
# from .models import Vehicle
# import os
# from django.conf import settings
#
#
# def detect_number_plate(file_path):
#     print("Processing file:", file_path)
#
#     image = cv2.imread(file_path)
#     if image is None:
#         return "Error: Failed to load image."
#
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     text = pytesseract.image_to_string(gray)
#     plate = ''.join(filter(str.isalnum, text)).upper()
#
#     matched = Vehicle.objects.filter(number_plate=plate).first()
#     if matched:
#         return f"Access Granted to {matched.owner_name} - {matched.number_plate}"
#     return f"Access Denied: No match found. Detected Text: {text.strip()}"
#
#     # if matched:
#     #     #     message = f"Access Granted to {matched.owner_name} - {matched.number_plate}"
#     #     # else:
#     #     #     message = f"Access Denied: No match found. Detected Text: {text.strip()}"

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

