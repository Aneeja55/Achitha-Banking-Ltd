import cv2
import pytesseract
import re
from datetime import datetime

# --------------------------------------------------
# VERHOEFF ALGORITHM TABLES (For Aadhaar Validation)
# --------------------------------------------------

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


# ==================================================
#              BANK ELIGIBILITY SYSTEM
# ==================================================

print("="*55)
print("        BANK ACCOUNT ELIGIBILITY SYSTEM")
print("="*55)

# --------------------------------------------------
# STEP 1: Load Image
# --------------------------------------------------

print("\n📄 Reading Aadhaar Document...")

image_path = "aadhar.jpeg"   # Make sure filename matches exactly
image = cv2.imread(image_path)

if image is None:
    print("❌ Image not found. Keep aadhar.jpeg in this folder.")
    exit()

print("✅ Document Loaded Successfully")


# --------------------------------------------------
# STEP 2: Preprocess (Resize Only - No Damage)
# --------------------------------------------------

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Resize for better OCR accuracy
gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
text = pytesseract.image_to_string(gray)


# --------------------------------------------------
# STEP 3: Extract Aadhaar Number
# --------------------------------------------------

print("\n🔎 Extracting Aadhaar Number...")

aadhaar_match = re.findall(r'\d{4}\s\d{4}\s\d{4}', text)

if not aadhaar_match:
    print("❌ Aadhaar Number Not Found")
    exit()

aadhaar_display = aadhaar_match[0]
aadhaar_number = aadhaar_display.replace(" ", "")

print(f"✅ Aadhaar Detected: {aadhaar_display}")


# --------------------------------------------------
# STEP 4: Validate Aadhaar
# --------------------------------------------------

print("\n🔐 Validating Aadhaar Number...")

if validate_verhoeff(aadhaar_number):
    print("✅ Aadhaar is Mathematically Valid")
else:
    print("❌ Aadhaar Failed Validation")
    exit()


# --------------------------------------------------
# STEP 5: Manual DOB Entry (Reliable)
# --------------------------------------------------

print("\n📅 Date of Birth Verification")
print("-"*40)

dob = input("Enter DOB (DD/MM/YYYY): ")

try:
    birth_date = datetime.strptime(dob, "%d/%m/%Y")
except:
    print("❌ Invalid DOB Format")
    exit()

today = datetime.today()
age = today.year - birth_date.year - (
    (today.month, today.day) < (birth_date.month, birth_date.day)
)

print(f"🎂 Calculated Age: {age} years")


# --------------------------------------------------
# FINAL ELIGIBILITY RESULT
# --------------------------------------------------

print("\n" + "="*55)

if age >= 18:
    print("🎉 RESULT: CUSTOMER IS ELIGIBLE")
    print("✔ Age Criteria Satisfied (18+)")
else:
    print("❌ RESULT: CUSTOMER IS NOT ELIGIBLE")
    print("✖ Age Below 18")

print("="*55)
print("        VERIFICATION COMPLETE")
print("="*55)
