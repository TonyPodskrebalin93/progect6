from fastapi import FastAPI, Path, HTTPException
from typing import Annotated, List
from pydantic import BaseModel


app = FastAPI()
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/users')
async def get_users() -> List[User]:
    # Возвращаем список всех пользователей
    return users


@app.post('/user/{username}/{age}')
async def registered_user(username: str, age: int) -> User:
    # Регистрируем нового пользователя с уникальным ID
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int) -> User:
    # Обновляем данные существующего пользователя
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user

    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def deleted_user(user_id: int) -> User:
    # Удаляем пользователя по его ID
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user

    raise HTTPException(status_code=404, detail='User was not found')