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

        # Process background
        bg_kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
        bg_erode = cv2.erode(img_thresh, bg_kernel1) # erode captions
        bg_kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
        bg_dilate = cv2.dilate(bg_erode, bg_kernel2) # thicken circle
        bg_invert = ~bg_dilate

        # Embiggen sunspots
        # Bigger kernel for erosion than dilation, resulting in net growth
        # proportional to the original size.
        dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        erode_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        img_combine = img_thresh.copy()        # for the result
        img_dilate_cache = img_thresh.copy()   # keep cache for accumulative dilation
        # Erode and dilate alternatingly. As the outer loop progresses, only the bigger
        # spots are not dilated away and get embiggened proportionally more (inner loop)
        for i in range(1, 4):
            # Erode (embiggen) first, to make sure we don't lose the smallest spots.
            img_erode = cv2.erode(img_dilate_cache, erode_kernel)
            for j in range(i-1):
                img_erode = cv2.erode(img_erode, erode_kernel)

            # Combine the result with what we have
            img_combine = cv2.min(img_combine, img_erode)

            # Dilate (ensmallen) to remove the smallest spots for the next round
            img_dilate_cache = cv2.dilate(img_dilate_cache, dilate_kernel)

        # Combining with background results in ring outline, while keeping sunspots
        img_combine = cv2.max(img_combine, bg_invert)

        # Resize
        img_resize = cv2.resize(img_combine, (72, 72), interpolation=cv2.INTER_NEAREST)
        
        return img_resize

    def needs_refetch(self):
        if self.last_refetch_time is None:
            return True
        elapsed = datetime.now() - self.last_refetch_time
        return elapsed >= timedelta(minutes=360)
