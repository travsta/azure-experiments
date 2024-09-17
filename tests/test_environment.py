import os
import pytest
from dotenv import load_dotenv
import yaml
import conda.cli.python_api as Conda

def test_env_variables_loaded():
    load_dotenv()
    assert 'MODEL_ENDPOINT_URL' in os.environ
    assert 'MODEL_KEY' in os.environ

def test_conda_environment_api():
    with open('config/environment_api_local.yml', 'r') as f:
        env_config = yaml.safe_load(f)
    
    env_name = env_config['name']
    
    # Check if the environment exists
    envs = Conda.run_command(Conda.Commands.INFO, "--json")[0]
    env_names = [os.path.basename(env) for env in envs['envs']]
    assert env_name in env_names

    # Check if key packages are installed
    packages = Conda.run_command(Conda.Commands.LIST, "-n", env_name, "--json")[0]
    package_names = [package['name'] for package in packages]
    
    required_packages = ['python', 'pip', 'requests', 'azure-functions']
    for package in required_packages:
        assert package in package_names

def test_conda_environment_model():
    with open('config/environment_model_local.yml', 'r') as f:
        env_config = yaml.safe_load(f)
    
    env_name = env_config['name']
    
    # Check if the environment exists
    envs = Conda.run_command(Conda.Commands.INFO, "--json")[0]
    env_names = [os.path.basename(env) for env in envs['envs']]
    assert env_name in env_names

    # Check if key packages are installed
    packages = Conda.run_command(Conda.Commands.LIST, "-n", env_name, "--json")[0]
    package_names = [package['name'] for package in packages]
    
    required_packages = ['python', 'pip', 'numpy', 'scikit-learn']
    for package in required_packages:
        assert package in package_names

@pytest.mark.parametrize("config_file", [
    "config/environment_api_local.yml",
    "config/environment_api_azure.yml",
    "config/environment_model_local.yml",
    "config/environment_model_azure.yml"
])
def test_conda_env_files(config_file):
    assert os.path.isfile(config_file)
    with open(config_file, 'r') as f:
        env_config = yaml.safe_load(f)
    assert 'name' in env_config
    assert 'dependencies' in env_config