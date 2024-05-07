#!/usr/bin/python

#################
# GUI Interface for the Watch Dog in TKinter

# TO DO:
# Error and exception handling
# Focus
# Actual valid button combs (on + exp + tl only or just on)
# maybe need to be able to identify if already running?
# make check box ticks larger


##################

import tkinter as tk
from tkinter import messagebox
from tkinter import font
import subprocess

##################


class WatchDogFrame:
    def __init__(self, parent):
        print("Initialising WatchDog Frame")
        # Main Frame
        self.parent = parent
        self.state_label = None
        self.button = None
        self.button_frame = None
        self.on = False  # Watchdog State
        self.state_label_text = "OFF"

        self.watchdog_frame = tk.Frame(parent, bg='light grey', bd=5)
        self.make_watchdog_button()
        self.watchdog_frame.pack(fill=tk.BOTH, expand=True)

    def make_watchdog_button(self):
        ############
        # COMPONENT:
        self.button_frame = tk.LabelFrame(self.watchdog_frame, bg='light grey', bd=5,
                                          highlightbackground="#6c6c6c")
        self.button_frame.pack(padx=20, pady=25, fill=tk.BOTH, expand=True)
        # BUTTON:
        self.button = tk.Button(self.button_frame, text="Turn On Watchdog", bg="#394dcd", fg="white",  # "#008080"
                                font=(self.parent.font, 20, "bold"), command=self.toggle_state, bd=5, relief=tk.RAISED)
        self.button.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        self.button.pack(padx=20, pady=40, fill=tk.BOTH, expand=True)
        # LABEL:
        self.state_label = tk.Label(self.button_frame, font=(self.parent.font, 16), bg='light grey', fg="#000080", bd=5)
        self.state_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        self.state_label.pack(padx=2, pady=4, fill=tk.BOTH, expand=True)
        self.load_text()

    def toggle_state(self):
        try:
            self.on = not self.on  # Toggle on/off
            if self.on:
                self.button.config(bg="#e52e2e", text="Turn Off Watchdog", font=(self.parent.font, 20, "bold"))
                self.state_label_text = "ON "
                self.parent.run_script('watchdog_on')
            else:
                self.button.config(bg="#394dcd", text="Turn On Watchdog", font=(self.parent.font, 20, "bold"))
                self.state_label_text = "OFF"
                self.parent.run_script('watchdog_off')
            self.load_text()
        except Exception as e:
            self.parent.show_message(f"Error Toggling States: \n {e}")

    def load_text(self):
        self.state_label.config(text="Watch Dog is {}".format(self.state_label_text))


class LogMonitorFrame:

    def __init__(self, parent):
        self.check_ns = None
        self.check_nn = None
        self.tele_frame = None
        self.ns_state_var = None
        self.nn_state_var = None
        self.entry = None
        self.entry_var = None
        self.check_button = None
        self.log_state_var = None
        print("Initialising Log Monitor Frame")

        self.parent = parent

        # construct
        self.logmonitor_frame = tk.LabelFrame(parent, bg='light grey', bd=5, text="Monitor Log",
                                              font=(parent.font, 12, "bold"), highlightbackground="#6c6c6c")
        # functions
        self.make_lm_check_button()
        self.make_lm_entry()
        self.make_lm_tl_checks()
        # pack
        self.logmonitor_frame.pack(padx=20, pady=20)

    def make_lm_check_button(self):
        # CHECK BUTTON:
        self.parent.log_state_var = tk.IntVar()
        self.check_button = tk.Checkbutton(self.logmonitor_frame, text="Log Errors", fg="#000080",
                                           font=(self.parent.font, 12, "bold"),
                                           selectcolor="#008080", relief=tk.RAISED, command=self.run_log_script,
                                           variable=self.log_state_var, bd=3)
        self.check_button.flash()
        self.check_button.pack(padx=20, pady=20, side=tk.LEFT, expand=True)

    def make_lm_entry(self):
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.logmonitor_frame, textvariable=self.entry_var, bd=3)
        self.entry.config(width=8)
        self.entry.pack(padx=10, pady=10, side=tk.LEFT, expand=True)

    def make_lm_tl_checks(self):
        self.nn_state_var = tk.IntVar()
        self.ns_state_var = tk.IntVar()
        #
        self.tele_frame = tk.LabelFrame(self.logmonitor_frame, bg='light grey', borderwidth=0, highlightthickness=0)  
        self.check_nn = tk.Checkbutton(self.tele_frame, text="NN", fg="#000080", font=(self.parent.font, 12, "bold"),
                                       selectcolor="#008080", relief=tk.RAISED, bd=3, variable=self.nn_state_var)
        self.check_ns = tk.Checkbutton(self.tele_frame, text="NS", fg="#000080", font=(self.parent.font, 12, "bold"),
                                       selectcolor="#008080", relief=tk.RAISED, bd=3, variable=self.ns_state_var)
        self.check_nn.pack(padx=10, pady=10, side=tk.TOP, expand=True)
        self.check_ns.pack(padx=10, pady=10, side=tk.TOP, expand=True)
        self.check_nn.flash()
        self.check_ns.flash()
        self.tele_frame.pack(padx=20, pady=20, side=tk.LEFT, expand=True)

    def run_log_script(self):
        self.parent.show_message("Log Monitor Not Yet Available.")
        try:
            if self.parent.on and self.log_state_var.get() == 1 and not self.entry_var.get():
                # Flash the entry box
                self.entry.config(bg="#FFC0CB")  # pink
                self.entry.after(250, self.reset_entry_bg)
            elif self.parent.on and self.log_state_var.get() == 1 and not (self.nn_state_var or self.ns_state_var):
                self.parent.show_message("Error: Which Antenna?")
            else:
                parameter = self.entry_var.get()
                # run_script('./script.sh parameter')
        except Exception as e:
            self.parent.show_message(f"Error Running Log Script: \n {e}")

    def reset_entry_bg(self):
        # Reset background color to white
        self.entry.config(bg="white")


class Window(tk.Tk):
    # the window that holds the component frames
    def __init__(self):
        print("Initialising main window")
        super().__init__()
        ###
        self.popup = None
        self.title("Watch Dog GUI")
        self.geometry("600x600")
        self.minsize(400, 200)
        self.configure(bg='light grey')
        self.font = 'Consolas'
        self.check_fonts()
        self.bind_all("<Button-1>", lambda event: event.widget.focus_set())

        try:
            self.watchdog_frame = WatchDogFrame(self)
            self.logmonitor_frame = LogMonitorFrame(self)
        except Exception as e:
            self.show_message(f"Error Starting GUI: \n {e}")
            self.destroy()

    def show_message(self, message):
        self.popup = tk.messagebox.showerror(title="Error", message=message)

    def run_script(self, script):
        try:
            subprocess.run([script])
        except Exception as e:
            self.show_message(f"Error Running Script: \n {e}")

    def check_fonts(self):
        if self.font not in font.families():
            print('adopting Arial')
            self.font = 'Arial'
        if self.font not in font.families():
            print('adopting default font')
            self.font = font.families()[0]
        print(self.font)

##################


if __name__ == "__main__":
    watchdog_gui = Window()
    watchdog_gui.mainloop()
