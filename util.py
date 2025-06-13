import string
import easyocr

reader = easyocr.Reader(['en'], gpu=False)

dict_char_to_int = {'O': '0', 'I': '1', 'J': '3', 'A': '4', 'G': '6', 'S': '5'}
dict_int_to_char = {'0': 'O', '1': 'I', '3': 'J', '4': 'A', '6': 'G', '5': 'S'}


def write_csv(results, output_path):
    with open(output_path, 'w') as f:
        f.write('{},{},{},{},{},{},{}\n'.format('frame_nmr', 'car_id', 'car_bbox',
                                                'license_plate_bbox', 'license_plate_bbox_score', 'license_number',
                                                'license_number_score'))

        for frame_nmr in results.keys():
            for car_id in results[frame_nmr].keys():
                car_data = results[frame_nmr][car_id]
                if 'car' in car_data and 'license_plate' in car_data:
                    plate_data = car_data['license_plate']
                    if 'text' in plate_data:
                        f.write('{},{},{},{},{},{},{}\n'.format(
                            frame_nmr,
                            car_id,
                            f"[{car_data['car']['bbox'][0]} {car_data['car']['bbox'][1]} {car_data['car']['bbox'][2]} {car_data['car']['bbox'][3]}]",
                            f"[{plate_data['bbox'][0]} {plate_data['bbox'][1]} {plate_data['bbox'][2]} {plate_data['bbox'][3]}]",
                            plate_data['bbox_score'],
                            plate_data['text'],
                            plate_data['text_score']
                        ))


def license_complies_format(text):
    return 6 <= len(text) <= 12 and text.isalnum()


def format_license(text):
    license_plate_ = ''
    mapping = {0: dict_int_to_char, 1: dict_int_to_char, 4: dict_int_to_char,
               5: dict_int_to_char, 6: dict_int_to_char,
               2: dict_char_to_int, 3: dict_char_to_int}
    for j in range(min(len(text), 7)):
        if text[j] in mapping.get(j, {}):
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]
    license_plate_ += text[7:] if len(text) > 7 else ''
    return license_plate_


def read_license_plate(license_plate_crop):
    detections = reader.readtext(license_plate_crop)
    for detection in detections:
        bbox, text, score = detection
        text = ''.join(filter(str.isalnum, text.upper()))
        if license_complies_format(text):
            return format_license(text), score
    return None, None


def get_car(license_plate, detections_):
    x1, y1, x2, y2, score, class_id = license_plate
    for j in range(len(detections_)):
        xcar1, ycar1, xcar2, ycar2, car_id = detections_[j]
        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            return detections_[j]
    return -1, -1, -1, -1, -1
