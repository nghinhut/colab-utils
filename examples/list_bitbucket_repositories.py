import os
import sys
from pathlib import Path

import colab_utils as utils


def main():
    # Set your Bitbucket credentials
    # In a real scenario, you'd want to use environment variables or a secure method to store these
    os.environ['BITBUCKET_USERNAME'] = 'your_bitbucket_username'
    os.environ['BITBUCKET_APP_PASSWORD'] = 'your_bitbucket_app_password'

    # Set your Bitbucket workspace slug
    workspace = "your-workspace-slug"  # Replace with your actual workspace slug

    try:
        # List repositories
        repos = utils.bitbucket.list_bitbucket_repos(workspace)

        # Print repository information
        print(f"Found {len(repos)} repositories in workspace '{workspace}':\n")
        for repo in repos:
            print(f"Name: {repo['name']}")
            print(f"Slug: {repo['slug']}")
            print(f"Description: {repo.get('description', 'No description')}")
            print(f"Created on: {repo['created_on']}")
            print(f"Updated on: {repo['updated_on']}")
            print(f"Main branch: {repo['mainbranch']['name']}")
            print(f"URL: {repo['links']['html']['href']}")
            print("-" * 50)

        # Optional: Handle pagination if there are more than 100 repositories
        if len(repos) == 100:
            print("There might be more repositories. Implement pagination to fetch them all.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()