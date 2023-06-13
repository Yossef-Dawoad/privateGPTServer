# privteGPTServer
a fast-api server to talk with state-of-the-art Open source LLM Models with/out your custom data


## Introductions
privategptserver is using state-of-the-art open source large language models (as of now it's `falcon7B`) allowing users   
to opt in run the server and call the LLM with api calls or integrate it with your own data   
by simply upload your pdf file and chat with it **without the need for powerfull GPUs or CPUs**

> Note: this not near a final product,this still work in progress and it's in the very early stage but it works, I plan to first  
>  easing the user experance to run the server then optimize it, adding more LLM  
>  and would be more than happy to accpet any contribution  

## How to install ?
### peotry single command
this repo uses poetry as package managent to ease the devlopement so you need to install it first
```bash
pip install poetry
```
and then jsut run the below command to install all needed packages
```bash
poetry install
```
### or  (no-poetry)   
normal `requirements.txt` with command 
```bash
pip install -r requirements.txt
```
## How to run the server ?
this server uses `falcon7B` model and `e5-base-v2` embeddings so it need to download these  
models which require roughly `~6 GB` free from your Disk and RAM to load it   
- first you have to navigate to [HuggingFaceHub](https://huggingface.co/settings/tokens) singup and generate new token   
- create `.env` file in the current directory where the `app.py` live place `huggingfacehub_api_token=YOUR-TOKEN-HERE`
- now go to the command line and type the follwing to run the server
### with poetry
```bash 
poetry run uvicorn main:app 
#or
#poetry run uvicorn main:app --port $PORT 
```
### or (no-peotry)
```bash
uvicorn main:app 
```
- now the server is running to test the api in the command line you can do the next  
first make sure you have curl installed   

**on Linux:**  
```bash 
sudo apt install curl 
```
**on Windows:**  
```bash 
winget install curl
```
## Testing the endpoints
To test the endpoints for this server in your command line, you can use curl commands like this:

- To ask a question over the llm use the `/ask/` endpoint, you can use something like:

```bash
curl http://localhost:8000/ask/?question="your question here"
```

where `your question here` is the question you want to ask.

- To upload files to the `/upload-files/` endpoint, you can use something like:

```bash
curl -L -F "file=@YourFileName" http://localhost:8000/upload_files/
```

where `filename` is the name of the file you want to upload. You can also upload multiple files by adding more `-F` options.

- To perform similarity search on a query using the `/similarity-search/` endpoint, you can use something like:

```bash
curl http://localhost:8000/similarity_search/?query="your query here"
```

where `your query here` is the text you want to search for.

- To ask a question over the data using the `/ask-with-data/` endpoint, you can use something like:

```bash
curl http://localhost:8000/ask_question/?question="your question here"
```

where `your question here` is the question you want to ask.


