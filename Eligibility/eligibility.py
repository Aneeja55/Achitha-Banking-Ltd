import re
import cv2
import pytesseract
import re
from datetime import datetime

# ================= VERHOEFF =================

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
    c = 0
    number = number[::-1]
    for i in range(len(number)):
        c = d[c][p[i % 8][int(number[i])]]
    return c == 0


class EligibilityChecker:

    @staticmethod
    def check_eligibility():
        print("\n===== ELIGIBILITY CHECK =====")

        manual = input("Enter Aadhaar manually? (yes/no): ").lower()

        if manual == "yes":
            aadhaar = input("Enter Aadhaar (12 digits): ").replace(" ", "")
        else:
            image_path = input("Enter Aadhaar image path: ")
            image = cv2.imread(image_path)
            if image is None:
                print("Image not found.")
                return None

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
            match = re.findall(r'\d{4}\s\d{4}\s\d{4}', text)

            if not match:
                print("Aadhaar not found.")
                return None

            aadhaar = match[0].replace(" ", "")

        if len(aadhaar) != 12 or not validate_verhoeff(aadhaar):
            print("Invalid Aadhaar.")
            return None

        dob = input("Enter DOB (DD/MM/YYYY): ")

        try:
            birth = datetime.strptime(dob, "%d/%m/%Y")
        except:
            print("Invalid DOB.")
            return None

        today = datetime.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

        if age < 18:
            print("Not eligible.")
            return None

        print("Eligible for account creation.")
        return aadhaar


if __name__ == "__main__":
    EligibilityChecker.check_eligibility()
