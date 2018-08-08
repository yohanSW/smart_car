from image_processing import image_processing
import cv2
img = cv2.VideoCapture(0)
while True:
    print(image_processing(img))