from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import animation
from collections import deque
from mailMIME import BioreactorGmailBot
import random
import os
import csv
import threading


class TwoLiveData:
    def __init__(self, interval=8, max_life=28):
        """ Initiates the live data visualisation tool.
        This tool will create two live graphs stacked on top of another that will continuously update as long as there's
        a constant stream of input data.
        Additionally, it will save all incoming data to .csv file in a dedicated directory.

        Parameters
        ----------
        interval (Int, optional): Limits the number of data points that are on the graph at a particular frame.
        max_life (Int, optional): Maximum lifespan of a saved .csv file in days. After this period, the .csv file will
            be deleted from the system.
        """
        self.fig, self.ax = plt.subplots(2)
        plt.tight_layout(pad=1.08, h_pad=1.5)
        self.today = datetime.today().strftime("%d/%m/%Y")
        self.y = deque([], interval)
        self.h = deque([], interval)
        self.t = deque([], interval)
        self.mail_bot = BioreactorGmailBot("bioreactor.bot@gmail.com", "75q3@*NyiVDKmr_k")
        self.max_life = max_life

        # Clear everything in data.
        for i in os.listdir("data"):
            os.remove(os.path.join("data", i))

    def gen_data(self):
        """ Generates random data
        *Used for testing purposes
        namely for reading and recording data.

        Return
        ------
        A list of values (Strings) that will be stored as a row in the final .csv file.
        """
        return [datetime.now().strftime("%H:%M:%S"), random.randint(0, 50), random.randint(0, 50) * (-1)]

    def animate(self, i):
        """ Called once every frame to update graph by creating a new one, creating the illusion of live-data.

        Parameter
        ---------
        i (?): Don't know, it's needed for FuncAnimation though.
        """
        # print("Time: ", self.t)
        # print("Melb Temp: ", self.y)
        # print("Antarctic Temp: ", self.h)

        # Actual sensor input here
        genY = random.randint(0, 50)
        genH = random.randint(0, 50) * (-1)
        time = datetime.now().strftime("%H:%M:%S")

        directory = os.path.join("data", self.today + ".csv")
        also_today = str(datetime.today().date())
        new_day = False

        if self.today != also_today:
            directory = os.path.join("data", also_today + ".csv")
            new_day = True

        with open(directory, "a+", newline='', encoding="utf-8") as seesv:
            writer = csv.writer(seesv)
            if new_day:
                # Remove the oldest file:
                # Taken from: https://stackoverflow.com/questions/47739262/find-remove-oldest-file-in-directory

                list_of_files = os.listdir('data')
                if len(list_of_files) >= self.max_life:
                    oldest_file = min(list_of_files, key=os.path.getctime)
                    os.remove(os.path.abspath(oldest_file))

                writer.writerow(["Time", "Melbourne Temp", "Antarctic Temp"])
                self.today = also_today
            writer.writerow([time, genY, genH])

        # Sends a mail to the email address if Melbourne temperature exceeds 30C.
        mail_thread = threading.Thread(target=self.mail_bot.conditional_send,
                                       # args = ([genY]),
                                       kwargs={"to":"fedexef285@zevars.com" ,
                                               "subject":"Too hot!!!",
                                               "message": "Wow! It's {}°C in Melbourne!",
                                               "condition": lambda x: x[0] > 30,
                                               "auto_parse":True,
                                               "attach_file": os.path.join("data", self.today+".csv")},
                                       daemon=True)
        #self.mail_bot.conditional_send("fedexef285@zevars.com", "Too hot!!!", "Wow! It's {}°C in Melbourne!",
        #                               lambda x: x[0] > 30, genY, auto_parse=True, attach_file = os.path.join("data", self.today+".csv"))
        mail_thread.start()

        self.t.append(time)
        self.y.append(genY)
        self.h.append(genH)

        self.ax[0].clear()

        self.ax[0].plot(self.t, self.y)
        self.ax[0].set_title('Melbourne Temperature')

        self.ax[1].clear()

        self.ax[1].plot(self.t, self.h, c="green")
        self.ax[1].set_title('Antarctica Temperature')

        for a in self.ax.flat:
            a.set(xlabel='Time', ylabel='°C')

    def animator(self, interval=1000):
        """ Called to animate the live graph. It just has to exist somewhere in run-time as a variable.

        Parameter
        ---------
        interval (Int, optional): Determines the frame update rate (milliseconds).

        Return
        ------
        FuncAnimation
        """
        return animation.FuncAnimation(self.fig, self.animate, interval=interval)


if __name__ == "__main__":
    producer = TwoLiveData()
    ani = producer.animator()
    plt.show()
# ani = animation.FuncAnimation(fig, animate, interval=1000)
# animate(1)

# plt.show()
