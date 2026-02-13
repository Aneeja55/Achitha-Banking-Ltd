from acc import acc

class acc_creator:
    def __init__(self, repository):
        self.repository = repository

        last_acc, last_cust = self.repository.get_last_ids()
        self.next_account_no = last_acc
        self.next_customer_id = last_cust


    def generate_account_no(self):
        self.next_account_no += 1
        return f"A{self.next_account_no}"

    def generate_customer_id(self):
        self.next_customer_id += 1
        return f"C{self.next_customer_id}"

    def create_account(self, name, dob, phone, email, acc_type, pin, opening_balance):
        acc_no = self.generate_account_no()
        cust_id = self.generate_customer_id()

        account = acc(
            acc_no,
            cust_id,
            name,
            dob,
            phone,
            email,
            acc_type,
            pin,
            opening_balance
        )

        self.repository.save_account(account)
        return account
