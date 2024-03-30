from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI
import cloneGit
import reading_files
import creds
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import uuid

openai_api_key = creds.openai_api_key

# Prompt the user to enter the GitHub repository URL
repo_url = input("Please enter the GitHub repository URL: ")

# Basic validation for the URL (optional)
if not repo_url.startswith("http://") and not repo_url.startswith("https://"):
    print("Please enter a valid URL.")
else:
    local_dir = "cloned_repo" 
    cloneGit.clone_repository(repo_url, local_dir)
    print("\nAll files in the repository directory:")

    all_files = cloneGit.list_files_repo(local_dir)
    print(f"Number of code files cloned: {len(all_files)}")
    chunks = reading_files.load_split_file(local_dir)

    # Ensure each chunk has a unique ID
    chunks_with_ids = [(uuid.uuid4().hex, chunk) for chunk in chunks]

    # Convert list of tuples into two lists
    ids, texts = zip(*chunks_with_ids)  # Separates IDs and texts into two lists

    db = Chroma.from_documents(texts, OpenAIEmbeddings(disallowed_special=(),openai_api_key=openai_api_key), ids=ids)
    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 8},
    )

    llm = ChatOpenAI(model_name="gpt-3.5-turbo",openai_api_key = openai_api_key)
    memory = ConversationSummaryMemory(
        llm=llm, memory_key="chat_history", return_messages=True
    )
    qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)
    question = "Explain what does this repository do and mention some of the functions and system design of the given application in the repo"
    result = qa.invoke(question)
    print(result["answer"])

    cloneGit.delete_repository(local_dir)
