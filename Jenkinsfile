// Jenkinsfile (updated) - safe, checks for docker and ensures PYTHONPATH for pytest
pipeline {
  agent any

  environment {
    DOCKER_IMAGE = "vortexfrenzy/22:latest"
    // Use PATH+ addition to append common Homebrew locations on macOS
    // (If your docker is in a different location, update the value below)
    PATH = "/opt/homebrew/bin:/usr/local/bin:${env.PATH}"
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
        // ensure pytest can import app
        sh 'PYTHONPATH=. . .venv/bin/activate && pytest -q'
      }
    }

    stage('Verify docker available') {
      steps {
        // quick guard: fail early with clear message if docker is missing
        sh '''
          if ! command -v docker >/dev/null 2>&1; then
            echo "ERROR: docker CLI not found in PATH. Make sure Docker Desktop is running on the Jenkins host and Docker CLI is accessible to the Jenkins user."
            echo "If on macOS, ensure docker path (which docker) is in PATH for Jenkins. Typical locations: /opt/homebrew/bin or /usr/local/bin"
            exit 2
          fi
          docker --version
        '''
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
          sh 'echo $DOCKER_PASS | docker login --username $DOCKER_USER --password-stdin'
          sh "docker push ${env.DOCKER_IMAGE}"
        }
      }
    }
  }

  post {
    always {
      // attempt to list images if docker exists; otherwise skip listing
      sh '''
        if command -v docker >/dev/null 2>&1; then
          docker images || true
        else
          echo "docker not available to Jenkins - images not listed."
        fi
      '''
    }
    failure {
      echo "One or more stages failed — check Console Output."
    }
  }
}
