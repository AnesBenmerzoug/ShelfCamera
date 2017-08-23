import cv2
import sys
from shelfcamera import ShelfCamera

video_path = "../videos/PrixCameraLat.mov"

capture = cv2.VideoCapture(video_path)

if not capture.isOpened():
    print "Couldn't open video"
    sys.exit()

try:
    ShelfCamera(video=capture)
finally:
    capture.release()
    cv2.destroyAllWindows()
