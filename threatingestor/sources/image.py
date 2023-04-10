import os
import sys
import requests
import datetime
import iocextract
import numpy as np
from loguru import logger

try:
    import numpy as np
except ImportError:
    logger.info("Missing the following package(s): numpy")
    sys.exit()

try:
    import cv2
except ImportError:
    logger.info("Missing the following package(s): opencv-python")
    sys.exit()

try:
    import pytesseract
except ImportError:
    logger.info("Missing the following package(s): pytesseract")
    sys.exit()

from threatingestor.sources import Source
import threatingestor.artifacts

class Plugin(Source):
    """
    Image text extraction using Google's OCR Tesseract engine and computer vision
    """

    def __init__(self, name, img=""):
        self.name = name
        self.img = img

        if "http" in img:
            with open("/tmp/data.png", "wb") as i:
                i.write(requests.get(str(self.img)).content)

    def run(self, saved_state):
        saved_state = datetime.datetime.utcnow().isoformat()[:-7] + "Z"

        if os.path.exists("/tmp/data.png"):
            data = cv2.imread("/tmp/data.png")
        else:
            # No image is present
            try:
                data = cv2.imread(self.img)
            except TypeError:
                pass

        try:
            # Helps with preprocessing by converting to a grayscale
            grayscale_img = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)

            # Creates a binary image by using the proper threshold from cv and inverts the binary
            invert_img = cv2.bitwise_not(cv2.threshold(grayscale_img, 130, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1])

            # Helps with cleanup
            process_iter = cv2.dilate(cv2.erode(invert_img, np.ones((2,2), np.uint8), iterations=1), np.ones((2,2), np.uint8), iterations=1)

            # Converts image data to a string
            img_data = pytesseract.image_to_string(process_iter)

            artifact_list = []

            title = "Image: {0}".format(self.img)
            description = 'URL: {u}\nTask autogenerated by ThreatIngestor from source: {s}'
            description = description.format(s=self.name, u=list(iocextract.extract_urls(img_data)))
            artifact = threatingestor.artifacts.Task(title, self.name, reference_link=str(list(iocextract.extract_urls(img_data))), reference_text=description)
            artifact_list.append(artifact)
                
        except cv2.error:
            raise FileNotFoundError

        return saved_state, artifact_list