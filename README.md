# privteGPTServer
a fast-api server to talk with state-of-the-art LLM Open source Models with/out your custom data


## Introductions
privategptserver is using state-of-the-art open source large language models (as of now it's `falcon7B`) allowing users   
to opt in run the server and call the LLM with api calls or integrate it with your own data   
by simply upload your pdf file and chat with it **without the need for powerfull GPUs or CPUs**

> Note: this still work in progress and it's in the very early stage but it works 
> i plan to add more LLM and optimize the server and would be more than happy to accpet any contribution  

## How to install **pre-requests** packages with single command
this repo uses poetry as package managent to ease the devlopement so you need to install it first
```bash
pip install poetry
```
and then jsut run the below command to install all needed packages
```bash
poetry install
```
## How to run ?
this server uses `falcon7B` model and `e5-base-v2` embeddings so it need to download these  
models which require roughly `~6 GB` free from your Disk and RAM to load it 
```bash 
poetry run uvicorn main:app 
#or
#poetry run uvicorn main:app --port $PORT 
```
