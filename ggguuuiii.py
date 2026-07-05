import tkinter as tk
import random

# ---------- Settings ----------
max_temperature = 25.0
min_temperature = 22.0

fan_on = False
ac_on = False
heater_on = False
windows_open=False

def read_temperature():
    """Pretend to read a sensor by picking a random temperature."""  
    return round(random.uniform(15, 35), 1)


def control_temperature(current_temperature):
    """Decide which devices should be ON or OFF."""
    global fan_on, ac_on, heater_on, windows_open

    if current_temperature > max_temperature:
        fan_on, ac_on, heater_on, windows_open = True, True, False, True
        message = "TOO HOT! AC turned ON, Fan turned ON and windows OPEN."
    elif current_temperature < min_temperature:
        fan_on, ac_on, heater_on , windows_open= False, False, True, False
        message = "TOO COLD! Heater turned ON."
    else:
        fan_on, ac_on, heater_on, windows_open = False, False, False
        message = "PERFECT TEMPERATURE! Everything OFF."

    return message


def update_display():
    """Read temp, decide on devices, then update all the labels on screen."""
    temperature = read_temperature()
    message = control_temperature(temperature)

    temp_label.config(text=f"Current Temperature: {temperature} °C")
    message_label.config(text=message)

    ac_label.config(text="AC: ON" if ac_on else "AC: OFF",
                     fg="green" if ac_on else "red")
    fan_label.config(text="Fan: ON" if fan_on else "Fan: OFF",
                      fg="green" if fan_on else "red")
    heater_label.config(text="Heater: ON" if heater_on else "Heater: OFF",
                         fg="green" if heater_on else "red")
    windows_label.config(text="Windows: OPEN" if windows_open else "windows: CLOSED",
                         fg="green" if windows_open else "red")
    
   # Run this same function again after 5000 milliseconds (5 seconds)
    window.after(5000, update_display)


# ---------- Build the window ----------
window = tk.Tk()
window.title("Smart Home Temperature Control")
window.geometry("450x400")

title_label = tk.Label(window, 
                       text="SMART HOME TEMP CONTROL",
                        font=("ROBOTO", 14, "bold"))
title_label.pack(pady=10)

range_label = tk.Label(window, text=f"Min: {min_temperature}°C   Max: {max_temperature}°C")
range_label.pack()

temp_label = tk.Label(window, text="Current Temperature: -- °C", font=("Arial", 12))
temp_label.pack(pady=10)

message_label = tk.Label(window, text="", font=("Arial", 12), wraplength=300)
message_label.pack(pady=5)

ac_label = tk.Label(window, text="AC: OFF", font=("Arial", 12))
ac_label.pack(pady=2)

fan_label = tk.Label(window, text="Fan: OFF", font=("Arial", 12))
fan_label.pack(pady=2)

heater_label = tk.Label(window, text="Heater: OFF", font=("Arial", 12))
heater_label.pack(pady=2)

windows_label = tk.Label(window, text="Windows: OPEN", font=("Arial", 12))
windows_label.pack(pady=2)

update_display()
window.mainloop()
