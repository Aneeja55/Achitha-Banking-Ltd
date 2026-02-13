from Account_Creation.account_repo import AccountRepository

class AccountDeletion:

    @staticmethod
    def deactivate_account(account_no, pin):
        accounts = AccountRepository.load_accounts()

        if account_no not in accounts:
            print("Account not found.")
            return False

        if accounts[account_no]["Pin"] != pin:
            print("Incorrect PIN.")
            return False

        accounts[account_no]["Status"] = "Deactivated"

        AccountRepository.update_balance(account_no, accounts[account_no]["Balance"])
        print("Account deactivated.")
        return True
