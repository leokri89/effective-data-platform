import cv2
from PIL import Image
import numpy as np
from io import BytesIO
import json
import base64

image = cv2.imencode('.jpg', image_cv)[1]
image_code = str(base64.b64encode(image))[2:-1]