import random

import log
from MousePointAPI import mouse_click_game_menu, mouse_click_back_city, mouse_click_select_role
from direction_move import move
import torch
import time
import directkeys
from directkeys import ReleaseKey
from skill_recgnize import attack
from small_recgonize import current_door
from utils.general import (xyxy2xywh)


#  从赛利亚房间进入海伯伦地图
def auto_come_hbl():
    # 推理屏幕前需要先进入地下城
    directkeys.PressKey(directkeys.direct_dic["DOWN"])
    time.sleep(1)
    directkeys.ReleaseKey(directkeys.direct_dic["DOWN"])
    directkeys.PressKey(directkeys.direct_dic["RIGHT"])
    time.sleep(10)
    directkeys.ReleaseKey(directkeys.direct_dic["RIGHT"])
    # 选择海伯伦的预言所
    directkeys.PressKey(directkeys.direct_dic["UP"])
    time.sleep(0.5)
    directkeys.ReleaseKey(directkeys.direct_dic["UP"])
    directkeys.key_press('SPACE')


class Strategy:
    def __init__(self, info):
        self.info = info
        self.names = self.info.get_names()
        self.action_cache = None  # 当前程序正在按下的按键x
        self.press_delay = 0.1  # 按压时间
        self.release_delay = 0.1  # 释放时间
        self.det = None
        self.im0s = None
        self.im = None
        self.door1_time_start = -1  # 上次在第一个图的时间
        self.pre_options_time = -1  # 上次选择地下城的时间

        self.next_door = str(self.info.get_next_door())
        self.move_material = str(self.info.get_move_material())

        self.thx = 30  # 捡东西时，x方向的阈值
        self.thy = 28  # 捡东西时，y方向的阈值
        self.attx = 150  # 攻击时，x方向的阈值
        self.atty = 50  # 攻击时，y方向的阈值

        # 加载技能释放顺序
        self.skills_list_origin = self.info.skills_list
        self.skills_list = self.skills_list_origin.copy()

        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(self.names))]

        #  没找到人物时的移动移动方向
        self.not_found_role_direct = 'RIGHT'

        # 连续检测在BOSS房间的次数
        self.consecutive_boss_door = 0

        self.thread_event = self.info.get_thread_event()

        # 当前所在房间号
        self.door_index = 0
        # 上次检测时房间号
        self.pre_door_index = 0

        self.pre_press_next_time = -1
        # 上次因为找不到标签而移动的时间点
        self.pre_nothing_move_time = -1

    def set_detect_result(self, det, im0s, im):
        self.det = det
        self.im0s = im0s
        self.im = im

    def run(self):
        while True:
            try:
                self.thx = 44  # 捡东西时，x方向的阈值
                self.thy = 30  # 捡东西时，y方向的阈值
                self.attx = 150  # 攻击时，x方向的阈值
                self.atty = 50  # 攻击时，y方向的阈值

                im0 = self.im0s.copy()

                # 推来出来的标签位置
                img_object = []
                # 推理出来的标签
                cls_object = []
                hero_conf = 0
                # 人物在集合中的下标
                hero_index = -1
                # 遍历该对象的位置、类别。并保存到集合中
                for idx, (*xyxy, conf, cls) in enumerate(reversed(self.det)):

                    # 转换xywh形式，方便计算距离
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4))).view(-1).tolist()
                    cls = int(cls)
                    img_object.append(xywh)
                    cls_object.append(self.names[cls])

                    if self.names[cls] == 'hero' and conf > hero_conf:
                        hero_conf = conf
                        hero_index = idx
                self.pre_door_index = self.door_index
                self.door_index = current_door(im0)
                if 'select' in cls_object:
                    pass
                # 继续下个地下城
                if "options" in cls_object:
                    self.select_next_time()
                    continue

                if hero_index == -1:
                    # 没找到角色
                    self.not_found_role()
                    continue
                else:
                    hero_xywh = img_object[hero_index]
                    # 因为找到的是称号位置，需要考虑人物身高
                    hero_xywh[1] += 190

                # 打怪
                if "monster" in cls_object:
                    self.monster(im0, hero_xywh, cls_object, img_object)

                # 捡材料
                if 'hero' in cls_object and ('material' in cls_object or 'money' in cls_object):
                    self.material_money(hero_xywh, cls_object, img_object)

                # 移动到下一个地图
                if "door" in cls_object and "monster" not in cls_object and "material" not in cls_object \
                        and "money" not in cls_object:
                    self.move_next_door(im0, hero_xywh, cls_object, img_object)

                # 在第一个房间上buff
                if self.door_index == 0 and time.time() - self.door1_time_start > 10:
                    self.current_door0()

                # 没有识别到 则向右走
                if "money" not in cls_object and "material" not in cls_object and "monster" not in cls_object \
                        and "door" not in cls_object and 'options' not in cls_object:
                    self.nothing()

            except Exception as e:
                log.info(e)
            self.thread_event.wait()

    # 在第一个房间
    def current_door0(self):
        self.door1_time_start = time.time()
        # 开局向右移动一段距离，修复开局卡位置问题
        move(direct="RIGHT_DOWN", material=True, action_cache=self.action_cache, press_delay=self.release_delay,
             release_delay=self.release_delay)
        time.sleep(0.3)
        self.release_action_cache()
        directkeys.key_press('H')
        log.info('房间号:{}, 当前按键:{}, 开启buff').format(self.door_index, self.action_cache)
        time.sleep(1)
        directkeys.key_press('T')
        log.info('房间号:{}, 当前按键:{}, 开启一觉').format(self.door_index, self.action_cache)
        time.sleep(1)
        directkeys.key_press('Y')
        log.info('房间号:{}, 当前按键:{}, 开启二觉').format(self.door_index, self.action_cache)
        time.sleep(1)
        directkeys.key_press('U')
        log.info('房间号:{}, 当前按键:{}, 支配之环').format(self.door_index, self.action_cache)
        time.sleep(1)
        self.action_cache = None

    # 打怪
    def monster(self, im0, hero_xywh, cls_object, img_object):
        door_index = current_door(im0)
        skill = self.skills_list[door_index]
        directkeys.key_press(skill)
        log.info('房间号:{}, 当前按键:{}, 打怪:释放技能攻击'.format(self.door_index, self.action_cache))
        self.release_action_cache()

        min_distance = float('inf')  # 取无穷小
        monster_box = None
        direct = None
        # 取最近的怪的坐标
        for idx, (c, box) in enumerate(zip(cls_object, img_object)):
            if c == 'monster':
                dis = ((hero_xywh[0] - box[0]) ** 2 + (hero_xywh[1] - box[1]) ** 2) ** 0.5  # 怪与角色的距离
                if dis < min_distance:
                    monster_box = box
                    min_distance = dis
        # 处于攻击距离
        if abs(hero_xywh[0] - monster_box[0]) < self.attx and abs(hero_xywh[1] - monster_box[1]) < self.atty:
            skill_name = attack(im0)
            directkeys.key_press(skill_name)
            log.info('房间号:{}, 当前按键:{}, 释放技能攻击{}'.format(self.door_index, self.action_cache, skill_name))
            self.release_action_cache()
            # break
        # 怪物在英雄右上  ， 左上     左下   右下
        elif monster_box[1] - hero_xywh[1] < 0 < monster_box[0] - hero_xywh[0]:
            # y方向 小于攻击距离
            if abs(monster_box[1] - hero_xywh[1]) < self.thy:
                direct = "RIGHT"
            elif hero_xywh[1] - monster_box[1] < monster_box[0] - hero_xywh[0]:
                direct = "RIGHT_UP"
            elif hero_xywh[1] - monster_box[1] >= monster_box[0] - hero_xywh[0]:
                direct = "UP"
        elif monster_box[1] - hero_xywh[1] < 0 and monster_box[0] - hero_xywh[0] < 0:
            if abs(monster_box[1] - hero_xywh[1]) < self.thy:
                direct = "LEFT"
            elif hero_xywh[1] - monster_box[1] < hero_xywh[0] - monster_box[0]:
                direct = "LEFT_UP"
            elif hero_xywh[1] - monster_box[1] >= hero_xywh[0] - monster_box[0]:
                direct = "UP"
        elif monster_box[1] - hero_xywh[1] > 0 > monster_box[0] - hero_xywh[0]:
            if abs(monster_box[1] - hero_xywh[1]) < self.thy:
                direct = "LEFT"
            elif monster_box[1] - hero_xywh[1] < hero_xywh[0] - monster_box[0]:
                direct = "LEFT_DOWN"
            elif monster_box[1] - hero_xywh[1] >= hero_xywh[0] - monster_box[0]:
                direct = "DOWN"
        elif monster_box[1] - hero_xywh[1] > 0 and monster_box[0] - hero_xywh[0] > 0:
            if abs(monster_box[1] - hero_xywh[1]) < self.thy:
                direct = "RIGHT"
            elif monster_box[1] - hero_xywh[1] < monster_box[0] - hero_xywh[0]:
                direct = "RIGHT_DOWN"
            elif monster_box[1] - hero_xywh[1] >= monster_box[0] - hero_xywh[0]:
                direct = "DOWN"
        if direct is not None:
            self.action_cache = move(direct=direct, material=True, action_cache=self.action_cache,
                                     press_delay=self.press_delay,
                                     release_delay=self.release_delay)

    # 进入下一个房间
    def move_next_door(self, im0, hero_xywh, cls_object, img_object):
        log.info('房间号:{}, 当前按键:{}, 顺图:准备进入下个房间'.format(self.door_index, self.action_cache))
        door_box = None
        direct = None
        for idx, (c, box) in enumerate(zip(cls_object, img_object)):
            if c == 'door':
                door_box = box
                door_box[1] += 60
        # 门的位置在屏幕的左边偏下
        if door_box[0] < im0.shape[0] * 0.1 and door_box[1] > im0.shape[1] * 0.2:
            log.info('房间号:{}, 当前按键:{}, 顺图:门的位置小于抓取的一半，在左侧不符合顺图要求,向RIGHT_UP移动'.format(
                self.door_index, self.action_cache))
            self.action_cache = move(direct="RIGHT_UP", action_cache=self.action_cache,
                                     press_delay=self.press_delay,
                                     release_delay=self.release_delay)
            # break
        # 门在右下方
        elif door_box[1] - hero_xywh[1] < 0 < door_box[0] - hero_xywh[0]:
            if abs(door_box[1] - hero_xywh[1]) < self.thy and abs(door_box[0] - hero_xywh[0]) < self.thx:
                self.action_cache = None
            elif abs(door_box[1] - hero_xywh[1]) < self.thy:
                direct = "RIGHT"
            elif hero_xywh[1] - door_box[1] < door_box[0] - hero_xywh[0]:
                direct = "RIGHT_UP"
            elif hero_xywh[1] - door_box[1] >= door_box[0] - hero_xywh[0]:
                direct = "UP"
        #  门在右上方
        elif door_box[1] - hero_xywh[1] < 0 and door_box[0] - hero_xywh[0] < 0:
            if abs(door_box[1] - hero_xywh[1]) < self.thy and abs(door_box[0] - hero_xywh[0]) < self.thx:
                self.action_cache = None
                # break
            elif abs(door_box[1] - hero_xywh[1]) < self.thy:
                direct = "LEFT"
            elif hero_xywh[1] - door_box[1] < hero_xywh[0] - door_box[0]:
                direct = "LEFT_UP"
            elif hero_xywh[1] - door_box[1] >= hero_xywh[0] - door_box[0]:
                direct = "UP"
        # 门在左下方
        elif door_box[1] - hero_xywh[1] > 0 > door_box[0] - hero_xywh[0]:
            if abs(door_box[1] - hero_xywh[1]) < self.thy and abs(door_box[0] - hero_xywh[0]) < self.thx:
                self.action_cache = None
                # break
            elif abs(door_box[1] - hero_xywh[1]) < self.thy:
                direct = "LEFT"
            elif door_box[1] - hero_xywh[1] < hero_xywh[0] - door_box[0]:
                direct = "LEFT_DOWN"
            elif door_box[1] - hero_xywh[1] >= hero_xywh[0] - door_box[0]:
                direct = "DOWN"
        # 门在左上方
        elif door_box[1] - hero_xywh[1] > 0 and door_box[0] - hero_xywh[0] > 0:
            if abs(door_box[1] - hero_xywh[1]) < self.thy and abs(door_box[0] - hero_xywh[0]) < self.thx:
                self.action_cache = None
                # break
            elif abs(door_box[1] - hero_xywh[1]) < self.thy:
                direct = "RIGHT"
            elif door_box[1] - hero_xywh[1] < door_box[0] - hero_xywh[0]:
                direct = "RIGHT_DOWN"
            elif door_box[1] - hero_xywh[1] >= door_box[0] - hero_xywh[0]:
                direct = "DOWN"
        if direct is not None:
            log.info('房间号:{}, 当前按键:{}, 顺图:进入下一房间:{} hero_xywh {} {} {} {}, door_box {} {} {} {}'.
                     format(self.door_index, self.action_cache, direct, hero_xywh[0], hero_xywh[1], hero_xywh[2],
                            hero_xywh[3], door_box[0], door_box[1], door_box[2], door_box[3]))
            self.action_cache = move(direct=direct, action_cache=self.action_cache,
                                     press_delay=self.press_delay,
                                     release_delay=self.release_delay)
        else:
            log.info('房间号:{}, 当前按键:{}, 顺图:方向计算失败 hero_xywh {} {} {} {}, door_box {} {} {} {}'.
                     format(self.door_index, self.action_cache, hero_xywh[0], hero_xywh[1], hero_xywh[2], hero_xywh[3],
                            door_box[0], door_box[1], door_box[2], door_box[3]))
            time.sleep(0.5)

    # 没有检测到其他标签
    def nothing(self):
        # 减少频率，目的是避免检测准确率不高导致影响顺图和捡材料
        if time.time() - self.pre_nothing_move_time > 2:
            log.info('房间号:{}, 当前按键:{}, 没有检测到其他标签, 向{}移动'
                     .format(self.door_index, self.action_cache, 'RIGHT_UP'))
            self.action_cache = move(direct='RIGHT_UP', action_cache=self.action_cache,
                                     press_delay=self.press_delay,
                                     release_delay=self.release_delay)
            # 移动1S后释放
            time.sleep(1)
            self.release_action_cache()
            self.pre_nothing_move_time = time.time()

    # 没找到人物
    def not_found_role(self):
        log.info('房间号:{}, 当前按键:{}, 没有检测到人物, 向{}移动'.format(self.door_index, self.action_cache,
                                                                           self.not_found_role_direct))
        self.action_cache = move(direct=self.not_found_role_direct, action_cache=self.action_cache,
                                 press_delay=self.press_delay,
                                 release_delay=self.release_delay)
        if self.not_found_role_direct == 'RIGHT':
            self.not_found_role_direct = 'LEFT'
        elif self.not_found_role_direct == 'LEFT':
            self.not_found_role_direct = 'UP'
        elif self.not_found_role_direct == 'UP':
            self.not_found_role_direct = 'DOWN'
        elif self.not_found_role_direct == 'DOWN':
            self.not_found_role_direct = 'RIGHT'

    #  选择继续通关
    def select_next_time(self):
        if time.time() - self.pre_press_next_time > 10:
            self.release_action_cache()
            directkeys.key_press('ESC')
            log.info('按下ESC取消加百利或德利拉')
            time.sleep(1)
            directkeys.key_press(self.move_material)
            time.sleep(1)
            log.info('next_door:移动物品到脚下')
            directkeys.key_press("X", 3)
            # 继续
            directkeys.key_press(self.next_door)
            log.info('next_door:重新开始F1')
            #
            # 技能释放顺序，重新初始化
            self.skills_list = self.skills_list_origin.copy()
            self.pre_press_next_time = time.time()
        else:
            log.info('next_door:间隔时间短跳过处理,并暂停6S')
        time.sleep(6)

    # 捡材料
    def material_money(self, hero_xywh, cls_object, img_object):
        min_distance = float("inf")
        material_box = None
        hero_xywh[1] = hero_xywh[1] + (hero_xywh[3] // 2) * 0.7
        self.thx = self.thx / 2
        self.thy = self.thy / 2
        log.info('房间号:{}, 当前按键:{},  捡材料:寻找最进的材料'.format(self.door_index, self.action_cache))
        for idx, (c, box) in enumerate(zip(cls_object, img_object)):
            if c == 'material' or c == "money":
                dis = ((hero_xywh[0] - box[0]) ** 2 + (hero_xywh[1] - box[1]) ** 2) ** 0.5
                if dis < min_distance:
                    material_box = box
                    min_distance = dis
        direct = None
        if abs(material_box[0] - hero_xywh[0]) < self.thx and abs(material_box[1] - hero_xywh[1]) < self.thy:
            self.release_action_cache()
            time.sleep(1)
            directkeys.key_press("X")
            log.info("房间号:{}, 当前按键:{}, 捡材料:捡材料".format(self.door_index, self.action_cache))
            # break
        elif material_box[1] - hero_xywh[1] < 0 < material_box[0] - hero_xywh[0]:
            if abs(material_box[1] - hero_xywh[1]) < self.thy:
                direct = 'RIGHT'
            elif hero_xywh[1] - material_box[1] < material_box[0] - hero_xywh[0]:
                direct = 'RIGHT_UP'
            elif hero_xywh[1] - material_box[1] >= material_box[0] - hero_xywh[0]:
                direct = 'UP'
        elif material_box[1] - hero_xywh[1] < 0 and material_box[0] - hero_xywh[0] < 0:
            if abs(material_box[1] - hero_xywh[1]) < self.thy:
                direct = 'LEFT'
            elif hero_xywh[1] - material_box[1] < hero_xywh[0] - material_box[0]:
                direct = 'LEFT_UP'
            elif hero_xywh[1] - material_box[1] >= hero_xywh[0] - material_box[0]:
                direct = 'UP'
        elif material_box[1] - hero_xywh[1] > 0 > material_box[0] - hero_xywh[0]:
            if abs(material_box[1] - hero_xywh[1]) < self.thy:
                direct = 'LEFT'
            elif material_box[1] - hero_xywh[1] < hero_xywh[0] - material_box[0]:
                direct = 'LEFT_DOWN'
            elif material_box[1] - hero_xywh[1] >= hero_xywh[0] - material_box[0]:
                direct = 'DOWN'
        elif material_box[1] - hero_xywh[1] > 0 and material_box[0] - hero_xywh[0] > 0:
            if abs(material_box[1] - hero_xywh[1]) < self.thy:
                direct = 'RIGHT'
            elif material_box[1] - hero_xywh[1] < material_box[0] - hero_xywh[0]:
                direct = 'RIGHT_DOWN'
            elif material_box[1] - hero_xywh[1] >= material_box[0] - hero_xywh[0]:
                direct = 'DOWN'
        if direct is not None:
            log.info('房间号:{}, 当前按键:{}, 捡材料:向材料移动:{}'.format(self.door_index, self.action_cache, direct))
            self.action_cache = move(direct=direct, material=True, action_cache=self.action_cache,
                                     press_delay=self.press_delay,
                                     release_delay=self.release_delay)
        # break

    #  松开键盘上正在按着的键
    def release_action_cache(self):
        log.info('房间号:{},当前按键:{},  释放按下的按键'.format(self.door_index, self.action_cache))
        if self.action_cache is None:
            pass
        elif self.action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
            ReleaseKey(directkeys.direct_dic[self.action_cache.strip().split("_")[0]])
            ReleaseKey(directkeys.direct_dic[self.action_cache.strip().split("_")[1]])
            self.action_cache = None
        else:
            ReleaseKey(directkeys.direct_dic[self.action_cache])
            self.action_cache = None

    #  更换成下一个角色（不选择）
    def select_next_role(self):
        #  点击游戏菜单
        mouse_click_game_menu(self.info.screen_x0, self.info.screen_y0)
        time.sleep(1)
        #  点击返回城镇
        mouse_click_back_city(self.info.screen_x0, self.info.screen_y0)
        time.sleep(1)
        #  点击选择角色
        mouse_click_select_role(self.info.screen_x0, self.info.screen_y0)
        #  方向键右选择下一个角色
        directkeys.PressKey(directkeys.direct_dic["RIGHT"])
        time.sleep(0.05)
        directkeys.ReleaseKey(directkeys.direct_dic["RIGHT"])

    # 重置当前对象的信息
    def rest(self):
        self.action_cache = None  # 当前程序正在按下的按键x

        self.door1_time_start = -1  # 上次在第一个图的时间
        self.pre_options_time = -1  # 上次选择地下城的时间

        #  没找到人物时的移动移动方向
        self.not_found_role_direct = 'RIGHT'

        # 连续检测在BOSS房间的次数
        self.consecutive_boss_door = 0

        self.door_index = 0
        self.pre_door_index = 0
