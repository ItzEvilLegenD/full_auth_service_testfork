#библиотеки
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import httpx

#импорты из файлов
from routers.routes_8001 import LoginRequest


# еще незакоченная версия

QUERY_URL = "http://127.0.0.1:8003" 
BACKEND_URL = "http://127.0.0.1:8000" 

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # исключения
        path = request.url.path

        if path in ["/docs", "/openapi.json"]:
            return await call_next(request)
        
        body = None
        # Логика для /register
        if path == "/register" and request.method == "POST":
            try:
                body = await request.json()
                user = LoginRequest(**body)
                query_url = f"{QUERY_URL}{path}"
                # Асинхронный запрос к Query_Service для проверки существования пользователя
                async with httpx.AsyncClient() as client:
                    try:
                        response = await client.request(
                            method='POST',
                            url=query_url, 
                            params={"username": user.username}, 
                            timeout=5
                        )
                        
                        return JSONResponse(
                            status_code=response.status_code,
                            content=response.json(),
                            headers=dict(response.headers)
                        )

                    except httpx.RequestError:
                        return JSONResponse(status_code=503, content={"detail": "Database connection failed"})
                    except Exception as e:
                        return JSONResponse(status_code=500, content={"detail": str(e)})
                
            except Exception as e:
                return JSONResponse(status_code=400, content={"detail": str(e)})

        # Логика для /signin
        elif path == "/signin" and request.method == "POST":
            try:
                body = await request.json()
                user = LoginRequest(**body)

                # Асинхронный запрос к Query_Service для проверки логина и пароля
                async with httpx.AsyncClient() as client:
                    try:
                        response = await client.get(f"{QUERY_URL}{path}", params={"username": user.username}, timeout=5)
                    except httpx.RequestError as e:
                        return JSONResponse(status_code=503, content={"detail": "Database connection failed"})
                
                if response.status_code == 200:
                    
                    headers = {
                        "x-username": user.username,
                        "x-user-hashed_password": str(hash(user.password))  
                    }
                    return JSONResponse(
                        status_code=200,
                        content={"message": "Login successfully"},
                        headers=headers  
                    )
                elif response.status_code == 401:
                    return JSONResponse(status_code=401, content={"detail": "Invalid username or password"})
                else:
                    raise HTTPException(status_code=response.status_code, detail="Error communicating with database")
            except Exception as e:
                return JSONResponse(status_code=400, content={"detail": str(e)})

        # Логика для остальных маршрутов
        else:
            
            x_username = request.headers.get("x-username")
            x_hashed_password = request.headers.get("x-user-hashed_password")

            if not x_username or not x_hashed_password:
                return JSONResponse(status_code=403, content={"detail": "Forbidden"})

            # Перенаправление запроса на Backend
            async with httpx.AsyncClient() as client:
                try:
                    
                    backend_url = f"{BACKEND_URL}{path}"
                    method = request.method
                    body = None

                    if request.method in ["POST", "GET", "DELETE"]:
                        body = await request.json()

                    # Отправляем запрос на Backend
                    response = await client.request(method, backend_url, json=body, timeout=5.0)

                    # Возвращаем ответ от Backend
                    return JSONResponse(
                        status_code=response.status_code,
                        content=response.json(),
                        headers=dict(response.headers)
                    )
                except httpx.RequestError:
                    return JSONResponse(status_code=503, content={"detail": "Service unavailable"})
                except Exception as e:
                    return JSONResponse(status_code=500, content={"detail": str(e)})