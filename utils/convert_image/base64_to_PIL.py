import cv2
from PIL import Image
import numpy as np
from io import BytesIO
import json
import base64

rj = request.get_json() # Pass the base64 data through POST request
base64Image = rj['base64Image']
byte_date = base64.b64decode(base64Image)

try:
    imagede = Image.open(BytesIO(byte_date)).convert('RGB') # Convert to PIL
except Exception as e:
    print('Open Error! Try again!')
    raise e

image = np.array(imagede) # Convert PIL format image to numpy