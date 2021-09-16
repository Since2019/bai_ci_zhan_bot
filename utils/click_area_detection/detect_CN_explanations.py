import numpy as np
import cv2 as cv
import os
import datetime

# 設置Kernel
kernel = np.ones((5, 5), np.uint8)

# 设置putText函数字体
font = cv.FONT_HERSHEY_SIMPLEX


OUTPUT_PATH = os.path.join(
    os.getcwd(), 'IMG_TEMP', 'detect_CN_explanations')


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

    return squares, square_centers, img


def find_squares_bichromatic(img):
    squares = []
    square_centers = []

    img = cv.GaussianBlur(img, (3, 3), 0)

    # img = canny.copy()

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    bin = cv.Canny(gray, 5, 10, apertureSize=3)

    imgDialation = cv.dilate(bin, kernel, iterations=1)

    # cv.imshow("imgDialation", imgDialation)
    # cv.imshow('canny', bin)

    contours, _hierarchy = cv.findContours(
        imgDialation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    print("轮廓数量：%d" % len(contours))

    index = 0
    # 轮廓遍历
    for cnt in contours:
        cnt_len = cv.arcLength(cnt, True)  # 计算轮廓周长
        cnt = cv.approxPolyDP(cnt, 0.02*cnt_len, True)  # 多边形逼近
        # 条件判断逼近边的数量是否为4，轮廓面积是否大于1000，检测轮廓是否为凸的
        if len(cnt) == 4 and cv.contourArea(cnt) > 2000 and cv.isContourConvex(cnt):
            (x, y, w, h) = cv.boundingRect(cnt)
            cv.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            M = cv.moments(cnt)  # 计算轮廓的矩
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])  # 轮廓重心

            cnt = cnt.reshape(-1, 2)
            max_cos = np.max(
                [angle_cos(cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4]) for i in range(4)])
            # 只检测矩形（cos90° = 0）

            if max_cos < 0.15:
                # 检测四边形（不限定角度范围）
                # if True:
                index = index + 1
                cv.putText(img, ("#%d" % index), (cx, cy),
                           font, 0.7, (255, 0, 255), 2)

                squares.append(cnt)
                square_centers.append((cx, cy))

    # 给它围上绿色的框框
    cv.drawContours(img, squares, -1, (0, 0, 255), 2)

    cv.imwrite(os.path.join(
        os.getcwd(), "IMG_TEMP", 'exp '+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        + '.jpg'),
        img
    )

    print("保存路径：")
    print((os.path.join(
        OUTPUT_PATH, datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        + '.jpg')))

    cv.imwrite(os.path.join(
        OUTPUT_PATH, datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        + '.jpg'),
        img)

    return squares, square_centers, img


# 寻找单词图片
def find_pictures(frame):
    '''
        在main中识别video的frame，并返回
        - 轮廓            square_cnts
        - 轮廓中心        square_centers
        - 处理后的图片结果 img
    '''
    square_cnts, square_centers, img = find_squares(frame)


def extract_paraphrase_boxes_by_color(frame):
    __debug__ and print("extract_paraphrase_boxes_by_color()")
    '''
        {frame} 是待检测的帧
        用inRange函数来进行阈值提取并返回符合颜色的区域
    '''

    low = np.array([255, 255, 255])
    high = np.array([255, 255, 255])

    frame = cv.inRange(src=frame, lowerb=low, upperb=high)  # HSV高低阈值，提取图像部分区域
    # low = np.array([154, 255, 215])
    # high = np.array([154, 255, 255])

    '''
        inRange之后会把图片转换成一维数组
        要把它弄成三维的才能够进行下一步的处理
        cv.cvtColor(dst, cv.COLOR_GRAY2BGR)就是做了这件事
    '''
    gray_three_channel = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
    return gray_three_channel, frame


def find_CN_paraphrase_boxes(frame):
    '''
        这个function用于判断是否含有中文释义的框，
        {frame} 是待检测的帧
    '''
    # {dst} 是用inRange阈值检测出来的颜色区域
    dst, frame = extract_paraphrase_boxes_by_color(frame)

    # 在提取的颜色区域中寻找矩形轮廓
    square_cnts,  square_centers, img = find_squares_bichromatic(dst)
    return square_cnts, square_centers, img


# 测试用的main函数：
if __name__ == '__main__':
    # 输入的图片源
    img = cv.imread("../../testing_images/flashcard_without_pictures.jpg")
    # img = cv.imread("../../testing_images/continue_button.jpg")
    #
    # squares,  square_centers, img = find_squares(img)
    # print(square_centers)

    dst, frame = extract_paraphrase_boxes_by_color(img)
    cv.imshow('dst', dst)

    squares,  square_centers, img = find_squares_bichromatic(dst)

    print(squares, square_centers)

    # cv.drawContours(img, squares, -1, (0, 0, 255), 2)

    # cv.imshow('squares', img)

    # cv.imshow('frame', frame)

    # cv2.imshow('result', img)
    # cv2.waitKey(0)

    # ch = cv.waitKey()

    print('Done')
