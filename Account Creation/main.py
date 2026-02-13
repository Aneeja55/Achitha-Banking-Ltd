from account_repo import account_repo
from acc_creator import acc_creator

csv_path = input("Enter CSV file path to store account details: ")

repo = account_repo(csv_path)
creator = acc_creator(repo)

print("***Welcome to Achitha Banking Ltd.***")
print("\n--- ENTER CUSTOMER DETAILS ---")
name = input("Full Name       : ")
dob = input("Date of Birth   : ")
phone = input("Phone Number    : ")
email = input("Email ID        : ")

print("\nSelect Account Type")
print("1. Savings")
print("2. Current")

choice = input("Enter choice (1 or 2): ")

if choice == "1":
    acc_type = "Savings"
elif choice == "2":
    acc_type = "Current"
else:
    print("Invalid account type selected.")
    exit()

pin=input("Enter pin: ")

opening_balance = float(input("Enter Opening Balance: "))

account = creator.create_account(
    name,
    dob,
    phone,
    email,
    acc_type,
    pin,
    opening_balance
)

print(account)
