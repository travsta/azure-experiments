# Repository Structure

This document provides a comprehensive overview of the file and directory structure of the Instagram Topic Classification project.

```
instagram-topic-classifier/
│
├── .github/
│   └── workflows/
│       ├── model-ci-cd.yml        # CI/CD pipeline for the model
│       └── api-ci-cd.yml          # CI/CD pipeline for the API
│
├── src/
│   ├── model/
│   │   ├── dummy_model.py         # Implementation of the DummyTopicClassifier
│   │   └── score.py               # Script for Azure ML model deployment
│   │
│   └── api/
│       └── function_app.py        # Azure Function implementation
│
├── tests/
│   ├── model/
│   │   ├── test_dummy_model.py    # Unit tests for dummy_model.py
│   │   └── test_score.py          # Unit tests for score.py
│   │
│   └── api/
│       └── test_function_app.py   # Unit tests for function_app.py
│
├── config/
│   ├── endpoint.yml               # Azure ML endpoint configuration
│   ├── deployment.yml             # Azure ML deployment configuration
│   ├── environment_model.yml      # Conda environment specification for the model
│   ├── environment_api.yml        # Conda environment specification for the API
│   └── pytest.ini                 # Pytest configuration file
│
├── docs/
│   └── architecture.md            # Detailed architecture description
│
├── scripts/
│   ├── create_model_env.sh        # Script to create model development environment
│   ├── create_api_env.sh          # Script to create API development environment
│   └── run_tests_with_coverage.sh # Script to run tests with coverage
│
├── .gitignore                     # Specifies intentionally untracked files to ignore
├── LICENSE                        # License file
├── README.md                      # Project overview and setup instructions
└── REPO_STRUCTURE.md              # This file
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

#### `tests/model/`
Contains tests for the model components.
- `test_dummy_model.py`: Tests for the DummyTopicClassifier.
- `test_score.py`: Tests for the Azure ML scoring script.

#### `tests/api/`
Contains tests for the API components.
- `test_function_app.py`: Tests for the Azure Function implementation.

### `config/`
Contains configuration files for the project.
- `endpoint.yml`: Defines the Azure ML endpoint configuration.
- `deployment.yml`: Specifies the deployment settings for the model in Azure ML.
- `environment_model.yml`: Defines the Conda environment for the model component.
- `environment_api.yml`: Defines the Conda environment for the API component.
- `pytest.ini`: Configuration file for pytest, including coverage settings.

### `docs/`
Contains additional documentation for the project.
- `architecture.md`: Provides a detailed description of the system architecture.

### `scripts/`
Contains utility scripts for environment setup and testing.
- `create_model_env.sh`: Script to set up the local development environment for the model.
- `create_api_env.sh`: Script to set up the local development environment for the API.
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
