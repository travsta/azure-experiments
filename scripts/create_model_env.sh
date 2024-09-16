#!/bin/bash

set -e

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Setting up model development environment using environment files in config/ ..."

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

# Check if this is for Azure deployment
read -p "Is this for Azure deployment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ENV_FILE="$SCRIPT_DIR/../config/environment_model_azure.yml"
else
    ENV_FILE="$SCRIPT_DIR/../config/environment_model_local.yml"
fi

echo "Creating Conda environment for model development using $ENV_FILE..."

conda env create -f "$ENV_FILE"

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate $ENV_NAME

echo "Model development environment setup complete."
echo "To activate this environment, use: conda activate $ENV_NAME"