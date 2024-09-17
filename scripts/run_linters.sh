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

# Run pylint
echo "Running pylint..."
pylint src/$ENV tests/$ENV

# Run flake8
echo "Running flake8..."
flake8 src/$ENV tests/$ENV

# Deactivate the conda environment
conda deactivate

echo "Linting completed."