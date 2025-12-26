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
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\\Desktop", 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, style[0])
        winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, style[1])

def set_wallpaper(image_path: str, style_name: str):
    if not os.path.isfile(image_path):
        messagebox.showerror("File Error", "Selected file does not exist.")
        return
    set_registry_style(style_name)
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, image_path,
        SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
    )
    messagebox.showinfo("Success", f"Wallpaper set:\n{os.path.basename(image_path)}")

class WallpaperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wallpaper Setter")
        self.geometry("700x500")
        self.resizable(False, False)

        self.selected_path = tk.StringVar(value="")
        self.selected_style = tk.StringVar(value="Fill")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        wall_tab = tk.Frame(notebook)
        settings_tab = tk.Frame(notebook)
        about_tab = tk.Frame(notebook)

        notebook.add(wall_tab, text="Wallpapers")
        notebook.add(settings_tab, text="Settings")
        notebook.add(about_tab, text="About")

        self.create_wallpapers_tab(wall_tab)
        self.create_settings_tab(settings_tab)
        self.create_about_tab(about_tab)

    def create_wallpapers_tab(self, frm):
        tk.Button(frm, text="Upload your own", command=self.browse_image).pack(anchor="w", pady=10, padx=10)
        tk.Label(frm, text="Preset Wallpapers:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10)
        list_frame = tk.Frame(frm)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.load_presets(list_frame, MAIN_FOLDER)
        self.load_presets(list_frame, GLOW_FOLDER)

        tk.Label(frm, text="Style:", font=("Segoe UI", 10)).pack(anchor="w", padx=10, pady=(10, 0))
        tk.OptionMenu(frm, self.selected_style, *STYLE_MAP.keys()).pack(anchor="w", padx=10, pady=10)

        tk.Button(frm, text="Apply Selected Wallpaper", command=self.apply_wallpaper).pack(anchor="w", padx=10, pady=20)

    def create_settings_tab(self, frm):
        tk.Label(frm, text="Choose wallpaper style from dropdown in Wallpapers tab.", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=10)

    def create_about_tab(self, frm):
        tk.Label(frm, text="Created by the Fluffy-Pancake Team", font=("Segoe UI", 12, "bold"), fg="purple").pack(pady=40)
        tk.Label(frm, text="Thanks for using our wallpaper app!", font=("Segoe UI", 10)).pack()
        year = datetime.now().year
        tk.Label(frm, text=f"© {year} Fluffy-Pancake Team. All rights reserved.", font=("Segoe UI", 8), fg="gray").pack(side="bottom", pady=10)

    def browse_image(self):
        path = filedialog.askopenfilename(
            title="Choose your image",
            filetypes=[("Image files", "*.bmp *.jpg *.jpeg *.png"), ("All files", "*.*")],
        )
        if path:
            self.selected_path.set(path)

    def load_presets(self, container, folder):
        if not os.path.isdir(folder):
            return
        files = [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))]
        if not files:
            return
        tk.Label(container, text=f"Folder: {folder}", font=("Segoe UI", 9, "italic")).pack(anchor="w", pady=(5, 0))
        for fname in files:
            path = os.path.join(folder, fname)
            tk.Button(container, text=fname, command=lambda p=path: self.selected_path.set(p)).pack(anchor="w", pady=2)

    def apply_wallpaper(self):
        path = self.selected_path.get().strip()
        style = self.selected_style.get()
        if not path:
            messagebox.showwarning("Missing file", "Please choose an image.")
            return
        set_wallpaper(path, style)

if __name__ == "__main__":
    app = WallpaperApp()
    app.mainloop()
