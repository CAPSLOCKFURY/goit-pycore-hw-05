import functools
import sys
from collections.abc import Callable

import phone_registry

default_unexpected_exception_handler: Callable[[Exception], str] = lambda e: "Unexpected exception occurred:" + str(e)


def command_handler(invalid_input_error_message: str,
                    unexpected_exception_message_handler: Callable[[Exception], str] = default_unexpected_exception_handler):
    def decorator(func: Callable[..., str]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TypeError:
                return invalid_input_error_message
            except Exception as e:
                return unexpected_exception_message_handler(e)

        return wrapper

    return decorator


@command_handler(invalid_input_error_message="Invalid command usage, hello command doesn't take any arguments")
def hello_command_handler() -> str:
    return "How can I help you?"


@command_handler(invalid_input_error_message="Invalid command usage, correct usage: add [name] [number]")
def add_command_handler(name: str, number: str) -> str:
    phone_registry.save_phone(name, number)
    return "Successfully saved phone number"


@command_handler(invalid_input_error_message="Invalid command usage, correct usage: change [name] [number]")
def change_command_handler(name: str, number: str) -> str:
    if not phone_registry.find_phone(name):
        return f"Phone number for name {name}, doesn't exist"
    else:
        phone_registry.save_phone(name, number)
        return "Successfully changed phone number"


@command_handler(invalid_input_error_message="Invalid command usage, correct usage: phone [name]")
def phone_command_handler(name: str) -> str:
    phone_number = phone_registry.find_phone(name)
    if not phone_number:
        return f"Phone number for name {name}, doesn't exist"
    else:
        return f"Phone number for name {name} is '{phone_number}'"


@command_handler(invalid_input_error_message="Invalid command usage, all command doesn't take any arguments")
def all_command_handler() -> str:
    phone_numbers = phone_registry.get_all_saved_phones()
    if len(phone_numbers) == 0:
        return "No saved phone numbers"
    else:
        return "All saved phone numbers: \n" + "\n".join(f"{name}: {phone}" for name, phone in phone_numbers)


@command_handler(invalid_input_error_message="Invalid command usage, exit or close command doesn't take any arguments")
def exit_command_handler() -> str:
    sys.exit(0)
