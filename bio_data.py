import json
import os
from copy import deepcopy


class SettingsManager:
    def __init__(self, key="tube"):
        self.directory = dir_dict[key]
        with open(self.directory, 'r') as f:
            self.settings = json.load(f)
        self.default_settings = deepcopy(self.settings)
        self.changed = False

    def get(self):
        return self.settings

    def update(self, key, value):
        self.settings[key] = value
        self.changed = True

    def save(self):
        if self.changed:
            #print(self.settings)
            with open(self.directory, "w+") as f:
                json.dump(self.settings, f, indent=4)
            self.changed = False
            self.default_settings = self.settings
            print("Saved settings: ", self.settings)

    def settings_set(self, widget, category, key):
        widget.set(self.settings[category][key])

    def is_changed(self):
        return self.changed


tube_dir = os.path.join("assets", "settings", "hardware_settings.json")
data_dir = os.path.join("assets", "settings", "data_settings.json")
dir_dict = {"tube": tube_dir, "data": data_dir}
for i in range(1,7):
    n = f"tube{i}"
    dir_dict[n] = os.path.join("assets", "settings", n+".json")

if __name__ == "__main__":
    a = SettingsManager()