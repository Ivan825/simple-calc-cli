// Jenkinsfile - for vortexfrenzy/22
pipeline {
  agent any

  environment {
    DOCKER_IMAGE = "vortexfrenzy/22:latest"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Prepare Python') {
      steps {
        sh 'python3 --version || true'
        sh 'python3 -m venv .venv || true'
        sh '. .venv/bin/activate && pip install --upgrade pip'
        sh '. .venv/bin/activate && pip install -r requirements.txt'
      }
    }

    stage('Run tests') {
      steps {
        sh '. .venv/bin/activate && pytest -q'
      }
    }

    stage('Build Docker image') {
      steps {
        sh "docker build -t ${env.DOCKER_IMAGE} ."
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                          usernameVariable: 'DOCKER_USER',
                                          passwordVariable: 'DOCKER_PASS')]) {
          // login and push
          sh 'echo $DOCKER_PASS | docker login --username $DOCKER_USER --password-stdin'
          sh "docker push ${env.DOCKER_IMAGE}"
        }
      }
    }
  }

  post {
    always {
      sh 'docker images || true'
    }
    failure {
      echo "One or more stages failed — check Console Output."
    }
  }
}
