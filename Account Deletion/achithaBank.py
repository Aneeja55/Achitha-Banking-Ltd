import csv

class AccountDeletion:
    FILE = "users1.csv"
    
    # ================= LOAD USERS =================
    @staticmethod
    def load_users(filepath=None):
        file_path = filepath or AccountDeletion.FILE
        users = {}
        try:
            with open(file_path, "r") as f:
                for line in f:
                    u, p, pin, s, l = line.strip().split(",")
                    users[u] = {
                        "password": p,
                        "pin": pin,
                        "status": int(s),   # 1 = active, 0 = deactivated
                        "locked": int(l)    # 1 = locked
                    }
        except FileNotFoundError:
            pass
        return users

    # ================= SAVE USERS =================
    @staticmethod
    def save_users(users, filepath=None):
        file_path = filepath or AccountDeletion.FILE
        with open(file_path, "w") as f:
            for u in users:
                f.write(
                    u + "," +
                    users[u]["password"] + "," +
                    users[u]["pin"] + "," +
                    str(users[u]["status"]) + "," +
                    str(users[u]["locked"]) + "\n"
                )

    # ================= DEACTIVATE ACCOUNT =================
    @staticmethod
    def deactivate_account(username, password, filepath=None):
        users = AccountDeletion.load_users(filepath)
        
        if username not in users:
            print("❌ Account does not exist.")
            return False

        if users[username]["locked"] == 1:
            print("❌ Account is LOCKED.")
            return False

        attempts = 3
        while attempts > 0:
            if users[username]["password"] == password:
                users[username]["status"] = 0
                AccountDeletion.save_users(users, filepath)
                print("✅ Account deactivated successfully.")
                return True
            else:
                attempts -= 1
                if attempts > 0:
                    print(f"❌ Incorrect password. Attempts left: {attempts}")

        # 🔐 Lock after 3 wrong password attempts
        users[username]["locked"] = 1
        AccountDeletion.save_users(users, filepath)
        print("❌ Too many incorrect attempts. Account has been LOCKED.")
        return False

    # ================= DELETE ACCOUNT =================
    @staticmethod
    def delete_account(username, password, filepath=None):
        users = AccountDeletion.load_users(filepath)
        
        if username not in users:
            print("❌ Account does not exist.")
            return False

        if users[username]["locked"] == 1:
            print("❌ Account is LOCKED.")
            return False

        if users[username]["status"] == 1:
            print("❌ Account must be deactivated before deletion.")
            return False

        attempts = 3
        while attempts > 0:
            if users[username]["password"] == password:
                del users[username]
                AccountDeletion.save_users(users, filepath)
                print("✅ Account permanently deleted.")
                return True
            else:
                attempts -= 1
                if attempts > 0:
                    print(f"❌ Incorrect password. Attempts left: {attempts}")

        # 🔐 Lock after 3 wrong password attempts
        users[username]["locked"] = 1
        AccountDeletion.save_users(users, filepath)
        print("❌ Too many incorrect attempts. Account has been LOCKED.")
        return False
