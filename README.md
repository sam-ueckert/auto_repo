# Quickly create a repo, upload it to GitHub, and launch Vscode in that directory
Add this script to your path to qucickly create a new repo.
Usage:
python auto_repo *parent_directory* *repo_name*

The script will create a repo with a dummy readme.md file. It will commit that file.
It will add .venv to the .gitignore.
It will create a new Python venv in the .venv subdirectory of the new repo.
It will push tje repo to Github using PAT authentication.

Modify the .env file to include youre PAT and the path to your Vscode installation.
