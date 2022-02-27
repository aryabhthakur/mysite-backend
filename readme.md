This project is distributed into two part, **Backend** and **Frontend**.
| Repo | URL 
|---------------|--------------------
| Frontend - Next.js (ReactJS)| https://github.com 
| Backend - FastAPI (Python) | https://github.com 

You are currently in **Backend** Repo developed in Python3 using FastAPI, 
Before you start using it, Install required packages by running following command in your Terminal from project path, where main.py file is located.

    pip install -r requirements.txt

To start server type the following command in your Terminal.

     uvicorn main:app --reload --host localhost --port 8000
  This will start [uvicorn](https://github.com/encode/uvicorn) server, you can access server using `http://localhost:8000` and API Docs at `http://localhost:8000/docs` it uses Swagger UI for API documentations.

There's couple of extra files in `apis/*` which contains in-active APIs or under-development APIs, you can delete them, if you want to. Here's folder structure :
|Folder / File | Description  |
|--|--|
| apis/* | Contains all APIs, each file is set of APIs related to db models 
| database/* | Contains all Database CRUD functions, DB Models, Pydantic Schemas & DB interface 
| main.py | Main App file containing FastAPI initialisation, routes, middlewares & so on.

> If your are getting CORS error, add your domain or ip or access url to main.py 's origins list.

Open Issue if you are facing any kind of errors. Package list can be found in requirements.txt

**Note** :  

> This API is knowingly limited to one-user registration, Coz its suppose to a personal portfolio site.
>  Soon I will release a platform version of it, with features like Articles, Roles, Better Authentication and so on. 