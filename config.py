import yaml


class config:

    def __init__(self, config_path='config.yml') -> None:
        self.params = yaml.load(open(config_path, 'r', encoding='utf-8').read(), Loader=yaml.SafeLoader)

    def run_param(self):
        return [self.params['weights'], self.params['source'], self.params['device'], self.params['view_img']]

    def move_material(self):
        return self.params['move_material']

    def next_door(self):
        return self.params['next_door']

    def skills_list(self):
        return self.params['skills_list']

    def celia_into_door(self):
        return self.params['celia_into_door']
