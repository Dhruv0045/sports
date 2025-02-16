from github import Github

GITHUB_TOKEN = "your_new_generated_token_here"
REPO_NAME = "Dhruv0045/sports"

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

files = repo.get_contents("")
print("📂 Files in the repository:")
for file in files:
    print(file.path)  # This should list all files
