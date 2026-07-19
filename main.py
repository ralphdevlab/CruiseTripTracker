import mysql.connector
from mysql.connector import Error
from datetime import datetime

# ─────────────────────────────────────────
#  DATABASE CONNECTION
# ─────────────────────────────────────────
def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root1234",
        database="CruiseDB"
    )

# ─────────────────────────────────────────
#  VALIDATION HELPERS
# ─────────────────────────────────────────
def validate_text(prompt, field_name, min_len=2, max_len=100):
    """Validates that input is non-empty text within length limits."""
    while True:
        value = input(prompt).strip()
        if not value:
            print(f"  ERROR: {field_name} cannot be empty. Please enter a value.")
        elif len(value) < min_len:
            print(f"  ERROR: {field_name} must be at least {min_len} characters long.")
        elif len(value) > max_len:
            print(f"  ERROR: {field_name} cannot exceed {max_len} characters.")
        elif any(char.isdigit() for char in value) and field_name not in ["Ship Name", "Cabin Number", "Port Name"]:
            print(f"  ERROR: {field_name} should not contain numbers.")
        else:
            return value

def validate_date(prompt, field_name):
    """Validates date input in YYYY-MM-DD format."""
    while True:
        value = input(prompt).strip()
        if not value:
            print(f"  ERROR: {field_name} cannot be empty.")
            continue
        try:
            parsed = datetime.strptime(value, "%Y-%m-%d")
            if parsed.year < 2000 or parsed.year > 2100:
                print(f"  ERROR: {field_name} year must be between 2000 and 2100.")
            else:
                return value
        except ValueError:
            print(f"  ERROR: {field_name} must be in YYYY-MM-DD format (e.g. 2025-08-15).")
            print(f"         Make sure month is 01-12 and day is 01-31.")

def validate_int(prompt, field_name, min_val=1, max_val=99999):
    """Validates integer input within a given range."""
    while True:
        value = input(prompt).strip()
        if not value:
            print(f"  ERROR: {field_name} cannot be empty.")
            continue
        if not value.isdigit():
            print(f"  ERROR: {field_name} must be a whole number with no letters or symbols.")
            continue
        value = int(value)
        if value < min_val:
            print(f"  ERROR: {field_name} must be at least {min_val}.")
        elif value > max_val:
            print(f"  ERROR: {field_name} cannot exceed {max_val}.")
        else:
            return value

def validate_age(prompt):
    """Validates passenger age specifically."""
    while True:
        value = input(prompt).strip()
        if not value:
            print(f"  ERROR: Age cannot be empty.")
            continue
        if not value.isdigit():
            print(f"  ERROR: Age must be a whole number (e.g. 25). No letters or symbols.")
            continue
        value = int(value)
        if value < 1:
            print(f"  ERROR: Age must be at least 1.")
        elif value > 120:
            print(f"  ERROR: Age cannot exceed 120.")
        else:
            return value

def validate_cabin(prompt):
    """Validates cabin number format (letter + numbers, e.g. A101)."""
    while True:
        value = input(prompt).strip().upper()
        if not value:
            print(f"  ERROR: Cabin number cannot be empty.")
        elif len(value) < 2 or len(value) > 10:
            print(f"  ERROR: Cabin number must be between 2 and 10 characters (e.g. A101, B22).")
        elif not value[0].isalpha():
            print(f"  ERROR: Cabin number must start with a letter (e.g. A101, B22, C305).")
        elif not value[1:].isdigit():
            print(f"  ERROR: Cabin number must have a letter followed by numbers only (e.g. A101).")
        else:
            return value

def validate_cruise_id(prompt):
    """Validates that a cruise ID exists in the database."""
    while True:
        cid = validate_int(prompt, "Cruise ID")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT cruise_id FROM Cruises WHERE cruise_id = %s", (cid,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if not result:
            print(f"  ERROR: Cruise ID {cid} does not exist. Use option 2 to view valid Cruise IDs.")
        else:
            return cid

