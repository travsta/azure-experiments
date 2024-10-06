# Repository Structure

This document provides a comprehensive overview of the Instagram Topic Classification project's file and directory structure.

## Overview

The project is organized into several key directories:

- `src/`: Contains the main source code, separated into `api/` and `model/` subdirectories.
- `tests/`: Contains all unit tests, mirroring the structure of `src/`.
- `config/`: Houses configuration files for different environments and Azure services.
- `.github/workflows/`: Contains CI/CD pipeline definitions.
- `scripts/`: Includes utility scripts for environment setup and testing.
- `docs/`: Contains additional project documentation.

The root directory contains configuration files and the main README.

```
instagram-topic-classifier/
│
├── .github/
│   └── workflows/
│       ├── model-ci-cd.yml          # CI/CD pipeline for the model
│       └── api-ci-cd.yml            # CI/CD pipeline for the API
│
├── src/
│   ├── model/
│   │   ├── dummy_model.py           # Implementation of the DummyTopicClassifier
│   │   └── score.py                 # Script for Azure ML model deployment
│   │
│   └── api/
│       └── function_app.py          # Azure Function implementation
│
├── tests/
│   ├── test_dummy_model.py          # Unit tests for dummy_model.py
│   ├── test_score.py                # Unit tests for score.py
│   ├── test_function_app.py         # Unit tests for function_app.py
│   └── smoke.py                     # End to end test for app after deployed to Azure
│
├── config/
│   ├── azure_environment.yml        # Azure ML environment configuration
│   ├── classifier-endpoint.yml      # Azure ML endpoint configuration
│   ├── blue-deployment.yml          # Azure ML configuration for stable blue deployments as part of blue/green strategy
│   ├── green-deployment.yml         # Azure ML configuration for novel green deployments as part of blue/green strategy
│   ├── environment_api_local.yml    # Conda environment specification for local API development
│   ├── environment_api_azure.yml    # Conda environment specification for API deployment on Azure
│   ├── environment_model_local.yml  # Conda environment specification for local model development
│   ├── environment_model_azure.yml  # Conda environment specification for model deployment on Azure
│   ├── requirements.txt             # Copy of requirements from environment_api_azure.yml as required for Azure Functions .venv creation
│   ├── host.json                    # Configuration file for Azure Functions app
│   └── pytest.ini                   # Pytest configuration file
│
├── docs/
│   ├── modeling-approach.md         # Explanation of approach to development and maintenance of the supporting model
│   └── architecture.md              # Detailed architecture description
│
├── scripts/
│   ├── create_api_env.sh            # Script to create API development environment
│   ├── create_model_env.sh          # Script to create model development environment
│   └── run_tests_with_coverage.sh   # Script to run tests with coverage
│
├── .gitignore                       # Specifies intentionally untracked files for git to ignore
├── .funcignore                      # Specifies intentionally untracked files for azure functions deployment actions to ignore
├── .env.example                     # Sample .env file for configuring the API in local runs/tests
├── LICENSE                          # License file
├── README.md                        # Project overview and setup instructions
└── REPO_STRUCTURE.md                # This file
```

## Directory and File Descriptions

### `.github/`
Contains GitHub-specific files, including workflow definitions for GitHub Actions.
- `workflows/model-ci-cd.yml`: Defines the CI/CD pipeline for the model component, including testing, coverage reporting, and deployment to Azure ML.
- `workflows/api-ci-cd.yml`: Defines the CI/CD pipeline for the API component, including testing, coverage reporting, and deployment to Azure Functions.

### `src/`
Contains the main source code for the project, separated into model and API components.

#### `src/model/`
Contains files related to the topic classification model.
- `dummy_model.py`: Implements the DummyTopicClassifier used for development and testing.
- `score.py`: Defines how the model is loaded and used in Azure ML.

#### `src/api/`
Contains files related to the API implementation.
- `function_app.py`: Implements the Azure Function that serves as the API endpoint.

### `tests/`
Contains all unit tests for the project, mirroring the structure of the `src/` directory.
- `test_dummy_model.py`: Tests for the DummyTopicClassifier.
- `test_score.py`: Tests for the Azure ML scoring script.
- `test_function_app.py`: Tests for the Azure Function implementation.

### `config/`
Contains configuration files for the project.
- `azure_environment.yml`: Defines the Azure ML environment configuration.
- `classifier-endpoint.yml`: Defines the Azure ML endpoint configuration.
- `blue-deployment.yml`: Configuration for the "blue" deployment in a blue-green deployment strategy.
- `green-deployment.yml`: Configuration for the "green" deployment in a blue-green deployment strategy.
- `environment_api_local.yml`: Defines the Conda environment for local API development.
- `environment_api_azure.yml`: Defines the Conda environment for API deployment on Azure.
- `environment_model_local.yml`: Defines the Conda environment for local model development.
- `environment_model_azure.yml`: Defines the Conda environment for model deployment on Azure.
- `pytest.ini`: Configuration file for pytest, including coverage settings.
- `requirements.txt`: A version of environment_api_azure.yml that is compatible with Python venv as required for the Azure Function.
- `host.json`: A file with necessary configuration items for the Azure Function serving the API.
These files are crucial for managing the Azure infrastructure and deployments for both the model and API components of the project.

### `docs/`
Contains additional documentation for the project.
- `architecture.md`: Provides a detailed description of the system architecture.
- `modeling-approach.md`: Explanation of approach to development and maintenance of the supporting model.

### `scripts/`
Contains utility scripts for environment setup and testing.
- `create_api_env.sh`: Script to set up the development environment for the API, choosing between local and Azure configurations.
- `create_model_env.sh`: Script to set up the development environment for the model, choosing between local and Azure configurations.
- `run_tests_with_coverage.sh`: Script to run tests with coverage for either model or API.

### Root Directory Files
- `.gitignore`: Specifies files that Git should ignore.
- `LICENSE`: Contains the license information for the project.
- `README.md`: Provides an overview of the project, setup instructions, and usage guidelines.
- `REPO_STRUCTURE.md`: This file, explaining the repository structure.

## Note
This structure separates the model-related files from the API-related files, reflecting their deployment to different services (Azure ML for the model and Azure Functions for the API). It includes configuration files for environment management, testing, Azure ML deployment, and separate CI/CD pipelines for the model and API components. 

The `config/` directory centralizes all configuration files, making it easier to manage environment specifications, testing configurations, and deployment settings.

The CI/CD pipelines (`.github/workflows/`) are set up to run tests, report coverage, and deploy each component independently, triggered by changes in their respective directories.

As the project grows, remember to update this file to reflect any changes in the repository structure.
