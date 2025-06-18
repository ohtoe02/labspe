#!/usr/bin/env python3
"""
Script to create a visual security report image
"""

from PIL import Image, ImageDraw, ImageFont
import json
import os

def create_security_report_image():
    """Create a visual security report image"""
    
    # Image dimensions
    width = 1200
    height = 1600
    background_color = (255, 255, 255)
    
    # Create image
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a better font, fallback to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 32)
        header_font = ImageFont.truetype("arial.ttf", 24)
        text_font = ImageFont.truetype("arial.ttf", 16)
        small_font = ImageFont.truetype("arial.ttf", 12)
    except:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Colors
    title_color = (0, 51, 102)  # Dark blue
    header_color = (51, 102, 153)  # Blue
    text_color = (0, 0, 0)  # Black
    critical_color = (220, 20, 60)  # Crimson
    warning_color = (255, 140, 0)  # Orange
    success_color = (34, 139, 34)  # Forest green
    
    y_offset = 50
    
    # Title
    title = "ПРАКТИКА 207: ОТЧЕТ ПО БЕЗОПАСНОСТИ"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, y_offset), title, fill=title_color, font=title_font)
    y_offset += 80
    
    # Student info
    student_info = "Выполнил: Вяткин Сергей Юрьевич | Дата: 18.06.2025"
    info_bbox = draw.textbbox((0, 0), student_info, font=text_font)
    info_width = info_bbox[2] - info_bbox[0]
    draw.text(((width - info_width) // 2, y_offset), student_info, fill=text_color, font=text_font)
    y_offset += 60
    
    # Project description
    draw.text((50, y_offset), "ОПИСАНИЕ ПРОЕКТА:", fill=header_color, font=header_font)
    y_offset += 35
    
    description_lines = [
        "• Flask веб-приложение с намеренными уязвимостями",
        "• Система авторизации, загрузки файлов, админ-панель",
        "• Интеграция инструментов безопасности в CI/CD",
        "• Мониторинг с Prometheus и Grafana"
    ]
    
    for line in description_lines:
        draw.text((70, y_offset), line, fill=text_color, font=text_font)
        y_offset += 25
    
    y_offset += 30
    
    # Security tools section
    draw.text((50, y_offset), "ИНСТРУМЕНТЫ БЕЗОПАСНОСТИ:", fill=header_color, font=header_font)
    y_offset += 35
    
    # Bandit results
    draw.text((70, y_offset), "1. BANDIT - Статический анализ Python кода", fill=text_color, font=text_font)
    y_offset += 25
    draw.text((90, y_offset), "✓ Обнаружено 12 уязвимостей", fill=critical_color, font=text_font)
    y_offset += 20
    draw.text((90, y_offset), "• Высокий риск: 6 (Command Injection, MD5, Debug Mode)", fill=critical_color, font=small_font)
    y_offset += 18
    draw.text((90, y_offset), "• Средний риск: 2 (SQL Injection, Network Binding)", fill=warning_color, font=small_font)
    y_offset += 18
    draw.text((90, y_offset), "• Низкий риск: 4 (Subprocess, Hardcoded secrets)", fill=text_color, font=small_font)
    y_offset += 35
    
    # Safety results
    draw.text((70, y_offset), "2. SAFETY - Анализ уязвимостей в зависимостях", fill=text_color, font=text_font)
    y_offset += 25
    draw.text((90, y_offset), "✓ Обнаружено 6 уязвимостей в зависимостях", fill=critical_color, font=text_font)
    y_offset += 20
    draw.text((90, y_offset), "• Werkzeug < 3.0.6: DoS, Path Traversal, Code Execution", fill=critical_color, font=small_font)
    y_offset += 18
    draw.text((90, y_offset), "• Bandit < 1.7.7: SQL Injection detection issues", fill=warning_color, font=small_font)
    y_offset += 35
    
    # CI/CD Pipeline
    draw.text((70, y_offset), "3. CI/CD PIPELINE - GitHub Actions", fill=text_color, font=text_font)
    y_offset += 25
    draw.text((90, y_offset), "✓ Автоматические проверки безопасности", fill=success_color, font=text_font)
    y_offset += 20
    draw.text((90, y_offset), "• Security Analysis (Bandit, Safety, pip-audit)", fill=text_color, font=small_font)
    y_offset += 18
    draw.text((90, y_offset), "• Docker Security (Trivy scanner)", fill=text_color, font=small_font)
    y_offset += 18
    draw.text((90, y_offset), "• Secrets Detection (GitLeaks)", fill=text_color, font=small_font)
    y_offset += 18
    draw.text((90, y_offset), "• OWASP Dependency Check", fill=text_color, font=small_font)
    y_offset += 35
    
    # Key vulnerabilities
    draw.text((50, y_offset), "КЛЮЧЕВЫЕ УЯЗВИМОСТИ:", fill=header_color, font=header_font)
    y_offset += 35
    
    vulnerabilities = [
        ("🔴 КРИТИЧЕСКИЕ:", critical_color, [
            "SQL Injection в форме авторизации (CWE-89)",
            "Command Injection в админ-панели (CWE-78)",
            "MD5 хеширование паролей (CWE-327)",
            "Debug режим в продакшене (CWE-94)"
        ]),
        ("🟡 ВАЖНЫЕ:", warning_color, [
            "Небезопасная загрузка файлов (CWE-434)",
            "Отсутствие контроля доступа (CWE-732)",
            "Хардкод секретных ключей (CWE-259)"
        ]),
        ("🟢 ИСПРАВЛЕНО:", success_color, [
            "Настроена автоматизация проверок",
            "Создан comprehensive security pipeline",
            "Добавлен мониторинг безопасности"
        ])
    ]
    
    for category, color, items in vulnerabilities:
        draw.text((70, y_offset), category, fill=color, font=text_font)
        y_offset += 25
        for item in items:
            draw.text((90, y_offset), f"• {item}", fill=text_color, font=small_font)
            y_offset += 18
        y_offset += 15
    
    # Results summary
    draw.text((50, y_offset), "ИТОГИ:", fill=header_color, font=header_font)
    y_offset += 35
    
    summary_items = [
        "✅ Успешно интегрированы 5 инструментов безопасности",
        "✅ Создан CI/CD pipeline с автоматическими проверками",
        "✅ Обнаружено 18 уязвимостей различного уровня",
        "✅ Настроен мониторинг и логирование событий",
        "✅ Проект готов для educational purposes"
    ]
    
    for item in summary_items:
        draw.text((70, y_offset), item, fill=success_color, font=text_font)
        y_offset += 25
    
    y_offset += 30
    
    # Footer
    footer_text = "⚠️ ВНИМАНИЕ: Приложение содержит намеренные уязвимости для обучения"
    footer_bbox = draw.textbbox((0, 0), footer_text, font=text_font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    draw.text(((width - footer_width) // 2, y_offset), footer_text, fill=critical_color, font=text_font)
    
    # Save image
    img.save('Report.png', 'PNG', quality=95)
    print("✅ Security report image created: Report.png")

if __name__ == "__main__":
    create_security_report_image() 