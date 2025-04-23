pipeline {
    agent any
    
    stages {
        // Baixar o repositório do GitHub
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/ciberseguranca-pucpr/exemplo-comunicacao.git'
            }
        }
        
        // Preparar ambiente virtual
        stage('Preparação ambiente') {
            steps {
                sh 'python3 -m venv venv'
                sh 'venv/bin/pip install -r app/requirements.txt'
            }
        }
        
        stage('Teste') {
            steps {
                dir('app/') {
                    sh '../venv/bin/python -m pytest -s tests/test_app.py'
                }
            }
        }
    }
}