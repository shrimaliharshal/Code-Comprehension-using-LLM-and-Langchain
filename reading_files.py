from langchain import PromptTemplate, LLMChain

import creds
import cloneGit
import os
import uuid
import subprocess
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


from langchain.text_splitter import RecursiveCharacterTextSplitter, Language

from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser


def load_split_file(repo_path):
    loader = GenericLoader.from_filesystem(
        repo_path+ "/python",
        glob="**/*",
        suffixes=[".py"],
        exclude=["**/non-utf8-encoding.py"],
        parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),
    )
    documents = loader.load()
    print("Length of docs:",len(documents))
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
    )
    texts = python_splitter.split_documents(documents)
    print("Length of splits:",len(texts))
    return texts

def main():
    repo_url = "https://github.com/apache/spark.git"
    local_dir = "cloned_repo" 

        
    cloneGit.clone_repository(repo_url, local_dir)
        
    print("\nAll files in the repository directory:")
    all_files = cloneGit.list_files_repo(local_dir)
    # for file in all_files:
    #         print(file)
    print(f"Number of code files cloned: {len(all_files)}")
    # loading file
    
    
    chunks = load_split_file(local_dir)
    cloneGit.delete_repository(local_dir)

if __name__ == "__main__":
    main()