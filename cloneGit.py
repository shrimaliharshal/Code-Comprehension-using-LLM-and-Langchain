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

def list_tracked_files_in_repo(repo_path):
    """
    Lists all files tracked by Git in the specified repository.
    """
    try:
        repo = Repo(repo_path)
        if repo.bare:
            print("The specified repository is bare and does not contain a working copy.")
            return []

        # Getting a list of all files currently tracked by Git
        # This includes files in the latest commit on the currently checked-out branch
        files = []
        for item in repo.index.iter_blobs():
            # Ensure we're accessing the blob object correctly
            # If 'item' is a tuple, it might be structured differently, and the blob object could be accessed differently
            if isinstance(item, tuple):
                # If 'item' is a tuple, adjust this line to correctly access the blob object
                # Example adjustment if the blob is the first item in the tuple: blob = item[0]
                blob = item[0]  # Adjust this line based on the actual structure of 'item'
            else:
                blob = item

            # Access the path of the blob object
            files.append(blob.path)
        
        return files
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


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
        for file in files:
            # Construct the full filepath by joining the root with the file name
            file_path = os.path.join(root, file)
            files_list.append(file_path)
    return files_list





repo_url = "https://github.com/apache/spark.git" 
local_dir = "cloned_repo" 

    
clone_repository(repo_url, local_dir)

    
# print("\nListing all files tracked by Git:")
# tracked_files = list_tracked_files_in_repo(local_dir)
# for file in tracked_files:
#     print(file)

    
print("\nAll files in the repository directory:")
all_files = list_files_repo(local_dir)
for file in all_files:
    print(file)

    
delete_repository(local_dir)
