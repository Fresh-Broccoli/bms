# Copied from: https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
# Credits to Sentdex for providing this TKinter template for free.
# Fullscreen implementation: https://www.delftstack.com/howto/python-tkinter/how-to-create-full-screen-window-in-tkinter/

import matplotlib

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from two import TwoLiveData
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

LARGE_FONT = ("Verdana", 12)

dataGen = TwoLiveData()


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.attributes("-fullscreen", True)
        self.fullScreenState = False

        # self.bind("<F11>", self.toggleFullScreen)
        # self.bind("<Escape>", self.quitFullScreen)

        # tk.Tk.iconbitmap(self, default="leaf.ico") # Activating this crashes the Pi version.
        tk.Tk.wm_title(self, "Bioreactor Monitoring System")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Home, BioreactorSettings):
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
        label = tk.Label(self, text="Welcome Back Captain!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        f = dataGen.fig

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        button = tk.Button(self, text="Bioreactor Settings",
                           fg="white",
                           bg="black",
                           command=lambda: controller.show_frame(BioreactorSettings))
        button.pack()
        button.place(rely=.98, relx=.84, anchor=tk.SE, height=80, width=120)

        button1 = tk.Button(self, text="Quit",
                            fg="white",
                            bg="red",
                            command=lambda: confirm_box(controller.quit, "Are you sure you want to quit?"))
        button1.pack()

        button2 = tk.Button(self, text="Stakeholder Settings",
                            fg="white",
                            bg="black",
                            command=lambda: controller.show_frame(BioreactorSettings))
        button2.pack()
        button2.place(rely=.98, relx=.92, anchor=tk.SE, height=80, width=120)

        tubes = self.tube_button_maker()

    def tube_button_maker(self, buttons=6):
        out = []
        relx = 0.03
        rely = 0.92
        for i in range(buttons):
            out.append(tk.Button(self, text=f"Tube {i + 1}",
                                 fg="white",
                                 bg="green",
                                 ))
            out[-1].pack()
            out[-1].place(rely=rely, relx=relx, anchor=tk.SW, height=30, width=60)
            relx += 0.04
        return out


class BioreactorSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(Home))
        button1.pack()

        button2 = tk.Button(self, text="Quit",
                            fg="white",
                            bg="red",
                            command=lambda: confirm_box(controller.quit, "Are you sure you want to quit?"))
        button2.pack()


class StakeholderSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(Home))
        button1.pack()

        button2 = tk.Button(self, text="Quit",
                            fg="white",
                            bg="red",
                            command=lambda: confirm_box(controller.quit, "Are you sure you want to quit?"))
        button2.pack()


class TubeSettings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(Home))
        button1.pack()

        button2 = tk.Button(self, text="Quit",
                            fg="white",
                            bg="red",
                            command=lambda: confirm_box(controller.quit, "Are you sure you want to quit?"))
        button2.pack()


def confirm_box(func, message, *args):
    choice = messagebox.askyesno("Confirmation", message=message)
    if choice:
        func(*args)



if __name__ == "__main__":
    app = Application()
    ani = dataGen.animator(10000)
    app.mainloop()
