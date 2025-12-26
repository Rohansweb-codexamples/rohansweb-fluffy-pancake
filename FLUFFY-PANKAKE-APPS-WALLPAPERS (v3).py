import sys, os, ctypes, tkinter as tk
from tkinter import filedialog, messagebox, ttk
import winreg
from datetime import datetime

# Hide console window on Windows
if sys.platform == "win32":
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, 0)

# Windows constants
SPI_SETDESKWALLPAPER = 0x0014
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDWININICHANGE = 0x02

STYLE_MAP = {
    "Fill": ("10", "0"),
    "Fit": ("6", "0"),
    "Stretch": ("2", "0"),
    "Center": ("0", "0"),
    "Tile": ("0", "1"),
}

MAIN_FOLDER = r"C:\Users\Rohan\OneDrive\Apps\Walpapers app\Walpapers"
GLOW_FOLDER = os.path.join(MAIN_FOLDER, "glow")

def set_registry_style(style_name: str):
    style = STYLE_MAP.get(style_name, STYLE_MAP["Fill"])
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                        r"Control Panel\\Desktop", 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, style[0])
        winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, style[1])

def set_wallpaper(image_path: str, style_name: str):
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, image_path,
        SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
    )
    messagebox.showinfo("Success", "Wallpaper applied!")

class WallpaperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wallpaper Setter")
        self.geometry("750x550")
        self.resizable(False, False)

        self.selected_path = None
        self.selected_style = tk.StringVar(value="Fill")

        # Header
        header = tk.Frame(self, height=50, bg="#a020f0")
        header.pack(fill="x")
        tk.Label(header, text="Fluffy-Pancake Wallpaper App",
                 fg="white", bg="#a020f0",
                 font=("Segoe UI", 16, "bold")).pack(pady=5)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        wall_tab = tk.Frame(notebook, bg="#ffe6ff")
        settings_tab = tk.Frame(notebook, bg="#e6f7ff")
        about_tab = tk.Frame(notebook, bg="#e6ffe6")

        notebook.add(wall_tab, text="Wallpapers")
        notebook.add(settings_tab, text="Settings")
        notebook.add(about_tab, text="About")

        self.create_wallpapers_tab(wall_tab)
        self.create_settings_tab(settings_tab)
        self.create_about_tab(about_tab)

    # ---------------- WALLPAPERS TAB ----------------
    def create_wallpapers_tab(self, frm):
        tk.Button(frm, text="Upload your own",
                  bg="#ff66cc", fg="white",
                  activebackground="#ff33aa",
                  font=("Segoe UI", 11, "bold"),
                  command=self.browse_image)\
            .pack(anchor="w", pady=10, padx=10)

        tk.Label(frm, text="Preset Wallpapers:",
                 font=("Segoe UI", 12, "bold"),
                 bg="#ffe6ff")\
            .pack(anchor="w", padx=10)

        # Scrollable frame
        canvas = tk.Canvas(frm, bg="#ffe6ff", highlightthickness=0)
        scrollbar = tk.Scrollbar(frm, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#ffe6ff")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")

        self.list_frame = scroll_frame

        self.load_presets(scroll_frame, MAIN_FOLDER)
        self.load_presets(scroll_frame, GLOW_FOLDER)

        tk.Label(frm, text="Style:", font=("Segoe UI", 11, "bold"),
                 bg="#ffe6ff")\
            .pack(anchor="w", padx=10, pady=(10, 0))

        tk.OptionMenu(frm, self.selected_style, *STYLE_MAP.keys())\
            .pack(anchor="w", padx=10, pady=10)

        tk.Button(frm, text="Apply Wallpaper",
                  bg="#6633ff", fg="white",
                  activebackground="#4b26cc",
                  font=("Segoe UI", 13, "bold"),
                  height=2, width=20,
                  command=self.apply_wallpaper)\
            .pack(anchor="center", pady=20)

    # ---------------- SETTINGS TAB ----------------
    def create_settings_tab(self, frm):
        tk.Label(frm, text="Settings coming soon!",
                 font=("Segoe UI", 12, "bold"),
                 bg="#e6f7ff")\
            .pack(anchor="center", pady=20)

    # ---------------- ABOUT TAB ----------------
    def create_about_tab(self, frm):
        tk.Label(frm, text="Created by the Fluffy-Pancake Team",
                 font=("Segoe UI", 15, "bold"),
                 fg="#a020f0", bg="#e6ffe6")\
            .pack(pady=40)

        tk.Label(frm, text="Thanks for using our wallpaper app!",
                 font=("Segoe UI", 12), bg="#e6ffe6")\
            .pack()

        year = datetime.now().year
        tk.Label(frm, text=f"© {year} Fluffy-Pancake Team. All rights reserved.",
                 font=("Segoe UI", 9), fg="gray", bg="#e6ffe6")\
            .pack(side="bottom", pady=10)

    # ---------------- FILE PICKER ----------------
    def browse_image(self):
        path = filedialog.askopenfilename(
            title="Choose your image",
            filetypes=[("Image files", "*.bmp *.jpg *.jpeg *.png"), ("All files", "*.*")],
        )
        if path:
            self.selected_path = path

    # ---------------- LOAD PRESETS ----------------
    def load_presets(self, container, folder):
        if not os.path.isdir(folder):
            return

        files = [f for f in os.listdir(folder)
                 if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))]

        if not files:
            return

        tk.Label(container, text=f"Folder: {folder}",
                 font=("Segoe UI", 10, "italic"), bg="#ffe6ff")\
            .pack(anchor="w", pady=(5, 0))

        for fname in files:
            path = os.path.join(folder, fname)

            btn = tk.Button(container, text=fname,
                            bg="#ffccff", fg="black",
                            activebackground="#ff99ff",
                            font=("Segoe UI", 10, "bold"),
                            height=2,
                            command=lambda p=path: self.select_preset(p))

            btn.pack(anchor="w", pady=3)

    # ---------------- SELECT PRESET ----------------
    def select_preset(self, path):
        self.selected_path = path

    # ---------------- APPLY WALLPAPER ----------------
    def apply_wallpaper(self):
        if not self.selected_path:
            messagebox.showwarning("Missing file", "Please choose an image.")
            return

        set_wallpaper(self.selected_path, self.selected_style.get())

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app = WallpaperApp()
    app.mainloop()
