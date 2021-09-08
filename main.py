import numpy as np
import cv2
from PIL import ImageGrab
import time

# util code
from utils.click_area_detection import *
from utils.auto_clickers import *


def check_and_click_continue():
    check_continue_img = np.array(ImageGrab.grab())  # 转换为opencv可以识别的numpy数组
    button_cnts, button_centers, frame = find_continue_btn(check_continue_img)

    # 若弹出继续按钮 则进行点击
    if(len(button_centers) >= 1):
        for btn_center in button_centers:
            click_continue_btn(btn_center)
            time.sleep(1)
            break


# 请使用
if __name__ == '__main__':

    # 延时，让玩家可以有空打开全屏模式
    time.sleep(5)

    # # 判断 Game Area
    # img = ImageGrab.grab()
    # img_np = np.array(img)

    # find_first_non_black_pixel(img_np)

    # # 游戏区起始的那个pixel的坐标（非黑的像素）
    # starting_pixel = find_game_area(img_np)

    '''
        开启学习流程：
    '''
    while True:
        print("Taking a screenshot")
        img = ImageGrab.grab()  # 原始截图，参数可以为：x, y, w, h
        img_np = np.array(img)  # 转换为opencv可以识别的numpy数组
        # cv2.imshow("Screenshot", img_np)

        # frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

        # 寻找是否有图片可选择
        square_cnts, square_centers, frame = find_pictures(img_np)
        if(len(square_cnts) >= 4):
            print("Found flashcard pictures")
            '''
                TODO:
                click the pic by looping through {square_centers}
            '''
            for pic_center in square_centers:
                click_flashcard_picture(pic_center)
                time.sleep(1)

                print("查看是否弹出继续按钮")
                check_and_click_continue()

        # 没有找到图片，进行 是否为释义题/含有继续按钮 的判断
        else:
            print("Looking for CN paraprahse boxes")
            # 寻找释义题的框框：
            box_cnts,  box_centers, frame = find_CN_paraphrase_boxes(
                img_np)

            # 确实是释义题
            if(len(box_cnts) >= 4):
                '''
                    进行点击的操作
                    click the pic by looping through {box_centers}
                '''
                # 点击每一个释义
                for box_center in box_centers:
                    click_paraphrase_box(box_center)
                    time.sleep(1)

                    print("查看是否弹出继续按钮")
                    check_and_click_continue()

            # 不是释义题, 寻找继续按钮：
            else:
                print("looking for continue button")
                button_cnts, button_centers, frame = find_continue_btn(img_np)
                # 找到继续按钮，进行点击
                if(len(button_centers) >= 1):

                    '''
                        click the continue button by using the 0-th idx of {button_centers}
                    '''
                    for btn_center in button_centers:
                        click_continue_btn(btn_center)

                # 找不到继续按钮，进行下一项操作
                else:
                    # TODO 设置相应的纠错机制
                    print("can't find continue button")
                    continue

        if cv2.waitKey(1) & 0Xff == ord('q'):
            break

        k = cv2.waitKey(33)
        if k == 27:    # Esc key to stop
            break

    cv2.destroyAllWindows()
