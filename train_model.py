
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# =========================================================
# 1. LOAD DATASET
# =========================================================

DATA_FILE = "heart_disease.csv"
MODEL_FILE = "heart_model.pkl"

df = pd.read_csv(DATA_FILE)

print("\n================ DATASET ================")
print("Rows:", len(df))
print("Columns:", list(df.columns))

print("\nTarget distribution:")
print(df["target"].value_counts().sort_index())


# =========================================================
# 2. CHECK REQUIRED COLUMNS
# =========================================================

FEATURES = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal"
]

REQUIRED_COLUMNS = FEATURES + ["target"]

missing_columns = [
    column for column in REQUIRED_COLUMNS
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )


# =========================================================
# 3. PREPARE X AND y
# =========================================================

X = df[FEATURES].copy()
y = df["target"].astype(int)


# =========================================================
# 4. TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\n================ SPLIT ================")
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))


# =========================================================
# 5. TRAIN RANDOM FOREST
# =========================================================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)


# =========================================================
# 6. TEST MODEL
# =========================================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n================ MODEL RESULT ================")
print(
    f"Test Accuracy: {accuracy * 100:.2f}%"
)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# =========================================================
# 7. TRAIN FINAL MODEL USING ALL DATA
# =========================================================
#
# For your small demonstration dataset, after evaluating
# the model above, train the final saved model using all
# available records.
#
# This gives the final model access to all 30 rows.
# =========================================================

final_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

final_model.fit(X, y)


# =========================================================
# 8. SAVE MODEL
# =========================================================

joblib.dump(
    final_model,
    MODEL_FILE
)

print("\n================ COMPLETE ================")
print(
    f"Model saved successfully as: {MODEL_FILE}"
)
