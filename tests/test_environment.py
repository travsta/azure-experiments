import os
import pytest
from dotenv import load_dotenv
import yaml
import conda.cli.python_api as Conda

def test_env_variables_loaded():
    """
    Test if required environment variables are loaded from .env file.
    """
    load_dotenv()
    assert 'MODEL_ENDPOINT_URL' in os.environ, "MODEL_ENDPOINT_URL not found in environment. Ensure it's set in your .env file. The .env.example file can be used as a template"
    assert 'MODEL_KEY' in os.environ, "MODEL_KEY not found in environment. Ensure it's set in your .env file."

def test_conda_environment_api():
    """
    Test if the API Conda environment is set up correctly with all required packages.
    """
    with open('config/environment_api_local.yml', 'r') as f:
        env_config = yaml.safe_load(f)
    
    env_name = env_config['name']
    
    # Check if the environment exists
    envs = Conda.run_command(Conda.Commands.INFO, "--json")[0]
    env_names = [os.path.basename(env) for env in envs['envs']]
    assert env_name in env_names, f"Conda environment '{env_name}' not found. Run 'conda env create -f config/environment_api_local.yml' to create it."

    # Check if key packages are installed
    packages = Conda.run_command(Conda.Commands.LIST, "-n", env_name, "--json")[0]
    package_names = [package['name'] for package in packages]
    
    required_packages = ['python', 'pip', 'requests', 'azure-functions']
    for package in required_packages:
        assert package in package_names, f"Package '{package}' not found in '{env_name}' environment. Run 'conda install -n {env_name} {package}' to install it."

def test_conda_environment_model():
    """
    Test if the Model Conda environment is set up correctly with all required packages.
    """
    with open('config/environment_model_local.yml', 'r') as f:
        env_config = yaml.safe_load(f)
    
    env_name = env_config['name']
    
    # Check if the environment exists
    envs = Conda.run_command(Conda.Commands.INFO, "--json")[0]
    env_names = [os.path.basename(env) for env in envs['envs']]
    assert env_name in env_names, f"Conda environment '{env_name}' not found. Run 'conda env create -f config/environment_model_local.yml' to create it."

    # Check if key packages are installed
    packages = Conda.run_command(Conda.Commands.LIST, "-n", env_name, "--json")[0]
    package_names = [package['name'] for package in packages]
    
    required_packages = ['python', 'pip', 'numpy', 'scikit-learn']
    for package in required_packages:
        assert package in package_names, f"Package '{package}' not found in '{env_name}' environment. Run 'conda install -n {env_name} {package}' to install it."

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