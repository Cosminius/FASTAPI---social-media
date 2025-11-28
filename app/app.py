from fastapi import FastAPI

app = FastAPI()

text_posts={"post1 ":{"title" : "First Post", "content": "This is the content of the first post"},
            "post2 ":{"title" : "Second Post", "content": "This is the content of the second post"},
            "post3 ":{"title" : "Third Post", "content": "This is the content of the third post"}}


@app.get('/api/root')
def root():
    return {"Message": "Welcome to my API"}    

@app.get("/api/posts")
def get_allposts():
    return text_posts

@app.get("/api/posts/{post_id}")
def get_post(post_id: str):
    post_id = post_id.strip().lower()
    return text_posts.get(post_id)