from atlassian import Confluence
from atlassian import AzureDevOps
import json
import os

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

def export_page(child_page):
    export_content = confluence.get_page_as_markdown(child_page['id'])
    with open(f"{child_page['title']}.md", "w") as md_file:
        md_file.write(export_content)
    return child_page["title"]

def import_page(file_name):
    with open(f"{file_name}.md", "r") as md_file:
        md_content = md_file.read()
    azure_devops.create_wiki_page(project_name, file_name, md_content)
    os.remove(f"{file_name}.md")

root_page = confluence.get_root_page(space_key)
child_pages = export_import_pages(root_page["id"])

for child_page in child_pages:
    file_name = export_page(child_page)
    #import_page(file_name)