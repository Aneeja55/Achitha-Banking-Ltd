import re
import csv
import os
import cv2
import pytesseract
from datetime import datetime
from collections import defaultdict

# ============================================
# CONFIGURATION FILES
# ============================================
ACCOUNTS_FILE = "all_accounts.csv"
TRANSACTIONS_FILE = "all_transactions.csv"
LOGIN_FILE = "bank_users.csv"

# ============================================
# VERHOEFF ALGORITHM (For Aadhaar Validation)
# ============================================
d = [
    [0,1,2,3,4,5,6,7,8,9],
    [1,2,3,4,0,6,7,8,9,5],
    [2,3,4,0,1,7,8,9,5,6],
    [3,4,0,1,2,8,9,5,6,7],
    [4,0,1,2,3,9,5,6,7,8],
    [5,9,8,7,6,0,4,3,2,1],
    [6,5,9,8,7,1,0,4,3,2],
    [7,6,5,9,8,2,1,0,4,3],
    [8,7,6,5,9,3,2,1,0,4],
    [9,8,7,6,5,4,3,2,1,0]
]

p = [
    [0,1,2,3,4,5,6,7,8,9],
    [1,5,7,6,2,8,3,0,9,4],
    [5,8,0,3,7,9,6,1,4,2],
    [8,9,1,6,0,4,3,5,2,7],
    [9,4,5,3,1,2,6,8,7,0],
    [4,2,8,6,5,7,3,9,0,1],
    [2,7,9,3,8,0,6,4,1,5],
    [7,0,4,6,9,1,3,2,5,8]
]

def validate_verhoeff(number):
    """Validate Aadhaar using Verhoeff algorithm"""
    c = 0
    number = number[::-1]
    for i in range(len(number)):
        c = d[c][p[i % 8][int(number[i])]]
    return c == 0


# ============================================
# MODULE 1: ELIGIBILITY CHECK
# ============================================
class EligibilityChecker:
    @staticmethod
    def extract_aadhaar(image_path):
        """Extract and validate Aadhaar from image"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return None, "Image not found"
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            text = pytesseract.image_to_string(gray)
            
            aadhaar_match = re.findall(r'\d{4}\s\d{4}\s\d{4}', text)
            if not aadhaar_match:
                return None, "Aadhaar not found in image"
            
            aadhaar_display = aadhaar_match[0]
            aadhaar_number = aadhaar_display.replace(" ", "")
            return aadhaar_number, aadhaar_display
        except Exception as e:
            return None, f"Error processing image: {str(e)}"
    
    @staticmethod
    def check_eligibility():
        """Check customer eligibility"""
        print("\n" + "="*55)
        print("     BANK ACCOUNT ELIGIBILITY CHECK")
        print("="*55)
        
        # Aadhaar validation
        print("\n📄 Step 1: Aadhaar Verification")
        print("-"*40)
        
        use_manual = input("Enter Aadhaar manually? (yes/no): ").strip().lower()
        
        if use_manual == "yes":
            aadhaar_input = input("Enter Aadhaar (XXXX XXXX XXXX): ").strip()
            aadhaar_number = aadhaar_input.replace(" ", "")
        else:
            image_path = input("Enter image path (aadhar.jpeg): ").strip()
            if not image_path:
                image_path = "aadhar.jpeg"
            
            aadhaar_number, aadhaar_display = EligibilityChecker.extract_aadhaar(image_path)
            if aadhaar_number is None:
                print(f"❌ {aadhaar_display}")
                return None
            print(f"✅ Aadhaar Found: {aadhaar_display}")
        
        # Validate Aadhaar
        if len(aadhaar_number) != 12 or not aadhaar_number.isdigit():
            print("❌ Invalid Aadhaar format")
            return None
        
        if not validate_verhoeff(aadhaar_number):
            print("❌ Aadhaar failed validation")
            return None
        
        print("✅ Aadhaar is valid")
        
        # DOB verification
        print("\n📅 Step 2: Age Verification")
        print("-"*40)
        dob = input("Enter DOB (DD/MM/YYYY): ").strip()
        
        try:
            birth_date = datetime.strptime(dob, "%d/%m/%Y")
        except:
            print("❌ Invalid DOB format")
            return None
        
        today = datetime.today()
        age = today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )
        
        print(f"🎂 Calculated Age: {age} years")
        
        if age < 18:
            print("❌ Not eligible (Age must be 18+)")
            return None
        
        print("✅ Age criteria satisfied")
        print("\n" + "="*55)
        print("🎉 ELIGIBLE FOR ACCOUNT CREATION")
        print("="*55)
        
        return aadhaar_number


# ============================================
# MODULE 2: ACCOUNT CREATION & REPOSITORY
# ============================================
class AccountRepository:
    @staticmethod
    def initialize_files():
        """Initialize CSV files if they don't exist"""
        if not os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, "w", newline="") as f:
                f.write("FullName,DOB,PhoneNumber,EmailId,AccountNo,CustomerID,AccountType,Pin,Balance,Status\n")
        
        if not os.path.exists(TRANSACTIONS_FILE):
            with open(TRANSACTIONS_FILE, "w", newline="") as f:
                f.write("AccountNo,Date,Time,TransactionType,Amount,Balance\n")
        
        if not os.path.exists(LOGIN_FILE):
            with open(LOGIN_FILE, "w", newline="") as f:
                f.write("username,password\n")
    
    @staticmethod
    def get_last_ids():
        """Get last account and customer IDs"""
        try:
            with open(ACCOUNTS_FILE, "r") as f:
                lines = f.readlines()
            
            if len(lines) <= 1:
                return 5000, 1000
            
            last = lines[-1].strip().split(",")
            last_acc_no = int(last[4][1:])
            last_cust_id = int(last[5][1:])
            
            return last_acc_no, last_cust_id
        except:
            return 5000, 1000
    
    @staticmethod
    def save_account(name, dob, phone, email, acc_type, pin, opening_balance):
        """Save new account to CSV"""
        last_acc, last_cust = AccountRepository.get_last_ids()
        
        acc_no = f"A{last_acc + 1}"
        cust_id = f"C{last_cust + 1}"
        status = "Active"
        
        with open(ACCOUNTS_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, dob, phone, email, acc_no, cust_id, acc_type, pin, opening_balance, status])
        
        return acc_no, cust_id
    
    @staticmethod
    def load_accounts():
        """Load all accounts"""
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
    def get_account(account_no):
        """Get specific account"""
        accounts = AccountRepository.load_accounts()
        return accounts.get(account_no)
    
    @staticmethod
    def update_balance(account_no, new_balance):
        """Update account balance"""
        accounts = AccountRepository.load_accounts()
        if account_no in accounts:
            accounts[account_no]["Balance"] = str(new_balance)
            
            with open(ACCOUNTS_FILE, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=accounts[account_no].keys())
                writer.writeheader()
                for acc_no, acc_data in accounts.items():
                    writer.writerow(acc_data)


