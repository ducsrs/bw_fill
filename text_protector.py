from PIL import Image
# import cv2
import pytesseract
from pytesseract import Output


class Protector:
    def __init__(self, img: Image):
        self.boxes = set()
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\sike.exe'
        # ^uncomment to test uninstalled tesseract
        try:
            d = pytesseract.image_to_data(img, output_type=Output.DICT)
        except pytesseract.TesseractNotFoundError:
            raise NameError
        else:
            # adapted from https://stackoverflow.com/questions/20831612/
            size = img.size[0] * img.size[1]
            n_boxes = len(d['level'])
            for i in range(n_boxes):
                if d['conf'][i] == '-1':
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    if h * w < 0.3 * size:
                        # throws out extraneous boxes around entire graph
                        self.boxes.add((x, y, w, h))
        # print(self.boxes)

    def check_boxes(self, x, y):
        """Returns True if (x, y) contains text"""
        for box in self.boxes:
            if box[0] < x < (box[0] + box[2]) and box[1] < y < (box[1] + box[3]):
                return True
        return False
