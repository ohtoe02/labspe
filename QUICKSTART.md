# 🚀 БЫСТРЫЙ СТАРТ - Security Demo

## Минимальный запуск (5 минут)

### 1. Установка зависимостей
```bash
cd web
pip install -r requirements.txt
```

### 2. Запуск приложения
```bash
python app.py
```

### 3. Доступ к приложению
- **Веб-интерфейс:** http://localhost:5000
- **Метрики:** http://localhost:8000/metrics
- **Логин:** admin / admin123

## Проверка безопасности (2 минуты)

```bash
# Статический анализ
bandit -r . -f txt

# Проверка зависимостей
safety check

# Комплексная проверка
python security_check.py
```

## Docker запуск (3 минуты)

```bash
# Сборка и запуск
docker-compose up -d

# Сканирование безопасности
docker-compose --profile security-scan up zap
```

## Доступы после Docker запуска

- **Приложение:** http://localhost:5000
- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3000 (admin/admin)

## Основные уязвимости для тестирования

### SQL Injection
```
Логин: admin' OR '1'='1' --
Пароль: любой
```

### Command Injection
```
Admin Panel → Command: whoami && dir
```

### File Upload
```
Загрузить файл с расширением .php или .exe
```

## Созданные отчеты

- `bandit-report.json` - Отчет статического анализа
- `safety-report.json` - Отчет уязвимостей зависимостей
- `Report.png` - Визуальный отчет

## Структура проекта

```
ВяткинСЮ/
├── web/                    # Flask приложение
├── .github/workflows/      # CI/CD pipeline
├── Readme.md              # Полный отчет
├── Report.png             # Визуальный отчет
└── QUICKSTART.md          # Эта инструкция
```

---
**⚠️ ВНИМАНИЕ:** Только для обучения! Содержит намеренные уязвимости. 