import requests
import os

# Configuration
ORG_NAME = "solvro"  # Replace with your GitHub org name
README_PATH = "../profile/README.md"  # Path to your README

# GitHub API URL
API_URL = f"https://api.github.com/orgs/{ORG_NAME}/members?page=1&per_page=100"

def fetch_org_members():
    response = requests.get(API_URL)
    if response.status_code == 200:
        print(f"Fetched {len(response.json())} members")
        return response.json()
    else:
        print(f"Error fetching members: {response.status_code}")
        return []

def generate_member_html(member):
    login = member["login"]
    avatar_url = member["avatar_url"]
    profile_url = member["html_url"]
    return f'''
  <a href="{profile_url}">
    <img style="border-radius: 50%" src="{avatar_url}" width="50" height="50" alt="@{login}" />
  </a>'''

def update_readme(members):
    with open(README_PATH, "r", encoding="utf-8") as file:
        readme_content = file.read()

    new_members_html = "\n".join([generate_member_html(m) for m in members])


    start = readme_content.find("<!-- START_SECTION:members -->")
    end = readme_content.find("<!-- END_SECTION:members -->")

    if start != -1 and end != -1:
        start += len("<!-- START_SECTION:members -->")
        updated_content = readme_content[:start] + "\n" + new_members_html + "\n" + readme_content[end:]
    else:
        print("Error parsing README")
        return

    if not os.path.exists(README_PATH):
        print(f"README not found at {README_PATH}")
        return

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(updated_content)

    print("README updated")

if __name__ == "__main__":
    members = fetch_org_members()
    if members:
        update_readme(members)
    else:
        print("No members fetched.")


