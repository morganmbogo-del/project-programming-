import tkinter as tk
from tkinter import messagebox

CORRECT_PIN = "6732"
attempts = 4
entered = ""

def update_display():
    dots_label.config(text="● " * len(entered) + "○ " * (4 - len(entered)))

def press(d):
    global entered
    if len(entered) < 4:
        entered += d
        update_display()
        if len(entered) == 4:
            root.after(150, check_pin)

def backspace():
    global entered
    entered = entered[:-1]
    update_display()

def check_pin():
    global entered, attempts
    if entered == CORRECT_PIN:
        messagebox.showinfo("Access", "Access granted! Welcome home.")
        root.destroy()
    else:
        attempts -= 1
        entered = ""
        update_display()
        if attempts > 0:
            status_label.config(text=f"Incorrect PIN. Attempts remaining: {attempts}")
        else:
            status_label.config(text="Account locked! No attempts left.")
            for btn in keypad_buttons:
                btn.config(state="disabled")

root = tk.Tk()
root.title("Enter PIN")
root.geometry("260x380")
root.resizable(False, False)

tk.Label(root, text=" Enter PIN", font=("Arial", 16, "bold")).pack(pady=10)
 security-and-access
dots_label = tk.Label(root, text="O O O O", font=("Arial", 20))

dots_label = tk.Label(root, text="O O O O", font=("Arial", 22)) main
dots_label.pack()
status_label = tk.Label(root, text="Unlock to access the house", fg="gray")
status_label.pack(pady=5)

frame = tk.Frame(root)
frame.pack()

keypad_buttons = []
keys = ["1","2","3","4","5","6","7","8","9","","0","<"]
for i, k in enumerate(keys):
    if k == "":
        continue
    cmd = backspace if k == "<" else (lambda d=k: press(d))
    btn = tk.Button(frame, text=k, width=5, height=2, font=("Arial", 14), command=cmd)
    btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
    keypad_buttons.append(btn)
 security-and-access
root.mainloop()

root.mainloop()
 main
