def print_colored(message, color="white"):
    """
    Print colored log messages to the console.

    Args:
    - message (str): The message to be printed.
    - color (str): The color of the message. Defaults to 'white'.
                   Available colors: 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'.
    """
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
    }

    end_color = "\033[0m"

    if color not in colors:
        print("Invalid color. Using default color 'white'.")
        color = "white"

    colored_message = f"{colors[color]}{message}{end_color}"
    print(colored_message)
