# Базовый образ Python
FROM python:3.12-slim

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Копирование файла зависимостей в контейнер
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование остальных файлов приложения
COPY . .

# Открытие порта, на котором работает Flask
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "app.py"]