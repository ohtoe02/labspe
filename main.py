import ast


def multiply_and_add(number):
    return number * 10 + number


def main():
    user_input = input("Введите число: ")
    number = ast.literal_eval(user_input)  # Безопасное преобразование
    result = multiply_and_add(number)
    print(result)
    return result


if __name__ == "__main__":
    main()
