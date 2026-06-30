import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading

class SmartHomeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Home :Temperature Control System")
        self.root.geometry("600x500")
       # self.root.resizable(False, False)
        
        # Initialize variables
        self.max_temp = 24.0
        self.min_temp = 23.0
        self.fan_on = False
        self.ac_on = False
        self.heater_on = False
        self.current_temp = 22
        self.running = False
        #self.monitor_thread = None
        
        # Setup GUI
        self.setup_gui()
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text=" SMART HOME TEMPERATURE CONTROL", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Temperature Settings Section
       # settings_frame = ttk.LabelFrame(main_frame, text="Temperature Settings", padding="10")
      #  settings_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Min Temperature
        ttk.Label(settings_frame, text="Minimum Temperature:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.min_entry = ttk.Entry(settings_frame, width=10)
        self.min_entry.grid(row=0, column=1, sticky=tk.W, pady=2)
        self.min_entry.insert(0, "20.0")
        
        # Max Temperature
        ttk.Label(settings_frame, text="Maximum Temperature:").grid(row=0, column=2, sticky=tk.W, pady=2, padx=(20,0))
        self.max_entry = ttk.Entry(settings_frame, width=10)
        self.max_entry.grid(row=0, column=3, sticky=tk.W, pady=2)
        self.max_entry.insert(0, "25.0")
        
        # Set Button
        ttk.Button(settings_frame, text="Apply Settings", command=self.apply_settings).grid(row=0, column=4, padx=(10,0))
        
        # Current Temperature Display
        temp_frame = ttk.LabelFrame(main_frame, text="Current Status", padding="10")
        temp_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Temperature reading
        self.temp_label = ttk.Label(temp_frame, text="🌡️  Temperature: 22.0°C", 
                                   font=('Arial', 24, 'bold'))
        self.temp_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Status Message
        self.status_label = ttk.Label(temp_frame, text="Status: Waiting to start...", 
                                      font=('Arial', 12))
        self.status_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Device Status Section
        device_frame = ttk.LabelFrame(main_frame, text="Device Status", padding="10")
        device_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # AC Status
        self.ac_label = ttk.Label(device_frame, text="❄️  AC: OFF", 
                                  font=('Arial', 12), foreground='red')
        self.ac_label.grid(row=0, column=0, padx=20, pady=5)
        
        # Heater Status
        self.heater_label = ttk.Label(device_frame, text="🔥  Heater: OFF", 
                                      font=('Arial', 12), foreground='red')
        self.heater_label.grid(row=0, column=1, padx=20, pady=5)
        
        # Fan Status
        self.fan_label = ttk.Label(device_frame, text="💨  Fan: OFF", 
                                   font=('Arial', 12), foreground='red')
        self.fan_label.grid(row=0, column=2, padx=20, pady=5)
        
        # Control Buttons Section
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        self.start_button = ttk.Button(control_frame, text="▶️  Start Monitoring", 
                                       command=self.start_monitoring, width=15)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="⏹️  Stop Monitoring", 
                                      command=self.stop_monitoring, width=15, state='disabled')
        self.stop_button.grid(row=0, column=1, padx=5)
        
        ttk.Button(control_frame, text="🔄  Manual Reading", 
                  command=self.manual_reading, width=15).grid(row=0, column=2, padx=5)
        
        # History/Log Section
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="5")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = tk.Text(log_frame, height=6, width=60, state='disabled')
        self.log_text.grid(row=0, column=0, padx=5, pady=5)
        
        # Scrollbar for log
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text['yscrollcommand'] = scrollbar.set
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
    def apply_settings(self):
        """Apply the temperature settings from input fields"""
        try:
            min_temp = float(self.min_entry.get())
            max_temp = float(self.max_entry.get())
            
            if min_temp >= max_temp:
                messagebox.showerror("Error", "Minimum temperature must be less than maximum temperature!")
                return
                
            self.min_temp = min_temp
            self.max_temp = max_temp
            self.log_message(f"Settings updated: Min={min_temp}°C, Max={max_temp}°C")
            messagebox.showinfo("Success", "Temperature settings applied successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid temperature values!")
    
    def read_temperature(self):
        """Simulate reading temperature from sensor"""
        # Simulate realistic temperature fluctuation
        change = random.uniform(-0.5, 0.5)
        self.current_temp = round(self.current_temp + change, 1)
        
        # Keep temperature within a realistic range
        if self.current_temp < 18:
            self.current_temp = 18.0
        elif self.current_temp > 32:
            self.current_temp = 32.0
            
        return self.current_temp
    
    def control_temperature(self, current_temp):
        """Control devices based on temperature"""
        if current_temp > self.max_temp:
            self.fan_on = True
            self.ac_on = True
            self.heater_on = False
            status = "TOO HOT! AC and Fan ON"
            self.log_message(f"🌡️  {current_temp}°C - TOO HOT! AC:ON, Fan:ON, Heater:OFF")
            
        elif current_temp < self.min_temp:
            self.fan_on = False
            self.ac_on = False
            self.heater_on = True
            status = "TOO COLD! Heater ON"
            self.log_message(f"🌡️  {current_temp}°C - TOO COLD! AC:OFF, Fan:OFF, Heater:ON")
            
        else:
            self.fan_on = False
            self.ac_on = False
            self.heater_on = False
            status = "✅ PERFECT TEMPERATURE! All devices OFF"
            self.log_message(f"🌡️  {current_temp}°C - PERFECT! All devices OFF")
        
        # Update GUI
        self.update_display(current_temp, status)
        
    def update_display(self, temp, status):
        """Update all GUI elements with current status"""
        # Update temperature display
        self.temp_label.config(text=f"🌡️  Temperature: {temp}°C")
        self.status_label.config(text=f"Status: {status}")
        
        # Update device status with colors
        self.ac_label.config(text=f"❄️  AC: {'ON' if self.ac_on else 'OFF'}", 
                            foreground='green' if self.ac_on else 'red')
        self.heater_label.config(text=f"🔥  Heater: {'ON' if self.heater_on else 'OFF'}", 
                                foreground='green' if self.heater_on else 'red')
        self.fan_label.config(text=f"💨  Fan: {'ON' if self.fan_on else 'OFF'}", 
                             foreground='green' if self.fan_on else 'red')
    
    def log_message(self, message):
        """Add a message to the log"""
        self.log_text.config(state='normal')
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)  # Auto-scroll to bottom
        self.log_text.config(state='disabled')
    
    def monitor_loop(self):
        """Main monitoring loop running in separate thread"""
        while self.running:
            temp = self.read_temperature()
            self.control_temperature(temp)
            time.sleep(3)  # Check every 3 seconds
    
    def start_monitoring(self):
        """Start the temperature monitoring"""
        if not self.running:
            self.running = True
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
            self.log_message("🟢 Monitoring started")
            
            # Start monitoring in a separate thread
            self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop the temperature monitoring"""
        if self.running:
            self.running = False
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
            self.log_message("🔴 Monitoring stopped")
            
            # Turn off all devices
            self.fan_on = False
            self.ac_on = False
            self.heater_on = False
            self.update_display(self.current_temp, "System idle - All devices OFF")
    
    def manual_reading(self):
        """Take a single manual temperature reading"""
        if not self.running:
            temp = self.read_temperature()
            self.control_temperature(temp)
            self.log_message(f"📊 Manual reading taken: {temp}°C")
        else:
            messagebox.showinfo("Info", "Monitoring is already running. Manual readings will be taken automatically.")


def main():
    root = tk.Tk()
    app = SmartHomeGUI(root)
    
    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()