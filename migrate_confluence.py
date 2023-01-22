import json
from atlassian import Confluence

# Read credentials from .secrets.json file
with open(".secrets.json", "r") as f:
    creds = json.load(f)

# Connect to Confluence using personal token
confluence = Confluence(url=creds["url"], personal_token=creds["personal_token"])

# Define a function to convert a Confluence page to markdown
def confluence_to_markdown(page_id):
    page = confluence.get_page_by_id(page_id)
    markdown = confluence.convert_content_to_markdown(page["body"]["storage"]["value"])
    return markdown

# Use the function to export a specific Confluence page to markdown
page_id = 12345
markdown = confluence_to_markdown(page_id)
print(markdown)