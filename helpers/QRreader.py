import cv2
import os

def read_qr_code(filename:str)->str:
    """Read an image and read the QR code.
    
    Args:
        filename (string): Path to file
    
    Returns:
        qr (string): Value from QR code
    """
    fname = os.path.abspath("downloads/" + filename)

    # try:
    #     img = cv2.imread(fname)
    #     detect = cv2.QRCodeDetector()
    #     retval, value, points, straight_qrcode = detect.detectAndDecodeMulti(img)
    #     return value[0]
    # except:
    #     return "error"

    try:
        img = cv2.imread(fname)
        detect = cv2.QRCodeDetector()
        retval, value, points, straight_qrcode = detect.detectAndDecodeMulti(img)
        if value != []:
            return value[0]
    except:
        return ""
    
