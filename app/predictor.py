import os
from pathlib import Path

import joblib

from app.repository_features import get_repository_features


MODEL_PATH = Path(
    os.environ.get(
        "BUILD_FAILURE_MODEL_PATH",
        "/var/jenkins_home/models/random_forest_build_failure_model.pkl"
    )
)


def predict_repository_failure(repo_url):
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    model = joblib.load(MODEL_PATH)

    features = get_repository_features(repo_url)

    probability = model.predict_proba(features)[0]

    classes = [int(value) for value in model.classes_]

    failure_probability = float(
        probability[classes.index(1)]
    )

    prediction = int(model.predict(features)[0])

    return {
        "repository": repo_url,
        "prediction": "FAILURE" if prediction == 1 else "SUCCESS",
        "failure_probability": failure_probability,
        "features": features
    }


if __name__ == "__main__":
    url = input("Enter GitHub repository URL: ").strip()

    result = predict_repository_failure(url)

    print("\nBUILD FAILURE PREDICTION")
    print("-----------------------------")
    print("Repository:", result["repository"])
    print("Prediction:", result["prediction"])
    print(
        "Failure probability:",
        f"{result['failure_probability']:.2%}"
    )
    print("-----------------------------")
