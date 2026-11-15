pipeline {
    agent any

    stages {
        stage('Project Check') {
            steps {
                echo 'Build Failure Prediction project started'
            }
        }

        stage('Python Check') {
            steps {
                sh 'python3 --version'
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh 'python3 -m venv .venv-jenkins'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '.venv-jenkins/bin/python -m pip install --upgrade pip'
                sh '.venv-jenkins/bin/python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '.venv-jenkins/bin/python -m pytest'
            }
        }

        stage('Verify ML Model') {
            steps {
                sh '.venv-jenkins/bin/python scripts/verify_model.py'
            }
        }

        stage('Repository Failure Prediction') {
            steps {
                withEnv(['REPOSITORY_URL=https://github.com/apache/commons-lang']) {
                    sh '.venv-jenkins/bin/python -m app.predictor'
                }
            }
        }
    }

    post {
        success {
            echo 'Tests and ML prediction completed successfully'
        }

        failure {
            echo 'Pipeline failed'
        }
    }
}
