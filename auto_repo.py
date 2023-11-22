#! /usr/bin/env python3

import argparse
import os
import sys
import subprocess
import traceback
import venv
from dotenv import load_dotenv
from git import Repo
from github import Github

# only if you want to load the settings from a file
# import yaml

# Alternatively, load the settings from the settings file from the directory where the script is located
# script_dir = os.path.dirname(os.path.realpath(__file__))
# settings_file = os.path.join(script_dir, 'settings.yml')
# with open('settings.yml', 'r') as f:
#     settings = yaml.safe_load(f)


def create_directory(repo_parent_dir, repo_name):
    repo_path = os.path.join(repo_parent_dir, repo_name)
    try:
        os.mkdir(repo_path)
        return repo_path
    except FileExistsError as e:
        print(f"Directory {repo_name} already exists: {e}")
    except Exception as e:
        print(f"Failed to create directory {repo_name}: {e}")
        print(traceback.format_exc())
        sys.exit(1)
    return repo_path


def init_repo(repo_path, repo_name):
    try:
        repo = Repo.init(repo_path)

        # Create a new README.md file
        print(os.path.join(repo_path, "README.md"))
        with open(os.path.join(repo_path, "README.md"), "w") as f:
            f.write("New Project")

        # Make a local commit
        repo.git.add("--all")
        try:
            repo.git.commit("-m", "Initial commit")
        except:
            print("No changes to commit")
        # Create a new GitHub repo
        github = Github(github_token)
        user = github.get_user()
        github_repo = user.create_repo(repo_name)

        # Push the local commit to the GitHub repo
        origin = repo.create_remote("origin", github_repo.html_url)
        origin.push(refspec="master:master")
        return repo_path
    except Exception as e:
        print(f"Failed to initialize repo {repo_name}: {e}")
        print(traceback.format_exc())
        sys.exit(1)


# Create a virtual environment
def create_venv(repo_path, name=".venv"):
    print(os.path.join(repo_path, name))

    try:
        venv.create(os.path.join(repo_path, name))
        # Create a .gitignore file that includes .venv
        with open(os.path.join(repo_path, ".gitignore"), "w") as f:
            f.write(".venv\n")
    except Exception as e:
        print(f"Failed to create virtual environment: {e}")
        print(traceback.format_exc())
        sys.exit(1)


def open_vscode(repo_path):
    # Open VS Code
    subprocess.run([vscode_path, repo_path])


def main_cli():
    parser = argparse.ArgumentParser(
        prog="auto-repo",
        description="Initializes a development environment using python "
        "virtual environments, git, and VS Code",
        epilog="Contribute at: https://github.com/sam-ueckert/auto_repo",
    )
    parser.add_argument("repository-parent-directory")
    parser.add_argument("repository-name")
    args = parser.parse_args()
    repo_name = vars(args)["repository-name"]
    repo_path = create_directory(vars(args)["repository-parent-directory"], repo_name)

    load_dotenv()

    github_token = os.getenv("GITHUB_PAT")
    vscode_path = os.getenv("VSCODE_LOCATION")

    print(repo_path)
    init_repo(repo_path, repo_name)
    create_venv(repo_path)
    open_vscode(repo_path)


if __name__ == "__main__":
    main_cli()
