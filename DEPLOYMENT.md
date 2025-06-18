# Инструкция по развертыванию CI/CD

## Подготовка репозитория

1. **Создайте публичный GitHub репозиторий**
2. **Загрузите код проекта в репозиторий**
3. **Настройте ветку `main` как основную**

## Настройка SonarCloud

1. **Регистрация**:
   - Перейдите на https://sonarcloud.io/
   - Войдите через GitHub аккаунт
   - Создайте организацию (может совпадать с именем пользователя)

2. **Настройка проекта**:
   - Нажмите "Analyze new project"
   - Выберите ваш репозиторий
   - Скопируйте Project Key и Organization

3. **Обновите sonar-project.properties**:
   ```properties
   sonar.projectKey=ваш-project-key
   sonar.organization=ваша-организация
   ```

4. **Создайте токен**:
   - Account → Security → Generate Token
   - Скопируйте токен

## Настройка GitHub Secrets

В настройках репозитория → Settings → Secrets and variables → Actions:

1. **SONAR_TOKEN**: Токен из SonarCloud
2. **GITHUB_TOKEN**: Создается автоматически

## Активация пайплайна

1. **Сделайте commit в ветку `main`**
2. **Проверьте во вкладке Actions выполнение пайплайна**
3. **Исправьте возможные ошибки в настройках**

## Локальное тестирование

```bash
# Запуск тестов backend
cd backend
pip install -r requirements.txt
pip install pytest pytest-asyncio httpx pytest-cov
python -m pytest tests/ -v

# Запуск тестов frontend  
cd ../frontend
npm install
npm test

# Проверка безопасности (опционально)
pip install safety bandit
safety check -r requirements.txt
bandit -r . -f json
```

## Мониторинг и метрики

- **GitHub Actions**: Время выполнения пайплайна
- **SonarCloud**: Качество кода и покрытие тестами
- **GitHub Security**: Обнаруженные уязвимости

## Troubleshooting

**Проблема**: SonarCloud недоступен
- **Решение**: Пайплайн продолжит работу (continue-on-error: true)

**Проблема**: Тесты падают
- **Решение**: Проверьте логи в Actions, исправьте код

**Проблема**: Docker образы не собираются
- **Решение**: Убедитесь в корректности Dockerfile'ов 