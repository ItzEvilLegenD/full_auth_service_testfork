from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx  # Для запросов к Postgres
from pydantic import BaseModel, EmailStr
app = FastAPI()

# Конфигурация
POSTGRES_SERVICE_URL = "http://localhost:8003"  # URL Postgres-сервиса

# Модель данных
class UserCreate(BaseModel):
    user_id: int
    name: str
    age: int
    email: EmailStr
    role: str
    username: str
    hashed_password: str

# получение x-username и x-user-hashed-password
def verify_auth(request: Request):
    # Получает значения заголовков из HTTP-запроса
    x_username = request.headers.get("x-username")
    x_password = request.headers.get("x-user-hashed-password")
    # if not (x_username and x_password):
    #    raise HTTPException(status_code=401, detail="Missing authentication headers")
    return {"username": x_username, "hashed_password": x_password}

# Маршруты
@app.post("/add_user")
async def add_user(user_data: UserCreate, request: Request):
    # Получить словарь или ошибку
    auth = verify_auth(request) # Ничего не делает
    
    # Переадресация запроса к Postgres (8003)
    async with httpx.AsyncClient() as client:
        postgres_response = await client.post(
            f"{POSTGRES_SERVICE_URL}/add_user", # Куда отправлять запрос
            json=user_data.dict(),# конвертирует Pydantic-модель в словарь (тело запроса)
        )
    
    # Вернуть ответ клиенту
    return JSONResponse(content=postgres_response.json(), status_code=postgres_response.status_code)

@app.delete("/delete_user/{user_id}")
async def delete_user(user_id: int, request: Request):

    auth = verify_auth(request)
    
    async with httpx.AsyncClient() as client:
        postgres_response = await client.delete(
            f"{POSTGRES_SERVICE_URL}/delete_user/{user_id}",
        )
    

    return JSONResponse(content=postgres_response.json(), status_code=postgres_response.status_code)

@app.get("/get_user/{user_id}")
async def get_all_users(user_id: int, request: Request):

    auth = verify_auth(request)
    
    async with httpx.AsyncClient() as client:
        postgres_response = await client.get(
            f"{POSTGRES_SERVICE_URL}/get_user/{user_id}",
        )

    # возможно, JSONResponse некорректно обработает результат, если получен список
    return JSONResponse(content=postgres_response.json(), status_code=postgres_response.status_code)

@app.get("/get_all_users")
async def get_all_users(request: Request):

    auth = verify_auth(request)
    
    async with httpx.AsyncClient() as client:
        postgres_response = await client.get(
            f"{POSTGRES_SERVICE_URL}/get_all_users",
        )

    # возможно, JSONResponse некорректно обработает результат, если получен список
    return JSONResponse(content=postgres_response.json(), status_code=postgres_response.status_code)

    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_back:app", host="0.0.0.0", port=8000, reload=True)