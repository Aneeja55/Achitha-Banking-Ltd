import csv
from datetime import datetime
import os

class DepositSystem:
    def __init__(self, balance, filepath):
        self.balance = balance
        self.filepath = filepath

    def deposit_money(self, amount):
        if amount <= 0:
            print("❌ Invalid amount! Deposit must be positive.")
            return False
        
        self.update_balance(amount)
        self.update_csv(amount)
        print("✅ Amount deposited successfully.")
        return True

    def update_balance(self, amount):
        self.balance += amount

    def update_csv(self, amount):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        with open(self.filepath, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date, time, amount, self.balance])

    def show_balance(self):
        print(f"💰 Updated balance: ₹ {self.balance}")
        return self.balance
