import os
from fastapi import FastAPI, File, UploadFile, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from pathlib import Path
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain import PromptTemplate, HuggingFaceHub
from langchain.chains import RetrievalQA

import models
from database import engine, sessionLocal
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Initialize the embedding model and the llm
embedding_model_name = "intfloat/e5-base-v2"
llm_repo_id = "tiiuae/falcon-7b-instruct"

# Define a dependency for creating an embedding model
def get_embedding_model():
    # embedding_model_name = 'intfloat/e5-base-v2'
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    return embeddings

# Define a dependency for creating an llm
def get_llm():
    # repo_id = "tiiuae/falcon-7b-instruct"
    llm = HuggingFaceHub(
        repo_id=llm_repo_id,
        huggingfacehub_api_token='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',
        model_kwargs={"temperature":0.6, "max_new_tokens":1024}
    )
    return llm


## setup the database

models.Base.metadata.create_all(bind=engine)
def get_db():
    db = sessionLocal()
    try: yield db
    finally: db.close()

# Define a dependency for creating a prompt template
def get_prompt_template():
    template = """
    You are a helpfull assistant. you gives helpful, summarized, and polite answers to the user's questions given the below context.

    {context}

    question: {question}
    """
    prompt = PromptTemplate(template=template, input_variables=['context', "question"])
    return prompt

# Define a global variable for the vector database
vectordb = None

# Define a function for processing uploaded files and creating embeddings in the background
def process_files(files: list[UploadFile], embeddings: HuggingFaceEmbeddings):
    global vectordb # use the global variable
    # Create loaders for each file
    loaders = [UnstructuredFileLoader(file.file) for file in files]
    # Load the documents from each loader
    documents = [loader.load()[0] for loader in loaders]
    # Split the documents into text parts using RecursiveCharacterTextSplitter
    docs = RecursiveCharacterTextSplitter(
        chunk_size=750,
        chunk_overlap=100,
        separators=[",", "\n", "\n\n"]
    ).split_documents(documents)
    # Create a chroma database from the documents and embeddings
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory='db'
    )





# Define a global variable for the vector database
vectordb = None


# Define an endpoint for uploading text files and creating embeddings
@app.post("/upload_files/")
async def upload_files(
    files: list[UploadFile] = File(...),
    embeddings: HuggingFaceEmbeddings = Depends(get_embedding_model),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    # Validate that all files are text files by checking their content type
    for file in files:
        if not file.content_type.startswith("text/"):
            return JSONResponse(status_code=400, content={"message": f"Invalid file type: {file.content_type}"})
    
    # Add a background task to process the files and create embeddings asynchronously
    background_tasks.add_task(process_files, files, embeddings)

    # Return a success message with the number of documents processed
    return {"message": f"Processed {len(files)} documents"}


# Define an endpoint for performing similarity search on a query
@app.get("/similarity_search/")
async def similarity_search(
    query: str,
    embeddings: HuggingFaceEmbeddings = Depends(get_embedding_model)
):
    global vectordb # use the global variable
    # Check if the vector database is initialized
    if vectordb is None:
        return JSONResponse(status_code=400, content={"message": "No documents uploaded yet"})
    # Check if the query is not empty
    if not query:
        return JSONResponse(status_code=400, content={"message": "Query cannot be empty"})
    # Perform similarity search on the query using the vector database
    docs = vectordb.similarity_search(query)
    # Return a list of matching documents with their metadata and page content
    return {"results": [{"metadata": doc.metadata,
                        "page_content": doc.page_content} for doc in docs]}



# Define an endpoint for asking questions over the data using RetrievalQA
@app.get("/ask-with-data/")
async def ask_question_with_data(
    question: str,
    llm: HuggingFaceHub = Depends(get_llm),
    prompt: PromptTemplate = Depends(get_prompt_template)
    ):
    global vectordb  # use the global variable
# Check if the vector database is initialized
    if vectordb is None:
        return JSONResponse(status_code=400, content={"message": "No documents uploaded yet"})
    # Check if the question is not empty
    if not question:
        return JSONResponse(status_code=400, content={"message": "Question cannot be empty"})
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
        "answer": results['result'],
        "source_documents": results['source_documents']
    }


# Define an endpoint for asking questions over the data using RetrievalQA
@app.get("/ask/")
async def ask_question(
    question: str,
    llm: HuggingFaceHub = Depends(get_llm),
    ):

    template = """
You are a helpfull assistant. you gives helpful, summarized, and polite answers to the user's questions.
question: {question}
""".format(question=question)
    
    results = llm(template)
    return {
        "answer": results
    }