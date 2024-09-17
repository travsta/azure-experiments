import os
import pytest
from dotenv import load_dotenv
import yaml

def test_env_variables_loaded():
    """
    Test if required environment variables are loaded from .env file.
    """
    load_dotenv()
    assert 'MODEL_ENDPOINT_URL' in os.environ, "MODEL_ENDPOINT_URL not found in environment. Ensure it's set in your .env file."
    assert 'MODEL_KEY' in os.environ, "MODEL_KEY not found in environment. Ensure it's set in your .env file."

@pytest.mark.parametrize("config_file", [
    "config/environment_api_local.yml",
    "config/environment_api_azure.yml",
    "config/environment_model_local.yml",
    "config/environment_model_azure.yml"
])
def test_conda_env_files(config_file):
    """
    Test if all required Conda environment configuration files exist and have the correct structure.
    """
    assert os.path.isfile(config_file), f"Configuration file '{config_file}' not found. Ensure it exists in the config directory."
    with open(config_file, 'r') as f:
        env_config = yaml.safe_load(f)
    assert 'name' in env_config, f"'name' key not found in '{config_file}'. Ensure the file has a 'name' field specifying the environment name."
    assert 'dependencies' in env_config, f"'dependencies' key not found in '{config_file}'. Ensure the file has a 'dependencies' field listing required packages."

def test_project_structure():
    """
    Test if the basic project structure is correct.
    """
    assert os.path.isdir("src"), "The 'src' directory is missing. Ensure the project structure is correct."
    assert os.path.isdir("src/api"), "The 'src/api' directory is missing. Ensure the project structure is correct."
    assert os.path.isdir("src/model"), "The 'src/model' directory is missing. Ensure the project structure is correct."
    assert os.path.isdir("tests"), "The 'tests' directory is missing. Ensure the project structure is correct."
    assert os.path.isdir("config"), "The 'config' directory is missing. Ensure the project structure is correct."
    assert os.path.isdir("scripts"), "The 'scripts' directory is missing. Ensure the project structure is correct."