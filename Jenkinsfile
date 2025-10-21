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
                 echo "Deploying to Kubernetes..."
                    // Apply the deployment & service (first-time or updates)
                bat 'kubectl apply -f k8s/service.yaml'
                bat 'kubectl set image deployment/journal-deployment journal-container=zzonnaa/journal-app:v1'
            }
        }
        stage('Restart Deployment') {
            steps {
                echo "Restarting Deployment to pick up new image..."
                bat "kubectl rollout restart deployment/journal-deployment"
            }
        }
    }
}
