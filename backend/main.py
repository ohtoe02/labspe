from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Any
import logging
from db import database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Docker Compose Web App",
    description="API для работы с пользователями в веб-приложении",
    version="1.0.0"
)

@app.middleware("http")
async def add_utf8_header(request, call_next):
    response = await call_next(request)
    if response.headers.get("content-type", "").startswith("application/json"):
        response.headers["content-type"] = "application/json; charset=utf-8"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Имя пользователя")
    email: EmailStr = Field(..., description="Email адрес пользователя")

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: str

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Any = None

@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI приложение запускается...")
    if database.connect():
        logger.info("Подключение к базе данных установлено")
    else:
        logger.error("Не удалось подключиться к базе данных")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FastAPI приложение останавливается...")
    database.disconnect()

@app.get("/", response_model=Dict[str, str])
async def read_root():
    return {
        "message": "FastAPI бэкенд работает!",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health", response_model=Dict[str, str])
async def health_check():
    db_status = "connected" if database.is_connected() else "disconnected"
    return {
        "status": "healthy",
        "database": db_status,
        "message": "Все системы работают"
    }

@app.get("/api/users", response_model=APIResponse)
async def get_users():
    try:
        users = database.get_users()
        logger.info(f"API: получен запрос на список пользователей, найдено: {len(users)}")
        
        return APIResponse(
            success=True,
            message="Пользователи получены успешно",
            data={"users": users}
        )
        
    except Exception as e:
        logger.error(f"API: ошибка при получении пользователей: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера при получении пользователей"
        )

@app.post("/api/users", response_model=APIResponse)
async def create_user(user: UserCreate):
    try:
        logger.info(f"API: получен запрос на создание пользователя: {user.name}, {user.email}")
        
        user_id = database.add_user(user.name, user.email)
        
        if user_id:
            logger.info(f"API: пользователь создан с ID: {user_id}")
            return APIResponse(
                success=True,
                message="Пользователь добавлен успешно",
                data={"user_id": user_id}
            )
        else:
            logger.error("API: не удалось добавить пользователя в базу данных")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удалось добавить пользователя. Возможно, email уже используется."
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API: неожиданная ошибка при создании пользователя: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера при создании пользователя"
        )

@app.get("/api/users/{user_id}", response_model=APIResponse)
async def get_user(user_id: int):
    return APIResponse(
        success=False,
        message="Endpoint не реализован",
        data=None
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 