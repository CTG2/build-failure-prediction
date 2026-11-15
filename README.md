# Design Build Failure Prediction Using Random Forest

## 1. Project Overview

**Design Build Failure Prediction Using Random Forest** is a Machine Learning and DevOps project that predicts the likelihood of build failures in Java software repositories.

The project integrates a trained Random Forest classification model with Jenkins Continuous Integration (CI). It extracts repository information from GitHub, processes the extracted features using the ML model, predicts the build outcome and compares the prediction with an actual Maven build.

The objective is to demonstrate how Machine Learning can support software development and DevOps workflows through automated build outcome prediction.

### Key Features

- Automatic extraction of GitHub repository information.
- Identification of repository build tools and development configurations.
- Random Forest classification for build outcome prediction.
- Calculation of build failure probability.
- Jenkins pipeline automation.
- Automated Python dependency installation and testing.
- Actual Java project checkout and Maven build execution.
- Comparison between ML predictions and actual build results.

---

## 2. Problem Statement

Build failures can interrupt software development, delay integration and increase debugging effort.

Traditional Continuous Integration systems identify build failures when a build is executed. This project explores the use of Machine Learning to predict possible build outcomes using repository-level characteristics.

A trained Random Forest classifier analyses historical Java software build data and predicts one of two outcomes:

- **SUCCESS:** The model predicts a successful build.
- **FAILURE:** The model predicts a failed build.

The prediction is integrated into a Jenkins pipeline and compared against the result of an actual Maven build.

---

## 3. System Architecture

The project consists of four main components:

1. **Repository Feature Extraction:** Retrieves repository metadata and examines files and folders through the GitHub REST API.
2. **Machine Learning Prediction:** Loads the trained Random Forest model and calculates the predicted build outcome and failure probability.
3. **Jenkins Automation:** Executes project checks, dependency installation, Python tests, model verification and repository prediction.
4. **Actual Build Comparison:** Clones a Java repository, executes Maven and compares its actual result with the model prediction.

### Architecture Diagram

```text
             GitHub Java Repository
                       |
                       v
             GitHub REST API
                       |
                       v
          Repository Feature Extraction
                       |
                       v
                17 Input Features
                       |
                       v
             Random Forest Model
                       |
                       v
              Build Prediction
                       |
                       v
              Failure Probability
                       |
                       v
               Jenkins Pipeline
                       |
              +--------+--------+
              |                 |
              v                 v
        Python Tests       Clone Repository
              |                 |
              v                 v
        Model Check          Maven Build
              |                 |
              +--------+--------+
                       |
                       v
             Prediction Comparison
                       |
                       v
               Final Build Result
```

---

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development and ML inference |
| Scikit-learn | Random Forest classification |
| Pandas | Feature preparation |
| NumPy | Numerical processing |
| Joblib | Model loading |
| Requests | GitHub API communication |
| Pytest | Automated Python testing |
| Git | Version control |
| GitHub | Source code hosting |
| Jenkins | CI pipeline automation |
| Docker | Jenkins container environment |
| Java JDK 21 | Java build environment |
| Apache Maven 3.9.9 | Java project build execution |
| PowerShell | Local development commands |

---

## 5. Machine Learning Model

### Algorithm

The project uses a **Random Forest Classifier**. Random Forest is an ensemble machine learning algorithm that combines multiple decision trees to perform classification.

The trained model is stored as a Scikit-learn Pipeline and loaded using Joblib.

### Model Configuration

- Algorithm: Random Forest Classifier
- Number of estimators: 500
- Number of input features: 17
- Classification type: Binary classification
- Scikit-learn version: 1.6.1
- Model serialization: Joblib

### Classification Mapping

| Numeric Class | Predicted Outcome |
|---|---|
| 0 | SUCCESS |
| 1 | FAILURE |

### Input Features

The model uses 17 repository-level features:

