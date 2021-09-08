import cv2
import numpy as np


def find_first_non_black_pixel(frame):
    __debug__ and print("find_first_none_black_pixel")

    # 遍历row和col
    for row_idx, row in enumerate(frame):
        for (col_idx, pixel) in enumerate(row):
            # print(pixel)
            # print(np.array([0, 0, 0]))
            # print(pixel == np.array([0, 0, 0]))
            # print(type(col))
            '''
                黑色为[0 0 0] 
                用np.ndarray.all() 判断比较结果是否为 [True True True]
            '''
            if(np.ndarray.all(pixel != np.array([0, 0, 0]))):
                print(f'index: row: {row_idx} col : {col_idx}')
                print((row_idx, col_idx))
                # print((row_idx, col_idx)[0])
                # print((row_idx, col_idx)[1])
                return (row_idx, col_idx)
            # print(pixel)


def find_game_area(frame):
    img = frame

    # 色相（H）是色彩的基本属性，就是平常所说的颜色名称，如红色、黄色等。
    # 饱和度（S）是指色彩的纯度，越高色彩越纯，低则逐渐变灰，取0-100%的数值。
    # 明度（V），取0-100%。
    # OpenCV中H,S,V范围是0-180,0-255,0-255
    # low = np.array([0, 0, 0])
    # high = np.array([180, 255, 46])

    # low = np.array([100, 100, 100])
    # high = np.array([160, 261, 246])

    #               82  117 197
    # Target Value: 224 237 255

    low = np.array([255, 236, 224])
    high = np.array([255, 236, 224])

    # low = np.array([154, 255, 215])
    # high = np.array([154, 255, 255])

    dst = cv2.inRange(src=img, lowerb=low, upperb=high)  # HSV高低阈值，提取图像部分区域

    # cv2.imshow("dst", dst)

    # 寻找白色的像素点坐标。
    # 白色像素值是255，所以np.where(dst==255)
    print(len(dst))

    xy = np.column_stack(np.where(dst >= 1))

    print(dst)

    print(xy)

    # 在原图的红色数字上用 金黄色 描点填充。
    for c in xy:
        # print(c)
        # 注意颜色值是(b,g,r)，不是(r,g,b)
        # 坐标:c[1]是x,c[0]是y
        cv2.circle(img=img, center=(int(c[1]), int(
            c[0])), radius=1, color=(0, 215, 255), thickness=1)

    cv2.imshow('dst', dst)
    cv2.imshow('result', img)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()
