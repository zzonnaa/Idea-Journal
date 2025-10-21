pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = 'dockerhub-creds'  // Jenkins credential ID (username/password)
    DOCKERHUB_USER = 'YOUR_DOCKERHUB_USERNAME'
    IMAGE_NAME = "${env.DOCKERHUB_USER}/idea-journal"
    KUBECONFIG_CREDENTIAL = 'kubeconfig' // Jenkins credential with kubeconfig file
    K8S_DEPLOYMENT = 'idea-journal'
    K8S_NAMESPACE = 'default'
  }

  triggers {
    // Git webhook will trigger; optional polling fallback
    // pollSCM('H/5 * * * *')
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          // Tag with build number or git short hash
          def tag = "${env.BUILD_NUMBER}"
          env.IMAGE_TAG = tag
          sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
        }
      }
    }

    stage('Push Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS, usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh "echo $DH_PASS | docker login -u $DH_USER --password-stdin"
          sh "docker push ${IMAGE_NAME}:${env.IMAGE_TAG}"
          // update latest tag too
          sh "docker tag ${IMAGE_NAME}:${env.IMAGE_TAG} ${IMAGE_NAME}:latest"
          sh "docker push ${IMAGE_NAME}:latest"
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        withCredentials([file(credentialsId: env.KUBECONFIG_CREDENTIAL, variable: 'KUBECONF')]) {
          // Use kubectl from the agent; apply manifests after substituting image tag
          sh "kubectl --kubeconfig=$KUBECONF set image deployment/${env.K8S_DEPLOYMENT} idea-journal=${IMAGE_NAME}:${env.IMAGE_TAG} -n ${env.K8S_NAMESPACE} || true"
          // If set-image failed (first time), apply manifests
          sh "kubectl --kubeconfig=$KUBECONF apply -f k8s/deployment.yaml -n ${env.K8S_NAMESPACE}"
          sh "kubectl --kubeconfig=$KUBECONF apply -f k8s/service.yaml -n ${env.K8S_NAMESPACE}"
        }
      }
    }
  }

  post {
    success {
      echo "Deployed ${IMAGE_NAME}:${env.IMAGE_TAG}"
    }
    failure {
      echo "Build or deploy failed"
    }
  }
}