| No. | Feature | Description |
|---:|---|---|
| 1 | stars | GitHub repository star count |
| 2 | forks | GitHub repository fork count |
| 3 | repo_age_days | Repository age in days |
| 4 | days_since_last_push | Days since the latest repository push |
| 5 | Ant | Ant build tool indicator |
| 6 | Buildr | Buildr build tool indicator |
| 7 | Gradle | Gradle build tool indicator |
| 8 | Make | Make build tool indicator |
| 9 | Maven | Maven build tool indicator |
| 10 | SBT | SBT build tool indicator |
| 11 | Ivy | Apache Ivy indicator |
| 12 | Eclipse | Eclipse configuration indicator |
| 13 | IntelliJ IDEA | IntelliJ IDEA configuration indicator |
| 14 | NetBeans | NetBeans configuration indicator |
| 15 | Travis CI | Travis CI configuration indicator |
| 16 | Git submodules | Git submodule configuration indicator |
| 17 | tool | Detected build tool category |

The feature extractor prepares these inputs in the column order expected by the trained model.

### Model Evaluation Results

The model was evaluated using repository-grouped training, validation and testing splits.

| Dataset Split | Records |
|---|---:|
| Training | 10,340 |
| Validation | 2,076 |
| Testing | 2,066 |
| Total labelled records | 14,482 |

The recorded evaluation results are:

| Metric | Result |
|---|---:|
| Accuracy | 60.31% |
| Failure Precision | 60.92% |
| Failure Recall | 57.50% |
| Failure F1-Score | 59.16% |
| ROC-AUC | 0.6425 |

---

## 6. Dataset

The project uses the historical Java software build dataset described in the following research publication:

**Sulír et al. (2020), Large-Scale Dataset of Local Java Software Build Results, Data, 5(3), Article 86.**

Research paper: https://doi.org/10.3390/data5030086  
OSF dataset: https://doi.org/10.17605/OSF.IO/UMK3W

### Dataset Summary

| Category | Records |
|---|---:|
| Successful builds | 7,423 |
| Failed builds | 7,059 |
| Total labelled records | 14,482 |
| Unlabelled records excluded | 5,518 |

The dataset provides historical local Java software build outcomes and repository-related characteristics for model development and evaluation.

---

## 7. Project Folder Structure

```text
build-failure-prediction/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── repository_features.py
│   └── predictor.py
│
├── data/
├── ml/
│
├── scripts/
│   ├── verify_model.py
│   └── compare_build.py
│
├── tests/
│   └── test_main.py
│
├── .gitignore
├── Dockerfile.jenkins
├── Jenkinsfile
├── pytest.ini
├── README.md
└── requirements.txt
```

### Important Files

| File | Description |
|---|---|
| app/main.py | Core application functions |
| app/repository_features.py | GitHub repository feature extraction |
| app/predictor.py | Random Forest prediction and probability calculation |
| scripts/verify_model.py | ML model verification |
| scripts/compare_build.py | Prediction and actual build comparison |
| tests/test_main.py | Automated Python tests |
| Jenkinsfile | Jenkins pipeline configuration |
| Dockerfile.jenkins | Jenkins Docker image configuration |
| requirements.txt | Python dependencies |
| pytest.ini | Pytest configuration |

---

## 8. Installation and Local Setup

### Prerequisites

- Python 3
- Git
- Docker Desktop
- Java JDK
- Apache Maven

The Jenkins environment used for the demonstration includes Python 3.13.5, Java 21 and Maven 3.9.9.

### Step 1: Clone the Repository

```powershell
git clone https://github.com/CTG2/build-failure-prediction.git
cd build-failure-prediction
```

### Step 2: Create a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Run Python Tests

```powershell
python -m pytest
```

### Step 5: Verify the ML Model

Make sure the model file is available at the configured location, then run:

```powershell
python scripts/verify_model.py
```

---

## 9. GitHub Repository Feature Extraction

The feature extraction module is `app/repository_features.py`.

It uses the GitHub REST API to retrieve public repository information and inspect the repository file tree. The extractor identifies:

- Repository stars and forks.
- Repository creation date.
- Latest push date.
- Build configuration files.
- Build tool indicators.
- IDE configuration folders.
- Travis CI configuration.
- Git submodule configuration.

The extracted information is converted into a Pandas DataFrame containing the 17 model input features.

