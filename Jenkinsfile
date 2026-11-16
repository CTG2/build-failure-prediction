
pipeline {
    agent any

    parameters {
        string(
            name: 'REPOSITORY_URL',
            defaultValue: 'https://github.com/apache/commons-codec',
            description: 'GitHub repository to test'
        )
    }

    stages {
        stage('Project Check') {
            steps {
                echo 'Build Failure Prediction project started'
                echo "Repository: ${params.REPOSITORY_URL}"
            }
        }

        stage('Python Check') {
            steps {
                sh 'python3 --version'
                sh 'mvn -version'
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
                withEnv([
                    "REPOSITORY_URL=${params.REPOSITORY_URL}",
                    'PREDICTION_OUTPUT_PATH=prediction.json'
                ]) {
                    sh '.venv-jenkins/bin/python -m app.predictor'
                }
            }
        }

        stage('Checkout Java Repository') {
            steps {
                sh 'rm -rf target-repo'

                withEnv(["REPOSITORY_URL=${params.REPOSITORY_URL}"]) {
                    sh 'git clone --depth 1 "$REPOSITORY_URL" target-repo'
                }
            }
        }

        stage('Run Actual Maven Build') {
            steps {
                script {
                    int buildStatus = sh(
                        returnStatus: true,
                        script: 'cd target-repo && mvn -B -DskipTests package'
                    )

                    def actualResult = buildStatus == 0 ? 'SUCCESS' : 'FAILURE'

                    writeFile(
                        file: 'build_result.txt',
                        text: actualResult
                    )

                    echo "ACTUAL MAVEN BUILD RESULT: ${actualResult}"
                }
            }
        }

        stage('Compare Prediction with Actual Build') {
            steps {
                sh '.venv-jenkins/bin/python scripts/compare_build.py'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed: prediction and actual build comparison finished.'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs above.'
        }
    }
}
