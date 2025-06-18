# Практика 207: Безопасность веб-приложений

**Выполнил:** Вяткин Сергей Юрьевич  
**Дата:** 18.06.2025  
**Тема:** Использование инструментов безопасности в веб-приложении

## Описание проекта

Создано демонстрационное Flask веб-приложение с намеренными уязвимостями безопасности для обучения и тестирования инструментов анализа безопасности. Проект включает в себя:

- Веб-приложение на Flask с функциями авторизации, загрузки файлов и административной панели
- Систему мониторинга на основе Prometheus и Grafana
- CI/CD pipeline с автоматическими проверками безопасности
- Comprehensive security testing with multiple tools

## Архитектура приложения

```
ВяткинСЮ/
├── web/                          # Основное приложение
│   ├── app.py                   # Flask приложение
│   ├── templates/               # HTML шаблоны
│   ├── static/css/             # CSS стили
│   ├── requirements.txt        # Python зависимости
│   ├── Dockerfile             # Docker конфигурация
│   ├── docker-compose.yml     # Многоконтейнерное развертывание
│   ├── security_check.py      # Скрипт проверки безопасности
│   └── monitoring/            # Конфигурации мониторинга
└── .github/workflows/          # CI/CD pipeline
    └── security.yml           # GitHub Actions workflow
```

## Функционал приложения

### Основные функции:
- **Авторизация и регистрация** - система пользователей с сессиями
- **Dashboard** - персональная панель пользователя
- **Загрузка файлов** - функция upload с проверкой безопасности
- **Административная панель** - выполнение системных команд
- **Мониторинг** - Prometheus метрики и health checks

### Намеренные уязвимости (для обучения):
1. **SQL Injection** - в форме авторизации
2. **Command Injection** - в административной панели
3. **Insecure File Upload** - отсутствие проверки типов файлов
4. **Weak Password Hashing** - использование MD5
5. **Debug Mode** - включен в продакшн окружении
6. **Hardcoded Secrets** - слабый секретный ключ
7. **Missing Access Control** - отсутствие проверки прав доступа

## Инструменты безопасности

### 1. Bandit - Анализ безопасности Python кода

**Установка:**
```bash
pip install bandit==1.7.5
```

**Использование:**
```bash
bandit -r . -f txt              # Текстовый вывод
bandit -r . -f json -o report.json  # JSON отчет
```

**Результаты:**
- Обнаружено **12 уязвимостей**
- Высокий уровень: **6** (MD5 хеширование, Command Injection, Debug Mode)
- Средний уровень: **2** (SQL Injection, Binding to all interfaces)
- Низкий уровень: **4** (Subprocess usage, Hardcoded passwords)

### 2. Safety - Проверка уязвимостей в зависимостях

**Установка:**
```bash
pip install safety==2.3.4
```

**Использование:**
```bash
safety check                    # Проверка зависимостей
safety check --json            # JSON формат
```

**Результаты:**
- Обнаружено **6 уязвимостей** в зависимостях
- Уязвимости в Werkzeug: DoS, Path Traversal, Code Execution
- Уязвимости в Bandit: SQL Injection detection issues

### 3. GitHub Actions CI/CD Pipeline

**Конфигурация:** `.github/workflows/security.yml`

**Этапы проверки:**
1. **Security Analysis** - Bandit, Safety, pip-audit
2. **Docker Security** - Trivy vulnerability scanner
3. **Secrets Detection** - GitLeaks
4. **Dependency Check** - OWASP Dependency Check
5. **Code Quality** - Flake8, Pylint

**Триггеры:**
- Push в main/develop ветки
- Pull requests
- Ежедневно в 02:00 UTC

### 4. Docker Security

**Dockerfile** - мультистейдж сборка с минимальным базовым образом
**Docker Compose** - включает Prometheus, Grafana, OWASP ZAP

**Проверка безопасности:**
```bash
docker build -t security-demo .
docker run --rm -v $(pwd):/app aquasec/trivy image security-demo
```

## Результаты анализа безопасности

### Bandit Report Summary:
- **Total lines of code:** 242
- **Issues by severity:**
  - High: 6 (Critical security issues)
  - Medium: 2 (Important security issues)  
  - Low: 4 (Minor security issues)

### Safety Report Summary:
- **Packages scanned:** 73
- **Vulnerabilities found:** 6
- **Affected packages:** werkzeug, bandit
- **Severity:** High (Code Execution, DoS, Path Traversal)

### Key Findings:

1. **Critical Issues (High Severity):**
   - MD5 password hashing (CWE-327)
   - Command injection in admin panel (CWE-78)
   - Flask debug mode enabled (CWE-94)

2. **Important Issues (Medium Severity):**
   - SQL injection vulnerability (CWE-89)
   - Binding to all interfaces (CWE-605)

3. **Dependency Vulnerabilities:**
   - Werkzeug versions < 3.0.6 (multiple CVEs)
   - Bandit version < 1.7.7 (SQL injection detection)

## Рекомендации по устранению

### Немедленные действия:
1. **Обновить зависимости:**
   ```bash
   pip install werkzeug>=3.0.6
   pip install bandit>=1.7.7
   ```

2. **Исправить критические уязвимости:**
   - Заменить MD5 на bcrypt/Argon2
   - Добавить параметризованные SQL запросы
   - Отключить debug режим в продакшене
   - Реализовать проверку прав доступа

3. **Усилить защиту загрузки файлов:**
   - Валидация типов файлов
   - Сканирование на вирусы
   - Ограничение размера файлов

### Долгосрочные улучшения:
1. **Мониторинг безопасности:**
   - Централизованное логирование
   - Алерты на подозрительную активность
   - Regular security scans

2. **Защита приложения:**
   - Rate limiting
   - Web Application Firewall (WAF)
   - Security headers (CSP, HSTS, etc.)

3. **Процесс разработки:**
   - Обязательные security checks в CI/CD
   - Регулярные penetration tests
   - Security training для команды

## Команды для запуска

### Локальная разработка:
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск приложения
python app.py

# Проверка безопасности
python security_check.py
```

### Docker развертывание:
```bash
# Сборка и запуск
docker-compose up -d

# Сканирование безопасности
docker-compose --profile security-scan up zap
```

### CI/CD проверки:
```bash
# Локальный запуск аналогично CI
bandit -r . -f txt
safety check
flake8 .
```

## Доступ к приложению

- **Веб-приложение:** http://localhost:5000
- **Prometheus метрики:** http://localhost:8000/metrics
- **Prometheus UI:** http://localhost:9090
- **Grafana:** http://localhost:3000 (admin/admin)

**Тестовые данные:**
- Логин: `admin`
- Пароль: `admin123`

## Заключение

Проект успешно демонстрирует:
- Комплексный подход к безопасности веб-приложений
- Интеграцию инструментов безопасности в CI/CD процесс
- Автоматизацию проверок безопасности
- Мониторинг и логирование security events

Обнаружено **18 уязвимостей** различного уровня критичности, что подтверждает эффективность используемых инструментов безопасности.

## Дополнительные материалы

- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Safety Documentation](https://pyup.io/safety/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Features](https://docs.github.com/en/code-security)

---

**Примечание:** Данное приложение создано исключительно в образовательных целях и содержит намеренные уязвимости. Не используйте его в продакшн окружении без устранения всех выявленных проблем безопасности. 