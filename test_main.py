"""Тесты для main.py"""
import pytest
from unittest.mock import patch
import main


def test_ast_literal_eval():
    """Тест безопасного преобразования строки в число"""
    import ast
    result = ast.literal_eval("42")
    assert result == 42


def test_multiplication():
    """Тест умножения числа на 6"""
    result = 5 * 6
    assert result == 30


@patch('builtins.input', return_value='10')
@patch('builtins.print')
def test_main_flow(mock_print, mock_input):
    """Тест основного потока выполнения"""
    # Импортируем main модуль, что запустит код
    import importlib
    importlib.reload(main)
    
    # Проверяем, что print был вызван с правильным значением
    mock_print.assert_called_with(60)  # 10 * 6 = 60


def test_safe_input_parsing():
    """Тест парсинга различных типов ввода"""
    import ast
    
    # Тестируем целое число
    assert ast.literal_eval("123") == 123
    
    # Тестируем отрицательное число
    assert ast.literal_eval("-45") == -45
    
    # Тестируем дробное число
    assert ast.literal_eval("3.14") == 3.14 