class AccountCreator:
    @staticmethod
    def create_account(name, dob, phone, email, acc_type, pin, opening_balance):
        """Create new account"""
        print("\n" + "="*55)
        print("     ACCOUNT CREATION")
        print("="*55)
        
        acc_no, cust_id = AccountRepository.save_account(name, dob, phone, email, acc_type, pin, opening_balance)
        
        # Add login credentials
        login_exists = False
        try:
            with open(LOGIN_FILE, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row and row.get("username") == acc_no:
                        login_exists = True
        except:
            pass
        
        if not login_exists:
            with open(LOGIN_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([acc_no, pin])
        
        print(f"\n✅ ACCOUNT CREATED SUCCESSFULLY")
        print(f"Full Name    : {name}")
        print(f"Customer ID : {cust_id}")
        print(f"Account No  : {acc_no}")
        print(f"Account Type: {acc_type}")
        print(f"Opening Balance: ₹ {opening_balance}")
        print(f"Status      : Active")
        print("="*55)
        
        return acc_no


# ============================================
# MODULE 3: LOGIN SYSTEM
# ============================================
class LoginSecurity:
    attempts_dict = {}
    locked_users = set()
    current_user = None
    
    @staticmethod
    def login(username, password):
        """Login user"""
        if username in LoginSecurity.locked_users:
            print("❌ Account locked")
            return False
        
        try:
            with open(LOGIN_FILE, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row and row.get("username") == username and row.get("password") == password:
                        print("✅ Login successful")
                        LoginSecurity.attempts_dict[username] = 0
                        LoginSecurity.current_user = username
                        return True
        except:
            pass
        
        LoginSecurity.attempts_dict[username] = LoginSecurity.attempts_dict.get(username, 0) + 1
        print("❌ Invalid login")
        
        if LoginSecurity.attempts_dict[username] >= 3:
            LoginSecurity.locked_users.add(username)
            print("❌ Account locked after 3 attempts")
        else:
            print(f"Attempts left: {3 - LoginSecurity.attempts_dict[username]}")
        
        return False
    
    @staticmethod
    def change_password(username, old, new):
        """Change password"""
        try:
            with open(LOGIN_FILE, "r") as f:
                lines = f.readlines()
            
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
                print("❌ Old password incorrect")
            
            with open(LOGIN_FILE, "w") as f:
                f.writelines(new_lines)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    @staticmethod
    def logout():
        """Logout user"""
        print("✅ Logged out successfully")
        LoginSecurity.current_user = None


# ============================================
# MODULE 4: DEPOSIT SYSTEM
# ============================================
class DepositSystem:
    @staticmethod
    def deposit_money(account_no, amount):
        """Deposit money to account"""
        if amount <= 0:
            print("❌ Invalid amount! Deposit must be positive.")
            return False
        
        account = AccountRepository.get_account(account_no)
        if not account:
            print("❌ Account not found")
            return False
        
        current_balance = float(account["Balance"])
        new_balance = current_balance + amount
        
        # Update balance
        AccountRepository.update_balance(account_no, new_balance)
        
        # Record transaction
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        
        with open(TRANSACTIONS_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([account_no, date, time, "Deposit", amount, new_balance])
        
        print(f"✅ Amount deposited successfully")
        print(f"Amount: ₹ {amount}")
        print(f"New Balance: ₹ {new_balance}")
        return True
    
    @staticmethod
    def show_balance(account_no):
        """Show current balance"""
        account = AccountRepository.get_account(account_no)
        if not account:
            print("❌ Account not found")
            return
        
        print(f"Current Balance: ₹ {account['Balance']}")


# ============================================
# MODULE 5: ACCOUNT DETAILS & TRANSACTIONS
# ============================================
class AccountDetails:
    @staticmethod
    def load_transactions():
        """Load all transactions"""
        transactions = defaultdict(list)
        try:
            with open(TRANSACTIONS_FILE, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row:
                        transactions[row["AccountNo"]].append(row)
        except:
            pass
        return transactions
    
    @staticmethod
    def display_account(account_no):
        """Display account details"""
        account = AccountRepository.get_account(account_no)
        if not account:
            print("❌ Account not found")
            return
        
        print("\n" + "="*50)
        print("         ACCOUNT DETAILS")
        print("="*50)
        print(f"Full Name     : {account['FullName']}")
        print(f"DOB           : {account['DOB']}")
        print(f"Phone Number  : {account['PhoneNumber']}")
        print(f"Email ID      : {account['EmailId']}")
        print(f"Account No    : {account['AccountNo']}")
        print(f"Customer ID   : {account['CustomerID']}")
        print(f"Account Type  : {account['AccountType']}")
        print(f"Balance       : ₹ {account['Balance']}")
        print(f"Status        : {account['Status']}")
        print("="*50)
    
    @staticmethod
    def display_transactions(account_no):
        """Display transaction history"""
        transactions = AccountDetails.load_transactions()
        txn_list = transactions.get(account_no, [])
        
        if not txn_list:
            print("\n❌ No transactions found")
            return
        
        print("\n" + "="*50)
        print("     TRANSACTION HISTORY")
        print("="*50)
        
        txn_list_sorted = sorted(txn_list, key=lambda x: x["Date"], reverse=True)
        
        for txn in txn_list_sorted:
            symbol = "➕" if txn["TransactionType"].lower() == "deposit" else "➖"
            print(f"{symbol} {txn['TransactionType']} | ₹ {txn['Amount']} | {txn['Date']} {txn['Time']}")
        
        print("="*50)


# ============================================
# MODULE 6: ACCOUNT DELETION
# ============================================
class AccountDeletion:
    @staticmethod
    def deactivate_account(account_no, pin):
        """Deactivate account"""
        accounts = AccountRepository.load_accounts()
        
        if account_no not in accounts:
            print("❌ Account does not exist")
            return False
        
        account = accounts[account_no]
        if account["Pin"] != pin:
            print("❌ Incorrect PIN")
            return False
        
        account["Status"] = "Deactivated"
        
        with open(ACCOUNTS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=account.keys())
            writer.writeheader()
            for acc_no, acc_data in accounts.items():
                writer.writerow(acc_data)
        
        print("✅ Account deactivated successfully")
        return True
    
    @staticmethod
    def delete_account(account_no, pin):
        """Delete account"""
        accounts = AccountRepository.load_accounts()
        
        if account_no not in accounts:
            print("❌ Account does not exist")
            return False
        
        account = accounts[account_no]
        if account["Pin"] != pin:
            print("❌ Incorrect PIN")
            return False
        
        if account["Status"] != "Deactivated":
            print("❌ Account must be deactivated first")
            return False
        
        del accounts[account_no]
        
        with open(ACCOUNTS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(accounts.values())[0].keys() if accounts else [])
            writer.writeheader()
            for acc_data in accounts.values():
                writer.writerow(acc_data)
        
        print("✅ Account permanently deleted")
        return True


# ============================================
# MAIN BANKING SYSTEM
# ============================================
class BankingSystem:
    def __init__(self):
        AccountRepository.initialize_files()
        self.current_user = None
    
    def main_menu(self):
        """Main menu"""
        while True:
            print("\n" + "="*55)
            print("    WELCOME TO ACHITHA BANKING LIMITED")
            print("="*55)
            print("1. Check Eligibility & Create Account")
            print("2. Login to Account")
            print("3. Exit")
            print("="*55)
            
            choice = input("Enter choice (1-3): ").strip()
            
            if choice == "1":
                self.eligibility_and_account_creation()
            elif choice == "2":
                self.login_menu()
            elif choice == "3":
                print("\n✅ Thank you for banking with Achitha Banking Limited!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def eligibility_and_account_creation(self):
        """Check eligibility and create account"""
        aadhaar = EligibilityChecker.check_eligibility()
        if aadhaar is None:
            return
        
        print("\n" + "="*55)
        print("     ENTER ACCOUNT DETAILS")
        print("="*55)
        
        name = input("Full Name: ").strip()
        dob = input("Date of Birth (DD/MM/YYYY): ").strip()
        phone = input("Phone Number: ").strip()
        email = input("Email ID: ").strip()
        
        print("\nAccount Types: 1. Savings  2. Current  3. Business")
        acc_type_choice = input("Select Account Type (1-3): ").strip()
        acc_types = {"1": "Savings", "2": "Current", "3": "Business"}
        acc_type = acc_types.get(acc_type_choice, "Savings")
        
        pin = input("Set PIN (4 digits): ").strip()
        opening_balance = float(input("Opening Balance (₹): ").strip())
        
        if len(pin) != 4 or not pin.isdigit():
            print("❌ PIN must be 4 digits")
            return
        
        account_no = AccountCreator.create_account(name, dob, phone, email, acc_type, pin, opening_balance)
        print(f"\n💡 Save your Account Number: {account_no}")
    
    def login_menu(self):
        """Login and access account"""
        print("\n" + "="*55)
        print("     LOGIN")
        print("="*55)
        
        account_no = input("Account Number: ").strip()
        password = input("PIN: ").strip()
        
        if not LoginSecurity.login(account_no, password):
            return
        
        self.account_operations(account_no)
    
    def account_operations(self, account_no):
        """Account operations menu"""
        while True:
            print("\n" + "="*55)
            print("     ACCOUNT OPERATIONS")
            print("="*55)
            print("1. View Account Details")
            print("2. View Transaction History")
            print("3. Deposit Money")
            print("4. Show Balance")
            print("5. Change PIN")
            print("6. Deactivate Account")
            print("7. Delete Account")
            print("8. Logout")
            print("="*55)
            
            choice = input("Enter choice (1-8): ").strip()
            
            if choice == "1":
                AccountDetails.display_account(account_no)
            elif choice == "2":
                AccountDetails.display_transactions(account_no)
            elif choice == "3":
                amount = float(input("Enter amount to deposit: ").strip())
                DepositSystem.deposit_money(account_no, amount)
            elif choice == "4":
                DepositSystem.show_balance(account_no)
            elif choice == "5":
                old_pin = input("Enter old PIN: ").strip()
                new_pin = input("Enter new PIN: ").strip()
                LoginSecurity.change_password(account_no, old_pin, new_pin)
            elif choice == "6":
                pin = input("Enter PIN to confirm: ").strip()
                AccountDeletion.deactivate_account(account_no, pin)
            elif choice == "7":
                pin = input("Enter PIN to confirm: ").strip()
                AccountDeletion.delete_account(account_no, pin)
            elif choice == "8":
                LoginSecurity.logout()
                break
            else:
                print("❌ Invalid choice")


# ============================================
# RUN BANKING SYSTEM
# ============================================
if __name__ == "__main__":
    bank = BankingSystem()
    bank.main_menu()