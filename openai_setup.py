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


openai_api_key = creds.openai_api_key
repo_url = "https://github.com/apache/spark.git"
local_dir = "cloned_repo" 
cloneGit.clone_repository(repo_url, local_dir)
print("\nAll files in the repository directory:")
all_files = cloneGit.list_files_repo(local_dir)
print(f"Number of code files cloned: {len(all_files)}")
chunks = reading_files.load_split_file(local_dir)

db = Chroma.from_documents(chunks, OpenAIEmbeddings(disallowed_special=(),openai_api_key=openai_api_key))
retriever = db.as_retriever(
    search_type="mmr",  # Also test "similarity"
    search_kwargs={"k": 8},
)

llm = ChatOpenAI(model_name="gpt-3.5-turbo",openai_api_key = openai_api_key)
memory = ConversationSummaryMemory(
    llm=llm, memory_key="chat_history", return_messages=True
)
qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)
question = "What is this ode repository about"
result = qa(question)

result = qa.invoke(question)
# result["answer"]
print(result["answer"])

cloneGit.delete_repository(local_dir)
