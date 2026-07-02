import tkinter as tk
from tkinter import messagebox

# CLASSES
class Light:
    def __init__(self, name):
        self.name = name
        self.status = False
        self.brightness = 50

    def toggle(self):
        self.status = not self.status

    def increase(self):
        if self.brightness < 100:
            self.brightness += 1

    def decrease(self):
        if self.brightness > 0:
            self.brightness -= 1


class TV:
    def __init__(self):
        self.status = False
        self.channel = 1
        self.volume = 50

    def toggle(self):
        self.status = not self.status

    def next_channel(self):
        if self.status:
            self.channel += 1

    def volume_up(self):
        if self.volume < 100:
            self.volume += 5

    def volume_down(self):
        if self.volume > 0:
            self.volume -= 5


class Speaker:
    def __init__(self):
        self.status = False
        self.volume = 50

    def toggle(self):
        self.status = not self.status

    def volume_up(self):
        if self.volume < 100:
            self.volume += 1

    def volume_down(self):
        if self.volume > 0:
            self.volume -= 1


# OBJECTS
rooms = ["Living Room", "Bedroom", "Kitchen"]
lights = {room: Light(room) for room in rooms}

tv = TV()
speaker = Speaker()

light_widgets = {}

# COLORS
ON_COLOR = "#2ecc71"
OFF_COLOR = "#e74c3c"
BAR_BG = "#dddddd"
BAR_FILL = "#0000ff"

LIGHT_BG = "white"
LIGHT_CARD = "#f5f5f5"
LIGHT_FG = "black"

DARK_BG = "#1a1a2e"
DARK_CARD = "#16213e"
DARK_FG = "white"

sleep_mode_active = False


# THEME FUNCTION
def apply_theme(dark):
    bg = DARK_BG if dark else LIGHT_BG
    card = DARK_CARD if dark else LIGHT_CARD
    fg = DARK_FG if dark else LIGHT_FG

    root.configure(bg=bg)
    title.config(bg=bg, fg=fg)

    for label in theme_labels:
        label.config(bg=bg, fg=fg)

    for frame in theme_frames:
        frame.config(bg=bg)

    for label in theme_detail_labels:
        label.config(bg=bg, fg=fg)

    for frame in room_frames:
        frame.config(bg=card)

    for label in room_labels:
        label.config(bg=card, fg=fg)

    for label in brightness_labels:
        label.config(bg=card, fg=fg)

    for btn_frame in room_btn_frames:
        btn_frame.config(bg=card)


# GUI UPDATE FUNCTIONS
def update_status():
    for room, light in lights.items():
        widgets = light_widgets[room]

        if light.status:
            widgets["status_label"].config(text="ON", bg=ON_COLOR, fg="white")
        else:
            widgets["status_label"].config(text="OFF", bg=OFF_COLOR, fg="white")

        bar_canvas = widgets["bar_canvas"]
        bar_canvas.delete("fill")
        bar_width = 150
        fill_width = int(bar_width * (light.brightness / 100))
        bar_canvas.create_rectangle(0, 0, fill_width, 20, fill=BAR_FILL, outline="", tags="fill")

        widgets["brightness_label"].config(text=f"{light.brightness}%")

    if tv.status:
        tv_status_label.config(text="TV: ON", bg=ON_COLOR, fg="white")
    else:
        tv_status_label.config(text="TV: OFF", bg=OFF_COLOR, fg="white")

    tv_details.config(text=f"Channel: {tv.channel}    Volume: {tv.volume}")

    if speaker.status:
        speaker_status_label.config(text="SPEAKER: ON", bg=ON_COLOR, fg="white")
    else:
        speaker_status_label.config(text="SPEAKER: OFF", bg=OFF_COLOR, fg="white")

    speaker_details.config(text=f"Volume: {speaker.volume}")


# Light Functions
def toggle_light(room):
    lights[room].toggle()
    update_status()

def brighter(room):
    lights[room].increase()
    update_status()

def dimmer(room):
    lights[room].decrease()
    update_status()


# TV Functions
def toggle_tv():
    tv.toggle()
    update_status()

def channel():
    tv.next_channel()
    update_status()

def tv_up():
    tv.volume_up()
    update_status()

def tv_down():
    tv.volume_down()
    update_status()


# Speaker Functions
def toggle_speaker():
    speaker.toggle()
    update_status()

def speaker_up():
    speaker.volume_up()
    update_status()

def speaker_down():
    speaker.volume_down()
    update_status()


# SCENES
def movie_mode():
    global sleep_mode_active
    sleep_mode_active = False
    apply_theme(dark=False)

    lights["Living Room"].status = True
    lights["Living Room"].brightness = 20
    lights["Bedroom"].status = False
    lights["Kitchen"].status = False

    tv.status = True
    speaker.status = True
    speaker.volume = 70

    update_status()
    messagebox.showinfo("Scene", "Movie Mode Activated!")

def party_mode():
    global sleep_mode_active
    sleep_mode_active = False
    apply_theme(dark=False)

    for light in lights.values():
        light.status = True
        light.brightness = 100

    speaker.status = True
    speaker.volume = 90
    tv.status = False

    update_status()
    messagebox.showinfo("Scene", "Party Mode Activated!")

def sleep_mode():
    global sleep_mode_active
    sleep_mode_active = True
    apply_theme(dark=True)

    for light in lights.values():
        light.status = True
        light.brightness = 10

    tv.status = False
    speaker.status = False

    update_status()
    messagebox.showinfo("Scene", "Sleep Mode Activated!")


# GUI
root = tk.Tk()
root.title("Smart Home - Lighting & Entertainment")
root.geometry("900x600")
root.configure(bg="white")

