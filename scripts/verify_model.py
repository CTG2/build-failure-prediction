import os
from pathlib import Path

import joblib
import pandas as pd


MODEL_PATH = Path(
    os.environ.get(
        "BUILD_FAILURE_MODEL_PATH",
        "/var/jenkins_home/models/random_forest_build_failure_model.pkl"
    )
)

FEATURE_COLUMNS = [
    "stars",
    "forks",
    "repo_age_days",
    "days_since_last_push",
    "Ant",
    "Buildr",
    "Gradle",
    "Make",
    "Maven",
    "SBT",
    "Ivy",
    "Eclipse",
    "IntelliJ IDEA",
    "NetBeans",
    "Travis CI",
    "Git submodules",
    "tool"
]

# Mapping used during model training:
# 0 = Successful build (T)
# 1 = Failed build (F)
FAILURE_CLASS = 1


def verify_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    print("Loading Random Forest model...")

    model = joblib.load(MODEL_PATH)

    actual_features = list(model.feature_names_in_)

    if actual_features != FEATURE_COLUMNS:
        raise ValueError(
            "Model feature columns do not match expected columns.\n"
            f"Expected: {FEATURE_COLUMNS}\n"
            f"Found: {actual_features}"
        )

    classes = [int(value) for value in model.classes_]

    if set(classes) != {0, 1}:
        raise ValueError(
            f"Unexpected model classes: {classes}"
        )

    sample = {
        "stars": 1000,
        "forks": 100,
        "repo_age_days": 1500,
        "days_since_last_push": 30,
        "Ant": 0,
        "Buildr": 0,
        "Gradle": 0,
        "Make": 0,
        "Maven": 1,
        "SBT": 0,
        "Ivy": 0,
        "Eclipse": 0,
        "IntelliJ IDEA": 0,
        "NetBeans": 0,
        "Travis CI": 1,
        "Git submodules": 0,
        "tool": "Maven"
    }

    input_data = pd.DataFrame(
        [sample],
        columns=FEATURE_COLUMNS
    )

    probabilities = model.predict_proba(input_data)[0]

    failure_index = classes.index(FAILURE_CLASS)
    failure_probability = probabilities[failure_index]

    prediction = int(model.predict(input_data)[0])

    predicted_status = (
        "FAILURE" if prediction == 1 else "SUCCESS"
    )

    print("\nMODEL VERIFICATION SUCCESSFUL")
    print("--------------------------------")
    print(f"Model path: {MODEL_PATH}")
    print(f"Model classes: {classes}")
    print(f"Predicted class: {prediction}")
    print(f"Predicted build status: {predicted_status}")
    print(
        f"Build failure probability: {failure_probability:.2%}"
    )
    print("--------------------------------")
    print("Model loaded and test inference completed.")


if __name__ == "__main__":
    verify_model()
