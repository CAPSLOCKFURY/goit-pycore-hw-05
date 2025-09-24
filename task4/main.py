from typing import Callable, Tuple, Dict
import handlers

commands_registry: Dict[str, Callable[..., str]] = {
    "hello": handlers.hello_command_handler,
    "add": handlers.add_command_handler,
    "change": handlers.change_command_handler,
    "phone": handlers.phone_command_handler,
    "all": handlers.all_command_handler,
    "close": handlers.exit_command_handler,
    "exit": handlers.exit_command_handler,
}


def main():
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: \n")
        command, arguments = parse_input(user_input)
        command_result = call_command(command, arguments)
        print(command_result + "\n")


def parse_input(user_input: str) -> Tuple[str, list[str]]:
    command, *arguments = user_input.split(" ")
    return command.lower(), arguments


def call_command(command_name, arguments) -> str:
    if command_name not in commands_registry:
        return "Invalid command."
    command_handler = commands_registry[command_name]
    return command_handler(*arguments)


if __name__ == "__main__":
    main()
