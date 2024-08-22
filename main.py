import os
import win32gui
import win32ui
import win32con
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Label, Frame, Checkbutton, BooleanVar, simpledialog, Toplevel, Button
import numpy as np

# Global blacklist variable
blacklist = set()


def load_blacklist():
    global blacklist
    blacklist.clear()
    if os.path.exists("blacklist.txt"):
        with open("blacklist.txt", "r") as file:
            for line in file:
                blacklist.add(line.strip())


def save_blacklist():
    global blacklist
    with open("blacklist.txt", "w") as file:
        for item in blacklist:
            file.write(f"{item}\n")


def get_window_screenshot(hwnd):
    try:
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bot - top

        hwindc = win32gui.GetWindowDC(hwnd)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()

        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)

        memdc.BitBlt((0, 0), (width, height), srcdc, (0, 0), win32con.SRCCOPY)

        bmpinfo = bmp.GetInfo()
        bmpstr = bmp.GetBitmapBits(True)
        img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.ReleaseDC(hwnd, hwindc)
        memdc.DeleteDC()
        win32gui.DeleteObject(bmp.GetHandle())

        img_np = np.array(img)
        if not np.any(img_np):  # Check if the image is completely black
            return None

        return img
    except win32gui.error as e:
        print(f"Error capturing window: {e}")
        return None


def update_blacklist_periodically(root, frames, refresh_rate):
    global blacklist
    load_blacklist()
    # Update displayed thumbnails
    for hwnd, frame in list(frames.items()):
        window_text = win32gui.GetWindowText(hwnd)
        if window_text in blacklist:
            frame.destroy()
            del frames[hwnd]
    root.after(5000, update_blacklist_periodically, root, frames, refresh_rate)


def update_thumbnails(root, frames, refresh_rate):
    global blacklist
    for hwnd, frame in list(frames.items()):
        img = get_window_screenshot(hwnd)
        if img is not None:
            img.thumbnail((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            thumbnail_label = frame.winfo_children()[0]
            thumbnail_label.config(image=img_tk)
            thumbnail_label.image = img_tk
        else:
            frame.destroy()  # Remove the frame if the window is no longer valid
            del frames[hwnd]

    root.after(refresh_rate, update_thumbnails, root, frames, refresh_rate)


def create_monitoring_window(refresh_rate):
    global blacklist
    root = tk.Tk()
    root.title("Application Thumbnails")

    frames = {}

    def clear_frames():
        for frame in frames.values():
            frame.destroy()
        frames.clear()

    def enum_window_callback(hwnd, extra):
        window_text = win32gui.GetWindowText(hwnd)
        if win32gui.IsWindowVisible(hwnd) and window_text != "" and window_text not in blacklist:
            frame = Frame(root)
            frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)

            # Thumbnail
            thumbnail_label = Label(frame)
            thumbnail_label.pack(side="left")

            # Window name
            name_label = Label(frame, text=window_text, font=("Arial", 8))
            name_label.pack(side="left")

            def on_thumbnail_click(event, hwnd=hwnd):
                win32gui.SetForegroundWindow(hwnd)

            thumbnail_label.bind("<Button-1>", on_thumbnail_click)

            # Checkbox for blacklisting
            var = BooleanVar(value=True)

            def on_checkbox_toggle(var=var, window_text=window_text):
                global blacklist
                if not var.get():
                    blacklist.add(window_text)
                    save_blacklist()
                    frame.destroy()
                    del frames[hwnd]

            checkbox = Checkbutton(frame, variable=var, command=on_checkbox_toggle)
            checkbox.pack(side="left")

            frames[hwnd] = frame

    def manage_blacklist():
        global blacklist
        blacklist_window = Toplevel(root)
        blacklist_window.title("Blacklist Management")
        blacklist_window.geometry("300x400")

        def on_close():
            blacklist_window.destroy()
            clear_frames()
            win32gui.EnumWindows(enum_window_callback, None)

        for item in list(blacklist):
            var = BooleanVar(value=True)

            def on_blacklist_toggle(item=item, var=var):
                global blacklist
                if not var.get():
                    blacklist.remove(item)
                    save_blacklist()
                    blacklist_window.destroy()
                    manage_blacklist()  # Refresh the blacklist management window

            frame = Frame(blacklist_window)
            frame.pack(fill="both", expand=True, padx=5, pady=5)

            name_label = Label(frame, text=item, font=("Arial", 8))
            name_label.pack(side="left")

            checkbox = Checkbutton(frame, variable=var, command=on_blacklist_toggle)
            checkbox.pack(side="right")

        blacklist_window.protocol("WM_DELETE_WINDOW", on_close)

    Button(root, text="Blacklist Management", command=manage_blacklist).pack(side="bottom", pady=10)

    win32gui.EnumWindows(enum_window_callback, None)
    update_thumbnails(root, frames, refresh_rate)
    update_blacklist_periodically(root, frames, refresh_rate)

    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window while getting user input

    refresh_rate = simpledialog.askinteger(
        "Refresh Rate",
        "Enter refresh rate in ms:",
        minvalue=1,
        maxvalue=10000,
        initialvalue=100
    )
    root.destroy()  # Destroy the input dialog root window

    if refresh_rate is not None:
        load_blacklist()  # Load blacklist from file
        create_monitoring_window(refresh_rate)
