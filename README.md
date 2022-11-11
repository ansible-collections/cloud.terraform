# cloud.terraform

## Development

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip wheel
pip install -r requirements.txt
ANSIBLE_COLLECTIONS_PATH="../../" ansible-galaxy collection install -r requirements.yml

# second pass for requirements in collections
pip install -r  ../../azure/azcollection/requirements-azure.txt
pip install --no-deps "azure-cli==$(pip freeze | grep azure-cli-core | sed -E "s/.*?==(.*)/\1/")"
```

## Testing

To run integration tests, install `terraform` and ensure it is in your `PATH`.
If you want to run cloud integration tests, ensure you log in to the clouds:

```shell
# using the "default" profile on AWS
aws configure set aws_access_key_id     my-access-key
aws configure set aws_secret_access_key my-secret-key
aws configure set region                eu-north-1

# Azure login
az login
az account set --subscription <id>

# GCP login
gcloud auth application-default login
gcloud auth application-default set-quota-project <id>

ansible-test integration [target]
```
