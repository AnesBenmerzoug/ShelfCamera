import numpy as np
import cv2
from imutils.object_detection import non_max_suppression

ESC_keycode = 27

class ShelfCamera:
    ## Class Init Function
    def __init__(self, window_name="Shelf Camera", video=None):
        self.video = video
        self.window_name = window_name

        self.drawing = False
        self.shelf_area_index = 0

        self.shelf_line = [(0, 0), (0, 0)]
        self.shelf_area = np.array([[0, 0],
                                    [0, 0],
                                    [0, 0],
                                    [0, 0]], dtype=np.int32).reshape(-1, 1, 2)

        cv2.namedWindow(self.window_name)

        # Get the first frame
        ret, self.first_frame = self.video.read()

        # Drawing Shelf Line

        # Set Mouse Callback for Drawing the Shelf Line
        cv2.setMouseCallback(self.window_name, self.draw_shelf_line)

        # Make a copy of the First Frame
        self.shelf_line_frame = self.first_frame.copy()

        # Show image and wait for user to draw Shelf Line and Press the ESC key
        while True:
            cv2.imshow(self.window_name, self.shelf_line_frame)
            if cv2.waitKey(1) & 0xFF == ESC_keycode and not self.drawing:
                break

        # Drawing Shelf Area

        # Set Mouse Callback for Drawing the Shelf Area
        cv2.setMouseCallback(self.window_name, self.draw_shelf_area)

        # Make a copy of the First Frame
        self.shelf_area_frame = self.first_frame.copy()

        # Show image and wait for user to draw Shelf Area and Press the ESC key
        while True:
            cv2.imshow(self.window_name, self.shelf_area_frame)
            if cv2.waitKey(1) & 0xFF == ESC_keycode and not self.drawing:
                break

        # Remove mouse callback by giving an anonymous function that does nothing
        cv2.setMouseCallback(self.window_name, lambda event, x, y, flags, param: event)

        # Setting up People Detector
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        # Running Detection and Tracking loop
        self.detect_and_track_people()

    ## Detect and Track People Function
    def detect_and_track_people(self):
        while True:
            try:
                ok, frame = self.video.read()
                if not ok:
                    break
                cv2.imshow(self.window_name, frame)
                if cv2.waitKey(10) & 0xFF == ESC_keycode:
                    break
            except:
                break

    ## Draw Shelf Line Function
    def draw_shelf_line(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.shelf_line_frame = self.first_frame.copy()
            self.shelf_line[0] = (x, y)

        if event == cv2.EVENT_MOUSEMOVE:
            if self.drawing is True:
                self.shelf_line_frame = self.first_frame.copy()
                cv2.line(self.shelf_line_frame, self.shelf_line[0], (x, y), (255, 0, 0), 2)

        if event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.shelf_line[1] = (x, y)
            cv2.line(self.shelf_line_frame, self.shelf_line[0], self.shelf_line[1], (255, 0, 0), 2)

    ## Draw Shelf Area Function
    def draw_shelf_area(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            if self.shelf_area_index == 0:
                self.shelf_area_frame = self.first_frame.copy()
            self.shelf_area[self.shelf_area_index:, 0] = [x, y]
            self.shelf_area_index += 1
            cv2.polylines(self.shelf_area_frame, [self.shelf_area], True, (0, 255, 0))
        if event == cv2.EVENT_LBUTTONUP:
            if self.shelf_area_index == 4:
                self.shelf_area_frame = self.first_frame.copy()
                cv2.polylines(self.shelf_area_frame, [self.shelf_area], True, (0, 255, 0))
                self.shelf_area_index = 0
                self.drawing = False

    ## Class Destructor Function
    def __del__(self):
        self.video.release()