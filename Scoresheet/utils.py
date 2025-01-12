
import cv2
import numpy as np

def resize(img: np.ndarray, new_w, new_h) -> np.ndarray:
	if len(img.shape) == 3:
		h, w, _ = img.shape
	else:
		h, w = img.shape
	w_resize_scale = new_w / w
	h_resize_scale = new_h / h

	resized_img = cv2.resize(img, None, fx=w_resize_scale, fy=h_resize_scale)
	return resized_img