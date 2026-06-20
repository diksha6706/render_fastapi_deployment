from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, schemas
from auth import create_access_token, verify_token
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

##db dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

##login api
@app.post("/login")
def login():
    return {
        "access_token": create_access_token({"user": "admin"}),
        "token_type": "bearer"
    }
##home route
@app.get("/")
def home():
    return {"message": "Blog API is working!"}

##create blog(protected route)
@app.post("/blogs", response_model=schemas.BlogResponse)
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db), user = Depends(verify_token)):
    new_blog = models.Blog(title=blog.title, content=blog.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

##get all blogs
@app.get("/blogs")
def get_blogs(page: int = 1, limit: int = 5, search: str = Query(default=""), db: Session = Depends(get_db)):
    blogs = db.query(models.Blog)
    if search:
        blogs = blogs.filter(models.Blog.title.ilike(f"%{search}%"))

    total = blogs.count()
    start = (page - 1) * limit
    blogs = blogs.offset(start).limit(limit).all()
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "blogs": blogs
    }
    

##get blog by id
@app.get("/blogs/{blog_id}", response_model=schemas.BlogResponse)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

##update blog(protected route)
@app.put("/blogs/{blog_id}", response_model=schemas.BlogResponse)
def update_blog(blog_id: int, blog_update: schemas.BlogUpdate, db: Session = Depends(get_db), user= Depends(verify_token)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog.title = blog_update.title
    blog.content = blog_update.content
    db.commit()
    db.refresh(blog)
    return blog

##delete blog(protected route)
@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db), user= Depends(verify_token)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted successfully"}

