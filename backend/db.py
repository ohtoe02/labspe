import mysql.connector
from mysql.connector import Error
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.host = 'mysql'
        self.database = 'webapp'
        self.user = 'appuser'
        self.password = 'apppassword'
        self.connection = None
    
    def connect(self) -> bool:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci',
                autocommit=True
            )
            
            if self.connection.is_connected():
                logger.info("Успешно подключились к MySQL базе данных")
                return True
                
        except Error as e:
            logger.error(f"Ошибка подключения к MySQL: {e}")
            return False
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Соединение с MySQL закрыто")
    
    def is_connected(self) -> bool:
        return self.connection and self.connection.is_connected()
    
    def get_users(self) -> List[Dict]:
        if not self.is_connected():
            if not self.connect():
                return []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT id, name, email, created_at FROM users ORDER BY created_at DESC"
            cursor.execute(query)
            users = cursor.fetchall()
            cursor.close()
            
            for user in users:
                if user.get('created_at'):
                    user['created_at'] = user['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            
            logger.info(f"Получено {len(users)} пользователей")
            return users
            
        except Error as e:
            logger.error(f"Ошибка при получении пользователей: {e}")
            return []
    
    def add_user(self, name: str, email: str) -> Optional[int]:
        if not self.is_connected():
            if not self.connect():
                return None
        
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO users (name, email, created_at) VALUES (%s, %s, NOW())"
            cursor.execute(query, (name.strip(), email.strip()))
            
            user_id = cursor.lastrowid
            cursor.close()
            
            logger.info(f"Добавлен пользователь с ID: {user_id}")
            return user_id
            
        except Error as e:
            logger.error(f"Ошибка при добавлении пользователя: {e}")
            return None
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


database = Database() 