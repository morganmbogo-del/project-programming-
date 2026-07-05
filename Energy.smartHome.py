import tkinter as tk
import random

# -------------------------
# APPLIANCE BASE CONFIG
# -------------------------

appliances = [
    {"name": "Light",      "icon": "💡", "base_power": 12,   "variance": 2,   "always_on": True},
    {"name": "Television", "icon": "📺", "base_power": 120,  "variance": 15,  "always_on": True},
    {"name": "Speaker",    "icon": "🔊", "base_power": 35,   "variance": 20,  "always_on": False},
    {"name": "Thermostat", "icon": "🌡️", "base_power": 1500, "variance": 300, "always_on": False},
]

# Runtime state per appliance
state = {}
for a in appliances:
    state[a["name"]] = {
        "power": a["base_power"],
        "status": a["always_on"],
        "energy_kwh": 0.0,
        "units": 0.0,
    }

# -------------------------
# COLORS
# -------------------------

BG          = "#0d1117"
CARD_BG     = "#161b22"
CARD_BORDER = "#30363d"
ACCENT      = "#58a6ff"
GREEN       = "#3fb950"
ORANGE      = "#d29922"
RED         = "#f85149"
MUTED       = "#8b949e"
WHITE       = "#e6edf3"

UPDATE_MS   = 1500   # how often to refresh (ms)
TICK_HOURS  = UPDATE_MS / 1000 / 3600  # fraction of an hour per tick

# -------------------------
# WIDGET REFS
# -------------------------

card_widgets = {}   # name -> dict of label vars

# -------------------------
# SIMULATION LOGIC
# -------------------------

def get_bar(fraction, width=18):
    filled = int(fraction * width)
    filled = max(0, min(width, filled))
    return "█" * filled + "░" * (width - filled)

def tick():
    total_power  = 0
    total_energy = 0
    total_units  = 0

    for a in appliances:
        name = a["name"]
        s = state[name]

        # Randomly flip off/on appliances that aren't always-on
        if not a["always_on"]:
            if s["status"]:
                if random.random() < 0.08:   # 8% chance to turn off
                    s["status"] = False
            else:
                if random.random() < 0.12:   # 12% chance to turn on
                    s["status"] = True

        if s["status"]:
            # Fluctuate power realistically
            noise = random.uniform(-a["variance"], a["variance"])
            s["power"] = max(1, a["base_power"] + noise)
            s["energy_kwh"] += (s["power"] / 1000) * TICK_HOURS
            s["units"] = s["energy_kwh"]
        else:
            s["power"] = 0

        total_power  += s["power"]
        total_energy += s["energy_kwh"]
        total_units  += s["units"]

        # Update card
        w = card_widgets[name]
        on = s["status"]

        status_txt = "● ON " if on else "○ OFF"
        status_col = GREEN if on else RED
        w["status"].config(text=status_txt, fg=status_col)

        w["power"].config(text=f"{s['power']:>7.1f} W")

        bar_frac = s["power"] / (a["base_power"] + a["variance"] * 2 + 1)
        bar_col  = GREEN if bar_frac < 0.5 else (ORANGE if bar_frac < 0.8 else RED)
        w["bar"].config(text=get_bar(bar_frac), fg=bar_col)

        w["energy"].config(text=f"{s['energy_kwh']:.4f} kWh")
        w["units"].config(text=f"{s['units']:.4f} units")

    # Update totals
    total_bar_frac = min(total_power / 2000, 1.0)
    total_bar_col  = GREEN if total_bar_frac < 0.4 else (ORANGE if total_bar_frac < 0.75 else RED)

    lbl_total_power.config(text=f"{total_power:.1f} W")
    lbl_total_bar.config(text=get_bar(total_bar_frac, 30), fg=total_bar_col)
    lbl_total_energy.config(text=f"{total_energy:.4f} kWh")
    lbl_total_units.config(text=f"{total_units:.4f} units")

    root.after(UPDATE_MS, tick)


# -------------------------
# GUI
# -------------------------

root = tk.Tk()
root.title("Smart Home — Live Energy Dashboard")
root.configure(bg=BG)
root.geometry("700x600")
root.resizable(True, True)

