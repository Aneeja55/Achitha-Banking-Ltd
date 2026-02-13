import csv
import os

ACCOUNTS_FILE = "all_accounts.csv"
TRANSACTIONS_FILE = "all_transactions.csv"
LOGIN_FILE = "bank_users.csv"

class AccountRepository:

    @staticmethod
    def initialize_files():
        if not os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, "w") as f:
                f.write("FullName,DOB,PhoneNumber,EmailId,AccountNo,CustomerID,AccountType,Pin,Balance,Status\n")

        if not os.path.exists(TRANSACTIONS_FILE):
            with open(TRANSACTIONS_FILE, "w") as f:
                f.write("AccountNo,Date,Time,TransactionType,Amount,Balance\n")

        if not os.path.exists(LOGIN_FILE):
            with open(LOGIN_FILE, "w") as f:
                f.write("username,password\n")

    @staticmethod
    def get_last_ids():
        try:
            with open(ACCOUNTS_FILE, "r") as f:
                lines = f.readlines()
            if len(lines) <= 1:
                return 5000, 1000
            last = lines[-1].split(",")
            return int(last[4][1:]), int(last[5][1:])
        except:
            return 5000, 1000

    @staticmethod
    def save_account(data):
        with open(ACCOUNTS_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(data)

    @staticmethod
    def load_accounts():
        accounts = {}
        try:
            with open(ACCOUNTS_FILE, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    accounts[row["AccountNo"]] = row
        except:
            pass
        return accounts

    @staticmethod
    def update_balance(account_no, new_balance):
        accounts = AccountRepository.load_accounts()
        if account_no in accounts:
            accounts[account_no]["Balance"] = str(new_balance)
            with open(ACCOUNTS_FILE, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=accounts[account_no].keys())
                writer.writeheader()
                for acc in accounts.values():
                    writer.writerow(acc)
