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

# Will hold references to each room's widgets so we can update them
light_widgets = {}

# COLORS
ON_COLOR = "#2ecc71"   # green
OFF_COLOR = "#e74c3c"  # red
BAR_BG = "#dddddd"
BAR_FILL = "#0000ff"   # yellow/amber for brightness

# GUI UPDATE FUNCTIONS
def update_status():
    # --- Update each light/room ---
    for room, light in lights.items():
        widgets = light_widgets[room]

        if light.status:
            widgets["status_label"].config(text="ON", bg=ON_COLOR, fg="white")
        else:
            widgets["status_label"].config(text="OFF", bg=OFF_COLOR, fg="white")

        # Update brightness bar width based on percentage
        bar_canvas = widgets["bar_canvas"]
        bar_canvas.delete("fill")
        bar_width = 150  # total bar width in pixels
        fill_width = int(bar_width * (light.brightness / 100))
        bar_canvas.create_rectangle(
            0, 0, fill_width, 20,
            fill=BAR_FILL, outline="", tags="fill"
        )

        widgets["brightness_label"].config(text=f"{light.brightness}%")

    # --- Update TV ---
    if tv.status:
        tv_status_label.config(text="TV: ON", bg=ON_COLOR, fg="white")
    else:
        tv_status_label.config(text="TV: OFF", bg=OFF_COLOR, fg="white")

    tv_details.config(text=f"Channel: {tv.channel}    Volume: {tv.volume}")

    # --- Update Speaker ---
    if speaker.status:
        speaker_status_label.config(text="SPEAKER: ON", bg=ON_COLOR, fg="white")
    else:
        speaker_status_label.config(text="SPEAKER: OFF", bg=OFF_COLOR, fg="white")

    speaker_details.config(text=f"Volume: {speaker.volume}")


# Light Functions (now take a room name)

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
    for light in lights.values():
        light.status = True
        light.brightness = 100

    speaker.status = True
    speaker.volume = 90
    tv.status = False

    update_status()
    messagebox.showinfo("Scene", "Party Mode Activated!")

def sleep_mode():
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

title = tk.Label(
    root,
    text="SMART HOME SYSTEM",
    font=("Arial", 20, "bold"),
    bg="white"
)
title.pack(pady=10)


# LIGHTING SECTION (one block per room)
tk.Label(root, text="Lighting", font=("Arial", 14, "bold"), bg="white").pack(pady=(5, 0))

lighting_frame = tk.Frame(root, bg="white")
lighting_frame.pack(pady=5)

for i, room in enumerate(rooms):
    room_frame = tk.Frame(lighting_frame, bg="#f5f5f5", bd=1, relief="solid")
    room_frame.grid(row=0, column=i, padx=10, pady=5, sticky="n")

    tk.Label(room_frame, text=room, font=("Arial", 12, "bold"), bg="#f5f5f5").pack(pady=(5, 2))

    status_label = tk.Label(
        room_frame, text="OFF", font=("Arial", 10, "bold"),
        bg=OFF_COLOR, fg="white", width=10
    )
    status_label.pack(pady=2)

    # Brightness bar (Canvas as a simple progress bar)
    bar_canvas = tk.Canvas(room_frame, width=150, height=20, bg=BAR_BG, highlightthickness=0)
    bar_canvas.pack(pady=2)

    brightness_label = tk.Label(room_frame, text="50%", font=("Arial", 9), bg="#f5f5f5")
    brightness_label.pack()

    btn_frame = tk.Frame(room_frame, bg="#f5f5f5")
    btn_frame.pack(pady=5)

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


# TV SECTION
tk.Label(root, text="TV", font=("Arial", 14, "bold"), bg="white").pack(pady=(15, 0))

tv_frame = tk.Frame(root, bg="white")
tv_frame.pack(pady=5)

tv_status_label = tk.Label(
    tv_frame, text="TV: OFF", font=("Arial", 11, "bold"),
    bg=OFF_COLOR, fg="white", width=14
)
tv_status_label.grid(row=0, column=0, padx=5)

tv_details = tk.Label(tv_frame, text="Channel: 1    Volume: 50", bg="white")
tv_details.grid(row=0, column=1, padx=10)

tv_btns = tk.Frame(root, bg="white")
tv_btns.pack(pady=2)
tk.Button(tv_btns, text="TV ON/OFF", command=toggle_tv).grid(row=0, column=0, padx=3)
tk.Button(tv_btns, text="Next Channel", command=channel).grid(row=0, column=1, padx=3)
tk.Button(tv_btns, text="Volume -", command=tv_down).grid(row=0, column=2, padx=3)
tk.Button(tv_btns, text="Volume +", command=tv_up).grid(row=0, column=3, padx=3)


# SPEAKER SECTION
tk.Label(root, text="Speaker", font=("Arial", 14, "bold"), bg="white").pack(pady=(15, 0))

speaker_frame = tk.Frame(root, bg="white")
speaker_frame.pack(pady=5)

speaker_status_label = tk.Label(
    speaker_frame, text="SPEAKER: OFF", font=("Arial", 11, "bold"),
    bg=OFF_COLOR, fg="white", width=14
)
speaker_status_label.grid(row=0, column=0, padx=5)

speaker_details = tk.Label(speaker_frame, text="Volume: 50", bg="white")
speaker_details.grid(row=0, column=1, padx=10)

speaker_btns = tk.Frame(root, bg="white")
speaker_btns.pack(pady=2)
tk.Button(speaker_btns, text="Speaker ON/OFF", command=toggle_speaker).grid(row=0, column=0, padx=3)
tk.Button(speaker_btns, text="Volume -", command=speaker_down).grid(row=0, column=1, padx=3)
tk.Button(speaker_btns, text="Volume +", command=speaker_up).grid(row=0, column=2, padx=3)


# SCENE BUTTONS
tk.Label(root, text="Scenes", font=("Arial", 14, "bold"), bg="white").pack(pady=(15, 5))

scene_frame = tk.Frame(root, bg="white")
scene_frame.pack(pady=2)

tk.Button(scene_frame, text="Movie Mode", command=movie_mode).grid(row=0, column=0, padx=5)
tk.Button(scene_frame, text="Party Mode", command=party_mode).grid(row=0, column=1, padx=5)
tk.Button(scene_frame, text="Sleep Mode", command=sleep_mode).grid(row=0, column=2, padx=5)

update_status()

root.mainloop()
