import os

GITHUB_TOKEN = os.getenv("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")  # Make sure you're using the correct variable

if not GITHUB_TOKEN:
    print("❌ GitHub token is missing!")
else:
    print("✅ Token is loaded successfully!")
