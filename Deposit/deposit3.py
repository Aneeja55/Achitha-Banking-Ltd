import csv
from datetime import datetime
from Account_Creation.account_repo import AccountRepository, TRANSACTIONS_FILE

class DepositSystem:

    @staticmethod
    def deposit_money(account_no, amount):

        if amount <= 0:
            print("Invalid amount.")
            return False

        accounts = AccountRepository.load_accounts()

        if account_no not in accounts:
            print("Account not found.")
            return False

        current = float(accounts[account_no]["Balance"])
        new_balance = current + amount

        AccountRepository.update_balance(account_no, new_balance)

        now = datetime.now()

        with open(TRANSACTIONS_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                account_no,
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M:%S"),
                "Deposit",
                amount,
                new_balance
            ])

        print("Deposit successful. New balance:", new_balance)
        return True
