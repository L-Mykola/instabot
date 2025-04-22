import os

from src.utils.utils import load_json_file


class Settings:
    def __init__(self, root_dir):
        self.settings_path = os.path.join(root_dir, 'config/settings.json')
        self.raw_settings = load_json_file(self.settings_path)

        self.target_ids = self.raw_settings['target_ids']
        self.max_actions_per_run = self.raw_settings['max_actions_per_run']
        self.min_delay = self.raw_settings['min_delay']
        self.max_delay = self.raw_settings['max_delay']

        self.proxy = self.raw_settings['proxy']



