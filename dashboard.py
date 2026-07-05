import tkinter as tk
import subprocess
def open_temperature():
    subprocess.Popen(["python", "temperature.py"])
def open_security():
    subprocess.Popen(["python", "security.py"])
def open_lighting():
    subprocess.Popen(["python", "lighting.py"])
def open_energy():
    subprocess.Popen(["python", "energy_monitoring.py"])
root = tk.Tk()
root.title("Smart Home Dashboard")
root.geometry("700x500")
root.configure(bg="darkblue")
root.resizable(False, False)
title = tk.Label(
    root,
    text="SMART HOME CONTROL DASHBOARD",
    bg="darkblue",
    fg="white",
    font=("Arial", 20, "bold")
)
title.pack(pady=25)
subtitle = tk.Label(
    root,
    text="Select a Smart Home Module",
    bg="darkblue",
    fg="white",
    font=("Arial", 12)
)
subtitle.pack(pady=5)
button_colour = "lightblue"
button_width = 28
button_height = 2
temperature_button = tk.Button(
    root,
    text="🌡 Temperature & Climate",
    bg=button_colour,
    fg="white",
    font=("Arial", 12, "bold"),
    width=button_width,
    height=button_height,
    command=open_temperature
)
temperature_button.pack(pady=10)
security_button = tk.Button(
    root,
    text="🔒 Security & Access",
    bg=button_colour,
    fg="white",
    font=("Arial", 12, "bold"),
    width=button_width,
    height=button_height,
    command=open_security
)
security_button.pack(pady=10)
lighting_button = tk.Button(
    root,
    text="💡 Lighting & Entertainment",
    bg=button_colour,
    fg="white",
    font=("Arial", 12, "bold"),
    width=button_width,
    height=button_height,
    command=open_lighting
)
lighting_button.pack(pady=10)
energy_button = tk.Button(
    root,
    text="⚡ Energy Monitoring",
    bg=button_colour,
    fg="white",
    font=("Arial", 12, "bold"),
    width=button_width,
    height=button_height,
    command=open_energy
)
energy_button.pack(pady=10)
exit_button = tk.Button(
    root,
    text="Exit Dashboard",
    bg="red",
    fg="white",
    font=("Arial", 12, "bold"),
    width=20,
    command=root.destroy
)
exit_button.pack(pady=30)
root.mainloop()