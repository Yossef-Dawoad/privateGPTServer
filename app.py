import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain import PromptTemplate, HuggingFaceHub
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Initialize the embedding model and the llm
embedding_model_name = "intfloat/e5-base-v2"
embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

repo_id = "tiiuae/falcon-7b-instruct"
llm = HuggingFaceHub(
    repo_id=repo_id,
    huggingfacehub_api_token=os.getenv("huggingfacehub_api_token"),
    model_kwargs={"temperature": 0.6, "max_new_tokens": 1024},
)

# Define a template for the prompt
template = """
You are a helpfull assistant. you gives helpful, summarized, and polite answers to the user's questions given the below context.

{context}

question: {question}
"""
prompt = PromptTemplate(template=template, input_variables=["context", "question"])

# Define a global variable for the vector database
vectordb = None


# Define an endpoint for uploading text files and creating embeddings
@app.post("/upload_files/")
async def upload_files(files: list[UploadFile] = File(...)):
    global vectordb  # use the global variable
    # Create loaders for each file
    loaders = [UnstructuredFileLoader(file.file) for file in files]
    # Load the documents from each loader
    documents = [loader.load()[0] for loader in loaders]
    # Split the documents into text parts using RecursiveCharacterTextSplitter
    docs = RecursiveCharacterTextSplitter(
        chunk_size=750, chunk_overlap=100, separators=[",", "\n", "\n\n"]
    ).split_documents(documents)
    # Create a chroma database from the documents and embeddings
    vectordb = Chroma.from_documents(
        documents=docs, embedding=embeddings, persist_directory="db"
    )
    # Return a success message with the number of documents processed
    return {"message": f"Processed {len(documents)} documents"}


# Define an endpoint for performing similarity search on a query
@app.get("/similarity_search/")
async def similarity_search(query: str):
    global vectordb  # use the global variable
    # Check if the vector database is initialized
    if vectordb is None:
        return JSONResponse(
            status_code=400, content={"message": "No documents uploaded yet"}
        )
    # Perform similarity search on the query using the vector database
    docs = vectordb.similarity_search(query)
    # Return a list of matching documents with their metadata and page content
    return {
        "results": [
            {"metadata": doc.metadata, "page_content": doc.page_content} for doc in docs
        ]
    }


# Define an endpoint for asking questions over the data using RetrievalQA
@app.get("/ask_question/")
async def ask_question(question: str):
    global vectordb  # use the global variable
    # Check if the vector database is initialized
    if vectordb is None:
        return JSONResponse(
            status_code=400, content={"message": "No documents uploaded yet"}
        )
    # Create a RetrievalQA object using the llm, vector database and prompt template
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever(),
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True,
    )
    # Ask the question using the RetrievalQA object and get the results
    results = qa(question)
    # Return the answer and the source documents used to generate it
    return {
        "answer": results["result"],
        "source_documents": results["source_documents"],
    }
