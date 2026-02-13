import csv
from Account_Creation.account_repo import LOGIN_FILE

class LoginSecurity:

    attempts = {}
    locked = set()

    @staticmethod
    def login(username, password):

        if username in LoginSecurity.locked:
            print("Account locked.")
            return False

        try:
            with open(LOGIN_FILE, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["username"] == username and row["password"] == password:
                        print("Login successful.")
                        LoginSecurity.attempts[username] = 0
                        return True
        except:
            pass

        LoginSecurity.attempts[username] = LoginSecurity.attempts.get(username, 0) + 1

        if LoginSecurity.attempts[username] >= 3:
            LoginSecurity.locked.add(username)
            print("Account locked.")
        else:
            print("Invalid login.")

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
