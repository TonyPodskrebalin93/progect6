from fastapi import FastAPI, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/')
async def get_(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {"request": request, "users": users})

@app.get('/users/{user_id}')
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {"request": request, "user": users[user_id-1]})


@app.delete('/user/{user_id}')
async def delete_user(user_id: int):
    try:
        user = users.pop(user_id - 1)
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.post('/user/{username}/{age}')
async def create_user(user: User, username: str, age: int):
    user.id = 1 if not users else users[-1].id + 1
    user.username = username
    user.age = age
    users.append(user)
    print(users)
    return user


@app.put('/user/{user_id}/{username}/{age}')
def update_user(user_id: int, username: str, age: int, user: str = Body()):
    try:
        edit_user = users[user_id - 1]
        print(edit_user)
        edit_user.username = username
        edit_user.age = age
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")