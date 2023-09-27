import json


class Config:
    def __init__(self, window):
        self.window = window

        self.config_file_path = "./config.json"

    def store_config(self):
        config_json = {
            "width": self.window.width(),
            "height": self.window.height(),
            "last_file": self.window.current_file,
        }

        with open(self.config_file_path, "w") as file:
            json.dump(config_json, file)
