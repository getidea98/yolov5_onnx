import threading

from config import config


class GlobalInfo:

    def __init__(self, config_path='config.yml'):
        self.weights = None
        self.device = None
        self.source = None
        self.model = None
        self.dataset = None
        self.dt = None
        self.conf_thres = None
        self.iou_thres = None
        self.classes = None
        self.agnostic_nms = None
        self.max_det = None
        self.line_thickness = None
        self.names = None
        self.view_img = None

        # 加载yml加载器
        self.configYaml = config(config_path)
        self.weights, _, self.device, self.view_img = self.configYaml.run_param()

        # 当前顺图位置
        self.pass_list_index = 0

        # 检测屏幕的范围
        self.screen_x0, self.screen_y0, self.screen_x1, self.screen_y1 = -1, -1, -1, -1

        # 顺图过程中的技能释放顺序
        self.skills_list = self.configYaml.skills_list()

        self.thread_event = threading.Event()

    def get_next_door(self):
        return self.configYaml.next_door()

    def get_move_material(self):
        return self.configYaml.move_material()

    def set_model(self, model):
        self.model = model

    def get_model(self):
        return self.model

    def set_dataset(self, dataset):
        self.dataset = dataset

    def get_dataset(self):
        return self.dataset

    def set_dt(self, dt):
        self.dt = dt

    def get_dt(self):
        return self.dt

    def set_conf_thres(self, conf_thres):
        self.conf_thres = conf_thres

    def get_conf_thres(self):
        return self.conf_thres

    def set_iou_thres(self, iou_thres):
        self.iou_thres = iou_thres

    def get_iou_thres(self):
        return self.iou_thres

    def set_classes(self, classes):
        self.classes = classes

    def get_classes(self):
        return self.classes

    def set_agnostic_nms(self, agnostic_nms):
        self.agnostic_nms = agnostic_nms

    def get_agnostic_nms(self):
        return self.agnostic_nms

    def set_max_det(self, max_det):
        self.max_det = max_det

    def get_max_det(self):
        return self.max_det

    def set_line_thickness(self, line_thickness):
        self.line_thickness = line_thickness

    def get_line_thickness(self):
        return self.line_thickness

    def set_names(self, names):
        self.names = names

    def get_names(self):
        return self.names

    def set_view_img(self, view_img):
        self.view_img = view_img

    def get_view_img(self):
        return self.view_img

    def get_thread_event(self):
        return self.thread_event
