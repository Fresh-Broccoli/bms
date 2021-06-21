import json
import os
from copy import deepcopy


class SettingsManager:
    """ Manages backend settings for individual tubes and bioreactor settings.
    """
    def __init__(self, key="tube"):
        """ Initialises the manager,
        by loading up either a tube settings or data setting .txt file.
        Also creates a deepcopy of the loaded settings, which serves as a backup reference.
        :param key: a String that's either 'tube' or 'data'.
        """
        self.directory = dir_dict[key]
        with open(self.directory, 'r') as f:
            self.settings = json.load(f)
        self.default_settings = deepcopy(self.settings)
        self.changed = False

    def get(self):
        """ Gets the current settings
        :return: a dictionary that reflects the state of the settings.
        """
        return self.settings

    def update(self, key, value):
        """ Updates the settings dictionary.
        :param key: the name of the setting that we want to change.
        :param value: the value that we want to update the setting with.
        """
        self.settings[key] = value
        self.changed = True

    def save(self):
        """ Saves the current setting configuration.
        Save applies to both backend and the .txt file.
        """
        if self.changed:
            #print(self.settings)
            with open(self.directory, "w+") as f:
                json.dump(self.settings, f, indent=4)
            self.changed = False
            self.default_settings = self.settings
            print("Saved settings: ", self.settings)

    def is_changed(self):
        """ Checks to see if this button has been changed after its previous saved state.
        :return: a Boolean.
        """
        return self.changed


tube_dir = os.path.join("assets", "settings", "hardware_settings.json")
data_dir = os.path.join("assets", "settings", "data_settings.json")
dir_dict = {"tube": tube_dir, "data": data_dir}
for i in range(1,7):
    n = f"tube{i}"
    dir_dict[n] = os.path.join("assets", "settings", n+".json")

if __name__ == "__main__":
    a = SettingsManager()