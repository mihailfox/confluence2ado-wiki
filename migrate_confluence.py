import zipfile
import requests
import os
import json
import html2text
from bs4 import BeautifulSoup


# Load secrets from JSON file
with open(".secrets.json", "r") as secrets_file:
    secrets = json.load(secrets_file)

confluence_url = secrets["confluence_url"]
azure_devops_url = secrets["azure_devops_url"]
space_key = secrets["space_key"]
project_name = secrets["project_name"]
confluence_token = secrets["confluence_token"]
azure_devops_token = secrets["azure_devops_token"]

def export_import_pages(parent_id):
    # Get list of child pages for the parent page
    child_pages_url = f"{confluence_url}/content?spaceKey={space_key}&parentId={parent_id}"
    child_pages_response = requests.get(child_pages_url, headers={"Authorization": f"Basic {confluence_token}"})
    child_pages = child_pages_response.json()["results"]
    return child_pages

def export_page(child_page):
    export_url = f"{confluence_url}/content/{child_page['id']}/export/html"
    response = requests.get(export_url, headers={"Authorization": f"Basic {confluence_token}"})
    open(f"{child_page['title']}.html", "wb").write(response.content)
    return child_page["title"]

def convert_to_markdown(file_name):
    with open(f"{file_name}.html", "r") as html_file:
        html_content = html_file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    # Replace macro elements with their corresponding markdown representation
    for macro in soup.find_all(class_='confluence-macro'):
        macro_type = macro['data-macro-name']
        macro_body = macro.find_all('span')[0].get_text()
       
        if macro_type == 'code':
            macro_markdown = f"```{macro_body}```"
        elif macro_type == 'image':
            macro_markdown = f"![image]({macro_body})"
        else:
            macro_markdown = f"Macro of type {macro_type} is not supported"
        macro.replace_with(macro_markdown)

    # Use a library such as 'html2text' to convert the HTML to markdown
    md_content = html2text.html2text(str(soup))
    with open(f"{file_name}.md", "w") as md_file:
        md_file.write(md_content)
    os.remove(f"{file_name}.html")
    return file_name

def import_page(file_name):
    with open(f"{file_name}.md", "r") as md_file:
        md_content = md_file.read()
    import_url = f"{azure_devops_url}/{project_name}/_apis/wiki/wikis/{file_name}/pages?path={file_name}&content={md_content}"
    response = requests.put(import_url, headers={"Authorization": f"Basic {azure_devops_token}"})
    if response.status_code != 200:
        print(f"Error: Failed to import {file_name} to Azure DevOps Wiki. Status code: {response.status_code}")
    else:
        print(f"{file_name} imported to Azure DevOps Wiki with status code {response.status_code}")
        os.remove(f"{file_name}.md")

# Start recursive export and import with the root page
root_url = f"{confluence_url}/content?spaceKey={space_key}&expand=ancestors"
root_response = requests.get(root_url, headers={"Authorization": f"Basic {confluence_token}"})
root_page = root_response.json()["results"][0]

child_pages = export_import_pages(root_page["id"])

for child_page in child_pages:
    file_name = export_page(child_page)
    file_name = convert_to_markdown(file_name)
    #import_page(file_name)
