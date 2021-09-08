from pynput.mouse import Button, Controller


def click_continue_btn(continue_btn_center_px):
    '''
        Passes in a pixel tuple like (695, 400)
        Then pynput.mouse will be clicking that picture automatically.
    '''
    mouse = Controller()

    print(f"当前鼠标位置: {mouse.position}")  # 当前鼠标位置: (881, 467)

    mouse.position = continue_btn_center_px  # 此方法等价于mouse.move(100, 100)
    print(f"当前鼠标位置: {mouse.position}")  # 当前鼠标位置: (100, 100)
    mouse.click(Button.left, 1)


if __name__ == "__main__":
    click_continue_btn((500, 500))
