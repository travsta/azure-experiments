# Instagram Topic Classification

## Project Overview
This project implements a microservice for classifying Instagram posts by topic using Azure Functions and Azure Machine Learning. It provides a RESTful API endpoint that accepts the text of an Instagram post and returns probabilities for various topics.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Setup Instructions](#setup-instructions)
3. [Development Workflow](#development-workflow)
4. [Testing](#testing)
5. [Deployment](#deployment)
6. [Configuration Management](#configuration-management)
7. [CI/CD](#cicd)
8. [Contributing](#contributing)
9. [License](#license)

## Project Structure
The project is divided into two main components:
1. Topic Classification Model
2. API Service

Each component has separate Conda environments for local development and Azure deployment.

### Directory Structure
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
│   ├── requirements.txt             # Pytest configuration file
│   ├── host.json                    # Pytest configuration file
│   └── pytest.ini                   # Pytest configuration file
│
├── docs/
│   ├── modelling-approach.md        # Explanation of approach to development and maintenance of the supporting model
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

## Setup Instructions

### Prerequisites
- Python 3.11+
- Conda
- Azure Functions Core Tools
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

### Setting up the Environments Using conda

For the API environment:
   ```
   conda env create -f config/environment_api_local.yml
   ```

For the model environment:
   ```
   conda env create -f config/environment_model_local.yml
   ```


## Updating Environments
If changes are made to the environment files, update your existing environments using:

For the API environment:
   ```
   conda env update -f config/environment_api_local.yml
   ```

For the model environment:
   ```
   conda env update -f config/environment_model_local.yml
   ```


Note: Always update your environments when pulling changes that modify the environment files to ensure you have all necessary dependencies.
## Activating Environments

To activate the API environment: 
   ```
   conda activate instagram-topic-classifier-api
   ```
To activate the model environment: 
   ```
   conda activate instagram-topic-classifier-model
   ```

Remember to activate the appropriate environment before running tests or working on the respective components of the project.

### Azure Deployment Environments
The environment_api_azure.yml and environment_model_azure.yml files in the config/ directory are used for deployment to Azure. These environments are set up automatically during the deployment process and don't need to be created locally.
Note: The Azure environment files contain only the packages necessary for running the application in Azure and do not include testing packages.

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

Remember, while high coverage is important, it's equally important to have meaningful tests that verify the correct behavior of code.

## Deployment

### Setting Up Azure Resources

Before deploying your application, you need to set up the necessary Azure resources. Follow these steps to create an Azure account and set up the required components for Azure ML and Azure Functions.

#### 1. Login to or Create an Azure Account

1. Go to the [Azure website](https://azure.microsoft.com/en-us/free/) and click on "Sign In" or "Create a free account".
2a. If signing in, make sure you have some credit or valid payment info to activate Azure features.  
2b. If creating a new accout, follow the registration process, which will require you to provide some personal information and a credit card for identity verification (you won't be charged unless you explicitly upgrade).

#### 2. Set Up Azure Resources

Once you have accessed your Azure account, you need to create the necessary resources:

##### Create a Resource Group

1. Sign in to the [Azure Portal](https://portal.azure.com/).
2. Click on "Resource groups" in the left menu.
3. Click "Create" to make a new resource group.
4. Choose a name for your resource group and select a region.
5. Click "Review + create", then "Create".

##### Set Up Azure Machine Learning

1. In the Azure Portal, click "Create a resource".
2. Search for "Machine Learning" and select it.
3. Click "Create".
4. Fill in the required information, including:
   - Workspace name
   - Subscription
   - Resource group (select the one you just created)
   - Location
5. Click "Review + create", then "Create".
6. Wait for the deployment to complete.

##### Create an Azure ML Endpoint

1. Go to your Azure ML workspace.
2. In the left menu, under "Assets", click on "Endpoints".
3. Click "Create".
4. Choose "Real-time endpoint" and click "Next".
5. Give your endpoint a name (e.g., "exp-p-eu-topic-classifier").
6. Configure the compute and deployment settings as needed.
7. Click "Create" and wait for the endpoint to be created.

##### Set Up Azure Functions

1. In the Azure Portal, click "Create a resource".
2. Search for "Function App" and select it.
3. Click "Create".
4. Fill in the required information, including:
   - Function App name
   - Subscription
   - Resource group (select the one you created earlier)
   - Operating System (choose "Linux")
   - Runtime stack (choose "Python")
   - Version (choose the appropriate Python version)
5. Click "Review + create", then "Create".
6. Wait for the deployment to complete.

#### Setting Up Deployment Credentials

Now that you have created the necessary Azure resources, you need to set up several secrets in your GitHub repository. These secrets allow the GitHub Actions workflows to securely authenticate with Azure and access the necessary resources. Follow these steps to set up the required secrets:

1. **Navigate to your GitHub repository**
   - Go to the main page of your repository on GitHub.

2. **Access the repository settings**
   - Click on "Settings" in the top menu bar.

3. **Open the Secrets and Variables section**
   - In the left sidebar, click on "Secrets and variables", then select "Actions".

4. **Add the following secrets:**

   a. `AZURE_CREDENTIALS`
      - In the Azure Portal, open the Azure Cloud Shell.
      - Run the following command, replacing the placeholders with your values:
        ```
        az ad sp create-for-rbac --name "myapp-sp" --role contributor \
                                 --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
                                 --sdk-auth
        ```
      - Copy the entire JSON output.
      - In GitHub, click "New repository secret".
      - Name: `AZURE_CREDENTIALS`
      - Value: Paste the entire JSON output from the Azure CLI command.

   b. `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`
      - In the Azure Portal, go to your Function App you created earlier.
      - Click on "Overview", then "Get publish profile".
      - Copy the entire contents of the downloaded file.
      - In GitHub, click "New repository secret".
      - Name: `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`
      - Value: Paste the entire contents of the publish profile.

   c. `AZURE_RESOURCE_GROUP`
      - In GitHub, click "New repository secret".
      - Name: `AZURE_RESOURCE_GROUP`
      - Value: The name of the Azure Resource Group you created earlier.

   d. `AZURE_ML_WORKSPACE`
      - In GitHub, click "New repository secret".
      - Name: `AZURE_ML_WORKSPACE`
      - Value: The name of your Azure Machine Learning workspace you created earlier.

   e. `MODEL_ENDPOINT_URL`
      - In the Azure Portal, go to your ML model endpoint you created earlier.
      - In the endpoint details, find and copy the REST endpoint URL.
      - In GitHub, click "New repository secret".
      - Name: `MODEL_ENDPOINT_URL`
      - Value: Paste the endpoint URL.

   f. `MODEL_KEY`
      - In the Azure Portal, in your ML model endpoint details, find the Primary or Secondary key.
      - In GitHub, click "New repository secret".
      - Name: `MODEL_KEY`
      - Value: Paste the endpoint key.

   g. `AZURE_ML_ENDPOINT_NAME`
      - In GitHub, click "New repository secret".
      - Name: `AZURE_ML_ENDPOINT_NAME`
      - Value: The name of your Azure ML endpoint you created earlier.
  
   h. `AZURE_FUNCTIONAPP_NAME`
      - In the Azure Portal, in your Function App details, the name.
      - In GitHub, click "New repository secret".
      - Name: `AZURE_FUNCTIONAPP_NAME`
      - Value: Paste the function app name.

6. **Verify your secrets**
   - After adding all secrets, you should see them listed (with values hidden) in the "Actions secrets" section.

These secrets will be securely used by the GitHub Actions workflows to authenticate and interact with your Azure resources during the deployment process.

Remember to never share these secrets or commit them directly to your repository. GitHub Actions will automatically redact any accidental prints of these secrets in your workflow logs.

By setting up these secrets, you're ensuring that your CI/CD pipeline can securely access and deploy to your Azure resources without exposing sensitive information.

### Deploying the Model to Azure ML

After correctly configuring your Azure workspace and github secrets, the pipeline from model-ci-cd.yml can be used to deploy the model from the Actions tab.

### Deploying the API to Azure Functions

After correctly configuring your Azure workspace and github secrets, the pipeline from api-ci-cd.yml can be used to deploy the API from the Actions tab.

## Blue-Green Deployment Process
1. Pipelines deploy new versions to 'green' slot
2. Run smoke tests against 'green' slot
3. Gradually shift traffic from 'blue' to 'green'
4. Monitor for any issues
5. If successful, update 'blue' slot to match 'green'
6. If issues occur, revert traffic back to 'blue'

Criteria for full shift to green:
- All smoke tests pass
- Error rate below threshold
- Response times within acceptable range
- No significant increase in resource usage

## Scaling and Stress Testing
### Scaling
- Azure Functions: Auto-scales based on the number of events it needs to process
- Azure ML: Can be scaled by adjusting the AKS cluster

### Stress Testing
1. Use tools like Apache JMeter or Locust for load testing
2. Create test scenarios mimicking expected traffic patterns
3. Monitor performance metrics in Azure Monitor
4. Adjust scaling settings based on test results

## Configuration Management
This project uses environment variables for configuration. To set up:

1. Copy `.env.example` to `.env`
2. Fill in the values in `.env` with your actual configuration

For local development, also create a `local.settings.json` file in your function app directory.

Note: Never commit your `.env` or `local.settings.json` files to version control.

## Continuous Integration
This project uses GitHub Actions for CI/CD. The pipelines are defined in `.github/workflows/`:
- `api-ci-cd.yml`: CI/CD for the API
- `model-ci-cd.yml`: CI/CD for the model

Our CI pipeline automatically runs tests and checks coverage for all pull requests. You can see the results in the GitHub Actions tab of the repository.

The pipeline will post a comment on your pull request with the current coverage percentages for both the model and API components.

## Future Enhancements
1. Rate Limiting
   - Implement rate limiting in Azure API Management and storage warnings to manage cost
2. Azure Monitor Integration
   - Set up more comprehensive monitoring using Azure Monitor
3. Containerization
   - Migrate to a containerized solution deployed on Azure Kubernetes Service (AKS) with custom components to allow more granular control
4. Additional Testing
   - Implement more extensive integration and regression tests
   - Set up continuous testing pipelines independently from deployment pipelines to reduce unnecessary test execution
5. Security Enhancements
   - Implement Azure AD authentication or key based auth depending on other business and integration reqs

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
Travis - email@example.com

Project Link: [https://github.com/travsta/instagram-topic-classification](https://github.com/travsta/instagram-topic-classification)
