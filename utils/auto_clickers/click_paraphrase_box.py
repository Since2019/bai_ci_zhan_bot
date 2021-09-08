from pynput.mouse import Button, Controller


def click_paraphrase_box(paraphrase_box_center_px):
    '''
        Passes in a pixel tuple like (695, 400)
        Then pynput.mouse will be clicking that picture automatically.
    '''
    # 实例化Controller得到一个可以操作鼠标的对象
    mouse = Controller()
    print(f"当前鼠标位置: {mouse.position}")  # 当前鼠标位置: (881, 467)
    mouse.position = paraphrase_box_center_px  # 此方法等价于mouse.move(100, 100)
    print(f"当前鼠标位置: {mouse.position}")  # 当前鼠标位置: (100, 100)
    mouse.click(Button.left, 2)


if __name__ == "__main__":
    click_paraphrase_box((500, 500))
