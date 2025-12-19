from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from core.database import SessionLocal, engine, Base
import models, schemas

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# dummy post


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):

    test_posts_db = [
    {
        "id":0,
        "author": "amelia test",
        "text": "my first post",
    }
]
    return templates.TemplateResponse(
        "base.html", 
        {
            "request": request, 
            "message": "Hello, World!",
            "posts": test_posts_db
        }
    )

