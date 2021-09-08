import numpy as np
import cv2
from PIL import ImageGrab


def main():
    while True:
        img = ImageGrab.grab()  # x, y, w, h
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

        if cv2.waitKey(1) & 0Xff == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
