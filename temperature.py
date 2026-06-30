import time
import random
  
print("\n" + "=" * 40)
print("SMART HOME TEMPERATURE CONTROL SYSTEM")
print("=" * 40)

max_temperature = float(input("Enter max temperature: "))
min_temperature = float(input("Enter min temperature: "))

fan_on=False
ac_on=False
heater_on=False

def read_temperature():
    temperature = random.uniform(20,30)
    return round(temperature, 1)

def control_temperature(current_temperature):
    global fan_on
    global ac_on
    global heater_on

    if current_temperature > max_temperature:
        print("TOO HOT! Turning ON AC and Fan...")
        fan_on = True
        ac_on = True
        heater_on = False
        print(f"temp is {current_temperature} AC:on Fan:on, heater :off")
    elif current_temperature < min_temperature:
        print("TOO COLD! Turning ON Heater...")
        fan_on = False
        ac_on = False
        heater_on = True
        print(f"temp is {current_temperature} AC:off Fan:off heater :on")

    else:
        print("PERFECT TEMPERATURE! Turning everything OFF...")
        fan_on = False
        ac_on = False
        heater_on = False
        print(f"temp is {current_temperature} AC:off Fan:off heater :off")


def show_status():
    """This function prints the ON/OFF state of each device."""
    print("\nDEVICE STATUS:")
    print(f"   AC     : {' ON' if ac_on else ' OFF'}")
    print(f"   Heater : {' ON' if heater_on else ' OFF'}")
    print(f"   Fan    : {' ON' if fan_on else 'OFF'}")
    print("=" * 40)


print(f"Max Temperature: {max_temperature}")
print(f" Min Temperature: {min_temperature}")
print("=" * 40)



print(f"min={min_temperature} max={max_temperature}  \n")

while True:
    temperature = read_temperature()
    control_temperature(temperature)
    time.sleep(6)


