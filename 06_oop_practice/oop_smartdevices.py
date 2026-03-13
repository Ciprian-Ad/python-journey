# --- 1. The Parent Class (The Base) ---
class SmartDevice:
    def __init__(self, name):
        self.name = name
        self.is_on = False  # Every device has a power status

    def toggle_power(self):
        # Flips the power status True/False
        self.is_on = not self.is_on  # This is a neat trick to flip the boolean!
    def get_status(self):
        status = "ON" if self.is_on else "OFF"
        print(f"{self.name} is currently: {status}")

# --- 2. The Child Classes (The Specifics) ---
# Putting (SmartDevice) in parentheses tells Python: 
# "SmartLight gets everything SmartDevice has, plus extra stuff."
class SmartLight(SmartDevice):
    def __init__(self, name):
        super().__init__(name) # This calls the Parent's __init__ to set up the name and power!
        self.brightness = 100  # Only lights have brightness
        
    def set_brightness(self, value):
        if 0 <= value <= 100:
            self.brightness = value
        else:            
            print("Brightness must be between 0 and 100!") 

    # We "Override" the parent's status method to include brightness
    def get_status(self):
        # 1. Ask the Parent class to do its normal print statement first
        super().get_status() 
        # 2. Then add the specific light stuff!
        print(f"Brightness: {self.brightness}%")

class SmartThermostat(SmartDevice):
    def __init__(self, name):
        super().__init__(name)
        self.current_temp = 21.0
        self.target_temp = 21.0
        
    def set_temperature(self, target):
        self.target_temp = target

    def get_status(self):
        # 1. Ask the Parent class to do its normal print statement first
        super().get_status() 
        print(f"Current Temperature: {self.current_temp}°C")
        print(f"Target Temperature: {self.target_temp}°C")

# --- 3. The Hub (Composition) ---
class SmartHub:
    def __init__(self):
        self.devices = []

    # Because SmartLight and SmartThermostat are children of SmartDevice, 
    # isinstance(device, SmartDevice) will still work perfectly for both!
    def add_device(self, device: SmartDevice):
        self.devices.append(device)

    def turn_all_off(self):
        for device in self.devices:
            device.is_on = False  # This will turn them all off (or on if they were off!)

    def system_report(self):
        print("📊 Smart Hub System Report:")
        for device in self.devices:
            device.get_status()  # Each device will report its own status!

# --- Let's see it in action! ---
if __name__ == "__main__":
    living_room_light = SmartLight("Living Room Light")
    bedroom_thermostat = SmartThermostat("Bedroom Thermostat")
    
    myHub = SmartHub()
    myHub.add_device(living_room_light)
    myHub.add_device(bedroom_thermostat)
    
    # Turn on the light and set the thermostat
    living_room_light.toggle_power()  # Turns the light ON
    living_room_light.set_brightness(75)  # Dim the light to 75%
    
    bedroom_thermostat.toggle_power()  # Turns the thermostat ON
    bedroom_thermostat.set_temperature(22.5)  # Set target temp to 22.5°C
    
    myHub.system_report()

    print("-" * 20)
    # Now let's turn everything off with the hub!
    myHub.turn_all_off()
    myHub.system_report()