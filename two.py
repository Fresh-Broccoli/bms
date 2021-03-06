from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import animation
from collections import deque
from mailMIME import BioreactorGmailBot
import random
import os
import csv
import threading
import shutil
import json

class TwoLiveData:
    def __init__(self, parent):
        """ Initiates the live data visualisation tool.
        This tool will create two live graphs stacked on top of each other, and will continuously update both graphs as long as there's
        a constant stream of input data.
        Additionally, it will save all incoming data to .csv file in a dedicated directory.
        It also has a backend email bot that will send an email to relevant stakeholders when readings reach/exceed
        a certain threshold.
        """
        self.fig, self.ax = plt.subplots(2) # Draws two boxes (for graphs)
        self.tubes = [{} for _ in range(6)]
        self.parent = parent
        self.tube_statuses = self.parent.get_tube_statuses()
        self.load_settings() # Loads
        self.now = datetime.now()

        # Logging into Gmail...
        # Needed for the email bot to work.
        self.mail_bot = BioreactorGmailBot(parent, "bioreactor.bot@gmail.com", "75q3@*NyiVDKmr_k")

        # Clear everything in data.
        #for i in os.listdir("data"):
        #    os.remove(os.path.join("data", i))

    def gen_data(self):
        """ Generates random data
        *Used for testing purposes
        namely for reading and recording data.

        Return
        ------
        A list of values (Strings) that will be stored as a row in the final .csv file.
        """
        return [datetime.now().strftime("%H:%M:%S"), random.randint(6,9), random.randint(29, 31)]

    def animate(self, i):
        """ Called once every frame to update graph by creating a new one, creating the illusion of live-data.
        Since this function is executed one per tick (can be set to an arbitrary period of time like a second...), many
        things are done per tick:
            1. Reading/generating data
            2. Check time & and delete old files if need be.
            3. Check data thresholds and send emails to relevant stakeholders if need be.
            4. Save data.
            5. Plot data.
        Parameter
        ---------
        i (?): Don't know, but it's needed for FuncAnimation though.
        """

        # Actual sensor input here
        # Currently, I'm using randomly generated values. Feel free to replace those when sensors work.
        ph = [random.randint(6,9) for _ in self.tubes] # Need to generate a list with the length equal
        # to the maximum number of tubes. For tube numbers that will turned off/not being monitored, just use any dummy
        # value.
        # When attaching hardware code, make sure you store your data like this. If a sensor is turned off, just use
        # a dummy value such as 0 to maintain the same list structure. That dummy value won't be read by the system.
        temperature = [random.random()*3+28 for _ in self.tubes]

        # Recording time
        now = datetime.now()
        time = now.strftime("%H:%M:%S")

        directory = os.path.join("data", now.strftime("%d-%m-%Y"))

        new_day = not os.path.isdir(directory)
        # If we're in a new day, create a new directory with the date as its name.
        if new_day:
            os.mkdir(directory)

        for i in range(len(self.tubes)):
            if self.tube_statuses[i]:
                tube_dir = os.path.join(directory, f"tube{i+1}.csv")
                new_file = not os.path.isfile(tube_dir)
                with open(tube_dir, "a+", newline='', encoding="utf-8") as seesv:
                    writer = csv.writer(seesv)
                    # Check and see if this new .csv file already exists
                    if new_file: # If it doesn't exist, append heading
                        writer.writerow(["Time", "pH", "Temperature"])
                        # Remove the oldest file:
                        # Taken from: https://stackoverflow.com/questions/47739262/find-remove-oldest-file-in-directory
                        list_of_files = os.listdir('data')
                        if len(list_of_files) >= int(data_life[self.settings["data_life"]]):
                            oldest_file = min(list_of_files, key=os.path.getctime)
                            shutil.rmtree(os.path.abspath(oldest_file))
                    writer.writerow([time, ph[i], temperature[i]]) # Append new data


        """
        self.mail_bot.conditional_send_to_all(
            "Too Hot!",
            "At least one of your tubes are overheating",
            overheating_tubes,
            temperature,
            auto_heading=True,
            attach_file= [os.path.join(directory, f"tube{i+1}.csv") if self.tube_statuses[i] else 0 for i in range(len(self.tube_statuses))],
        )
        """
        """ Sending an email with threading
        # Delay times are inconsistent, but are quite short. 
        # Also requires a multi-core machine to run.
        
        mail_thread = threading.Thread(target=self.mail_bot.conditional_send,
                                       args = ("liset73655@zefara.com",
                                               "Too hot!!!",
                                               "Wow! It's {}??C in Melbourne!",
                                               lambda x: x[0] > 30,
                                               genY),
                                       kwargs={"auto_parse":True,
                                               "attach_file": os.path.join("data", self.today+".csv")},
                                       daemon=True)
        
        mail_thread.start()
        
        """
        """ Sending an email without threading.
        # Delay times are consistent, but are quite long.

        self.mail_bot.conditional_send("liset73655@zefara.com",
                                       "Too hot!!!",
                                       "Wow! It's {}??C in Melbourne!",
                                       lambda x: x[0] > 30,
                                       genY,
                                       auto_parse=True,
                                       attach_file=os.path.join("data", self.today+".csv"))
        """

        # In practice:
        mail_thread_temperature = threading.Thread(target=self.mail_bot.conditional_send_to_all,
                                       args = ("Tube threshold exceeded!!!",
                                               "At least one of your tubes are overheating or have bad pH levels. Please check the attached "
                                               ".csv file(s).",
                                               ph_temp,
                                               ph,
                                               temperature
                                               ),
                                       kwargs={"auto_heading":True,
                                               "auto_parse":False,
                                               "attach_file": [os.path.join(directory, f"tube{i+1}.csv") if self.tube_statuses[i] else 0 for i in range(len(self.tube_statuses))]
                                                   },
                                       #daemon=True
                                                   )

        mail_thread_temperature.start()



        # Clear previously graphed data:
        for axe in self.ax:
            axe.clear()
            axe.grid(axis='y')

        plt.rc('grid', linestyle=':', linewidth=1)

        # Adding newly produced/read data to prepare for data visualisation.
        self.times.append(time)
        for i in range(len(self.tubes)):
            if self.tube_statuses[i]:
                tube = self.tubes[i]
                if not tube:
                    self.update_tube(tube)
                tube["ph"].append(ph[i])
                tube["temperature"].append(temperature[i])
                self.ax[0].plot(self.times, tube["ph"], c=colours[i-1] ,label=f"Tube {i+1}")
                self.ax[1].plot(self.times, tube["temperature"], c=colours[i-1], label=f"Tube {i+1}")
        self.ax[0].legend(title="pH", loc="upper left")
        self.ax[1].legend(title="Temperature", loc="upper left")


        self.ax[0].set(ylabel="pH")
        self.ax[1].set(xlabel="Time", ylabel="??C")


        plt.setp(self.ax[0].get_xticklabels(), visible=False)


    def animator(self, interval=1000):
        """ Called to animate the live graph. It just has to exist somewhere in run-time as a variable.

        Parameter
        ---------
        interval (Int, optional): Determines the frame update rate (milliseconds).

        Return
        ------
        FuncAnimation
        """

        return animation.FuncAnimation(self.fig, self.animate, interval=self.translate_interval(self.settings["read_interval"]))
        #self.animater = animation.FuncAnimation(self.fig, self.animate, interval=read_interval[self.settings["read_interval"]])

    def load_settings(self):
        """ Loads settings data from data_settings.json
        Also creates an (settings) image of each tube.
        """
        #print("Load Settings called")
        settings_path = os.path.join("assets", "settings","data_settings.json")
        #if os.path.isfile(settings_path): # Checks and sees if there's a pre-existing settings file.
        with open(settings_path) as f: # If so, load its content as its settings
            self.settings = json.load(f)
        # These are temporary randomly generated data points. They will be replaced by actual data points soon.
        self.times = deque([], int(self.settings["data_points"]))

        for i, tube in enumerate(self.tubes):
            if self.tube_statuses[i]:
                self.prepare_new_tube(tube)


    def update_data_settings(self, settings):
        """ Sets the current data setting to the input setting
        Also updates tube settings to reflect on this change.
        :param settings: a dictionary with the settings that we want.
        """
        self.settings = settings
        self.tube_statuses = self.parent.get_tube_statuses()
        self.times = deque(self.times, int(self.settings["data_points"]))
        for i, tube in enumerate(self.tubes):
            if not self.tube_statuses[i]:
                tube.clear()
            else:
                self.update_tube(tube)

    def update_settings(self, settings):
        """ Sets the current data setting to the input setting
        :param settings: a dictionary with the settings that we want.
        """
        self.settings = settings

    def translate_interval(self, key):
        """ Translates settings value from string to int.
        In the bioreactor data settings page, there are drop down boxes with options such as '1sec', '1day', etc. They
        need to be translated to integers to reflect on these times.
        :param key: a string that'll be used to get the integer value that will reflect on it.
        :return: an integer that reflects on the value that the key is referring to.
        """
        return read_interval[key]

    def prepare_new_tube(self, tube):
        """ Initialises a tube deque
        Used for plotting data for a specific tube. The length is determined by the pre-loaded settings.
        :param tube: a dictionary that represents the settings used by a particular tube.
        """
        tube["ph"] = deque([], int(self.settings["data_points"]))
        tube["temperature"] = deque([], int(self.settings["data_points"]))
        # To add more parameters, just follow the following template:
        # tube[PARAMETER] = deque([], int(self.settings[PARAMETER]))
        # PARAMETER needs to be a valid setting in ...

    def update_tube(self, tube):
        """ Updates a specific tube.
        If the tube exists, update it with updated settings, otherwise, create a new tube.
        :param tube: a dictionary that represents the settings used by a particular tube.
        :return:
        """
        if tube:
            tube["ph"] = deque(tube["ph"], int(self.settings["data_points"]))
            tube["temperature"] = deque(tube["temperature"], int(self.settings["data_points"]))
        else:
            tube["ph"] = deque([0 for _ in self.times], int(self.settings["data_points"]))
            tube["temperature"] = deque([0 for _ in self.times], int(self.settings["data_points"]))

    def update_tube_status(self, tube_no, status):
        """ Updates the status of a particular tube.
        The status refers to whether or not the tube is online or offline.
        :param tube_no: the tube number of a particular tube.
        :param status: a boolean.
        """
        self.tube_statuses[tube_no-1] = status

    def tube_clear(self, tube_no):
        """ Clears all data recorded on a specific tube.
        :param tube_no: an integer allocated to each tube. Ranges from 1-6.
        """
        self.tubes[tube_no-1] = {"ph":deque([],int(self.settings["data_points"])),
                                 "temperature":deque([],int(self.settings["data_points"]))}

