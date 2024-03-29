import creds
import google.generativeai as genai
import chromadb
from langchain_google_genai import ChatGoogleGenerativeAI
from chromadb import Documents, EmbeddingFunction, Embeddings
import cloneGit
import reading_files
import pandas as pd
# If there is no env variable set for API key, you can pass the API key
# to the parameter `google_api_key` of the `ChatGoogleGenerativeAI` function:
# `google_api_key="key"`.


genai.configure(api_key=creds.GeminiAPI)


# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

model = genai.GenerativeModel('gemini-pro')

# response = model.generate_content("Hi")
# print(response.text)

# llm = ChatGoogleGenerativeAI(model="gemini-pro",
#                  temperature=0.7, top_p=0.85)



# for m in genai.list_models():
#   if 'embedContent' in m.supported_generation_methods:
#     print(m.name)

class GeminiEmbeddingFunction(EmbeddingFunction):
  def __call__(self, input: Documents) -> Embeddings:
    model = 'models/embedding-001'
    title = "Custom query"
    return genai.embed_content(model=model,
                                content=input,
                                task_type="retrieval_document",
                                title=title)["embedding"]


def create_chroma_db(documents, name):
  chroma_client = chromadb.Client()
  db = chroma_client.create_collection(name=name, embedding_function=GeminiEmbeddingFunction())

  for i, d in enumerate(documents):
    # Ensure that 'd' is a list of Document objects
    if not isinstance(d, list):
      d = [d] # Wrap the Document object in a list

    db.add(
      documents=d,
      ids=str(i)
    )
  return db

def main():
    repo_url = "https://github.com/apache/spark.git"
    local_dir = "cloned_repo" 
    cloneGit.clone_repository(repo_url, local_dir)
    print("\nAll files in the repository directory:")
    all_files = cloneGit.list_files_repo(local_dir)
    print(f"Number of code files cloned: {len(all_files)}")

    chunks = reading_files.load_split_file(local_dir)

    db = create_chroma_db(chunks, "Embeddings")
    pd.DataFrame(db.peek(3))
    


    cloneGit.delete_repository(local_dir)

if __name__ == "__main__":
    main()
