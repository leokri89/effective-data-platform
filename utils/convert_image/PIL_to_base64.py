import cv2
from PIL import Image
import numpy as np
from io import BytesIO
import json
import base64

image_pil = Image.fromarray(image_np) # image_np is the numpy data format
output_buffer = BytesIO()
image_pil.save(output_buffer, format='JPEG')
byte_data = output_buffer.getvalue()

# I need to convert to str here, otherwise it will be wrong if packaged into json
# json cannot be packed byte type needs to be converted to string type
image_code = str(base64.b64encode(byte_data))[2:-1]