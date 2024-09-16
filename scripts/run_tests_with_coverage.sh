#!/bin/bash

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

# Run pytest with coverage
pytest --cov=src/$ENV --cov-report=term-missing --cov-report=html tests/$ENV

# Deactivate the conda environment
conda deactivate

echo "Coverage report has been generated. Open htmlcov/index.html to view the detailed report."