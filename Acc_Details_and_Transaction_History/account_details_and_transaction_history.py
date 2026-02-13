from collections import defaultdict
import csv
from Account_Creation.account_repo import TRANSACTIONS_FILE, AccountRepository

class AccountDetails:

    @staticmethod
    def display_account(account_no):
        account = AccountRepository.load_accounts().get(account_no)

        if not account:
            print("Account not found.")
            return

        for key, value in account.items():
            print(f"{key}: {value}")

    @staticmethod
    def display_transactions(account_no):
        transactions = defaultdict(list)

        try:
            with open(TRANSACTIONS_FILE, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    transactions[row["AccountNo"]].append(row)
        except:
            pass

        for txn in transactions.get(account_no, []):
            print(txn)
