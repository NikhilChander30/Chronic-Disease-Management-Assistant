# bilstm_model.py
# Simulated Bi-Directional LSTM Disease Prediction (Rule-based)

def predict_disease(symptoms_text):
    text = symptoms_text.lower()

    # Fever
    if any(word in text for word in ["fever", "temperature", "high temp", "chills", "Dizzy"]):
        return "fever"

    # Diabetes
    elif any(word in text for word in ["diabetes", "sugar", "blood sugar", "frequent urination", "thirst"]):
        return "diabetes"

    # Hypertension
    elif any(word in text for word in ["bp", "blood pressure", "hypertension", "dizziness"]):
        return "hypertension"

    # Asthma
    elif any(word in text for word in ["asthma", "breathing", "shortness of breath", "wheezing"]):
        return "asthma"

    # Migraine
    elif any(word in text for word in ["migraine", "headache", "nausea", "light sensitivity", "Head Pain"]):
        return "migraine"

    # Allergy
    elif any(word in text for word in ["allergy", "itching", "sneezing", "rashes"]):
        return "allergy"

    # Cold
    elif any(word in text for word in ["cold", "runny nose", "sore throat", "cough", "throat pain"]):
        return "cold"

    # Flu
    elif any(word in text for word in ["flu", "body pain", "fatigue", "viral", "tiredness"]):
        return "flu"

    # Arthritis
    elif any(word in text for word in ["arthritis", "joint pain", "stiffness", "swelling"]):
        return "arthritis"

    # Thyroid
    elif any(word in text for word in ["thyroid", "weight gain", "weight loss", "hormone"]):
        return "thyroid"

    # Stomach Pain
    elif any(word in text for word in ["stomach pain", "abdominal", "gas", "acidity", "Stomach is aching"]):
        return "stomach pain"

    # Back Pain
    elif any(word in text for word in ["back pain", "spine", "lower back", "muscle pain"]):
        return "back pain"

    # Skin Infection
    elif any(word in text for word in ["skin infection", "boils", "redness", "pus"]):
        return "skin infection"

    # Overweight / Obesity
    elif any(word in text for word in ["overweight", "obesity", "weight gain", "fat"]):
        return "overweight"

    # Default fallback
    else:
        return "Visit the doctor immediately"