# Lists of widgets to re-theme
theme_labels = []
theme_frames = []
theme_detail_labels = []
room_frames = []
room_labels = []
brightness_labels = []
room_btn_frames = []

title = tk.Label(root, text="SMART HOME SYSTEM", font=("Arial", 20, "bold"), bg="white")
title.pack(pady=10)

# LIGHTING
lbl = tk.Label(root, text="Lighting", font=("Arial", 14, "bold"), bg="white")
lbl.pack(pady=(5, 0))
theme_labels.append(lbl)

lighting_frame = tk.Frame(root, bg="white")
lighting_frame.pack(pady=5)
theme_frames.append(lighting_frame)

for i, room in enumerate(rooms):
    room_frame = tk.Frame(lighting_frame, bg="#f5f5f5", bd=1, relief="solid")
    room_frame.grid(row=0, column=i, padx=10, pady=5, sticky="n")
    room_frames.append(room_frame)

    rlbl = tk.Label(room_frame, text=room, font=("Arial", 12, "bold"), bg="#f5f5f5")
    rlbl.pack(pady=(5, 2))
    room_labels.append(rlbl)

    status_label = tk.Label(room_frame, text="OFF", font=("Arial", 10, "bold"),
                            bg=OFF_COLOR, fg="white", width=10)
    status_label.pack(pady=2)

    bar_canvas = tk.Canvas(room_frame, width=150, height=20, bg=BAR_BG, highlightthickness=0)
    bar_canvas.pack(pady=2)

    brightness_label = tk.Label(room_frame, text="50%", font=("Arial", 9), bg="#f5f5f5")
    brightness_label.pack()
    brightness_labels.append(brightness_label)

    btn_frame = tk.Frame(room_frame, bg="#f5f5f5")
    btn_frame.pack(pady=5)
    room_btn_frames.append(btn_frame)

    tk.Button(btn_frame, text="ON/OFF", width=8,
              command=lambda r=room: toggle_light(r)).grid(row=0, column=0, columnspan=2, pady=2)
    tk.Button(btn_frame, text="−", width=3,
              command=lambda r=room: dimmer(r)).grid(row=1, column=0, padx=2)
    tk.Button(btn_frame, text="+", width=3,
              command=lambda r=room: brighter(r)).grid(row=1, column=1, padx=2)

    light_widgets[room] = {
        "status_label": status_label,
        "bar_canvas": bar_canvas,
        "brightness_label": brightness_label,
    }

# TV
lbl = tk.Label(root, text="TV", font=("Arial", 14, "bold"), bg="white")
lbl.pack(pady=(15, 0))
theme_labels.append(lbl)

tv_frame = tk.Frame(root, bg="white")
tv_frame.pack(pady=5)
theme_frames.append(tv_frame)

tv_status_label = tk.Label(tv_frame, text="TV: OFF", font=("Arial", 11, "bold"),
                           bg=OFF_COLOR, fg="white", width=14)
tv_status_label.grid(row=0, column=0, padx=5)

tv_details = tk.Label(tv_frame, text="Channel: 1    Volume: 50", bg="white")
tv_details.grid(row=0, column=1, padx=10)
theme_detail_labels.append(tv_details)

tv_btns = tk.Frame(root, bg="white")
tv_btns.pack(pady=2)
theme_frames.append(tv_btns)
tk.Button(tv_btns, text="TV ON/OFF", command=toggle_tv).grid(row=0, column=0, padx=3)
tk.Button(tv_btns, text="Next Channel", command=channel).grid(row=0, column=1, padx=3)
tk.Button(tv_btns, text="Volume -", command=tv_down).grid(row=0, column=2, padx=3)
tk.Button(tv_btns, text="Volume +", command=tv_up).grid(row=0, column=3, padx=3)

# SPEAKER
lbl = tk.Label(root, text="Speaker", font=("Arial", 14, "bold"), bg="white")
lbl.pack(pady=(15, 0))
theme_labels.append(lbl)

speaker_frame = tk.Frame(root, bg="white")
speaker_frame.pack(pady=5)
theme_frames.append(speaker_frame)

speaker_status_label = tk.Label(speaker_frame, text="SPEAKER: OFF", font=("Arial", 11, "bold"),
                                bg=OFF_COLOR, fg="white", width=14)
speaker_status_label.grid(row=0, column=0, padx=5)

speaker_details = tk.Label(speaker_frame, text="Volume: 50", bg="white")
speaker_details.grid(row=0, column=1, padx=10)
theme_detail_labels.append(speaker_details)

speaker_btns = tk.Frame(root, bg="white")
speaker_btns.pack(pady=2)
theme_frames.append(speaker_btns)
tk.Button(speaker_btns, text="Speaker ON/OFF", command=toggle_speaker).grid(row=0, column=0, padx=3)
tk.Button(speaker_btns, text="Volume -", command=speaker_down).grid(row=0, column=1, padx=3)
tk.Button(speaker_btns, text="Volume +", command=speaker_up).grid(row=0, column=2, padx=3)

# SCENES
lbl = tk.Label(root, text="Scenes", font=("Arial", 14, "bold"), bg="white")
lbl.pack(pady=(15, 5))
theme_labels.append(lbl)

scene_frame = tk.Frame(root, bg="white")
scene_frame.pack(pady=2)
theme_frames.append(scene_frame)

tk.Button(scene_frame, text="Movie Mode", command=movie_mode).grid(row=0, column=0, padx=5)
tk.Button(scene_frame, text="Party Mode", command=party_mode).grid(row=0, column=1, padx=5)
tk.Button(scene_frame, text="Sleep Mode", command=sleep_mode).grid(row=0, column=2, padx=5)

update_status()

root.mainloop()
