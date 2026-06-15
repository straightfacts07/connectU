from fastapi import FastAPI ,HTTPException
from app.schema import PostCreate
app = FastAPI()

text_post = {
    1: {"title": "post", "content": "cool post"},
    2: {"title": "travel", "content": "visited a new city"},
    3: {"title": "food", "content": "had delicious pizza"},
    4: {"title": "coding", "content": "learned FastAPI today"},
    5: {"title": "movie", "content": "watched a great film"},
    6: {"title": "music", "content": "listening to new songs"},
    7: {"title": "fitness", "content": "completed morning workout"},
    8: {"title": "books", "content": "reading a mystery novel"},
    9: {"title": "gaming", "content": "finished a tough level"},
    10: {"title": "work", "content": "completed project milestone"}
}

#limit is a list operation while text_post is a dictionary
#we will use query parameters inside of a function
@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_post.values())[:limit]
    return text_post

@app.get("/posts/{id}")
def get_post(id:int):
    if id not in text_post:
        raise HTTPException(status_code=404,detail="post not found")
    return text_post.get(id)



#we sent data from post api through a request body
#we gonna create a schema for this
#as we use pydantic model by default fastapi knows we are receiving a request body
#fastapi automatically identifies the type of  the data sent
#based on the data set in schema

@app.post("/posts")
def create_post(post:PostCreate):
    new_post={"title":post.title,"content":post.content}
    text_post[max(text_post.keys())+1] = new_post
    return new_post
     
#output type= by default docs doesnt shows us much what type of data the api will return after a post request
#so we can specify what type of data will be returned in the api itself