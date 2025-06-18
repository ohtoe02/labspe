import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import sys
import os

# Добавляем путь к модулям приложения
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

# Мокаем базу данных для тестов
@pytest.fixture
def mock_database():
    with patch('main.database') as mock_db:
        mock_db.connect.return_value = True
        mock_db.is_connected.return_value = True
        mock_db.get_users.return_value = [
            {
                "id": 1,
                "name": "Test User",
                "email": "test@example.com",
                "created_at": "2024-01-01 12:00:00"
            }
        ]
        mock_db.add_user.return_value = 1
        yield mock_db

def test_root_endpoint():
    """Тест главной страницы API"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "FastAPI бэкенд работает!"
    assert data["version"] == "1.0.0"
    assert data["status"] == "active"

def test_health_endpoint(mock_database):
    """Тест проверки здоровья системы"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"

def test_get_users(mock_database):
    """Тест получения списка пользователей"""
    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "users" in data["data"]
    assert len(data["data"]["users"]) == 1

def test_create_user(mock_database):
    """Тест создания нового пользователя"""
    user_data = {
        "name": "New User",
        "email": "newuser@example.com"
    }
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["user_id"] == 1

def test_create_user_invalid_email():
    """Тест создания пользователя с невалидным email"""
    user_data = {
        "name": "Test User",
        "email": "invalid-email"
    }
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 422  # Validation error

def test_create_user_empty_name():
    """Тест создания пользователя с пустым именем"""
    user_data = {
        "name": "",
        "email": "test@example.com"
    }
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 422  # Validation error

def test_get_user_not_implemented():
    """Тест получения конкретного пользователя (не реализован)"""
    response = client.get("/api/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["message"] == "Endpoint не реализован" 