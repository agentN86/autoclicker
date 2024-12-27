import tkinter as tk
import threading
import time
from pynput.mouse import Button, Controller
import keyboard
import webbrowser

class AutoClicker:
    def __init__(self, master):

        self.master = master
        self.master.title("Auto Clicker v1.0")
        self.master.iconbitmap("favicon.ico")
        self.master.geometry("300x250")
        self.master.resizable(False, False)
        
        self.is_running = False
        self.mouse = Controller()
        self.keybind = 'F6'

        self.labela = tk.Label(master, text="hours")
        self.labela.place(x=60, y=3)
        self.hoursEntry = tk.Entry(master, width=8)
        self.hoursEntry.insert(0, "0")
        self.hoursEntry.place(x=5, y=3)
        
        self.labelb = tk.Label(master, text="minutes")
        self.labelb.place(x=60, y=25)
        self.minutesEntry = tk.Entry(master, width=8)
        self.minutesEntry.insert(0, "0")
        self.minutesEntry.place(x=5, y=25)

        self.labelc = tk.Label(master, text="secs")
        self.labelc.place(x=60, y=47)
        self.secondsEntry = tk.Entry(master, width=8)
        self.secondsEntry.insert(0, "0")
        self.secondsEntry.place(x=5, y=47)

        self.labeld = tk.Label(master, text="milliseconds")
        self.labeld.place(x=60, y=69)
        self.millisecondsEntry = tk.Entry(master, width=8)
        self.millisecondsEntry.insert(0, "0")
        self.millisecondsEntry.place(x=5, y=69)

        self.typeofclick = tk.IntVar(value=1)
        tk.Radiobutton(root, text='Left Click', variable=self.typeofclick, value=1).place(x=150, y=3)
        tk.Radiobutton(root, text='Right Click', variable=self.typeofclick, value=2).place(x=150, y=25)
        
        self.keybind_button = tk.Button(master, text="Keybind Settings", command=self.openkeybindwin, width="18", pady="5")
        self.keybind_button.place(x=12, y=143)

        self.helpabout_button = tk.Button(master, text="About", command=self.openhelpwin, width="18", pady="5")
        self.helpabout_button.place(x=150, y=143)

        self.start_button = tk.Button(master, text="Start (F6)", command=self.start_clicking, width="18", pady="5")
        self.start_button.place(x=12, y=180)
        
        self.stop_button = tk.Button(master, text="Stop (F6)", command=self.stop_clicking, state=tk.DISABLED, width="18", pady="5")
        self.stop_button.place(x=150, y=180)
        
        self.status_label = tk.Label(master, text="Auto Clicker is ready...", fg="black")
        self.status_label.place(x=5, y=220)

        threading.Thread(target=self.listen_for_hotkey, daemon=True).start()

    def start_clicking(self):
        if self.is_running:
            return

        try:
            hours = float(self.hoursEntry.get())
            minutes = float(self.minutesEntry.get())
            seconds = float(self.secondsEntry.get())
            milliseconds = float(self.millisecondsEntry.get())

            equation = (hours * 3600) + (minutes * 60) + seconds + (milliseconds / 1000)

            self.interval = equation
            if self.interval < 0.001:
                self.status_label.config(text="Interval must be at least 0.001 seconds.", fg="red")
                return
            
            self.is_running = True
            self.status_label.config(text="Auto Clicker is running every {} seconds.".format(equation), fg="black")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            threading.Thread(target=self.clicker_thread, daemon=True).start()
        except ValueError:
            self.status_label.config(text="Please enter a valid number in each box.", fg="red")

    def stop_clicking(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Auto Clicker stopped.", fg="black")

    def clicker_thread(self):
        while self.is_running:
            if self.typeofclick.get() == 1:
                self.mouse.click(Button.left)
            else:
                self.mouse.click(Button.right)
            time.sleep(self.interval)

    def toggle(self):
        if self.is_running:
            self.stop_clicking()
        else:
            self.start_clicking()

    def listen_for_hotkey(self):
        keyboard.add_hotkey(self.keybind, self.toggle)
        keyboard.wait()

    def openkeybindwin(self):
        newwin = tk.Toplevel(self.master)
        newwin.title("Keybind Settings")
        newwin.geometry("260x50")
        newwin.resizable(False, False)

        entry = tk.Entry(newwin, width=12)
        entry.insert(0, self.keybind)
        entry.place(x=5, y=5)

        def apply_keybind():
            new_keybind = entry.get().upper()
            if new_keybind:
                try:
                    keyboard.remove_hotkey(self.keybind)
                    keyboard.add_hotkey(new_keybind, self.toggle)
                    self.keybind = new_keybind
                    self.status_label.config(text=f"Keybind updated to {self.keybind}", fg="black")
                    self.start_button.config(text="Start ({})".format(self.keybind))
                    self.stop_button.config(text="Stop ({})".format(self.keybind))
                    newwin.destroy()
                except Exception as e:
                    self.status_label.config(text=f"Error setting keybind, please reopen the app.", fg="red")
                    newwin.destroy()

        applyButton = tk.Button(newwin, text="Apply", width="5", pady="0", command=apply_keybind)
        applyButton.place(x=90, y=3)

    def openhelpwin(self):
        newwin = tk.Toplevel(self.master)
        newwin.title("About")
        newwin.geometry("230x100")
        newwin.resizable(False, False)

        def callback(url):
            webbrowser.open_new(url)

        labela = tk.Label(newwin, text="Auto Clicker v1.0.0", font=("Arial", 13))
        labela.pack()
        labelb = tk.Label(newwin, text="GitHub (agentn86)", cursor="hand2", fg="blue")
        labelb.pack()
        labelb.bind("<Button-1>", lambda e: callback('https://github.com/agentN86/autoclicker'))
        


if __name__ == "__main__":
    root = tk.Tk()
    autoclicker = AutoClicker(root)
    root.mainloop()