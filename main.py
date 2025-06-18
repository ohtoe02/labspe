"""Модуль main.py: пример использования Pylint."""

import ast

user_input = input("Введите число: ")
number = ast.literal_eval(user_input)  # Безопасное преобразование
print(number * 6)
