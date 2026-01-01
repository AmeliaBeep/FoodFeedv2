from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models.user import User
from models.content import Post
from core.database import SessionLocal, engine, Base
import models, schemas

# from fastapi import FastAPI, Depends, Request, Form, HTTPException
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.templating import Jinja2Templates
# from sqlalchemy.orm import Session
# from database import SessionLocal, engine, Base
# from models import User, Post
# from passlib.context import CryptContext


# Create tables
Base.metadata.create_all(bind=engine)

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

"""
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
"""

# Registration
# @app.get("/register", response_class=HTMLResponse)
# def register_page(request: Request):
#     return templates.TemplateResponse("register.html", {"request": request})

# @app.post("/register")
# def register(
#     request: Request, 
#     username: str = Form(...), 
#     password: str = Form(...), 
#     db: Session = Depends(get_db)
# ):
#     if db.query(User).filter(User.username == username).first():
#         return templates.TemplateResponse(
#             "register.html", {"request": request, "error": "Username already exists"}
#         )

#     hashed_password = pwd_context.hash(password)
#     user = User(username=username, hashed_password=hashed_password)
#     db.add(user)
#     db.commit()
#     return RedirectResponse(url="/login", status_code=303)

# # Login
# @app.get("/login", response_class=HTMLResponse)
# def login_page(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})

# @app.post("/login")
# def login(
#     request: Request, 
#     username: str = Form(...), 
#     password: str = Form(...), 
#     db: Session = Depends(get_db)
# ):
#     user = db.query(User).filter(User.username == username).first()
#     if not user:
#         return templates.TemplateResponse(
#             "login.html", {"request": request, "error": "User not found"}
#         )
#     if not pwd_context.verify(password, user.hashed_password):
#         return templates.TemplateResponse(
#             "login.html", {"request": request, "error": "Incorrect password"}
#         )
    
#     response = RedirectResponse(url="/", status_code=303)
#     response.set_cookie(key="user_id", value=str(user.id), httponly=True)
#     return response

# # Logout
# @app.get("/logout")
# def logout():
#     response = RedirectResponse(url="/login", status_code=303)
#     response.delete_cookie("user_id")
#     return response

# Home Page
@app.get("/", response_class=HTMLResponse)
def read_index(request: Request, db: Session = Depends(get_db)):
    
    posts = db.query(Post).all()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "posts": posts,
        }
    )

# Add Post
@app.post("/posts")
def add_post(request: Request, title: str = Form(...), db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)
    post = Post(title=title, owner_id=int(user_id))
    db.add(post)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

# Toggle Complete
@app.post("/posts/{post_id}/toggle")
def toggle_post(post_id: int, request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == int(user_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.completed = not post.completed
    db.commit()
    return RedirectResponse(url="/", status_code=303)

# Delete Post
@app.post("/posts/{post_id}/delete")
def delete_post(post_id: int, request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == int(user_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

# Update Post
@app.post("/posts/{post_id}/update")
def update_post(post_id: int, request: Request, title: str = Form(...), db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == int(user_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.title = title
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/add-post", response_class=HTMLResponse)
def add_post_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse("add_post.html", {"request": request, "user": user})
