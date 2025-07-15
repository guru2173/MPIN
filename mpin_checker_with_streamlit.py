
import streamlit as st

# PART A: Commonly Used MPINs
COMMON_MPINS = {
    "1234", "0000", "1111", "1212", "1122", "2222", "3333",
    "4444", "5555", "6666", "7777", "8888", "9999", "4321"
}

def is_commonly_used_mpin(mpin):
    return mpin in COMMON_MPINS

# PART B: Strength Check Based on Demographics (WEAK/STRONG)
def get_date_variants(date_str):
    if not date_str:
        return []
    try:
        day, month, year = date_str.split("-")
        y2 = year[-2:]
        return [
            day + month, month + day,
            day + y2, y2 + day,
            month + y2, y2 + month,
            year, y2
        ]
    except Exception:
        return []

# PART C: Full Evaluation with Reasons
def evaluate_mpin_full(mpin, dob=None, spouse_dob=None, anniversary=None):
    reasons = []
    if is_commonly_used_mpin(mpin):
        reasons.append("COMMONLY_USED")
    if mpin in get_date_variants(dob):
        reasons.append("DEMOGRAPHIC_DOB_SELF")
    if mpin in get_date_variants(spouse_dob):
        reasons.append("DEMOGRAPHIC_DOB_SPOUSE")
    if mpin in get_date_variants(anniversary):
        reasons.append("DEMOGRAPHIC_ANNIVERSARY")
    strength = "WEAK" if reasons else "STRONG"
    return {"strength": strength, "reasons": reasons}

# PART D: Valid MPIN Length
def is_valid_mpin(mpin):
    return mpin.isdigit() and len(mpin) in [4, 6]

# PART E: Test Cases
def run_all_tests():
    test_cases = [
        ("1234", "02-01-1998", "15-08-1995", "09-09-2020"),
        ("0201", "02-01-1998", None, None),
        ("9802", "02-01-1998", None, None),
        ("1508", None, "15-08-1995", None),
        ("0909", None, None, "09-09-2020"),
        ("4567", "02-01-1998", "15-08-1995", "09-09-2020"),
        ("1313", None, None, None),
        ("1998", "02-01-1998", None, None),
        ("0801", None, "01-08-1992", None),
        ("000000", "02-01-1998", None, None),
        ("199801", "02-01-1998", None, None),
        ("0198", "02-01-1998", None, None),
        ("020119", "02-01-1998", None, None),
        ("876543", None, None, None),
        ("0101", "01-01-2000", None, None),
        ("6666", None, None, None),
        ("1122", None, None, None),
        ("0000", None, None, None),
        ("1999", None, None, "01-01-1999"),
        ("010199", None, None, "01-01-1999"),
    ]
    for i, (mpin, dob, spouse_dob, anniv) in enumerate(test_cases, 1):
        if not is_valid_mpin(mpin):
            print(f"Test {i:02}: MPIN={mpin} ➜ INVALID LENGTH")
            continue
        result = evaluate_mpin_full(mpin, dob, spouse_dob, anniv)
        print(f"Test {i:02}: MPIN={mpin} ➜ {result}")

# ------------------- Streamlit UI -------------------

st.title("🔐 MPIN Strength Checker")

mpin = st.text_input("Enter MPIN (4 or 6 digits)", max_chars=6)
dob = st.text_input("Your DOB (DD-MM-YYYY)", placeholder="e.g. 02-01-1998")
spouse_dob = st.text_input("Spouse DOB (DD-MM-YYYY)", placeholder="optional")
anniversary = st.text_input("Anniversary (DD-MM-YYYY)", placeholder="optional")

if st.button("Check Strength"):
    if not is_valid_mpin(mpin):
        st.error("MPIN must be 4 or 6 digits.")
    else:
        result = evaluate_mpin_full(mpin, dob, spouse_dob, anniversary)
        st.markdown(f"**Strength:** `{result['strength']}`")
        if result["reasons"]:
            st.markdown("**Reasons:**")
            for r in result["reasons"]:
                st.write(f"- {r}")
        else:
            st.success("MPIN is strong and not guessable from common patterns or your data.")
