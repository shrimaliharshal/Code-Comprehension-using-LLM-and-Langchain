import git
import shutil
from pathlib import Path
from git import Repo
import os
def clone_repository(repo_url, local_dir):
    """
    Clones a GitHub repository to a specified local directory.
    """
    try:
        print(f"Cloning {repo_url} into {local_dir}")
        git.Repo.clone_from(repo_url, local_dir)
        print("Clone successful")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_repository(local_dir):
    """
    Deletes a cloned repository from the local file system.
    """
    try:
        shutil.rmtree(local_dir)
        print(f"Deleted {local_dir}")
    except Exception as e:
        print(f"Error deleting the directory: {e}")

def list_files_repo(repo_dir):
    """
    Lists all the files in the cloned repository directory.

    :param repo_dir: The path to the repository's local directory.
    :return: A list of paths to files within the repository.
    """
    files_list = []
    for root, dirs, files in os.walk(repo_dir):
        if ".git" in root:
            continue
        for file in files:
            # Construct the full filepath by joining the root with the file name
            file_path = os.path.join(root, file)
            files_list.append(file_path)
    return files_list

def main():
    repo_url = "https://github.com/shrimaliharshal/Real-time-Reddit-sentiment-analyzer.git" 
    local_dir = "cloned_repo" 

    
    clone_repository(repo_url, local_dir)
    
    print("\nAll files in the repository directory:")
    all_files = list_files_repo(local_dir)
    for file in all_files:
        print(file)
    print(f"Number of code files cloned: {len(all_files)}")

        
    delete_repository(local_dir)

if __name__ == "__main__":
    main()
