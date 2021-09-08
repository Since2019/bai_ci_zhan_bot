from pynput.mouse import Button, Controller


def click_flashcard_picture(flashcard_center_px):
    '''
        Passes in a pixel tuple like (695, 400)
        Then pynput.mouse will be clicking that picture automatically.
    '''
    # 实例化Controller得到一个可以操作鼠标的对象
    mouse = Controller()
    # mouse.position: 获取当前鼠标位置。
    # 屏幕左上角坐标为(0, 0) 右下角为(屏幕宽度, 屏幕高度)
    print(f"当前鼠标位置: {mouse.position}")  # 当前鼠标位置: (881, 467)

    # 给mouse.position赋值等于移动鼠标，这里相当于移动到(100, 100)的位置
    # 如果坐标小于0，那么等于0。如果超出屏幕范围，那么等于最大范围
    mouse.position = flashcard_center_px  # 此方法等价于mouse.move(100, 100)
    print(f"当前鼠标位置: {mouse.position}")  # 当前鼠标位置: (100, 100)

    # # 按下左键,同理Button.right是右键
    # mouse.press(Button.left)
    # # 松开左键
    # mouse.release(Button.left)
    # # 上面两行连在一起等于一次单击。如果上面两行紧接着再重复一次，那么整体会实现双击的效果
    # # 因为两次单击是连续执行的，没有等待时间。如果中间来一个time.sleep几秒，那么就变成两次单击了

    # # 当然鼠标点击我们有更合适的办法，使用click函数
    # # 该函数接收两个参数：点击鼠标的哪个键、以及点击次数
    # # 这里连续点击两次，等于双击
    mouse.click(Button.left, 2)


if __name__ == "__main__":
    click_flashcard_picture((500, 500))
