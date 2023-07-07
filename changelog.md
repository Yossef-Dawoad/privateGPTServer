## version 0.0.2
- using `-` instead of `underscore` for the endpoints
- add `ask/` endpoint for asking the llms directtly without data chatgpt style
- adding changeLog to track changes 

## version 0.0.3
- refactoring the code and big improvment across the codebase.  
- Use dependency injection to create a single instance of the embedding model,
the llm and the prompt template, and inject them into the endpoints that need them.
This would avoid creating them multiple times and make the code more modular and testable.  

- Use FastAPI's background tasks to process the uploaded files and create the embeddings 
asynchronously.This would improve the performance and responsiveness of the server, 
as it would not block the request while doing the heavy computation.  

- Add some error handling and validation to the endpoints,
such as checking if the files are valid text files, if the query or question is not empty
if the vector database is not corrupted, etc. This would make the server more robust and user-friendly.  

- Add some documentation and comments to the code, explaining what each endpoint does, what
parameters it expects and returns, what libraries and models it uses, etc. This would make
the code more readable and maintainable
- add requirements.txt file

## version 0.0.4+dev
- reorganized the code directory
- added docker support - postgress-database + pgadmin  
- dummy database setup not in use yet and not implemented correctly
- add `/api/` route for better consistancy 
