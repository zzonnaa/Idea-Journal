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
                // Correct tag format: username/repo:tag
                bat "docker tag journal-app:v1 zzonnaa/journal-app:v1"
                bat "docker push zzonnaa/journal-app:v1"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying to Kubernetes..."
                bat 'kubectl apply -f k8s/deployment.yaml --validate=false'
                bat 'kubectl apply -f k8s/service.yaml'
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
