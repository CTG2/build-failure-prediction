pipeline {
    agent any

    stages {
        stage('Project Check') {
            steps {
                echo 'Build Failure Prediction project started'
            }
        }

        stage('Environment Check') {
            steps {
                echo 'Jenkins pipeline is working'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully'
        }

        failure {
            echo 'Pipeline failed'
        }
    }
}
