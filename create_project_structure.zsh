#!/bin/zsh

# Function to create directories and files
create_structure() {
  mkdir -p $1
  if [ ! -z "$2" ]; then
    touch $1/$2
  fi
}

# Create main directories
create_structure src
create_structure src/domain
create_structure src/domain/entities
create_structure src/domain/use_cases
create_structure src/domain/interfaces
create_structure src/application
create_structure src/application/services
create_structure src/application/interfaces
create_structure src/infrastructure
create_structure src/infrastructure/persistence
create_structure src/infrastructure/external_services
create_structure src/infrastructure/k8s
create_structure src/interfaces
create_structure src/interfaces/api
create_structure src/interfaces/cli

# Create k8s-manifests and its subdirectories
create_structure k8s-manifests
create_structure k8s-manifests/model_serving deployment.yaml
create_structure k8s-manifests/model_serving service.yaml
create_structure k8s-manifests/model_training deployment.yaml
create_structure k8s-manifests/model_training service.yaml
create_structure k8s-manifests/speech_voice deployment.yaml
create_structure k8s-manifests/speech_voice service.yaml
create_structure k8s-manifests/datalake deployment.yaml
create_structure k8s-manifests/datalake service.yaml
create_structure k8s-manifests/knowledge_graph deployment.yaml
create_structure k8s-manifests/knowledge_graph service.yaml
create_structure k8s-manifests/caching deployment.yaml
create_structure k8s-manifests/caching service.yaml
create_structure k8s-manifests ingress.yaml

# Create dockerfiles directory and files
create_structure dockerfiles
create_structure dockerfiles triton.Dockerfile
create_structure dockerfiles nemo.Dockerfile
create_structure dockerfiles riva.Dockerfile
create_structure dockerfiles custom-nginx.Dockerfile

# Create config directory and files
create_structure config
create_structure config k3s-config.yaml
create_structure config kubeconfig

# Create scripts directory and files
create_structure scripts
create_structure scripts install-k3s.sh
create_structure scripts deploy-services.sh
create_structure scripts setup-environment.sh

# Create models directory and subdirectories
create_structure models
create_structure models/triton
create_structure models/nemo
create_structure models/riva

# Create data directory and subdirectories
create_structure data
create_structure data/arangodb
create_structure data/redis

# Create docs directory and files
create_structure docs
create_structure docs setup.md
create_structure docs usage.md

# Create root level files
touch .gitignore README.md pyproject.toml poetry.lock .flake8 .mypy.ini pytest.ini .pyre_configuration monkeytype.ini pytype.cfg tsconfig.json .pre-commit-config.yaml main.py

echo "Project structure created successfully!"
