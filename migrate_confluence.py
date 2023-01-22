from atlassian import Confluence
from atlassian import AzureDevOps
import json

# Load secrets from JSON file
with open(".secrets.json", "r") as secrets_file:
    secrets = json.load(secrets_file)

confluence_url = secrets["confluence_url"]
azure_devops_url = secrets["azure_devops_url"]
space_key = secrets["space_key"]
project_name = secrets["project_name"]
confluence_token = secrets["confluence_token"]
azure_devops_token = secrets["azure_devops_token"]

confluence = Confluence(
    url=confluence_url,
    username=confluence_token
)

azure_devops = AzureDevOps(
    url=azure_devops_url,
    personal_access_token=azure_devops_token
)

def export_import_pages(parent_id):
    child_pages = confluence.get_children_of_page(parent_id)
    return child_pages