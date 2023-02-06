# -- coding: utf-8 --
import time
from threading import Thread

import directkeys
from Strategy import Strategy, auto_come_hbl
import torch
import random

import log
from models.common import DetectMultiBackend
from utils.dataloaders import LoadScreenshots
from utils.general import (Profile, check_img_size, plot_one_box, non_max_suppression, cv2, scale_boxes, xyxy2xywh)
from utils.torch_utils import select_device


class Detect:
    def __init__(self,
                 global_info,
                 img=(640, 640)) -> None:
        self.global_info = global_info
        device = self.global_info.device
        device = select_device(device)
        weights = self.global_info.weights
        source = self.global_info.source
        view_img = self.global_info.view_img
        model = DetectMultiBackend(weights, device=device, dnn=False, fp16=False)

        stride, names, pt = model.stride, model.names, model.pt
        img = check_img_size(img, s=stride)  # check image size

        dataset = LoadScreenshots(source, img_size=img, stride=stride, auto=pt)

        # Run inference
        model.warmup(imgsz=(1 if pt or model.triton else 1, 3, *img))  # warmup
        self.global_info.set_model(model)
        self.global_info.set_dataset(dataset)
        self.global_info.set_dt((Profile(), Profile(), Profile()))
        self.global_info.set_conf_thres(0.25)
        self.global_info.set_iou_thres(0.45)
        self.global_info.set_classes(None)
        self.global_info.set_agnostic_nms(False)
        self.global_info.set_max_det(1000)
        self.global_info.set_line_thickness(3)
        self.global_info.set_names(names)
        self.global_info.set_view_img(view_img)
        self.door1_time_start = -20
        self.action_cache = None
        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(self.global_info.names))]
        self.thread_event = self.global_info.get_thread_event()

    # 主动推理屏幕的信息,并将推理信息放入
    def detect_screen(self):
        model = self.global_info.get_model()
        dataset = self.global_info.get_dataset()
        dt = self.global_info.get_dt()
        conf_thres = self.global_info.get_conf_thres()
        iou_thres = self.global_info.get_iou_thres()
        classes = self.global_info.get_classes()
        agnostic_nms = self.global_info.get_agnostic_nms()
        max_det = self.global_info.get_max_det()
        strategy = Strategy(self.global_info)
        if self.global_info.configYaml.celia_into_door:
            log.info('已开启celia_into_door参数，正在从赛利亚房间进入地下城')
            auto_come_hbl()  # 从赛利亚房间进入地下城
            time.sleep(1)
            log.info('已开启celia_into_door参数，已进入地下城')
            # 吃药触发大天域属性
            directkeys.key_press('1')
            time.sleep(1)
            directkeys.key_press('2')
            log.info('已开启celia_into_door参数，已进入地下城，已吃药触发大天域效果')
        t1 = Thread(target=strategy.run)
        t1.start()
        for _, im, im0s, _, _ in dataset:
            with dt[0]:
                im = torch.from_numpy(im).to(model.device)
                im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
                im /= 255  # 0 - 255 to 0.0 - 1.0
                if len(im.shape) == 3:
                    im = im[None]  # expand for batch dim
            # Inference
            with dt[1]:
                det = model(im, augment=False, visualize=False)
            # NMS
            with dt[2]:
                det = non_max_suppression(det, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

            det = det[0]
            if det is not None and len(det):
                im0 = im0s.copy()
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()
                strategy.set_detect_result(det, im0s, im)
                self.thread_event.set()
                if self.global_info.view_img:
                    for idx, (*xyxy, conf, cls) in enumerate(reversed(det)):
                        label = '%s %.2f' % (self.global_info.names[int(cls)], conf)
                        plot_one_box(xyxy, im0, label=label, color=self.colors[int(cls)], line_thickness=2)
                        if self.global_info.names[int(cls)] == 'hero':
                            hero_xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4))).view(-1).tolist()
                            cv2.circle(im0, (int(hero_xywh[0]), int(hero_xywh[1] + 190)), 1, (0, 0, 255), 10)

                        if self.global_info.names[int(cls)] == 'door':
                            door_xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4))).view(-1).tolist()
                            cv2.circle(im0, (int(door_xywh[0]), int(door_xywh[1]) + 60), 1, (0, 0, 255), 10)

                    im0 = cv2.resize(im0, (1280, 800))
                    cv2.imshow('DNF', im0)
                    if cv2.waitKey(5) & 0xFF == ord('q'):
                        raise StopIteration


