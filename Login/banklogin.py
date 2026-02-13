import csv

# Parent class
class SecurityBase:
    @staticmethod
    def system_info():
        print("Bank Login & Security System")


# Child class
class LoginSecurity(SecurityBase):

    path = ""
    attempts_dict = {}  # track login attempts per username
    locked_users = set()  # track locked accounts

    # Set CSV file path
    @staticmethod
    def set_path(filepath):
        LoginSecurity.path = filepath

    # Read CSV manually → Convert to list of dictionaries
    @staticmethod
    def read_data():
        try:
            with open(LoginSecurity.path, 'r') as file:
                lines = file.readlines()

            if not lines:
                print("CSV file empty")
                return []

            # First line = header
            keys = [k.strip() for k in lines[0].strip().split(',')]
            data = []

            for line in lines[1:]:
                values = [v.strip() for v in line.strip().split(',')]
                # Only username and password expected
                if len(values) < 2:
                    continue
                row = {"username": values[0], "password": values[1]}
                data.append(row)

            return data

        except FileNotFoundError:
            print("File not found")
            return []

    # Login function
    @staticmethod
    def login(username, password):
        if username in LoginSecurity.locked_users:
            print("❌ Account locked")
            return False

        data = LoginSecurity.read_data()
        for row in data:
            if row["username"] == username and row["password"] == password:
                print("✅ Login successful")
                LoginSecurity.attempts_dict[username] = 0
                return True

        # Invalid login
        LoginSecurity.attempts_dict[username] = LoginSecurity.attempts_dict.get(username, 0) + 1
        print("❌ Invalid login")

        # Lock after 3 attempts
        if LoginSecurity.attempts_dict[username] >= 3:
            LoginSecurity.locked_users.add(username)
            print("❌ Account locked after 3 attempts")
        else:
            print(f"Attempts left: {3 - LoginSecurity.attempts_dict[username]}")

        return False

    # Change password
    @staticmethod
    def change_password(username, old, new):
        try:
            with open(LoginSecurity.path, 'r') as file:
                lines = file.readlines()

            if not lines:
                print("CSV file empty")
                return

            header = lines[0]
            new_lines = [header]
            changed = False

            for line in lines[1:]:
                values = [v.strip() for v in line.strip().split(',')]
                if len(values) < 2:
                    continue
                if values[0] == username and values[1] == old:
                    values[1] = new
                    changed = True
                    print("✅ Password changed")
                new_line = ','.join(values) + "\n"
                new_lines.append(new_line)

            if not changed:
                print("❌ Old password incorrect or user not found")

            # Write back updated CSV
            with open(LoginSecurity.path, 'w') as file:
                file.writelines(new_lines)

        except Exception as e:
            print("❌ Error:", e)

    # Logout
    @staticmethod
    def logout():
        print("✅ Logged out successfully")
