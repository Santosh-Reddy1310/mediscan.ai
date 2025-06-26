import re

# ------------------- DIABETES FEATURES -------------------

def extract_glucose(text):
    match = re.search(r"glucose(?:\s*level)?(?:\s*of)?\s*[:\-]?\s*(\d+\.?\d*)\s*(mg/dl)?", text.lower())
    return float(match.group(1)) if match else None

def extract_blood_pressure(text):
    # Extracts only the first (systolic) value
    match = re.search(r"blood[\s_]?pressure(?:\s*reading)?(?:\s*was)?(?:\s*recorded)?(?:\s*at)?\s*[:\-]?\s*(\d+)(?:/\d+)?\s*mmhg", text.lower())
    return int(match.group(1)) if match else None

def extract_bmi(text):
    match = re.search(r"bmi(?:\s*index)?(?:\s*calculated\s*to)?\s*[:\-]?\s*(\d+\.?\d*)", text.lower())
    return float(match.group(1)) if match else None

def extract_age(text):
    match = re.search(r"age(?:\s*of)?\s*[:\-]?\s*(\d+)", text.lower())
    if match:
        return int(match.group(1))
    # Try to extract from phrase like "a 34-year-old"
    match = re.search(r"(\d+)[-\s]?year[-\s]?old", text.lower())
    return int(match.group(1)) if match else None

def extract_insulin(text):
    match = re.search(r"insulin(?:\s*levels?)?(?:\s*at)?\s*[:\-]?\s*(\d+\.?\d*)\s*(μu/ml|uU/ml|uU\/ml)?", text.lower())
    return float(match.group(1)) if match else None

def extract_skin_thickness(text):
    match = re.search(r"skin[\s_]?thickness(?:\s*of)?\s*[:\-]?\s*(\d+\.?\d*)\s*mm", text.lower())
    return float(match.group(1)) if match else None

def extract_pregnancies(text):
    # Try "history of 2 pregnancies" or "pregnancies: 2"
    match = re.search(r"history of (\d+) pregnancies", text.lower())
    if match:
        return int(match.group(1))
    match = re.search(r"pregnancies\s*[:\-]?\s*(\d+)", text.lower())
    return int(match.group(1)) if match else None

def extract_diabetes_pedigree(text):
    match = re.search(r"diabetes[\s_]?pedigree[\s_]?function(?:\s*(?:yielded|score|of|at|:|=))?\s*[:\-]?\s*(\d+\.?\d*)", text.lower())
    return float(match.group(1)) if match else None

# ------------------- BREAST CANCER FEATURES -------------------

def extract_radius_mean(text):
    match = re.search(r"radius[_\s]?mean(?:\s*measurement)?(?:\s*was)?(?:\s*documented)?(?:\s*at)?\s*[:\-]?\s*(\d+\.?\d*)\s*mm", text.lower())
    return float(match.group(1)) if match else None

def extract_texture_mean(text):
    match = re.search(r"texture[_\s]?mean(?:\s*values)?(?:\s*of)?(?:\s*at)?\s*[:\-]?\s*(\d+\.?\d*)", text.lower())
    return float(match.group(1)) if match else None

def extract_perimeter_mean(text):
    match = re.search(r"perimeter[_\s]?mean(?:\s*calculations)?(?:\s*showed)?(?:\s*at)?\s*[:\-]?\s*(\d+\.?\d*)\s*mm", text.lower())
    return float(match.group(1)) if match else None

def extract_area_mean(text):
    match = re.search(r"area[_\s]?mean(?:\s*was)?(?:\s*measured)?(?:\s*at)?\s*[:\-]?\s*(\d+\.?\d*)\s*mm[²2]", text.lower())
    return float(match.group(1)) if match else None

def extract_smoothness_mean(text):
    match = re.search(r"smoothness[_\s]?mean(?:\s*parameter)?(?:\s*was)?(?:\s*recorded)?(?:\s*as)?\s*[:\-]?\s*(\d+\.?\d*)", text.lower())
    return float(match.group(1)) if match else None

# ------------------- COMBINED WRAPPER -------------------

def extract_all_features(text):
    return {
        # Diabetes
        "glucose": extract_glucose(text),
        "blood_pressure": extract_blood_pressure(text),
        "bmi": extract_bmi(text),
        "age": extract_age(text),
        "insulin": extract_insulin(text),
        "skin_thickness": extract_skin_thickness(text),
        "pregnancies": extract_pregnancies(text),
        "dpf": extract_diabetes_pedigree(text),
        
        # Breast Cancer
        "radius_mean": extract_radius_mean(text),
        "texture_mean": extract_texture_mean(text),
        "perimeter_mean": extract_perimeter_mean(text),
        "area_mean": extract_area_mean(text),
        "smoothness_mean": extract_smoothness_mean(text),
    }
