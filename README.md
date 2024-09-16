# Instagram Topic Classification - Azure Experiments

## Project Overview
This project implements a microservice for classifying Instagram posts by topic using Azure Functions and Azure Machine Learning. It provides a RESTful API endpoint that accepts the text of an Instagram post and returns probabilities for various topics.

## Project Structure
The project is divided into two main components:
1. Topic Classification Model
2. API Service

Each component has its own Conda environment and deployment process.

### Directory Structure
```
instagram-topic-classifier/
├── src/
│   ├── model/                     # Model-related code
│   │   ├── dummy_model.py         # Implementation of the DummyTopicClassifier
│   │   └── score.py               # Script for Azure ML model deployment
│   └── api/
│       └── function_app.py        # Azure Function implementation
├── tests/
│   ├── model/                     # Model tests
│   └── api/                       # API tests
├── scripts/
│   ├── create_model_env.sh
│   ├── create_api_env.sh
│   └── run_tests_with_coverage.sh
├── docs/
│   └── architecture.md            # Detailed architecture description
├── .github/
│   └── workflows/
│       ├── model-ci-cd.yml        # CI/CD pipeline for the model
│       └── api-ci-cd.yml          # CI/CD pipeline for the API
├── config/
│   ├── endpoint.yml               # Azure ML endpoint configuration
│   ├── deployment.yml             # Azure ML deployment configuration
│   ├── environment_model.yml      # Conda environment specification for the model
│   ├── environment_api.yml        # Conda environment specification for the API
│   └── pytest.ini                 # Pytest configuration file
├── .gitignore
├── LICENSE
└── README.md               # This file
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Conda
- Node.js and npm (for Azure Functions Core Tools)
- Azure subscription (for deployment)

### Setting up the Model Environment
1. Navigate to the project root directory
2. Run the following command:
   ```
   ./scripts/create_model_env.sh
   ```
3. Follow the prompts in the script
4. Activate the environment:
   ```
   conda activate instagram-topic-classifier-model
   ```

### Setting up the API Environment
1. Navigate to the project root directory
2. Run the following command:
   ```
   ./scripts/create_api_env.sh
   ```
3. Follow the prompts in the script
4. Activate the environment:
   ```
   conda activate instagram-topic-classifier-api
   ```

## Development Workflow

### Working on the Model
1. Activate the model environment:
   ```
   conda activate instagram-topic-classifier-model
   ```
2. Navigate to `src/model/`
3. Implement your changes in `dummy_model.py` or `score.py`
4. Run tests:
   ```
   pytest ../../tests/model/
   ```

### Working on the API
1. Activate the API environment:
   ```
   conda activate instagram-topic-classifier-api
   ```
2. Navigate to `src/api/`
3. Implement your changes in `function_app.py`
4. Run tests:
   ```
   pytest ../../tests/api/
   ```
5. To test the Azure Function locally:
   ```
   func start
   ```

## Running Tests with Coverage

We use pytest-cov to monitor test coverage. Here's how to run tests with coverage:

1. For the model:
   ```
   ./scripts/run_tests_with_coverage.sh model
   ```

2. For the API:
   ```
   ./scripts/run_tests_with_coverage.sh api
   ```

These commands will run the tests, display a coverage report in the terminal, and generate an HTML report in the `htmlcov` directory.

### Coverage Requirements

Our CI pipeline requires a minimum of 80% test coverage for both the model and API components. Ensure your changes maintain or improve the coverage before submitting a pull request.

### Viewing Coverage Reports

After running the tests with coverage:

1. Terminal Report: This is displayed immediately after the tests run.
2. HTML Report: Open `htmlcov/index.html` in a web browser for a detailed, interactive coverage report.

Remember, while high coverage is important, it's equally important to have meaningful tests that verify the correct behavior of your code.

## Deployment

### Deploying the Model to Azure ML
(Add specific instructions for deploying the model to Azure ML)

### Deploying the API to Azure Functions
(Add specific instructions for deploying the API to Azure Functions)

## Continuous Integration

Our CI pipeline automatically runs tests and checks coverage for all pull requests. You can see the results in the GitHub Actions tab of the repository.

[![CI/CD Pipeline](https://github.com/<your-username>/<your-repo-name>/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/<your-username>/<your-repo-name>/actions/workflows/ci-cd.yml)

The pipeline will post a comment on your pull request with the current coverage percentages for both the model and API components.

## Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Run tests to ensure everything is working
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/<your-username>/instagram-topic-classification](https://github.com/<your-username>/instagram-topic-classification)
