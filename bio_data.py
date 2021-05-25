import json
import os
from copy import deepcopy

class BioSettingsManager:
    def __init__(self, file=os.path.join("assets", "settings", "bioreactor_settings.json")):
        self.directory = file
        with open(file, 'r') as f:
            self.settings = json.load(f)
        self.default_settings = deepcopy(self.settings)
        self.changed = False

    def get(self):
        return self.settings

    def update(self, category, key, value):
        self.settings[category][key] = value
        self.changed = True

    def save(self):
        if self.changed:
            with open(self.directory, "w+") as f:
                json.dump(self.settings, f, indent=4)
            self.changed = False
            self.default_settings = self.settings
            print("Saved settings: ", self.settings)

    def settings_set(self, widget, category, key):
        widget.set(self.settings[category][key])

    def is_changed(self):
        return self.changed