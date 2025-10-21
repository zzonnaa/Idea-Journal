pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                echo "Building Docker Image..."
                bat "docker build -t journal-app:v1 ."
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub_creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat '''
                        docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                    '''
                }
            }
        }

        stage('Push Docker Image to Dockerhub') {
            steps {
                echo "Pushing Docker image to Dockerhub..."
                bat "docker tag journal-app:v1 zzonnaa/journal-app:v1"
                bat "docker push zzonnaa/journal-app:v1"
            }
        }

        stage('Deploy/Update Kubernetes') {
            steps {
                echo "Deploying or updating Kubernetes deployment..."

                // Check if deployment exists
                bat '''
                kubectl get deployment journal-deployment
                if %ERRORLEVEL% NEQ 0 (
                    echo "Deployment does not exist, applying YAML..."
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                ) else (
                    echo "Deployment exists, updating image..."
                    kubectl set image deployment/journal-deployment journal-app=zzonnaa/journal-app:v1
                    kubectl rollout status deployment/journal-deployment
                )
                '''
            }
        }
    }
}
