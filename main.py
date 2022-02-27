import time
from fastapi import  FastAPI, Request
from database import models
from database.database import engine
from fastapi.security import OAuth2PasswordBearer
from dotenv import dotenv_values
from fastapi.middleware import gzip, trustedhost,cors
from apis import auth as AuthApi
from apis import frameworks as FrameworksApi
from apis import languages as LanguagesApi
from apis import projects as ProjectsApi
from apis import relations as RelationsApi
env = dotenv_values(".env")
models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

openapi_tags = [
    {
        "name":"Authentication",
        "description": "Endpoint relate to User Authentiocation or CRUD operations on <b>User Model & Schemas</b>",
    },
    {
        "name":"Articles",
        "description": "Endpoint relate to CRUD operations on <b>Articles Model & Schemas</b>",
    },
    {
        "name":"Projects",
        "description": "Endpoint relate to CRUD operations on <b>Projects Model & Schemas</b>",
    },
    {
        "name":"Languages",
        "description": "Endpoint relate to CRUD operations on <b>Languages Model & Schemas</b>",
    },
    {
        "name":"Frameworks",
        "description": "Endpoint relate to CRUD operations on <b>Frameworks Model & Schemas</b>",
    },
    {
        "name":"Relations",
        "description": "Endpoint relate to CRUD operations on <b>Relations Model & Schemas</b>",
    }
]
# FastApi Starts
app = FastAPI(
        title="Personal Site Api",
    description="Backend Api Server for My personal site based on Fastapi, for Developer CMS (<a href='https://github.com/aryabhthakur/'>Github</a>)",
    version="0.1",
    contact={
        "name": "Demo",
        "url": "https://aryabh.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=openapi_tags
)
origins = {
    "http://192.168.1.6",
    "http://192.168.1.6:3000",
    "http://0.0.0.0",
    "http://0.0.0.0:3000",    
    "http://localhost",
    "http://localhost:3000",  
}
# app.add_middleware(
#     trustedhost.TrustedHostMiddleware, allowed_hosts=env['TRUSTED_HOSTS']
# )
app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(gzip.GZipMiddleware)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Api Routes

app.include_router(AuthApi.router,tags=['Authentication'])
app.include_router(ProjectsApi.router,tags=['Projects'],prefix='/projects')
app.include_router(LanguagesApi.router,tags=['Languages'],prefix='/languages')
app.include_router(FrameworksApi.router,tags=['Frameworks'],prefix='/frameworks')
app.include_router(RelationsApi.router,tags=['Relations'],prefix='/relations')


    



    