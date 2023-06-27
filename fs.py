import random
import datetime
import csv

class SolarPanel:
    def __init__(self, panel_id):
        self.panel_id = panel_id
        self.voltage = 0
        self.current = 0
        self.temperature = 0

    def generate_data(self):
        # Simulating data for voltage, current, and temperature
        self.voltage = random.uniform(10, 50)
        self.current = random.uniform(1, 10)
        self.temperature = random.uniform(20, 60)


class Battery:
    def __init__(self, capacity):
        self.capacity = capacity
        self.charge_level = 0

    def charge(self, amount):
        self.charge_level = min(self.charge_level + amount, self.capacity)

    def discharge(self, amount):
        self.charge_level = max(self.charge_level - amount, 0)


class Load:
    def __init__(self, load_id, power_consumption):
        self.load_id = load_id
        self.power_consumption = power_consumption

    def edit_power_consumption(self, new_power_consumption):
        self.power_consumption = new_power_consumption


class SolarPowerManagementSystem:
    def __init__(self):
        self.solar_panels = []
        self.battery = None
        self.loads = []
        self.data_log = []

    def add_solar_panel(self, panel_id):
        panel = SolarPanel(panel_id)
        self.solar_panels.append(panel)
        print(f"Added solar panel with ID: {panel_id}")

    def remove_solar_panel(self, panel_id):
        for panel in self.solar_panels:
            if panel.panel_id == panel_id:
                self.solar_panels.remove(panel)
                print(f"Removed solar panel with ID: {panel_id}")
                break

    def find_solar_panel(self, panel_id):
        for panel in self.solar_panels:
            if panel.panel_id == panel_id:
                return panel
        return None

    def add_load(self):
        load_id = input("Enter the load ID: ")
        power_consumption = float(input("Enter the power consumption (in Watts): "))
        load = Load(load_id, power_consumption)
        self.loads.append(load)
        print(f"Added load with ID: {load_id}, Power consumption: {power_consumption} W")

    def remove_load(self):
        load_id = input("Enter the load ID to remove: ")
        for load in self.loads:
            if load.load_id == load_id:
                self.loads.remove(load)
                print(f"Removed load with ID: {load_id}")
                break

    def edit_load_power_consumption(self):
        load_id = input("Enter the load ID to edit power consumption: ")
        new_power_consumption = float(input("Enter the new power consumption (in Watts): "))
        for load in self.loads:
            if load.load_id == load_id:
                load.edit_power_consumption(new_power_consumption)
                print(f"Updated power consumption of load {load_id} to {new_power_consumption} W")
                break
        else:
            print(f"No load found with ID: {load_id}")

    def set_battery(self, capacity):
        self.battery = Battery(capacity)
        print(f"Set battery capacity to: {capacity} Wh")

    def simulate_solar_power_generation(self):
        total_power_generation = 0
        for panel in self.solar_panels:
            panel.generate_data()
            total_power_generation += panel.voltage * panel.current

        if self.battery:
            self.battery.charge(total_power_generation)

        self.data_log.append({
            "timestamp": datetime.datetime.now(),
            "power_generation": total_power_generation,
            "battery_charge_level": self.battery.charge_level if self.battery else None
        })

        self._power_distribution()

    def _power_distribution(self):
        total_power_consumption = 0
        for load in self.loads:
            total_power_consumption += load.power_consumption

        if self.battery:
            excess_power = self.battery.charge_level - total_power_consumption
            if excess_power > 0:
                self.battery.discharge(excess_power)
            else:
                deficit_power = total_power_consumption - self.battery.charge_level
                self.battery.charge(deficit_power)

        print("-------- Power Distribution --------")
        print(f"Total power consumption: {total_power_consumption} W")
        if self.battery:
            print(f"Battery charge level: {self.battery.charge_level} Wh")
        else:
            print("No battery set")
        print("------------------------------------")

    def save_data_log(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["timestamp", "power_generation", "battery_charge_level"])
            writer.writeheader()
            writer.writerows(self.data_log)

        print(f"Data log saved to {filename}")

    def load_data_log(self, filename):
        try:
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                self.data_log = [row for row in reader]

            print(f"Data log loaded from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with an empty data log.")

    def display_data_log(self):
        print("-------- Data Log --------")
        for log_entry in self.data_log:
            print(f"Timestamp: {log_entry['timestamp']}")
            print(f"Power Generation: {log_entry['power_generation']} W")
            if self.battery:
                print(f"Battery Charge Level: {log_entry['battery_charge_level']} Wh")
            print("--------------------------")

    def find_equipment_by_id(self, equipment_id):
        panel = self.find_solar_panel(equipment_id)
        if panel:
            print(f"Found solar panel with ID: {panel.panel_id}")
            print(f"Voltage: {panel.voltage} V")
            print(f"Current: {panel.current} A")
            print(f"Temperature: {panel.temperature} °C")
        else:
            print(f"No solar equipment found with ID: {equipment_id}")


def main_menu(solar_system):
    while True:
        print("--------- Main Menu ---------")
        print("1. Add Solar Panel")
        print("2. Remove Solar Panel")
        print("3. Add Load")
        print("4. Remove Load")
        print("5. Edit Load Power Consumption")
        print("6. Set Battery Capacity")
        print("7. Simulate Solar Power Generation and Distribution")
        print("8. Save Data Log")
        print("9. Load Data Log")
        print("10. Display Data Log")
        print("11. Find Solar Equipment by ID")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            panel_id = int(input("Enter the solar panel ID: "))
            solar_system.add_solar_panel(panel_id)
        elif choice == "2":
            panel_id = int(input("Enter the solar panel ID to remove: "))
            solar_system.remove_solar_panel(panel_id)
        elif choice == "3":
            solar_system.add_load()
        elif choice == "4":
            solar_system.remove_load()
        elif choice == "5":
            solar_system.edit_load_power_consumption()
        elif choice == "6":
            capacity = int(input("Enter the battery capacity (in Watt-hours): "))
            solar_system.set_battery(capacity)
        elif choice == "7":
            solar_system.simulate_solar_power_generation()
        elif choice == "8":
            filename = input("Enter the file path to save the data log (e.g., /path/to/data_log.csv): ")
            solar_system.save_data_log(filename)
        elif choice == "9":
            filename = input("Enter the file path to load the data log (e.g., /path/to/data_log.csv): ")
            solar_system.load_data_log(filename)
        elif choice == "10":
            solar_system.display_data_log()
        elif choice == "11":
            equipment_id = int(input("Enter the ID of the solar equipment to search for: "))
            solar_system.find_equipment_by_id(equipment_id)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


# Example usage
solar_system = SolarPowerManagementSystem()
main_menu(solar_system)
