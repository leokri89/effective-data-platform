import cv2
from PIL import Image
import numpy as np
from io import BytesIO
import json
import base64

image = Image.open("plane.jpg")
image.show()
img = cv2.cvtColor(numpy.asarray(image),cv2.COLOR_RGB2BGR)
cv2.imshow("OpenCV",img)
cv2.waitKey()