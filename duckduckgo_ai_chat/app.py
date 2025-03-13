# /// script
# dependencies = [
#   "requests",
#   "colorama",
# ]
# ///

import requests
import json
import sys
from threading import Thread
from queue import Queue
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

MODELS = {
    "1": "gpt-4o-mini",
    "2": "claude-3-haiku-20240307",
    "3": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    "4": "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "5": "o3-mini",
}


def print_banner():
    """Print a colorful welcome banner"""
    print(
        Fore.CYAN
        + r"""
888~-_   888   |  e88~-_  888  /   888~-_   888   |  e88~-_  888  /    e88~~\    ,88~-_   
888   \  888   | d888   \ 888 /    888   \  888   | d888   \ 888 /    d888      d888   \  
888    | 888   | 8888     888/\    888    | 888   | 8888     888/\    8888 __  88888    | 
888    | 888   | 8888     888  \   888    | 888   | 8888     888  \   8888   | 88888    | 
888   /  Y88   | Y888   / 888   \  888   /  Y88   | Y888   / 888   \  Y888   |  Y888   /  
888_-~    "8__/   "88_-~  888    \ 888_-~    "8__/   "88_-~  888    \  "88__/    `88_-~   
                                                                        AI CHAT CLI
"""
        + Style.RESET_ALL
    )


def accept_terms_of_service():
    print(
        Fore.YELLOW
        + "Before using this application, you must accept the terms of service."
    )
    print(
        Fore.YELLOW
        + "Please read the terms of service at: https://duckduckgo.com/aichat/privacy-terms"
    )
    while True:
        response = (
            input(
                Fore.GREEN
                + "Do you accept the terms of service? (yes/no): "
                + Style.RESET_ALL
            )
            .strip()
            .lower()
        )
        if response in ["yes", "y"]:
            return True
        elif response in ["no", "n"]:
            print(
                Fore.RED
                + "You must accept the terms of service to use this application. Exiting."
                + Style.RESET_ALL
            )
            return False
        else:
            print(
                Fore.MAGENTA
                + "Invalid input. Please enter 'yes' or 'no'."
                + Style.RESET_ALL
            )


def choose_model():
    print(Fore.CYAN + "\nPlease choose an AI model:" + Style.RESET_ALL)
    print(Fore.GREEN)
    for key, value in MODELS.items():
        print(f"{key}. {value}")
    print(Style.RESET_ALL)
    print()

    while True:
        choice = input(
            Fore.YELLOW + "Enter your choice (1-5): " + Style.RESET_ALL
        ).strip()
        if choice in MODELS:
            return MODELS[choice]
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)


def fetch_vqd():
    print(Fore.MAGENTA + "Initializing chat connection..." + Style.RESET_ALL)
    url = "https://duckduckgo.com/duckchat/v1/status"
    headers = {"x-vqd-accept": "1"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.headers.get("x-vqd-4")
    else:
        raise Exception(
            f"Failed to initialize chat: {response.status_code} {response.text}"
        )


def fetch_response(chat_url, vqd, model, messages):
    payload = {"model": model, "messages": messages}
    headers = {
        "x-vqd-4": vqd,
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }
    response = requests.post(chat_url, headers=headers, json=payload, stream=True)
    if response.status_code != 200:
        raise Exception(
            f"Failed to send message: {response.status_code} {response.text}"
        )
    return response


def process_stream(response, output_queue):
    for line in response.iter_lines():
        if line:
            line = line.decode("utf-8")
            if line == "data: [DONE]":
                break
            if line.startswith("data: "):
                try:
                    data = json.loads(line[6:])
                    message = data.get("message", "")
                    if message:
                        output_queue.put(message)
                except json.JSONDecodeError:
                    continue


def mainrun(args):
    """Inspired by duckduckGO-chat-cli"""
    # Clear screen (works on most terminals)
    print("\033[H\033[J", end="")

    print_banner()
    if not args.yes:
        if not accept_terms_of_service():
            sys.exit(0)

    if args.model is None:
        model = choose_model()
    else:
        model = MODELS[args.model]

    try:
        vqd = fetch_vqd()
    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
        sys.exit(1)

    print(
        Fore.GREEN
        + f"\nChat initialized successfully. You can start chatting with `{model}`"
        + Style.RESET_ALL
    )
    print(Fore.YELLOW + "Type 'exit' to end the conversation." + Style.RESET_ALL)
    print()

    chat_url = "https://duckduckgo.com/duckchat/v1/chat"
    messages = []

    while True:
        print()
        user_input = input(Fore.BLUE + "You: " + Style.RESET_ALL).strip()
        if user_input.lower() == "exit":
            print(Fore.MAGENTA + "Exiting chat. Goodbye!" + Style.RESET_ALL)
            break

        messages.append({"content": user_input, "role": "user"})

        try:
            response = fetch_response(chat_url, vqd, model, messages)
        except Exception as e:
            print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
            continue

        output_queue = Queue()
        thread = Thread(target=process_stream, args=(response, output_queue))
        thread.start()

        print()
        print(Fore.GREEN + "AI: " + Style.RESET_ALL, end=" ")
        while thread.is_alive() or not output_queue.empty():
            while not output_queue.empty():
                print(
                    Fore.CYAN + output_queue.get() + Style.RESET_ALL, end="", flush=True
                )

        print()
        thread.join()


if __name__ == "__main__":
    mainrun()
