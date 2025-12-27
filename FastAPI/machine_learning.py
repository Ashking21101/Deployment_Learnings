import pandas as pd
import numpy as np
import joblib



from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# =========================
# 1. LOAD DATA
# =========================
df = pd.read_excel("/Users/ashishtak/FastAPI_Tutorial/insurance_dataset_100_records_raw (1).xlsx")

# =========================
# 2. FEATURE ENGINEERING 
# =========================

# BMI
df["bmi"] = df["weight"] / (df["height"] ** 2)

# Age Group
def age_group(age):
    if age < 30:
        return "young"
    elif age < 55:
        return "middle_aged"
    else:
        return "senior"

df["age_group"] = df["age"].apply(age_group)

# Lifestyle Risk
def lifestyle_risk(row):
    if row["smoker"] and row["bmi"] > 30:
        return "high"
    elif row["smoker"] or row["bmi"] > 27:
        return "medium"
    else:
        return "low"

df["lifestyle_risk"] = df.apply(lifestyle_risk, axis=1)

# City Tier
city_tier_map = {
    "Mumbai": 1,
    "Delhi": 1,
    "Bangalore": 1,
    "Pune": 2,
    "Lucknow": 2
}

df["city_tier"] = df["city"].map(city_tier_map)

# =========================
# 3. ENCODING
# =========================
label_encoders = {}

categorical_cols = [
    "smoker",
    "city",
    "occupation",
    "age_group",
    "lifestyle_risk"
]

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Encode target
target_encoder = LabelEncoder()
df["insurance_premium_category"] = target_encoder.fit_transform(
    df["insurance_premium_category"]
)

# =========================
# 4. TRAIN / TEST SPLIT
# =========================
X = df.drop("insurance_premium_category", axis=1)
y = df["insurance_premium_category"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 5. MODEL TRAINING
# =========================
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# =========================
# 6. EVALUATION
# =========================
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# =========================
# 7. SAMPLE PREDICTION
# =========================
sample = X_test.iloc[0:1]
pred = model.predict(sample)

print("\nSample Prediction:", target_encoder.inverse_transform(pred))



joblib.dump(model, "model.pkl")
joblib.dump(label_encoders, "encoders.pkl")
joblib.dump(target_encoder, "target_encoder.pkl")