# --- Title bar ---
title_bar = tk.Frame(root, bg="#010409", pady=12)
title_bar.pack(fill="x")
tk.Label(title_bar, text="⚡  SMART HOME  —  LIVE ENERGY DASHBOARD",
         font=("Courier", 14, "bold"), bg="#010409", fg=ACCENT).pack()
tk.Label(title_bar, text="Simulated real-time power consumption",
         font=("Courier", 9), bg="#010409", fg=MUTED).pack()

# --- Appliance cards ---
cards_frame = tk.Frame(root, bg=BG)
cards_frame.pack(fill="both", expand=True, padx=16, pady=12)

for i, a in enumerate(appliances):
    name = a["name"]

    card = tk.Frame(cards_frame, bg=CARD_BG, highlightbackground=CARD_BORDER,
                    highlightthickness=1)
    card.grid(row=i//2, column=i%2, padx=8, pady=8, sticky="nsew")
    cards_frame.columnconfigure(i%2, weight=1)
    cards_frame.rowconfigure(i//2, weight=1)

    # Card header
    hdr = tk.Frame(card, bg=CARD_BG, padx=12, pady=8)
    hdr.pack(fill="x")

    tk.Label(hdr, text=f"{a['icon']}  {name}",
             font=("Courier", 13, "bold"), bg=CARD_BG, fg=WHITE).pack(side="left")
    status_lbl = tk.Label(hdr, text="● ON " if a["always_on"] else "○ OFF",
                          font=("Courier", 11, "bold"), bg=CARD_BG,
                          fg=GREEN if a["always_on"] else RED)
    status_lbl.pack(side="right")

    tk.Frame(card, bg=CARD_BORDER, height=1).pack(fill="x")

    # Card body
    body = tk.Frame(card, bg=CARD_BG, padx=12, pady=8)
    body.pack(fill="x")

    def row(parent, label, value, val_color=WHITE):
        f = tk.Frame(parent, bg=CARD_BG)
        f.pack(fill="x", pady=2)
        tk.Label(f, text=label, font=("Courier", 9), bg=CARD_BG,
                 fg=MUTED, width=14, anchor="w").pack(side="left")
        v = tk.Label(f, text=value, font=("Courier", 10, "bold"),
                     bg=CARD_BG, fg=val_color, anchor="w")
        v.pack(side="left")
        return v

    power_lbl  = row(body, "Power:",    f"{a['base_power']:.1f} W")
    bar_lbl    = tk.Label(body, text=get_bar(0.5), font=("Courier", 9),
                          bg=CARD_BG, fg=GREEN)
    bar_lbl.pack(anchor="w", pady=2)
    energy_lbl = row(body, "Energy:",   "0.0000 kWh", ACCENT)
    units_lbl  = row(body, "Units:",    "0.0000 units", ORANGE)

    card_widgets[name] = {
        "status": status_lbl,
        "power":  power_lbl,
        "bar":    bar_lbl,
        "energy": energy_lbl,
        "units":  units_lbl,
    }

# --- Totals panel ---
tk.Frame(root, bg=CARD_BORDER, height=1).pack(fill="x", padx=16)

totals = tk.Frame(root, bg="#010409", padx=16, pady=10)
totals.pack(fill="x")

tk.Label(totals, text="TOTALS", font=("Courier", 10, "bold"),
         bg="#010409", fg=MUTED).grid(row=0, column=0, sticky="w", padx=(0,20))

lbl_total_power  = tk.Label(totals, text="0.0 W", font=("Courier", 11, "bold"),
                             bg="#010409", fg=WHITE)
lbl_total_power.grid(row=0, column=1, padx=10)

lbl_total_bar = tk.Label(totals, text=get_bar(0, 30), font=("Courier", 9),
                          bg="#010409", fg=GREEN)
lbl_total_bar.grid(row=0, column=2, padx=10)

lbl_total_energy = tk.Label(totals, text="0.0000 kWh", font=("Courier", 10),
                             bg="#010409", fg=ACCENT)
lbl_total_energy.grid(row=0, column=3, padx=10)

lbl_total_units  = tk.Label(totals, text="0.0000 units", font=("Courier", 10),
                             bg="#010409", fg=ORANGE)
lbl_total_units.grid(row=0, column=4, padx=10)

# -------------------------
# START
# -------------------------
tick()
root.mainloop()
