# -- coding: utf-8 --
import argparse
import time

import directkeys
import log
from MousePointAPI import mouse_click_game_menu, mouse_click_back_city, mouse_click_select_role
from Win32guiUtil import Win32guiUtil
from detect import Detect
from global_info import GlobalInfo


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_path', default='config.yml')
    opt = parser.parse_args()
    gi = GlobalInfo(opt.config_path)
    gi.weights, gi.source, gi.device, gi.view_img = gi.cg.run_param()
    return gi


def main():
    # 解析入参
    global_info = GlobalInfo('config.yml')
    log.info('参数解析完成')
    # win32 = Win32guiUtil()
    # 将游戏放在最上层
    # win32.set_foreground_window()
    # (global_info.screen_x0, global_info.screen_y0, width, height) = win32.get_window_pos()
    (global_info.screen_x0, global_info.screen_y0, width, height) = 0, 0, 1920, 1080
    log.info('游戏屏幕位置解析完成。top:{} left:{} width:{} height:{}'
             .format(global_info.screen_x0, global_info.screen_y0, width, height))
    # 主屏幕
    global_info.source = 'screen 0 {} {} {} {}'.format(global_info.screen_x0, global_info.screen_y0,
                                                       width - global_info.screen_y0, height - global_info.screen_y0)

    # 加载dt对象
    dt = Detect(global_info)
    log.info('Detect对象创建完成')
    dt.detect_screen()  # 推理屏幕


if __name__ == "__main__":
    log.info('开始运行程序')
    main()
