from Eligibility.eligibility import EligibilityChecker
from Account_Creation.account_repo import AccountRepository
from Account_Creation.acc_creator import AccountCreator
from Deposit.deposit3 import DepositSystem
from Login.banklogin import LoginSecurity
from Acc_Details_and_Transaction_History.account_details_and_transaction_history import AccountDetails
from Account_Deletion.achithaBank import AccountDeletion

class BankingSystem:

    def __init__(self):
        AccountRepository.initialize_files()

    def main_menu(self):
        while True:
            print("\n1. Create Account")
            print("2. Login")
            print("3. Exit")

            choice = input("Choice: ")

            if choice == "1":
                aadhaar = EligibilityChecker.check_eligibility()
                if aadhaar:
                    self.create_account()

            elif choice == "2":
                self.login_flow()

            elif choice == "3":
                break

    def create_account(self):
        name = input("Name: ")
        dob = input("DOB: ")
        phone = input("Phone: ")
        email = input("Email: ")
        acc_type = input("Type: ")
        pin = input("PIN: ")
        balance = float(input("Opening balance: "))

        AccountCreator.create_account(
            name, dob, phone, email, acc_type, pin, balance
        )

    def login_flow(self):
        acc_no = input("Account No: ")
        pin = input("PIN: ")

        if LoginSecurity.login(acc_no, pin):
            self.account_menu(acc_no)

    def account_menu(self, acc_no):
        while True:
            print("\n1. Details")
            print("2. Transactions")
            print("3. Deposit")
            print("4. Deactivate")
            print("5. Logout")

            c = input("Choice: ")

            if c == "1":
                AccountDetails.display_account(acc_no)
            elif c == "2":
                AccountDetails.display_transactions(acc_no)
            elif c == "3":
                amt = float(input("Amount: "))
                DepositSystem.deposit_money(acc_no, amt)
            elif c == "4":
                pin = input("Confirm PIN: ")
                AccountDeletion.deactivate_account(acc_no, pin)
            elif c == "5":
                break


if __name__ == "__main__":
    bank = BankingSystem()
    bank.main_menu()
