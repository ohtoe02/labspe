import os
import subprocess
import json
from datetime import datetime

def run_command(command, description):
    print(f"\n🔍 {description}...")
    print("=" * 50)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Успешно выполнено")
            if result.stdout:
                print(result.stdout)
        else:
            print("⚠️ Обнаружены проблемы")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print("Ошибки:", result.stderr)
                
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Превышено время ожидания")
        return False
    except Exception as e:
        print(f"❌ Ошибка выполнения: {e}")
        return False

def main():
    print("🛡️ Простая проверка безопасности Flask приложения")
    print(f"📅 Дата проверки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    checks = [
        {
            "command": "bandit -r . -f txt --severity-level medium",
            "description": "Bandit - статический анализ безопасности"
        },
        {
            "command": "bandit -r . -f json -o bandit-report.json",
            "description": "Bandit - создание JSON отчета"
        },
        {
            "command": "safety check",
            "description": "Safety - проверка уязвимостей в зависимостях"
        },
        {
            "command": "safety check --json > safety-report.json",
            "description": "Safety - создание JSON отчета"
        },
        {
            "command": "flake8 app.py --max-line-length=127",
            "description": "Flake8 - проверка качества кода"
        }
    ]
    
    results = []
    for check in checks:
        success = run_command(check["command"], check["description"])
        results.append({
            "check": check["description"],
            "status": "PASS" if success else "FAIL"
        })
    
    print("\n📊 ИТОГИ ПРОВЕРКИ")
    print("=" * 50)
    
    passed = sum(1 for r in results if r["status"] == "PASS")
    total = len(results)
    
    for result in results:
        status_icon = "✅" if result["status"] == "PASS" else "❌"
        print(f"{status_icon} {result['check']}: {result['status']}")
    
    print(f"\n📈 Результат: {passed}/{total} проверок успешно")
    
    if passed == total:
        print("🎉 Все проверки пройдены!")
    else:
        print("⚠️ Обнаружены проблемы безопасности")
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "app": "Simple Flask Security Demo",
        "total_checks": total,
        "passed_checks": passed,
        "results": results
    }
    
    with open("security-summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Сводный отчет сохранен в security-summary.json")

if __name__ == "__main__":
    main() 