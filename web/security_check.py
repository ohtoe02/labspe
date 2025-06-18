#!/usr/bin/env python3
"""
Security Check Script
Скрипт для выполнения локальных проверок безопасности
"""

import subprocess
import sys
import json
import os
from datetime import datetime


def run_command(command, description):
    """Выполняет команду и возвращает результат"""
    print(f"\n{'='*50}")
    print(f"🔍 {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"⚠️ Stderr: {result.stderr}")
            
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"❌ Ошибка выполнения: {str(e)}")
        return False, "", str(e)


def main():
    """Основная функция для запуска всех проверок безопасности"""
    print("🛡️  SECURITY CHECK SUITE")
    print("=" * 60)
    print(f"Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # 1. Bandit Security Check
    print("\n1️⃣ Запуск Bandit Security Scan...")
    success, stdout, stderr = run_command(
        "bandit -r . -f json -o bandit-report.json",
        "Bandit - статический анализ безопасности Python кода"
    )
    results['bandit'] = {'success': success, 'stdout': stdout, 'stderr': stderr}
    
    # Показываем результаты Bandit в читаемом виде
    run_command("bandit -r . -f txt", "Bandit - детализированный отчет")
    
    # 2. Safety Check
    print("\n2️⃣ Запуск Safety Check...")
    success, stdout, stderr = run_command(
        "safety check --json --output safety-report.json",
        "Safety - проверка известных уязвимостей в зависимостях"
    )
    results['safety'] = {'success': success, 'stdout': stdout, 'stderr': stderr}
    
    # Показываем результаты Safety в читаемом виде
    run_command("safety check", "Safety - детализированный отчет")
    
    # 3. Flake8 Linting
    print("\n3️⃣ Запуск Flake8...")
    success, stdout, stderr = run_command(
        "flake8 . --count --statistics --max-line-length=127",
        "Flake8 - проверка качества кода"
    )
    results['flake8'] = {'success': success, 'stdout': stdout, 'stderr': stderr}
    
    # 4. Создание сводного отчета
    print("\n4️⃣ Создание сводного отчета...")
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'bandit': 'PASS' if results['bandit']['success'] else 'FAIL',
            'safety': 'PASS' if results['safety']['success'] else 'FAIL',
            'flake8': 'PASS' if results['flake8']['success'] else 'FAIL'
        },
        'details': results
    }
    
    # Сохраняем сводный отчет
    with open('security-summary.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # 5. Итоговая статистика
    print("\n" + "="*60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("="*60)
    
    total_checks = len(results)
    passed_checks = sum(1 for r in results.values() if r['success'])
    
    print(f"✅ Успешных проверок: {passed_checks}/{total_checks}")
    print(f"❌ Неудачных проверок: {total_checks - passed_checks}/{total_checks}")
    
    for check_name, result in results.items():
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"   {check_name.upper()}: {status}")
    
    # 6. Рекомендации по устранению
    print("\n" + "="*60)
    print("💡 РЕКОМЕНДАЦИИ ПО БЕЗОПАСНОСТИ")
    print("="*60)
    
    recommendations = [
        "1. Исправьте SQL инъекции - используйте параметризованные запросы",
        "2. Замените MD5 на bcrypt или Argon2 для хеширования паролей",
        "3. Добавьте валидацию загружаемых файлов",
        "4. Реализуйте проверку прав доступа для админ-панели",
        "5. Удалите debug=True из продакшн конфигурации",
        "6. Используйте криптографически стойкий секретный ключ",
        "7. Добавьте rate limiting для защиты от брутфорса",
        "8. Реализуйте логирование безопасности"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")
    
    print("\n" + "="*60)
    print("📁 Созданные отчеты:")
    print("   - bandit-report.json")
    print("   - safety-report.json") 
    print("   - security-summary.json")
    print("="*60)
    
    # Возвращаем код выхода
    if passed_checks == total_checks:
        print("🎉 Все проверки пройдены успешно!")
        return 0
    else:
        print("⚠️  Обнаружены проблемы безопасности!")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 