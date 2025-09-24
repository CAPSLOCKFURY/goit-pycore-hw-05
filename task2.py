from typing import Callable, Generator

def generator_numbers(text: str) -> Generator[float, None, None]:
    """Returns all numbers from text as float values"""
    for token in text.split():
        if token.replace('.', '', 1).isdigit():  # перевірка, що це число (ціле або з крапкою)
            yield float(token)

def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]):
    """sum all float values from text"""
    return sum(func(text))


text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")
