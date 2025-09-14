from pynput import keyboard
import tkinter as tk
from collections import deque

root = tk.Tk()
root.title("Key Overlay")
root.geometry("1250x30+50+550")
root.configure(bg="black")
root.attributes("-topmost", True)

text_var = tk.StringVar(value="Press keys...")
label = tk.Label(
    root,
    textvariable=text_var,
    font=("Arial", 18),
    fg="white",
    bg="black",
    anchor="w",
    justify="left"
)
label.pack(fill="both", expand=True, padx=5)

last_keys = deque()
pressed = set()

emoji_map = {
    "space": "␣",
    "shift": "⬆️",
    "enter": "↩️",
    "tab": "⇥",
    "backspace": "⌫",
    "ctrl_l": "⌃",
    "ctrl_r": "⌃",
    "alt_l": "⎇",
    "alt_r": "⎇",
}

def normalize_key(key):
    if isinstance(key, keyboard.KeyCode) and key.char:
        return key.char
    name = str(key).replace("Key.", "")
    return emoji_map.get(name.lower(), name)

def trim_to_fit():
    while last_keys:
        text_var.set(" ".join(last_keys))
        root.update_idletasks()
        if label.winfo_reqwidth() <= label.winfo_width():
            break
        last_keys.popleft()

def on_press(key):
    if key in pressed:
        return
    pressed.add(key)
    last_keys.append(normalize_key(key))
    trim_to_fit()

def on_release(key):
    pressed.discard(key)

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

root.mainloop()
