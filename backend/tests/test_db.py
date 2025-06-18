import pytest
from unittest.mock import MagicMock, patch, call
import sys
import os

# Добавляем путь к модулям приложения
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import database

class TestDatabase:
    """Тесты для модуля работы с базой данных"""

    @patch('db.mysql.connector.connect')
    def test_connect_success(self, mock_connect):
        """Тест успешного подключения к базе данных"""
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        
        result = database.connect()
        
        assert result is True
        mock_connect.assert_called_once()

    @patch('db.mysql.connector.connect')
    def test_connect_failure(self, mock_connect):
        """Тест неудачного подключения к базе данных"""
        mock_connect.side_effect = Exception("Connection failed")
        
        result = database.connect()
        
        assert result is False

    def test_is_connected_true(self):
        """Тест проверки подключения - подключен"""
        database.connection = MagicMock()
        database.connection.is_connected.return_value = True
        
        result = database.is_connected()
        
        assert result is True

    def test_is_connected_false(self):
        """Тест проверки подключения - не подключен"""
        database.connection = None
        
        result = database.is_connected()
        
        assert result is False

    def test_disconnect_with_connection(self):
        """Тест отключения при наличии соединения"""
        mock_connection = MagicMock()
        database.connection = mock_connection
        
        database.disconnect()
        
        mock_connection.close.assert_called_once()
        assert database.connection is None

    def test_disconnect_without_connection(self):
        """Тест отключения без соединения"""
        database.connection = None
        
        # Не должно вызывать исключений
        database.disconnect()
        
        assert database.connection is None

    @patch('db.database.connection')
    def test_get_users_success(self, mock_connection):
        """Тест успешного получения пользователей"""
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, "Test User", "test@example.com", "2024-01-01 12:00:00")
        ]
        
        result = database.get_users()
        
        assert len(result) == 1
        assert result[0]["name"] == "Test User"
        assert result[0]["email"] == "test@example.com"

    @patch('db.database.connection')
    def test_get_users_failure(self, mock_connection):
        """Тест ошибки при получении пользователей"""
        mock_connection.cursor.side_effect = Exception("Database error")
        
        result = database.get_users()
        
        assert result == []

    @patch('db.database.connection')
    def test_add_user_success(self, mock_connection):
        """Тест успешного добавления пользователя"""
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.lastrowid = 123
        
        result = database.add_user("New User", "new@example.com")
        
        assert result == 123
        mock_connection.commit.assert_called_once()

    @patch('db.database.connection')
    def test_add_user_failure(self, mock_connection):
        """Тест ошибки при добавлении пользователя"""
        mock_connection.cursor.side_effect = Exception("Database error")
        
        result = database.add_user("New User", "new@example.com")
        
        assert result is None
        mock_connection.rollback.assert_called_once() 