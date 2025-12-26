# --- HIDE CONSOLE WINDOW ON WINDOWS ---
import sys
if sys.platform == "win32":
    import ctypes
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, 0)  # 0 = SW_HIDE
# --------------------------------------

import os
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox

# Windows constants for SystemParametersInfo
SPI_SETDESKWALLPAPER = 0x0014
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDWININICHANGE = 0x02

# Registry paths/keys for wallpaper style
import winreg

STYLE_MAP = {
    # UI label: (WallpaperStyle, TileWallpaper)
    "Fill": ("10", "0"),
    "Fit": ("6", "0"),
    "Stretch": ("2", "0"),
    "Center": ("0", "0"),
    "Tile": ("0", "1"),
}

def set_registry_style(style_name: str):
    """Set style via registry under HKCU\Control Panel\Desktop."""
    style = STYLE_MAP.get(style_name, STYLE_MAP["Fill"])
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, style[0])
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, style[1])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to set style registry values:\n{e}")

def set_wallpaper(image_path: str, style_name: str):
    """Set the Windows wallpaper using SystemParametersInfoW."""
    if not os.path.isfile(image_path):
        messagebox.showerror("Error", "Selected file does not exist.")
        return

    # Update style first
    set_registry_style(style_name)

    # Call SystemParametersInfoW
    try:
        result = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            image_path,
            SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
        )
        if not result:
            raise ctypes.WinError()
        messagebox.showinfo("Success", "Wallpaper updated.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to set wallpaper:\n{e}")

class WallpaperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wallpaper Setter")
        self.geometry("420x200")
        self.resizable(False, False)

        # State
        self.selected_path = tk.StringVar(value="")
        self.selected_style = tk.StringVar(value="Fill")

        # UI
        self.create_widgets()

    def create_widgets(self):
        # File selection
        frm = tk.Frame(self, padx=14, pady=12)
        frm.pack(fill="both", expand=True)

        tk.Label(frm, text="Image file:").grid(row=0, column=0, sticky="w")
        entry = tk.Entry(frm, textvariable=self.selected_path, width=38)
        entry.grid(row=1, column=0, sticky="we", padx=(0, 8))
        btn_browse = tk.Button(frm, text="Browse...", command=self.browse_image)
        btn_browse.grid(row=1, column=1, sticky="e")

        # Style selection
        tk.Label(frm, text="Style:").grid(row=2, column=0, sticky="w", pady=(10, 0))
        style_menu = tk.OptionMenu(frm, self.selected_style, *STYLE_MAP.keys())
        style_menu.config(width=12)
        style_menu.grid(row=3, column=0, sticky="w")

        # Apply button
        btn_apply = tk.Button(frm, text="Set Wallpaper", command=self.apply)
        btn_apply.grid(row=4, column=0, sticky="w", pady=(16, 0))

        # Tips
        tip = tk.Label(frm, fg="#666", text="Supported formats: BMP, JPG, PNG (Windows converts internally).")
        tip.grid(row=5, column=0, sticky="w", pady=(8, 0))

        frm.columnconfigure(0, weight=1)

    def browse_image(self):
        path = filedialog.askopenfilename(
            title="Choose wallpaper image",
            filetypes=[
                ("Image files", "*.bmp *.jpg *.jpeg *.png"),
                ("All files", "*.*"),
            ],
        )
        if path:
            self.selected_path.set(path)

    def apply(self):
        path = self.selected_path.get().strip()
        style = self.selected_style.get()
        if not path:
            messagebox.showwarning("Missing file", "Please choose an image.")
            return
        set_wallpaper(path, style)

if __name__ == "__main__":
    # Start the GUI
    app = WallpaperApp()
    app.mainloop()
