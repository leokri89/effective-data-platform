import cv2
from PIL import Image
import numpy as np
from io import BytesIO
import json
import base64

imgData = base64.b64decode(base64_data)
nparr = np.fromstring(imgData, np.uint8)
img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)