import tkinter as tk
import random

# ---------- Settings ----------
max_temperature = 25.0
min_temperature = 20.0

fan_on = False
ac_on = False
heater_on = False


def read_temperature():
    """Pretend to read a sensor by picking a random temperature."""  
    return round(random.uniform(15, 35), 1)


def control_temperature(current_temperature):
    """Decide which devices should be ON or OFF."""
    global fan_on, ac_on, heater_on

    if current_temperature > max_temperature:
        fan_on, ac_on, heater_on = True, True, False
        message = "TOO HOT! AC and Fan turned ON."
    elif current_temperature < min_temperature:
        fan_on, ac_on, heater_on = False, False, True
        message = "TOO COLD! Heater turned ON."
    else:
        fan_on, ac_on, heater_on = False, False, False
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

    # Run this same function again after 3000 milliseconds (3 seconds)
    window.after(3000, update_display)


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

message_label = tk.Label(window, text="", font=("Arial", 11), wraplength=300)
message_label.pack(pady=5)

ac_label = tk.Label(window, text="AC: OFF", font=("Arial", 11))
ac_label.pack(pady=2)

fan_label = tk.Label(window, text="Fan: OFF", font=("Arial", 11))
fan_label.pack(pady=2)

heater_label = tk.Label(window, text="Heater: OFF", font=("Arial", 11))
heater_label.pack(pady=2)

# Start the automatic updates, then start the GUI loop
update_display()
window.mainloop()