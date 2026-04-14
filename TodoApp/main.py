from fastapi import FastAPI, Request, status
from .models import Base
from .database import engine
from .routers import Auth, admin, todos, users
from fastapi.staticfiles import StaticFiles
from .config import templates

app = FastAPI()

Base.metadata.create_all(bind=engine)



app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/healthy")
def health_check():
    return{'status': 'Healthy'}

app.include_router(Auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)