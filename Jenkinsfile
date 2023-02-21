pipeline {
  agent {
    node {
      label 'base'
    }

  }
  stages {
    stage('clone code') {
      agent none
      steps {
        container('base') {
          git(url: 'https://github.com/hengjingzhu/djangotest.git', credentialsId: 'github-id', branch: 'main', changelog: true, poll: false)
        }

        sh 'ls'
      }
    }

    stage('build & push') {
      agent none
      steps {
        container('base') {
          sh '''PROJECT_NAME="$(basename "$(git rev-parse --show-toplevel)")"
PROJECT_TAG="$(git describe --abbrev=0 --tags)"
docker build -f Dockerfile  -t $PROJECT_NAME:$PROJECT_TAG  . '''
        }

      }
    }

    stage('push latest') {
      agent none
      steps {
        container('base') {
          withCredentials([usernamePassword(credentialsId : 'dockerhub-aliyun' ,passwordVariable : 'ALIDOCKERPASSWORD' ,usernameVariable : 'ALIDOCKERUSERNAME' ,)]) {
            sh '''
project_name=$(basename "$(git rev-parse --show-toplevel)")
project_tag="$(docker images --format "{{.Tag}}" $project_name)"
project_id="$(docker images --format "{{.ID}}" $project_name)"


docker login --username=$ALIDOCKERUSERNAME $REGISTRY --password=$ALIDOCKERPASSWORD

docker tag $project_id $REGISTRY/$DOCKERHUB_NAMESPACE/$project_name:$project_tag


docker push $REGISTRY/$DOCKERHUB_NAMESPACE/$project_name:$project_tag

docker rmi $project_name:$project_tag
docker rmi $REGISTRY/$DOCKERHUB_NAMESPACE/$project_name:$project_tag'''
          }

        }

      }
    }

    stage('deploy to dev') {
      steps {
        input(id: 'deploy-to-dev', message: 'deploy to dev?')
        kubernetesDeploy(configs: 'deploy/dev-ol/**', enableConfigSubstitution: true, kubeconfigId: "$KUBECONFIG_CREDENTIAL_ID")
      }
    }

    stage('mail') {
      agent none
      steps {
        mail(to: 'david3311041@hotmail.com', subject: '构建成功', body: '成功')
      }
    }

  }
  environment {
    DOCKER_CREDENTIAL_ID = 'dockerhub-id'
    GITHUB_CREDENTIAL_ID = 'github-id'
    KUBECONFIG_CREDENTIAL_ID = 'demo-kubeconfig'
    REGISTRY = 'registry.cn-shanghai.aliyuncs.com'
    DOCKERHUB_NAMESPACE = 'davidzhu'
    GITHUB_ACCOUNT = 'kubesphere'
    APP_NAME = 'devops-java-sample'
  }
  parameters {
    string(name: 'TAG_NAME', defaultValue: '', description: '')
  }
}
