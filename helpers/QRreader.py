import cv2
import os
from pyzbar import pyzbar

def read_qr_code(filename:str)->str:

    fname = os.path.abspath("downloads/" + filename)

    try:
        img = cv2.imread(fname)

        value = pyzbar.decode(img)

        if value != []:
            return value[0].data.decode('utf-8')
        
        return ""
    except:
        return ""
    
