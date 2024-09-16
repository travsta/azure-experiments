#!/bin/bash

set -e

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Setting up API development environment using environment files in config/ ..."

if ! command -v conda &> /dev/null; then
    echo "Conda is not installed. Please install Conda and try again."
    exit 1
fi

ENV_NAME="instagram-topic-classifier-api"

if conda info --envs | grep -q $ENV_NAME; then
    read -p "Environment '$ENV_NAME' already exists. Do you want to recreate it? (y/[N]): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        conda env remove -n $ENV_NAME
    else
        read -p "Do you want to update the existing environment? ([Y]/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            REPLY="y"
        fi
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Exiting without changes."
            exit 0
        fi
    fi
fi

# Check if this is for Azure deployment
read -p "Is this for Azure deployment? (y/[N]): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ENV_FILE="$SCRIPT_DIR/../config/environment_api_azure.yml"
else
    ENV_FILE="$SCRIPT_DIR/../config/environment_api_local.yml"
fi

echo "Creating/Updating Conda environment for API development using $ENV_FILE..."

if conda info --envs | grep -q $ENV_NAME; then
    conda env update -f "$ENV_FILE" -n $ENV_NAME
else
    conda env create -f "$ENV_FILE"
fi

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate $ENV_NAME

if ! command -v npm &> /dev/null; then
    echo "npm is not installed. Please install Node.js and npm, then run this script again."
    exit 1
fi

echo "Installing Azure Functions Core Tools..."
npm install -g azure-functions-core-tools@3 --unsafe-perm true

echo "API development environment setup complete."
echo "To activate this environment, use: conda activate $ENV_NAME"