import numpy as np
import cv2 as cv

# 設置Kernel
kernel = np.ones((5, 5), np.uint8)

# 设置putText函数字体
font = cv.FONT_HERSHEY_SIMPLEX


# 计算两边夹角额cos值


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1)*np.dot(d2, d2)))


def find_squares(img):
    squares = []
    square_centers = []
    img = cv.GaussianBlur(img, (3, 3), 0)

    # img = canny.copy()

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    bin = cv.Canny(gray, 5, 10, apertureSize=3)

    imgDialation = cv.dilate(bin, kernel, iterations=2)

    # cv.imshow("imgDialation", imgDialation)
    # cv.imshow('canny', bin)

    contours, _hierarchy = cv.findContours(
        imgDialation, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    print("轮廓数量：%d" % len(contours))
    index = 0
    # 轮廓遍历
    for cnt in contours:
        cnt_len = cv.arcLength(cnt, True)  # 计算轮廓周长
        cnt = cv.approxPolyDP(cnt, 0.02*cnt_len, True)  # 多边形逼近
        # 条件判断逼近边的数量是否为4，轮廓面积是否大于1000，检测轮廓是否为凸的
        if len(cnt) == 4 and cv.contourArea(cnt) > 1000 and cv.isContourConvex(cnt):
            M = cv.moments(cnt)  # 计算轮廓的矩
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])  # 轮廓重心

            cnt = cnt.reshape(-1, 2)
            max_cos = np.max(
                [angle_cos(cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4]) for i in range(4)])
            # 只检测矩形（cos90° = 0）
            if max_cos < 0.1:
                # 检测四边形（不限定角度范围）
                # if True:
                index = index + 1
                cv.putText(img, ("#%d" % index), (cx, cy),
                           font, 0.7, (255, 0, 255), 2)
                squares.append(cnt)
                square_centers.append((cx, cy))

    return squares,  square_centers, img,


def find_continue_btn(frame):
    square_cnts, square_centers, img = find_squares(frame)
    return square_cnts, square_centers, img


def main(frame):
    # 输入的图片源
    img = cv.imread("./testing_images/continue_button.jpg")

    squares,  square_centers, img, = find_squares(img)
    print(square_centers)
    cv.drawContours(img, squares, -1, (0, 0, 255), 2)
    cv.imshow('squares', img)
    ch = cv.waitKey()

    print('Done')


# if __name__ == '__main__':
#     print(__doc__)
#     main()
#     cv.destroyAllWindows()
