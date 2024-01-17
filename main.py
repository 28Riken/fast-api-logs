from fastapi import FastAPI, HTTPException, Depends
from fastapi.openapi.models import Response
from pydantic import BaseModel
from typing import List
import logging


logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

info_handler = logging.FileHandler('app.log')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

logger = logging.getLogger('')
logger.addHandler(info_handler)

warning_handler = logging.FileHandler('warnings.log')
warning_handler.setLevel(logging.WARNING)
warning_handler.setFormatter(formatter)

logger = logging.getLogger('')
logger.addHandler(warning_handler)

error_handler = logging.FileHandler('errors.log')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

logger = logging.getLogger('')
logger.addHandler(error_handler)


app = FastAPI()


class Blog(BaseModel):
    title: str
    content: str

blogs = []

@app.post("/blogs/", response_model=Blog)
def create_blog(blog: Blog):
    blogs.append(blog)
    return blog

@app.get("/blogs/", response_model=List[Blog])
def read_blogs():
    return blogs

@app.get("/blogs/{blog_id=0000}", response_model=Blog)
def read_blog(blog_id: int):
    if blog_id < 0 or blog_id >= len(blogs):
        raise HTTPException(status_code=404, detail="Blog not found")
    return blogs[blog_id]

@app.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(blog_id: int, updated_blog: Blog):
    if blog_id < 0 or blog_id >= len(blogs):
        raise HTTPException(status_code=404, detail="Blog not found")
    blogs[blog_id] = updated_blog
    return updated_blog

@app.delete("/blogs/{blog_id}", response_model=Response)
def delete_blog(blog_id: int):
    if blog_id < 0 or blog_id >= len(blogs):
        raise HTTPException(status_code=404, detail="Blog not found")
    deleted_blog = blogs.pop(blog_id)
    return {"message": f"Blog with ID {blog_id} has been deleted", "deleted_blog": deleted_blog}
