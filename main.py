# Copied from: https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
# Credits to Sentdex for providing this TKinter template for free.
# Fullscreen implementation: https://www.delftstack.com/howto/python-tkinter/how-to-create-full-screen-window-in-tkinter/

import matplotlib
import time

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from two import TwoLiveData
from treeUI import StakeholderManager
from popups import confirm_box
import tkinter as tk


LARGE_FONT = ("Verdana", 12)
small_font = ("Verdana", 6)
LARGE_FONT_BOLD = LARGE_FONT[0] + " bold", 12
#dataGen = TwoLiveData()


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.attributes("-fullscreen", True)
        self.fullScreenState = False

        # self.bind("<F11>", self.toggleFullScreen)
        # self.bind("<Escape>", self.quitFullScreen)

        self.live_data_manager = TwoLiveData()

        # tk.Tk.iconbitmap(self, default="leaf.ico") # Activating this crashes the Pi version.
        tk.Tk.wm_title(self, "Bioreactor Monitoring System")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Home, BioreactorSettings, StakeholderSettings):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Home)

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.attributes("-fullscreen", self.fullScreenState)

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.attributes("-fullscreen", self.fullScreenState)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Home(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=5)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)

        self.now = time.strftime('%H:%M:%S')

        top = tk.Frame(self, )
        mid = tk.Frame(self, )
        bottom = tk.Frame(self, )

        top.rowconfigure(0, weight=1)
        top.rowconfigure(1, weight=3)
        top.rowconfigure(2, weight=3)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=8)
        top.columnconfigure(2, weight=1)

        for i in range(5):
            bottom.rowconfigure(i, weight=1)
        for i in range(16):
            bottom.columnconfigure(i, weight=1)

        top.grid(row=0, column=0, sticky="news")
        mid.grid(row=2, column=0, sticky="news")
        bottom.grid(row=4, column=0, sticky="news")

        title = tk.Label(top, text="Welcome Back Captain!", font=LARGE_FONT_BOLD)
        title.grid(row=0, column=1, sticky="news")

        self.clock = tk.Label(top, text=self.now, font=LARGE_FONT)
        self.clock.grid(row=0, column=0, sticky="news")

        quit_button = tk.Button(top,
                                text="Quit",
                                fg="white",
                                bg="red",
                                command=lambda: confirm_box(controller.quit, "Are you sure you want to quit?"))
        """
        quit_button = UserInteractor("Quit",
                                     tk.Button,
                                     top,
                                     text="Quit",
                                     fg="white",
                                     bg="red",
                                     command=lambda: confirm_box(controller.quit, "Are you sure you want to quit?")
                                     )
        """
        quit_button.grid(row=0, column=2, sticky="ne")

        bio_button = tk.Button(bottom,
                               text="Bioreactor Settings",
                               fg="white",
                               bg="black",
                               command=lambda: controller.show_frame(BioreactorSettings))
        """
        bio_button = UserInteractor("Bioreactor Settings",
                                    tk.Button,
                                    bottom,
                                    text="Bioreactor Settings",
                                    fg="white",
                                    bg="black",
                                    command=lambda: controller.show_frame(BioreactorSettings)
                                    )
        """

        bio_button.grid(row=1, column=12, rowspan=3, columnspan=1, sticky="news")

        stake_button = tk.Button(bottom,
                                 text="Stakeholder Settings",
                                 fg="white",
                                 bg="black",
                                 command=lambda: controller.show_frame(StakeholderSettings))

        """
        stake_button = UserInteractor("Stakeholder Settings",
                                      tk.Button,
                                      bottom,
                                      text="Stakeholder Settings",
                                      fg="white",
                                      bg="black",
                                      command=lambda: controller.show_frame(StakeholderSettings)
                                      )
        """

        stake_button.grid(row=1, column=14, rowspan=3, columnspan=1, sticky="news")

        tubes = self.tube_button_maker(bottom)

        f = controller.live_data_manager.fig
        canvas = FigureCanvasTkAgg(f, mid)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)

        """
        f = dataGen.fig

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        """

    def tube_button_maker(self, parent, buttons=6):
        out = []

        for i in range(buttons):
            out.append(

                UserInteractor(str(i),
                               tk.Button,
                               parent,
                               text=f"Tube {i + 1}",
                               fg="white",
                               bg="green")
            )

            out[-1].grid(row=2, column=i, sticky="ns")

        return out


class BioreactorSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        top = tk.Frame(self,
                       bg="red"
                       )
        bottom = tk.Frame(self,
                          bg="blue",
                          )

        top.grid(row=0, column=0, sticky="nesw")
        bottom.grid(row=1, column=0, sticky="nesw")

        for i in range(3):
            top.columnconfigure(i, weight=1)
            bottom.columnconfigure(i, weight=1)
        for i in range(5):
            top.rowconfigure(i, weight=1)
            bottom.rowconfigure(i, weight=1)

        label = tk.Label(top, text="Bioreactor Settings", font=LARGE_FONT_BOLD)
        label.grid(row=0,
                   column=1,
                   sticky="n",
                   padx=5,
                   pady=5)

        home_button = tk.Button(top,
                                text="Back to Home",
                                fg="white",
                                bg="green",
                                command=lambda: controller.show_frame(Home))
        """
        home_button = UserInteractor(
            "Home",
            tk.Button,
            top,
            text="Back to Home",
            fg="white",
            bg="green",
            command=lambda: controller.show_frame(Home)
        )
        """

        home_button.grid(row=0,
                         column=0,
                         sticky="nw",
                         padx=5,
                         pady=5)

        """
        ph_label = tk.Label(top,
                            text="pH: ",
                            font=LARGE_FONT)
        ph_label.grid(row=1,
                      column=0)

        ph_slider = UserInteractor("ph",
                                   tk.Scale,
                                   top,
                                   from_=4,
                                   to_=9,
                                   length=800,
                                   resolution=0.01,
                                   orient=tk.HORIZONTAL
                                   )

        ph_slider.grid(row=1,
                       column=1)
        
        """

        heater_label = tk.Label(top,
                              text="Heater: ",
                              font=LARGE_FONT)

        heater_label.grid(row=2,
                        column=0)


        interval_label = tk.Label(top,
                                  text="Graph Interval: ",
                                  font=LARGE_FONT)
        interval_label.grid(row=3,
                            column=0)

        interval_slider = UserInteractor(
            "read interval",
            tk.Scale,
            top,
            from_=1,
            to_=20,
            length=800,
            orient=tk.HORIZONTAL
        )

        """
        interval_slider = tk.Scale(top,
                                   from_=1,
                                   to_=20,
                                   length=800,
                                   orient=tk.HORIZONTAL)
        """

        interval_slider.grid(row=3,
                             column=1)

        read_label = tk.Label(bottom,
                              text="Read Interval: ",
                              font=LARGE_FONT)
        read_label.pack(side=tk.LEFT,
                        padx=(120, 0))

        read_entry = UserInteractor(
            "read interval",
            tk.Entry,
            bottom,
            width=80
        )

        """
        read_entry = tk.Entry(bottom,
                              width=80)
        """

        read_entry.pack(side=tk.RIGHT)

        data_entry = UserInteractor(
            "data lifespan",
            tk.Entry,
            bottom,
            width=80
        )
        """
        data_entry = tk.Entry(bottom,
                              width=80)
        """
        data_entry.pack(side=tk.LEFT,
                        padx=(120, 0))

        data_label = tk.Label(bottom,
                              text="Data Lifespan: ",
                              font=LARGE_FONT)
        data_label.pack(side=tk.RIGHT, padx=(0, 120))

        confirm = tk.Button(bottom,
                            text="Confirm",
                            command=lambda: confirm_box(get_parameters,
                                                        "Are you sure you want to make this change?",
                                                        interval_slider,
                                                        read_entry,
                                                        data_entry),
                            fg="white",
                            bg="red",
                            height=5,
                            width=20
                            )
        confirm.pack(side=tk.BOTTOM)


class StakeholderSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        top = tk.Frame(self, bg="red")
        top.grid(row=0, column=0, sticky="news")
        mid = tk.Frame(self, bg="yellow")
        mid.grid(row=1, column=0, sticky='news')
        bottom = tk.Frame(self, bg="blue")
        bottom.grid(row=2, column=0, sticky="nwes")

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        top.columnconfigure(2, weight=1)

        bottom.rowconfigure(0, weight=1)
        bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=1)
        bottom.columnconfigure(2, weight=1)

        title = tk.Label(top, text="Stakeholder Settings", font=LARGE_FONT_BOLD)
        title.grid(row=0, column=1, sticky="n")

        home_button = UserInteractor(
            "Home",
            tk.Button,
            top,
            text="Back to Home",
            fg="white",
            bg="green",
            command=lambda: controller.show_frame(Home)
        )

        home_button.grid(row=0,
                         column=0,
                         sticky="nw",
                         padx=5,
                         pady=5)

        stakeholders = open("stakeholders.csv", "r")
        table = StakeholderManager(mid, stakeholders.readline().split(","))
        table.insert_data_from_csv()

        add = UserInteractor("add",
                             tk.Button,
                             bottom,
                             text="Add Stakeholder",
                             font=("bold", 20),
                             command=table.insert_data
                             )

        add.grid(row=0,
                 column=0,
                 sticky="news",
                 padx=15,
                 pady=15
                 )

        delete = UserInteractor("delete",
                                tk.Button,
                                bottom,
                                text="Delete Stakeholder",
                                font=("bold", 20),
                                command=table.delete_data
                                )

        delete.grid(row=0,
                    column=1,
                    sticky="news",
                    padx=15,
                    pady=15
                    )

        clear = UserInteractor("clear",
                               tk.Button,
                               bottom,
                               text="Clear Stakeholders",
                               font=("bold", 20),
                               command=lambda: confirm_box(table.clear_data, "Are you sure you want to clear all data?")
                               )

        clear.grid(row=0,
                   column=2,
                   sticky="news",
                   padx=15,
                   pady=15
                   )


class TubeSettings(tk.Frame):
    def __init__(self, parent, controller, number=0):
        self.number = number
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=f"Tube {self.number} Settings", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        home_button = tk.Button(self, text="Back to Home",
                                command=lambda: controller.show_frame(Home))
        home_button.pack()

        quit_button = tk.Button(self, text="Quit",
                                fg="white",
                                bg="red",
                                command=lambda: confirm_box(controller.quit, "Are you sure you want to quit?"))
        quit_button.pack()


class UserInteractor:
    """ Class used for creating widgets that allow user-interaction.
    This class was created to store a name that will be used to identify collected data.
    """

    def __init__(self, name, type, *args, **settings):
        self.name = name
        self.widget = type(*args, **settings)
        # print(self.widget)

    def get(self):
        return self.widget.get()

    def pack(self, *args, **kwargs):
        # print(args, kwargs)
        self.widget.pack(*args, **kwargs)

    def place(self, *args, **kwargs):
        # print(args, kwargs)
        self.widget.place(*args, **kwargs)

    def grid(self, *args, **kwargs):
        # print(args, kwargs)
        self.widget.grid(*args, **kwargs)


def get_parameters(*widgets):
    """ Gets values from inserted widgets

    Parameter
    ---------
    widgets (List[String]*): Widget (variable) names are stored as Strings, which will be used as a reference to
        gather field values.

    Return
    ------
    A dictionary with the name of the widget as the key, and its value as the element.

    """
    out = dict([(widget.name, widget.get()) for widget in widgets])
    return out  # This output should be passed onto another function that will take them and make changes appropriately.


def print_output(func, *args):
    print(func(*args))

# Time and tick are copied from:
# https://www.daniweb.com/programming/software-development/code/216785/tkinter-digital-clock-python
def tick(page, tick_rate=1000):
    now = time.strftime("%H:%M:%S")
    if page.now != now:
        page.now = now
        page.clock.config(text=now)
    page.clock.after(tick_rate, lambda: tick(page, tick_rate))


if __name__ == "__main__":
    app = Application()
    tick(app.frames[Home])
    ani = app.live_data_manager.animator(1000)
    app.mainloop()
