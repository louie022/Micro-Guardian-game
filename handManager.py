import cv2
from handTracking import HandTracking
from hand import Hand

class HandManager:
    def __init__(self):
        # Initialize camera
        # self.cap = cv2.VideoCapture(0)
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)    # webcam
        
        # Set up hand tracking
        self.hand_tracking = HandTracking()
        self.hand = Hand()


    def reinitialize_camera(self):
        if self.cap is not None:
            self.cap.release()  # Release the current capture
            self.cap = None

        # self.cap = cv2.VideoCapture(0)  # Reinitialize capture
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Webcam


    def reset_hand_position(self):
        # reset the hand position
        self.hand_tracking.hand_x = -100
        self.hand_tracking.hand_y = -100


    def full_reset(self):
        self.reinitialize_camera()
        self.reset_hand_position()
        self.hand_tracking = HandTracking()
        self.hand = Hand()


    def update(self):
        # Load camera frame
        success, self.frame = self.cap.read()
        if not success or self.frame is None:
            print("Failed to capture frame")
            return

        # Scan hands
        self.frame = self.hand_tracking.scan_hands(self.frame)

        # Update hand position
        (x, y) = self.hand_tracking.get_hand_center()
        self.hand.rect.center = (x, y)
        self.hand.left_click = self.hand_tracking.hand_closed
        # print("hand closed:", self.hand.left_click)

         # switch hand/fist based on handpose
        if self.hand.left_click:
            self.hand.image = self.hand.fist_image.copy()
        else:
            self.hand.image = self.hand.hand_image.copy()

        cv2.waitKey(1)


    def draw_hand(self, surface):
        self.hand.draw(surface)