def validate_passenger_id(prompt):
    """Validates that a passenger ID exists in the database."""
    while True:
        pid = validate_int(prompt, "Passenger ID")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT passenger_id FROM Passengers WHERE passenger_id = %s", (pid,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if not result:
            print(f"  ERROR: Passenger ID {pid} does not exist. Use option 6 to view valid Passenger IDs.")
        else:
            return pid

def validate_port_id(prompt):
    """Validates that a port ID exists in the database."""
    while True:
        pid = validate_int(prompt, "Port ID")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT port_id FROM Ports WHERE port_id = %s", (pid,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if not result:
            print(f"  ERROR: Port ID {pid} does not exist. Use option 10 to view valid Port IDs.")
        else:
            return pid

# ─────────────────────────────────────────
#  CRUISE CLASS
# ─────────────────────────────────────────
class Cruise:
    def __init__(self, cruise_line, ship_name, destination, departure_date, duration_days, cruise_id=None):
        self.cruise_id = cruise_id
        self.cruise_line = cruise_line
        self.ship_name = ship_name
        self.destination = destination
        self.departure_date = departure_date
        self.duration_days = duration_days

    def add_cruise(self):
        conn = get_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO Cruises (cruise_line, ship_name, destination, departure_date, duration_days)
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (self.cruise_line, self.ship_name, self.destination,
                             self.departure_date, self.duration_days))
        conn.commit()
        print(f"\n  SUCCESS: Cruise '{self.ship_name}' added successfully!")
        cursor.close()
        conn.close()

    @staticmethod
    def get_all_cruises():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Cruises")
        rows = cursor.fetchall()
        if not rows:
            print("\n  No cruises found in the database.")
        else:
            print("\n--- ALL CRUISES ---")
            for row in rows:
                print(f"  ID: {row[0]} | Line: {row[1]} | Ship: {row[2]} | Destination: {row[3]} | Departure: {row[4]} | Duration: {row[5]} days")
        cursor.close()
        conn.close()

    @staticmethod
    def update_cruise(cruise_id, new_destination):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Cruises SET destination = %s WHERE cruise_id = %s",
                       (new_destination, cruise_id))
        conn.commit()
        print(f"\n  SUCCESS: Cruise {cruise_id} destination updated to '{new_destination}'")
        cursor.close()
        conn.close()

    @staticmethod
    def delete_cruise(cruise_id):
        conn = get_connection()
        cursor = conn.cursor()
        # Check for linked passengers or ports first
        cursor.execute("SELECT COUNT(*) FROM Passengers WHERE cruise_id = %s", (cruise_id,))
        pcount = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Ports WHERE cruise_id = %s", (cruise_id,))
        portcount = cursor.fetchone()[0]
        if pcount > 0 or portcount > 0:
            print(f"\n  ERROR: Cannot delete Cruise {cruise_id} — it still has {pcount} passenger(s) and {portcount} port(s) linked to it.")
            print(f"         Delete those first, then delete the cruise.")
        else:
            cursor.execute("DELETE FROM Cruises WHERE cruise_id = %s", (cruise_id,))
            conn.commit()
            print(f"\n  SUCCESS: Cruise {cruise_id} deleted.")
        cursor.close()
        conn.close()

