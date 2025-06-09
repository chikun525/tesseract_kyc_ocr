import cv2
import numpy as np

def auto_crop_address_region(img_path, template_path, crop_w=None, crop_h=200, x_offset=0, y_offset=120):
    import cv2
    img = cv2.imread(img_path)
    template = cv2.imread(template_path, 0)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc

    card_h, card_w = img.shape[:2]
    crop_x1 = int(card_w * 0.55)
    crop_x2 = card_w
    crop_y1 = top_left[1] + y_offset
    crop_y2 = crop_y1 + crop_h

    address_crop = img[crop_y1:crop_y2, crop_x1:crop_x2]
    return address_crop



