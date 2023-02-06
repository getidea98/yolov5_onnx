from small_recgonize import current_door


class RiskManagement:
    def __init__(self):
        self.im0 = None
        self.current_door_index = 0
        self.pre_door_index = 0
        self.consecutive_number = 0

    def run(self):
        while True:
            current_door0 = current_door(self.im0)
            if current_door0 == self.current_door_index:
                self.consecutive_number += 1
            else :
                self.consecutive_number = 0

            if self.consecutive_number > 15:
                self.pre_door_index = self.current_door_index
                self.current_door_index = current_door0

