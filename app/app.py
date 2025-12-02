from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate

app = FastAPI()

text_posts = {
    1: {"title": "First Post", "content": "This is the content of the first post"},
    2: {"title": "Second Post", "content": "This is the content of the second post"},
    3: {"title": "Third Post", "content": "This is the content of the third post"},
    4: {"title": "Fourth Post", "content": "This is the content of the fourth post"},
    5: {"title": "Fifth Post", "content": "This is the content of the fifth post"},
    6: {"title": "Sixth Post", "content": "This is the content of the sixth post"},
    7: {"title": "Seventh Post", "content": "This is the content of the seventh post"},
    8: {"title": "Eighth Post", "content": "This is the content of the eighth post"},
    9: {"title": "Ninth Post", "content": "This is the content of the ninth post"},
    10: {"title": "Tenth Post", "content": "This is the content of the tenth post"},
}


@app.get('/api/root')
def root():
    return {"Message": "Welcome to my API"}    

@app.get("/api/posts")
def get_all_posts(limit: int = None): #poti sa faci sa fie obligatoriu 
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    if post_id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(post_id)


@app.post("/api/posts")
def create_post(post: PostCreate):
    post_id = max(text_posts.keys()) + 1
    text_posts[post_id] = post.model_dump()
    return text_posts[post_id]

@app.delte("/api/posts/{post_id}")
def delete_post(post_id: int):
    if post_id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    text.post

