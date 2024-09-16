#!/bin/bash

set -e

echo "Setting up model development environment using config/environment_model.yml ..."

if ! command -v conda &> /dev/null; then
    echo "Conda is not installed. Please install Conda and try again."
    exit 1
fi

ENV_NAME="instagram-topic-classifier-model"

if conda info --envs | grep -q $ENV_NAME; then
    read -p "Environment '$ENV_NAME' already exists. Recreate? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        conda env remove -n $ENV_NAME
    else
        echo "Exiting without changes."
        exit 0
    fi
fi

echo "Creating Conda environment for model development..."

# Check if this is for Azure deployment
read -p "Is this for Azure deployment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    AZURE_DEPLOY=1 conda env create -f environment_model.yml
else
    conda env create -f environment_model.yml
fi

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate $ENV_NAME

echo "Model development environment setup complete."
echo "To activate this environment, use: conda activate $ENV_NAME"
