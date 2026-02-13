class account_repo:
    def __init__(self, file_path):
        self.file_path = file_path


        try:
            f = open(self.file_path, "x")
            f.write(
                "FullName,DOB,PhoneNumber,EmailId,"
                "AccountNo,CustomerID,AccountType,Pin,Balance,Status\n"
            )
            f.close()
        except FileExistsError:
            pass

    def save_account(self, account):
        f = open(self.file_path, "a")
        f.write(
            f"{account.name},"
            f"{account.dob},"
            f"{account.phone},"
            f"{account.email},"
            f"{account.acc_no},"
            f"{account.cust_id},"
            f"{account.acc_type},"
            f"{account.pin},"
            f"{account.balance},"
            f"{account.status}\n"
        )
        f.close()


    def get_last_ids(self):
        try:
            f = open(self.file_path, "r")
            lines = f.readlines()
            f.close()

            if len(lines) <= 1:
                return 5000, 1000  # starting values

            last = lines[-1].strip().split(",")

            last_acc_no = int(last[4][1:])   # remove 'A'
            last_cust_id = int(last[5][1:])  # remove 'C'

            return last_acc_no, last_cust_id

        except:
            return 5000, 1000
