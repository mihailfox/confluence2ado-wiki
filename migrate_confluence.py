from atlassian import Confluence
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

def confluence_to_markdown(page_id):
    page = confluence.get_page_by_id(page_id)
    markdown = confluence.convert_content_to_markdown(page["body"]["storage"]["value"])
    return markdown

# Use the function to export a specific Confluence page to markdown
page_id = 12345
markdown = confluence_to_markdown(page_id)
print(markdown)