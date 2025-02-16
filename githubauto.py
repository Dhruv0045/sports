from github import Github

GITHUB_TOKEN = "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"
REPO_NAME = "Dhruv0045/sports"

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

files = repo.get_contents("")
print("📂 Files in the repository:")
for file in files:
    print(file.path)  # This should list all files
