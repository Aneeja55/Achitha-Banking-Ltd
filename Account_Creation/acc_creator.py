import csv
from Account_Creation.account_repo import AccountRepository, LOGIN_FILE

class AccountCreator:

    @staticmethod
    def create_account(name, dob, phone, email, acc_type, pin, opening_balance):

        last_acc, last_cust = AccountRepository.get_last_ids()

        acc_no = f"A{last_acc + 1}"
        cust_id = f"C{last_cust + 1}"

        data = [
            name, dob, phone, email,
            acc_no, cust_id, acc_type,
            pin, opening_balance, "Active"
        ]

        AccountRepository.save_account(data)

        with open(LOGIN_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([acc_no, pin])

        print("Account created successfully.")
        print("Account Number:", acc_no)

        return acc_no