### Run Feature Extraction

```powershell
python -m app.repository_features
```

Enter a public GitHub repository URL when prompted. Example:

```text
https://github.com/apache/commons-lang
```

---

## 10. Build Failure Prediction

The prediction module is `app/predictor.py`.

The module performs the following operations:

1. Loads the trained Random Forest model.
2. Extracts features from the requested GitHub repository.
3. Passes the feature DataFrame to the trained pipeline.
4. Obtains classification probabilities using `predict_proba()`.
5. Identifies the predicted build outcome.
6. Calculates the failure probability.
7. Displays and optionally saves the prediction result.

### Model File Location

The model artifact is stored separately from the Git repository.

Windows:

```text
D:\jenkins-models\random_forest_build_failure_model.pkl
```

Jenkins:

```text
/var/jenkins_home/models/random_forest_build_failure_model.pkl
```

The model location can be configured using `BUILD_FAILURE_MODEL_PATH`.

### Run Prediction Locally

```powershell
$env:BUILD_FAILURE_MODEL_PATH = "D:\jenkins-models\random_forest_build_failure_model.pkl"
$env:REPOSITORY_URL = "https://github.com/apache/commons-lang"
python -m app.predictor
```

To save prediction details as JSON:

```powershell
$env:PREDICTION_OUTPUT_PATH = "prediction.json"
python -m app.predictor
```

The prediction output includes the repository URL, predicted outcome and failure probability.

---

## 11. Jenkins CI Pipeline

Jenkins automates the complete prediction and actual build comparison workflow. The Jenkins server runs inside a Docker container.

### Jenkins Environment

| Component | Configuration |
|---|---|
| Jenkins Job | build-failure-prediction |
| Jenkins URL | http://localhost:8080 |
| Container Name | jenkins |
| Docker Image | jenkins-python:lts |
| Python | 3.13.5 |
| Java | 21.0.12.1 |
| Maven | 3.9.9 |
| Model Location | /var/jenkins_home/models/random_forest_build_failure_model.pkl |

### Jenkins Model Setup

The following commands copy the model into the Jenkins container during environment setup:

```powershell
docker exec -u root jenkins mkdir -p /var/jenkins_home/models

docker cp "D:\jenkins-models\random_forest_build_failure_model.pkl" jenkins:/var/jenkins_home/models/random_forest_build_failure_model.pkl

docker exec -u root jenkins chown jenkins:jenkins /var/jenkins_home/models/random_forest_build_failure_model.pkl
```

### Jenkins Pipeline Stages

| Stage | Description |
|---|---|
| Project Check | Starts the project pipeline |
| Python Check | Checks Python and Maven versions |
| Create Virtual Environment | Creates the Jenkins Python environment |
| Install Dependencies | Installs project requirements |
| Run Tests | Runs automated tests using Pytest |
| Verify ML Model | Loads the trained model and verifies inference |
| Repository Failure Prediction | Extracts GitHub features and predicts the build outcome |
| Checkout Java Repository | Clones the target Java repository |
| Run Actual Maven Build | Executes the Maven package command |
| Compare Prediction with Actual Build | Compares model prediction with actual Maven result |

### Run the Jenkins Pipeline

1. Start Docker Desktop.
2. Ensure that the Jenkins container is running.
3. Open http://localhost:8080.
4. Select the `build-failure-prediction` job.
5. Click **Build Now**.
6. Open the latest build.
7. Select **Console Output** to inspect the pipeline execution.

Jenkins retrieves the Jenkinsfile from the project's GitHub repository and executes the configured stages.

---

## 12. Actual Maven Build and Prediction Comparison

The project includes an actual Java build execution stage.

The Jenkins pipeline clones the Apache Commons Lang repository:

https://github.com/apache/commons-lang

It executes the following Maven command:

```bash
mvn -B -DskipTests package
```

The Maven process exit code determines the actual build result:

- Exit code 0: SUCCESS
- Non-zero exit code: FAILURE

The pipeline saves the actual result in `build_result.txt`.

The prediction is saved in `prediction.json`.

The comparison script is `scripts/compare_build.py`. It reads both results and reports whether the model prediction matches the actual Maven outcome.