# ─────────────────────────────────────────
#  PASSENGER CLASS
# ─────────────────────────────────────────
class Passenger:
    def __init__(self, first_name, last_name, age, cabin_number, cruise_id, passenger_id=None):
        self.passenger_id = passenger_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.cabin_number = cabin_number
        self.cruise_id = cruise_id

    def add_passenger(self):
        conn = get_connection()
        cursor = conn.cursor()
        # Check for duplicate cabin on same cruise
        cursor.execute("SELECT passenger_id FROM Passengers WHERE cabin_number = %s AND cruise_id = %s",
                       (self.cabin_number, self.cruise_id))
        if cursor.fetchone():
            print(f"\n  ERROR: Cabin {self.cabin_number} is already occupied on Cruise {self.cruise_id}.")
            cursor.close()
            conn.close()
            return
        sql = """INSERT INTO Passengers (first_name, last_name, age, cabin_number, cruise_id)
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (self.first_name, self.last_name, self.age,
                             self.cabin_number, self.cruise_id))
        conn.commit()
        print(f"\n  SUCCESS: Passenger '{self.first_name} {self.last_name}' added successfully!")
        cursor.close()
        conn.close()

    @staticmethod
    def get_all_passengers():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Passengers")
        rows = cursor.fetchall()
        if not rows:
            print("\n  No passengers found in the database.")
        else:
            print("\n--- ALL PASSENGERS ---")
            for row in rows:
                print(f"  ID: {row[0]} | Name: {row[1]} {row[2]} | Age: {row[3]} | Cabin: {row[4]} | Cruise ID: {row[5]}")
        cursor.close()
        conn.close()

    @staticmethod
    def update_passenger(passenger_id, new_cabin):
        conn = get_connection()
        cursor = conn.cursor()
        # Check new cabin not already taken on the same cruise
        cursor.execute("SELECT cruise_id FROM Passengers WHERE passenger_id = %s", (passenger_id,))
        cruise_id = cursor.fetchone()[0]
        cursor.execute("SELECT passenger_id FROM Passengers WHERE cabin_number = %s AND cruise_id = %s AND passenger_id != %s",
                       (new_cabin, cruise_id, passenger_id))
        if cursor.fetchone():
            print(f"\n  ERROR: Cabin {new_cabin} is already occupied on that cruise.")
        else:
            cursor.execute("UPDATE Passengers SET cabin_number = %s WHERE passenger_id = %s",
                           (new_cabin, passenger_id))
            conn.commit()
            print(f"\n  SUCCESS: Passenger {passenger_id} cabin updated to '{new_cabin}'")
        cursor.close()
        conn.close()

    @staticmethod
    def delete_passenger(passenger_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Passengers WHERE passenger_id = %s", (passenger_id,))
        conn.commit()
        print(f"\n  SUCCESS: Passenger {passenger_id} deleted.")
        cursor.close()
        conn.close()

# ─────────────────────────────────────────
#  PORT CLASS
# ─────────────────────────────────────────
class Port:
    def __init__(self, port_name, country, arrival_date, cruise_id, port_id=None):
        self.port_id = port_id
        self.port_name = port_name
        self.country = country
        self.arrival_date = arrival_date
        self.cruise_id = cruise_id

    def add_port(self):
        conn = get_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO Ports (port_name, country, arrival_date, cruise_id)
                 VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (self.port_name, self.country, self.arrival_date, self.cruise_id))
        conn.commit()
        print(f"\n  SUCCESS: Port '{self.port_name}' added successfully!")
        cursor.close()
        conn.close()

    @staticmethod
    def get_all_ports():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Ports")
        rows = cursor.fetchall()
        if not rows:
            print("\n  No ports found in the database.")
        else:
            print("\n--- ALL PORTS ---")
            for row in rows:
                print(f"  ID: {row[0]} | Port: {row[1]} | Country: {row[2]} | Arrival: {row[3]} | Cruise ID: {row[4]}")
        cursor.close()
        conn.close()

    @staticmethod
    def update_port(port_id, new_arrival_date):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Ports SET arrival_date = %s WHERE port_id = %s",
                       (new_arrival_date, port_id))
        conn.commit()
        print(f"\n  SUCCESS: Port {port_id} arrival date updated to '{new_arrival_date}'")
        cursor.close()
        conn.close()

    @staticmethod
    def delete_port(port_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Ports WHERE port_id = %s", (port_id,))
        conn.commit()
        print(f"\n  SUCCESS: Port {port_id} deleted.")
        cursor.close()
        conn.close()

# ─────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────
def main():
    while True:
        print("\n========== CRUISE TRIP TRACKER ==========")
        print("1.  Add a Cruise")
        print("2.  View All Cruises")
        print("3.  Update a Cruise Destination")
        print("4.  Delete a Cruise")
        print("5.  Add a Passenger")
        print("6.  View All Passengers")
        print("7.  Update a Passenger Cabin")
        print("8.  Delete a Passenger")
        print("9.  Add a Port")
        print("10. View All Ports")
        print("11. Update a Port Arrival Date")
        print("12. Delete a Port")
        print("0.  Exit")
        print("==========================================")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            print("\n-- Add a Cruise --")
            cl   = validate_text("Cruise Line: ", "Cruise Line")
            sn   = validate_text("Ship Name: ", "Ship Name")
            dest = validate_text("Destination: ", "Destination")
            dep  = validate_date("Departure Date (YYYY-MM-DD): ", "Departure Date")
            dur  = validate_int("Duration (days): ", "Duration", min_val=1, max_val=365)
            Cruise(cl, sn, dest, dep, dur).add_cruise()

        elif choice == "2":
            Cruise.get_all_cruises()

        elif choice == "3":
            print("\n-- Update Cruise Destination --")
            Cruise.get_all_cruises()
            cid = validate_cruise_id("Cruise ID to update: ")
            nd  = validate_text("New Destination: ", "Destination")
            Cruise.update_cruise(cid, nd)

        elif choice == "4":
            print("\n-- Delete a Cruise --")
            Cruise.get_all_cruises()
            cid = validate_cruise_id("Cruise ID to delete: ")
            confirm = input(f"  Are you sure you want to delete Cruise {cid}? (yes/no): ").strip().lower()
            if confirm == "yes":
                Cruise.delete_cruise(cid)
            else:
                print("  Deletion cancelled.")

        elif choice == "5":
            print("\n-- Add a Passenger --")
            Cruise.get_all_cruises()
            fn  = validate_text("First Name: ", "First Name")
            ln  = validate_text("Last Name: ", "Last Name")
            age = validate_age("Age: ")
            cab = validate_cabin("Cabin Number (e.g. A101): ")
            cid = validate_cruise_id("Cruise ID: ")
            Passenger(fn, ln, age, cab, cid).add_passenger()

        elif choice == "6":
            Passenger.get_all_passengers()

        elif choice == "7":
            print("\n-- Update Passenger Cabin --")
            Passenger.get_all_passengers()
            pid = validate_passenger_id("Passenger ID to update: ")
            nc  = validate_cabin("New Cabin Number (e.g. B202): ")
            Passenger.update_passenger(pid, nc)

        elif choice == "8":
            print("\n-- Delete a Passenger --")
            Passenger.get_all_passengers()
            pid = validate_passenger_id("Passenger ID to delete: ")
            confirm = input(f"  Are you sure you want to delete Passenger {pid}? (yes/no): ").strip().lower()
            if confirm == "yes":
                Passenger.delete_passenger(pid)
            else:
                print("  Deletion cancelled.")

        elif choice == "9":
            print("\n-- Add a Port --")
            Cruise.get_all_cruises()
            pn  = validate_text("Port Name: ", "Port Name")
            co  = validate_text("Country: ", "Country")
            ad  = validate_date("Arrival Date (YYYY-MM-DD): ", "Arrival Date")
            cid = validate_cruise_id("Cruise ID: ")
            Port(pn, co, ad, cid).add_port()

        elif choice == "10":
            Port.get_all_ports()

        elif choice == "11":
            print("\n-- Update Port Arrival Date --")
            Port.get_all_ports()
            pid = validate_port_id("Port ID to update: ")
            nad = validate_date("New Arrival Date (YYYY-MM-DD): ", "Arrival Date")
            Port.update_port(pid, nad)

        elif choice == "12":
            print("\n-- Delete a Port --")
            Port.get_all_ports()
            pid = validate_port_id("Port ID to delete: ")
            confirm = input(f"  Are you sure you want to delete Port {pid}? (yes/no): ").strip().lower()
            if confirm == "yes":
                Port.delete_port(pid)
            else:
                print("  Deletion cancelled.")

        elif choice == "0":
            print("\nGoodbye!")
            break

        else:
            print("\n  ERROR: Invalid option. Please enter a number between 0 and 12.")

if __name__ == "__main__":
    main()