class acc:
    def __init__(self, acc_no, cust_id, name, dob, phone, email, acc_type, pin, balance):
        self.acc_no = acc_no
        self.cust_id = cust_id
        self.name = name
        self.dob = dob
        self.phone = phone
        self.email = email
        self.acc_type = acc_type
        self.pin = pin
        self.balance = balance
        self.status = "Active"

    def __str__(self):
        return (
            "\n--- ACCOUNT CREATED SUCCESSFULLY ---"
            f"\nFull Name    : {self.name}"
            f"\nCustomer ID : {self.cust_id}"
            f"\nAccount No  : {self.acc_no}"
            f"\nAccount Type: {self.acc_type}"
            f"\nAccount Pin : {self.pin}"
            f"\nBalance     : {self.balance}"
            f"\nStatus      : {self.status}"
        )
