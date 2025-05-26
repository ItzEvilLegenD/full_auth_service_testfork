from fastapi import FastAPI
import uvicorn
import sys
import asyncio
from query_database import Base, async_engine 
from query_router import router as query_router 

# Создаем экземпляр FastAPI
app = FastAPI(
    title="Query Service API",
    description="Service to interact with PostgreSQL database for user data.",
)

# Функция для создания таблиц при старте (если их нет)
@app.on_event("startup")
async def startup_event():
    try:
        async with async_engine.begin() as conn:
            print("Creating database tables...")
            # Строку раскоментировать, если нужно удалять таблицы при каждом запуске
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            print("Database tables created.")
    except Exception as e:
        print(f"Error during startup: {e}")
        sys.exit(1)

app.include_router(query_router)

# Точка входа для запуска через uvicorn (если запускать как скрипт)
async def run_server(app, port):
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(
        run_server(app, 8003),
    )

if __name__ == '__main__':
       asyncio.run(main())