def overheating_tubes(temperatures, threshold=30):
    """ Checks to see if input temperatures exceed the threshold.
    :param temperatures: a list of numbers representing temperature.
    :param threshold: the threshold number.
    :return: a list of boolean that determines whichever tube is overheating or not.
    """
    #print(temperatures)
    return [temp > threshold for temp in temperatures]

def bad_ph_tubes(phs, lower_threshold=7, upper_threshold=8):
    """ Same as overheating_tubes, but for pH.
    :param phs: a list of numbers representing pH.
    :param lower_threshold: the lower threshold number.
    :param upper_threshold: the upper threshold number.
    :return: a list of boolean that determines whichever tube is has a pH outside of its ideal range.
    """
    return [lower_threshold <= ph <= upper_threshold for ph in phs]

def ph_temp(ph, temp):
    """ Checks both temperature and pH
    Outputs True for a particular if the tube has bad pH, overheated, or both
    :param ph: a list of numbers representing pH.
    :param temp: a list of numbers representing temperature.
    :return: a list of boolean that determines whichever tube is overheating, has a bad pH level, or both.
    """
    t = overheating_tubes(temp)
    p = bad_ph_tubes(ph)
    return [t[i] or p[i] for i in range(len(t))]
# Converts data life keys to actual integer values.
with open(os.path.join("assets", "settings", "data_life.json")) as f:
    data_life = json.load(f)
# Converts read interval keys to actual integer values.
with open(os.path.join("assets", "settings", "read_interval.json")) as f:
    read_interval = json.load(f)

# More colours at: https://matplotlib.org/stable/gallery/color/named_colors.html
colours = ["cyan", "lime", "fuchsia", "gold", "navy", "teal"]

if __name__ == "__main__":
    producer = TwoLiveData()
    ani = producer.animator()
    plt.show()

