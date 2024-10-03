#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if an argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <environment>"
    echo "Where <environment> is either 'model' or 'api'"
    exit 1
fi

# Set the environment
ENV=$1

# Activate the correct conda environment
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate instagram-topic-classifier-$ENV

# Ensure pytest-cov is installed
pip install pytest-cov

# Define test files for each environment
MODEL_TEST_FILES=("tests/test_score.py" "tests/test_dummy_model.py" "tests/test_environment.py")
API_TEST_FILES=("tests/test_function_app.py" "tests/test_environment.py")

# Run pytest with coverage
if [ "$ENV" == "model" ]; then
    echo "Executing tests in: "
    echo "${MODEL_TEST_FILES[@]}"
    pytest --cov=src/model --cov-report=term-missing --cov-report=xml --cov-fail-under=80 "${MODEL_TEST_FILES[@]}"
elif [ "$ENV" == "api" ]; then
    echo "Executing tests in: "
    echo "${API_TEST_FILES[@]}"
    pytest --cov=src/api --cov-report=term-missing --cov-report=xml --cov-fail-under=80 "${API_TEST_FILES[@]}"
else
    echo "Invalid environment: $ENV"
    echo "Usage: $0 <environment>"
    echo "Where <environment> is either 'model' or 'api'"
    exit 1
fi

# Deactivate the conda environment
conda deactivate

echo "Coverage report has been generated. Open htmlcov/index.html to view the detailed report."