### Comparison Outcomes

| Predicted Result | Actual Result | Comparison |
|---|---|---|
| SUCCESS | SUCCESS | MATCH |
| FAILURE | FAILURE | MATCH |
| SUCCESS | FAILURE | MISMATCH |
| FAILURE | SUCCESS | MISMATCH |

A prediction mismatch is recorded as a comparison result and does not automatically fail the Jenkins pipeline.

**Note:** The Maven command uses `-DskipTests` to verify the packaging/build process without executing the Java test suite.

---

## 13. Demonstration Results

The integrated project successfully completed an end-to-end Jenkins execution using Apache Commons Lang.

### Jenkins Execution Summary

| Component | Result |
|---|---|
| Jenkins pipeline initialization | SUCCESS |
| Python environment | SUCCESS |
| Maven environment | SUCCESS |
| Dependency installation | SUCCESS |
| Python unit tests | 4 PASSED |
| ML model verification | SUCCESS |
| GitHub feature extraction | SUCCESS |
| Random Forest inference | SUCCESS |
| Java repository checkout | SUCCESS |
| Actual Maven build | SUCCESS |
| Prediction comparison | MATCH |
| Overall Jenkins pipeline | SUCCESS |

### Observed Prediction

Repository:

```text
https://github.com/apache/commons-lang
```

Model output:

```text
Prediction: SUCCESS
Failure probability: 48.28%
```

Actual Maven output:

```text
[INFO] BUILD SUCCESS
```

Prediction comparison:

```text
========== PREDICTION COMPARISON ==========

Repository:
https://github.com/apache/commons-lang

Predicted result: SUCCESS

Failure probability: 48.28%

Actual Maven result: SUCCESS

Comparison: MATCH

===========================================
```

Final Jenkins status:

```text
Finished: SUCCESS
```

This execution demonstrates the integration of repository feature extraction, Machine Learning inference, Jenkins automation, Maven build execution and prediction comparison.

---

## 14. Future Enhancements

Potential enhancements to the project include:

1. Improving repository feature extraction.
2. Evaluating additional Machine Learning classification algorithms.
3. Improving build failure prediction performance.
4. Expanding evaluation across more Java repositories.
5. Adding a prediction dashboard.
6. Maintaining prediction history and actual build outcomes.
7. Supporting additional Java build systems.
8. Generating automated prediction reports.
9. Integrating model evaluation into the CI workflow.

---

## 15. Conclusion

This project demonstrates the integration of Machine Learning and DevOps automation for Java software build outcome prediction.

A Random Forest classifier analyses repository characteristics and predicts whether a Java project is likely to build successfully or fail.

The model is integrated into a Jenkins CI pipeline that performs repository feature extraction, automated Python testing, model inference, Java repository checkout and Maven build execution.

The final comparison stage evaluates the predicted outcome against the actual Maven build result.

The successful end-to-end demonstration brings together:

- GitHub REST API integration.
- Repository feature extraction.
- Random Forest classification.
- Failure probability calculation.
- Python automated testing.
- Jenkins CI automation.
- Maven build execution.
- Prediction and actual outcome comparison.

---

## 16. References

1. Sulír, M. et al. (2020). Large-Scale Dataset of Local Java Software Build Results. *Data*, 5(3), Article 86. https://doi.org/10.3390/data5030086
2. OSF Dataset. https://doi.org/10.17605/OSF.IO/UMK3W
3. Scikit-learn Documentation. https://scikit-learn.org/
4. Random Forest Classifier Documentation. https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
5. Jenkins Documentation. https://www.jenkins.io/doc/
6. Apache Maven Documentation. https://maven.apache.org/guides/
7. GitHub REST API Documentation. https://docs.github.com/en/rest

---

## 17. Project Repository

**GitHub:** https://github.com/CTG2/build-failure-prediction

**Project Title:** Design Build Failure Prediction Using Random Forest  
**Domain:** Machine Learning and DevOps  
**Algorithm:** Random Forest Classification  
**CI Platform:** Jenkins  
**Build Automation:** Apache Maven
