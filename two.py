from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import animation
from collections import deque
from mailMIME import BioreactorGmailBot
import random
import os
import csv
import threading
import json

class TwoLiveData:
    def __init__(self):
        """ Initiates the live data visualisation tool.
        This tool will create two live graphs stacked on top of another that will continuously update as long as there's
        a constant stream of input data.
        Additionally, it will save all incoming data to .csv file in a dedicated directory.

        Parameters
        ----------

        """
        self.fig, self.ax = plt.subplots(2)
        #plt.tight_layout(pad=1.08, h_pad=1.5)
        self.y = []
        self.h = []
        self.t = []
        self.settings = self.load_settings()

        self.now = datetime.now()

        #self.mail_bot = BioreactorGmailBot("bioreactor.bot@gmail.com", "75q3@*NyiVDKmr_k")

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
        return [datetime.now().strftime("%H:%M:%S"), random.randint(6,9), random.randint(20, 40)]

    def animate(self, i):
        """ Called once every frame to update graph by creating a new one, creating the illusion of live-data.

        Parameter
        ---------
        i (?): Don't know, but it's needed for FuncAnimation though.
        """
        # print("Time: ", self.t)
        # print("Melb Temp: ", self.y)
        # print("Antarctic Temp: ", self.h)

        # Actual sensor input here
        genY = random.randint(6, 9)
        genH = random.randint(20, 40)

        other_data = [self.gen_data() for _ in range(5)]
        now = datetime.now()
        time = now.strftime("%H:%M:%S")

        directory = os.path.join("data", now.strftime("%d-%m-%Y") + ".csv")

        new_day = not os.path.isfile(directory)

        with open(directory, "a+", newline='', encoding="utf-8") as seesv:
            writer = csv.writer(seesv)
            # Check and see if this new .csv file already exists
            if new_day: # If it doesn't exist, append heading
                writer.writerow(["Time", "Average pH", "Average Temperature °C"])
                # Remove the oldest file:
                # Taken from: https://stackoverflow.com/questions/47739262/find-remove-oldest-file-in-directory
                list_of_files = os.listdir('data')
                if len(list_of_files) >= data_life[self.settings["data_life"]]:
                    oldest_file = min(list_of_files, key=os.path.getctime)
                    os.remove(os.path.abspath(oldest_file))
            writer.writerow([time, genY, genH]) # Append new data

        # Sends a mail to the email address if Melbourne temperature exceeds 30C.
        """ Sending an email with threading
        # Delay times are inconsistent, but are quite short. 
        # Also requires a multi-core machine to run.
        
        mail_thread = threading.Thread(target=self.mail_bot.conditional_send,
                                       args = ("liset73655@zefara.com",
                                               "Too hot!!!",
                                               "Wow! It's {}°C in Melbourne!",
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
                                       "Wow! It's {}°C in Melbourne!",
                                       lambda x: x[0] > 30,
                                       genY,
                                       auto_parse=True,
                                       attach_file=os.path.join("data", self.today+".csv"))
        
        # In practice:
        mail_thread = threading.Thread(target=self.mail_bot.conditional_send_to_all,
                                       args = ("Too hot!!!",
                                               "Wow! It's {}°C in Melbourne!",
                                               lambda x: x[0] > 30,
                                               genY),
                                       kwargs={"auto_heading":True,
                                               "auto_parse":True,
                                               "attach_file": os.path.join("data", self.today+".csv")},
                                       daemon=True)

        mail_thread.start()
	"""
        self.t.append(time)
        self.y.append(genY)
        self.h.append(genH)

        for i in range(5):
            self.other_y[i].append(other_data[i][1])
            self.other_h[i].append(other_data[i][2])

        for axe in self.ax:
            axe.clear()

        """
        # Bar Graph
        pH = [random.randint(6,9) for _ in range(6)]
        temp = [random.randint(20,60) for _ in range(6)]

        self.ax[0].bar([f"Tube {n}" for n in range(1,7)], pH, color="g")
        self.ax[1].bar([f"Tube {n}" for n in range(1,7)], temp, color="g")
        # End of Bar graph.
        """

        #Line graph
        self.ax[0].plot(self.t, self.y, label="Tube 1")
        self.ax[1].plot(self.t, self.h, label="Tube 1")

        for i in range(5):
            self.ax[0].plot(self.t, self.other_y[i], label=f"Tube {i+2}")
            self.ax[1].plot(self.t, self.other_h[i], label=f"Tube {i+2}")
        self.ax[0].legend(title="pH", loc="upper left")
        self.ax[1].legend(title="Temperature", loc="upper left")
        # End of Line graph

        self.ax[0].set(ylabel="pH")
        self.ax[1].set(xlabel="Time", ylabel="°C")

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
        return animation.FuncAnimation(self.fig, self.animate, interval=read_interval[self.settings["read_interval"]])

    def load_settings(self):
        settings_path = os.path.join("assets", "settings","data_settings.json")
        #if os.path.isfile(settings_path): # Checks and sees if there's a pre-existing settings file.
        with open(settings_path) as f: # If so, load its content as its settings
            settings = json.load(f)

        # These are temporary randomly generated data points. They will be replaced by actual data points soon.
        self.y = deque(self.y, int(settings["data_points"]))
        self.h = deque(self.h, int(settings["data_points"]))
        self.t = deque(self.t, int(settings["data_points"]))
        self.other_y, self.other_h = [deque([], int(settings["data_points"])) for _ in range(5)], [deque([],
                                                                                                         int(settings["data_points"])) for _ in range(5)]
        return settings

    def update_settings(self):
        pass

# Taken from: https://thispointer.com/python-get-last-n-lines-of-a-text-file-like-tail-command/
def get_last_n_lines(file_name, N):
    # Create an empty list to keep the track of last N lines
    list_of_lines = []
    # Open file for reading in binary mode
    with open(file_name, 'rb') as read_obj:
        # Move the cursor to the end of the file
        read_obj.seek(0, os.SEEK_END)
        # Create a buffer to keep the last read line
        buffer = bytearray()
        # Get the current position of pointer i.e eof
        pointer_location = read_obj.tell()
        # Loop till pointer reaches the top of the file
        while pointer_location >= 0:
            # Move the file pointer to the location pointed by pointer_location
            read_obj.seek(pointer_location)
            # Shift pointer location by -1
            pointer_location = pointer_location -1
            # read that byte / character
            new_byte = read_obj.read(1)
            # If the read byte is new line character then it means one line is read
            if new_byte == b'\n':
                # Save the line in list of lines
                list_of_lines.append(buffer.decode()[::-1])
                # If the size of list reaches N, then return the reversed list
                if len(list_of_lines) == N:
                    return list(reversed(list_of_lines))
                # Reinitialize the byte array to save next line
                buffer = bytearray()
            else:
                # If last read character is not eol then add it in buffer
                buffer.extend(new_byte)
        # As file is read completely, if there is still data in buffer, then its first line.
        if len(buffer) > 0:
            list_of_lines.append(buffer.decode()[::-1])
    # return the reversed list
    return list(reversed(list_of_lines))

with open(os.path.join("assets", "settings", "data_life.json")) as f:
    data_life = json.load(f)
with open(os.path.join("assets", "settings", "read_interval.json")) as f:
    read_interval = json.load(f)

if __name__ == "__main__":
    producer = TwoLiveData()
    ani = producer.animator()
    plt.show()

