from time import sleep
from pynput.keyboard import Key, Controller
import time

import cv2
import mss
import numpy
import pytesseract

keyboard = Controller()
key = Key.down

def page_down(keyboard, key):
    keyboard.press(key)
    keyboard.release(key)

def look_screen():
    with mss.mss() as sct:
        # Get information of monitor 2
        monitor_number = 3
        mon = sct.monitors[monitor_number]

        monitor = {
            "top": mon["top"] + 400,  # 100px from the top
            "left": mon["left"],  # 100px from the left
            "width": 500,
            "height": 200,
            "mon": monitor_number,
        }
        sct_img = sct.grab(monitor)
        im = numpy.asarray(sct_img)
        text = pytesseract.image_to_string(im)
        output = "sct.png".format(**monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        return text

def test_string(text):
    list_string = ['pagbank-ios-ci','kolomna','processos_govdados','valinor_public','sdtef-6157','sdtef-6162','message-center']
    for channel in list_string:
        if channel in text:
            return True
    return False

def process():
    sleep(10)
    found = False
    while found == False:
        text = look_screen()
        found = test_string(text)
        page_down(keyboard, key)

process()
