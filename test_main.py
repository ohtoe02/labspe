"""Тесты для модуля main.py"""

import pytest
from unittest.mock import patch
import main


def test_multiply_and_add_positive():
    """Тест с положительным числом"""
    result = main.multiply_and_add(5)
    assert result == 55


def test_multiply_and_add_negative():
    """Тест с отрицательным числом"""
    result = main.multiply_and_add(-3)
    assert result == -33


def test_multiply_and_add_zero():
    """Тест с нулем"""
    result = main.multiply_and_add(0)
    assert result == 0


def test_multiply_and_add_float():
    """Тест с дробным числом"""
    result = main.multiply_and_add(2.5)
    assert result == 27.5


@patch('builtins.input', return_value='10')
@patch('builtins.print')
def test_main_function(mock_print, mock_input):
    """Тест основной функции main()"""
    result = main.main()
    
    # Проверяем, что input был вызван
    mock_input.assert_called_once_with("Введите число: ")
    
    # Проверяем, что print был вызван с правильным значением
    mock_print.assert_called_once_with(110)  # 10 * 10 + 10 = 110
    
    # Проверяем возвращаемое значение
    assert result == 110


def test_ast_literal_eval_safety():
    """Тест безопасного преобразования ast.literal_eval"""
    import ast
    
    # Тестируем различные типы данных
    assert ast.literal_eval("42") == 42
    assert ast.literal_eval("-15") == -15
    assert ast.literal_eval("3.14") == 3.14
    
    # Проверяем, что небезопасные выражения вызывают ошибку
    with pytest.raises((ValueError, SyntaxError)):
        ast.literal_eval("__import__('os').system('ls')") 