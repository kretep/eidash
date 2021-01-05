from datetime import datetime, timedelta
import os
import requests
import numpy as np
import cv2

class SunspotData:

    def __init__(self):
        self.data = {}
        self.last_refetch_time = None

    def get_data(self):
        if self.needs_refetch():
            try:
                data = self.refetch()
                if data is not None:
                    self.data = self.process_data(data)
                    self.last_refetch_time = datetime.now()
            except:
                pass
        return self.data

    def refetch(self):
        try:
            url = os.environ["EIDASH_SUNSPOTS_URL"]
            response = requests.get(url)
            return response.content
        except Exception as e:
            print(e)

    def process_data(self, data):
        # Decode raw data
        data = np.asarray(bytearray(data), dtype="uint8")
        img_original = cv2.imdecode(data, cv2.IMREAD_COLOR)

        # Grayscale & threshold
        img = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
        _, img_thresh = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY)

        # Embiggen sunspots
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
        img_erode = cv2.erode(img_thresh, kernel)

        # Process background
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
        img_dilate = cv2.dilate(img_erode, kernel2)
        img_invert = 255 - img_dilate

        # Combining with background results in ring outline, while keeping sunspots
        img_combine = cv2.max(img_invert, img_erode)
        img_resize = cv2.resize(img_combine, (72, 72), interpolation=cv2.INTER_NEAREST)

        return img_resize

    def needs_refetch(self):
        if self.last_refetch_time is None:
            return True
        elapsed = datetime.now() - self.last_refetch_time
        return elapsed >= timedelta(minutes=360)
