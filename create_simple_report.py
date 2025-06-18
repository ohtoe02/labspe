#!/usr/bin/env python3
"""
Генератор простого визуального отчета для Flask приложения
"""

from PIL import Image, ImageDraw, ImageFont
import io
import base64

def create_simple_report():
    """Создание простого отчета о безопасности"""
    
    # Размеры изображения
    width, height = 1200, 800
    
    # Создание изображения
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Цвета
    colors = {
        'header': '#1e3d59',
        'success': '#28a745', 
        'warning': '#ffc107',
        'danger': '#dc3545',
        'info': '#17a2b8',
        'light': '#f8f9fa',
        'dark': '#343a40'
    }
    
    # Заголовок
    try:
        title_font = ImageFont.truetype("arial.ttf", 36)
        subtitle_font = ImageFont.truetype("arial.ttf", 24)
        text_font = ImageFont.truetype("arial.ttf", 18)
        small_font = ImageFont.truetype("arial.ttf", 14)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Заголовок отчета
    draw.rectangle([0, 0, width, 80], fill=colors['header'])
    draw.text((width//2, 25), "ПРОСТОЕ FLASK ПРИЛОЖЕНИЕ", font=title_font, 
              fill='white', anchor='mm')
    draw.text((width//2, 55), "Отчет безопасности", font=subtitle_font,
              fill='white', anchor='mm')
    
    # Основная информация
    y = 120
    draw.text((50, y), "📊 СВОДКА ПРИЛОЖЕНИЯ", font=subtitle_font, fill=colors['header'])
    y += 40
    
    info_items = [
        "• Тип: Простое Flask веб-приложение",
        "• Функции: Сообщения, поиск, админ панель",
        "• База данных: SQLite (simple.db)",
        "• Шаблоны: 4 простых HTML страницы",
        "• Зависимости: Flask, Werkzeug + security tools"
    ]
    
    for item in info_items:
        draw.text((70, y), item, font=text_font, fill=colors['dark'])
        y += 25
    
    # Уязвимости
    y += 20
    draw.text((50, y), "🔍 ОБНАРУЖЕННЫЕ УЯЗВИМОСТИ", font=subtitle_font, fill=colors['danger'])
    y += 40
    
    vulnerabilities = [
        ("SQL Injection", "Высокий", colors['danger']),
        ("Command Injection", "Высокий", colors['danger']),
        ("Debug Mode", "Средний", colors['warning']),
        ("Weak Secret Key", "Средний", colors['warning']),
        ("MD5 Hashing", "Низкий", colors['info'])
    ]
    
    for vuln, level, color in vulnerabilities:
        # Квадратик с цветом уровня
        draw.rectangle([70, y+2, 85, y+17], fill=color)
        draw.text((100, y), f"{vuln} - {level}", font=text_font, fill=colors['dark'])
        y += 25
    
    # Инструменты безопасности
    y += 20
    draw.text((50, y), "🛡️ ИСПОЛЬЗОВАННЫЕ ИНСТРУМЕНТЫ", font=subtitle_font, fill=colors['success'])
    y += 40
    
    tools = [
        "✅ Bandit - статический анализ Python кода",
        "✅ Safety - проверка уязвимостей в зависимостях", 
        "✅ Flake8 - качество и стиль кода",
        "✅ GitHub Actions - автоматизированные проверки",
        "✅ Docker - контейнеризация и безопасность"
    ]
    
    for tool in tools:
        draw.text((70, y), tool, font=text_font, fill=colors['dark'])
        y += 25
    
    # Правая колонка - статистика
    right_x = width // 2 + 50
    y = 120
    
    draw.text((right_x, y), "📈 СТАТИСТИКА", font=subtitle_font, fill=colors['info'])
    y += 40
    
    # Блок статистики
    stats_box = [right_x - 10, y - 10, width - 50, y + 180]
    draw.rectangle(stats_box, outline=colors['info'], width=2)
    
    stats = [
        "Строк кода: ~150",
        "Файлов Python: 2",
        "HTML шаблонов: 4", 
        "Уязвимостей: 5",
        "Инструментов: 5"
    ]
    
    for stat in stats:
        draw.text((right_x, y), stat, font=text_font, fill=colors['dark'])
        y += 25
    
    # Рекомендации
    y += 40
    draw.text((right_x, y), "💡 РЕКОМЕНДАЦИИ", font=subtitle_font, fill=colors['warning'])
    y += 40
    
    recommendations = [
        "1. Параметризованные SQL запросы",
        "2. Валидация ввода пользователя",
        "3. Отключить debug в продакшене",
        "4. Криптостойкий секретный ключ",
        "5. Современное хеширование паролей"
    ]
    
    for rec in recommendations:
        draw.text((right_x, y), rec, font=small_font, fill=colors['dark'])
        y += 20
    
    # Подвал
    footer_y = height - 60
    draw.rectangle([0, footer_y, width, height], fill=colors['light'])
    draw.text((width//2, footer_y + 15), "Простое приложение для изучения основ безопасности", 
              font=text_font, fill=colors['dark'], anchor='mm')
    draw.text((width//2, footer_y + 35), "⚠️ Только для образовательных целей", 
              font=small_font, fill=colors['danger'], anchor='mm')
    
    # Сохранение
    img.save('Report.png', 'PNG', quality=95)
    print("✅ Отчет сохранен как Report.png")
    
    return img

if __name__ == "__main__":
    create_simple_report() 