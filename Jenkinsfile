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
    }

    post {
        success {
            echo 'All tests passed successfully'
        }

        failure {
            echo 'Pipeline failed'
        }
    }
}
