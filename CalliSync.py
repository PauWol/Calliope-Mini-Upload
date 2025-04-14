import os
import time
import shutil
import sys
import json
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog

# -----------------------------
# RESOURCE PATH HELPER
# -----------------------------
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and when bundled by PyInstaller."""
    try:
        # PyInstaller stores bundled files in a temporary folder referenced by _MEIPASS.
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# -----------------------------
# CONFIGURATION
# -----------------------------
CONFIG_FILE = 'config.json'

def load_config():
    default_watch_folder = os.path.join(os.environ.get("USERPROFILE", ""), "Downloads", "calliope-upload")
    default_config = {
        "watch_folder": default_watch_folder,
        "caliope_drive": "E:\\",
        "check_interval": 2  # in seconds
    }
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_config, f, indent=4)
        return default_config
    else:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

config = load_config()

# -----------------------------
# HEX FILE HANDLING
# -----------------------------
def find_hex_file(folder):
    for file in os.listdir(folder):
        if file.lower().endswith(".hex"):
            return os.path.join(folder, file)
    return None

def move_hex_to_caliope(hex_path, target_drive, log_func):
    filename = os.path.basename(hex_path)
    destination = os.path.join(target_drive, filename)
    try:
        log_func("Moving " + filename + " to Calliope Mini...")
        shutil.move(hex_path, destination)
        log_func("✅ Done!")
    except Exception as e:
        log_func("❌ Error moving file: " + str(e))

# -----------------------------
# WATCH SERVICE (in a separate thread)
# -----------------------------
stop_event = threading.Event()

def watch_loop(log_func):
    watch_folder = config["watch_folder"]
    caliope_drive = config["caliope_drive"]
    check_interval = config["check_interval"]
    
    log_func("Watching for .hex files in " + watch_folder + "...")
    while not stop_event.is_set():
        hex_file = find_hex_file(watch_folder)
        if hex_file:
            move_hex_to_caliope(hex_file, caliope_drive, log_func)
        time.sleep(check_interval)

# -----------------------------
# SIMPLE TKINTER UI WITH SETTINGS
# -----------------------------
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("CalliSync")
        self.geometry("800x600")

        # Set icon using resource_path so it works when bundled.
        icon_path = resource_path("calliope.ico")
        self.iconbitmap(icon_path)

        self.log_area = ScrolledText(self, state="disabled", wrap="word")
        self.log_area.pack(expand=True, fill="both")
        
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="bottom", fill="x")
        self.start_button = tk.Button(self.button_frame, text="Start Service", command=self.start_service)
        self.start_button.pack(side="left", padx=5, pady=5)
        self.stop_button = tk.Button(self.button_frame, text="Stop Service", command=self.stop_service, state="disabled")
        self.stop_button.pack(side="left", padx=5, pady=5)
        self.settings_button = tk.Button(self.button_frame, text="Settings", command=self.open_settings)
        self.settings_button.pack(side="left", padx=5, pady=5)
        
        self.service_thread = None
        
    def log(self, message):
        self.log_area.config(state="normal")
        self.log_area.insert("end", message + "\n")
        self.log_area.see("end")
        self.log_area.config(state="disabled")
        
    def start_service(self):
        global stop_event
        stop_event.clear()
        self.service_thread = threading.Thread(target=watch_loop, args=(self.log,))
        self.service_thread.daemon = True  # Thread exits when main program exits.
        self.service_thread.start()
        self.log("Service started.")
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
    def stop_service(self):
        global stop_event
        stop_event.set()
        self.log("Service stopping...")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
    
    def open_settings(self):
        SettingsWindow(self)

class SettingsWindow(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.title("Settings")
        self.geometry("400x300")
        self.master = master

        tk.Label(self, text="Watch Folder:").pack(anchor="w", padx=10, pady=(10, 0))
        self.watch_folder_var = tk.StringVar(value=config.get("watch_folder", ""))
        self.watch_folder_entry = tk.Entry(self, textvariable=self.watch_folder_var, width=50)
        self.watch_folder_entry.pack(anchor="w", padx=10)
        tk.Button(self, text="Browse", command=self.browse_folder).pack(anchor="w", padx=10, pady=5)
        
        tk.Label(self, text="Calliope Drive:").pack(anchor="w", padx=10, pady=(10, 0))
        self.drive_var = tk.StringVar(value=config.get("caliope_drive", ""))
        self.drive_entry = tk.Entry(self, textvariable=self.drive_var, width=20)
        self.drive_entry.pack(anchor="w", padx=10)
        
        tk.Label(self, text="Check Interval (seconds):").pack(anchor="w", padx=10, pady=(10, 0))
        self.interval_var = tk.StringVar(value=str(config.get("check_interval", 2)))
        self.interval_entry = tk.Entry(self, textvariable=self.interval_var, width=10)
        self.interval_entry.pack(anchor="w", padx=10)
        
        tk.Button(self, text="Save Settings", command=self.save_settings).pack(pady=20)
    
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.watch_folder_var.get())
        if folder:
            self.watch_folder_var.set(folder)
    
    def save_settings(self):
        global config
        config["watch_folder"] = self.watch_folder_var.get()
        config["caliope_drive"] = self.drive_var.get()
        try:
            config["check_interval"] = int(self.interval_var.get())
        except ValueError:
            config["check_interval"] = 2  # fallback
        save_config(config)
        self.master.log("Settings updated.")
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
