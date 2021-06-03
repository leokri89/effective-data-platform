import cv2
from PIL import Image
import numpy as np
from io import BytesIO
import json
import base64

img = cv2.imread("plane.jpg")
cv2.imshow("OpenCV",img)
image = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
image.show()
cv2.waitKey()