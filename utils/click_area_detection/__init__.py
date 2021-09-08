#package: click_area_detection

# HACK: https://stackoverflow.com/questions/34753206/init-py-cant-find-local-modules
# HACK: https://stackoverflow.com/questions/54834348/python-importerror-cannot-import-name-init-py
from .detect_continue_btn import *
from .detect_pictures import *
from .detect_game_area import *
from .detect_CN_explanations import *

'''
    The functions we want to use in a single module,
    they have to be referenced like this:
'''
find_pictures = detect_pictures.find_pictures

find_continue_btn = detect_continue_btn.find_continue_btn

find_CN_paraphrase_boxes = detect_CN_explanations.find_CN_paraphrase_boxes

# detect_game_area:
find_first_non_black_pixel = detect_game_area.find_first_non_black_pixel
find_game_area = detect_game_area.find_game_area
