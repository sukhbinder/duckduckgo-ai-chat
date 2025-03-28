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
import random
from datetime import datetime
import os
import time

# Initialize colorama
init(autoreset=True)

DEBUG = True

MODELS = {
    "1": "gpt-4o-mini",
    "2": "claude-3-haiku-20240307",
    "3": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    "4": "mistralai/Mistral-Small-24B-Instruct-2501",
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
    headers = {
        "accept": "text/event-stream",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "origin": "https://duckduckgo.com",
        "referer": "https://duckduckgo.com/",
        "x-vqd-accept": "1",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        vqd_hash_1 = response.headers.get("x-vqd-hash-1", "")
        vqd = response.headers.get("x-vqd-4")
        if vqd:
            return vqd, vqd_hash_1
    else:
        raise Exception(
            f"Failed to initialize chat: {response.status_code} {response.text}"
        )


def fetch_response(chat_url, vqd, vqd_hash_1, model, messages):
    payload = {"model": model, "messages": messages}
    headers = {
        "accept": "text/event-stream",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "origin": "https://duckduckgo.com",
        "referer": "https://duckduckgo.com/",
        "x-vqd-4": vqd,
        "x-vqd-hash-1": "",
    }

    response = requests.post(chat_url, headers=headers, json=payload, stream=True)
    
    if DEBUG:
        if response.status_code == 418:
            return response
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


def checkquery(args):
    query = args.query
    stdin_prompt = None
    if not sys.stdin.isatty():
        stdin_prompt = sys.stdin.read()

    if stdin_prompt:
        bits = [stdin_prompt]
        if query:
            bits.append(query)
        query = " ".join(bits)
    return query


def reset_stdin():
    # Reset stdin if EOF was reached (needed for non-interactive input cases)
    if sys.stdin.closed or not sys.stdin.isatty():
        if sys.platform.startswith("win"):
            sys.stdin = open("CON", "r")
        else:
            sys.stdin = open("/dev/tty")


def get_download_folder():
    if os.name == "nt":  # Windows
        home_dir = os.environ["USERPROFILE"]
    elif os.name == "posix":  # Linux/Mac
        home_dir = os.path.expanduser("~")
    else:
        home_dir = os.getcwd()
    return os.path.join(home_dir, "Downloads")


def save_session(responses):
    datetime_str = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filepath = os.path.join(get_download_folder(), f"duckchat_{datetime_str}.txt")
    with open(filepath, "w") as fin:
        fin.writelines(responses)
    print(Fore.GREEN + f"\nChat saved successfully. {filepath}" + Style.RESET_ALL)


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

    query = checkquery(args)

    try:
        vqd, vqd_hash_1 = fetch_vqd()
    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
        sys.exit(1)

    print(
        Fore.GREEN
        + f"\nChat initialized successfully. You can start chatting with `{model}`"
        + Style.RESET_ALL
    )
    print(
        Fore.YELLOW
        + "Type 'exit' or 'quit' to end the conversation.\nType `/save` to save conversation"
        + Style.RESET_ALL
    )
    print()
    chat_url = "https://duckduckgo.com/duckchat/v1/chat"
    messages = []
    responses = [f"Your chat with {model}\n\n"]
    first = True
    while True:
        print()
        if query and first:
            user_input = query
            print(Fore.BLUE + "You: " + user_input + Style.RESET_ALL)
            first = False
        else:
            user_input = input(Fore.BLUE + "You: " + Style.RESET_ALL).strip()
        # Handle exit
        if user_input.lower() in ("exit", "quit"):
            print(Fore.MAGENTA + "Exiting chat. Goodbye!" + Style.RESET_ALL)
            break
        # Handle save
        if user_input.lower() in ("/save", "/export"):
            save_session(responses)
            continue

        messages.append({"content": user_input, "role": "user"})
        responses.append(f"User: {user_input}\n\n")

        try:
            response = fetch_response(chat_url, vqd, vqd_hash_1, model, messages)
        except Exception as e:
            print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
            continue

        vqd_hash_1 = response.headers.get("x-vqd-hash-1", vqd_hash_1)
        output_queue = Queue()
        thread = Thread(target=process_stream, args=(response, output_queue))
        thread.start()

        print()
        response_text = ""
        print(Fore.GREEN + "AI: " + Style.RESET_ALL, end=" ")
        while thread.is_alive() or not output_queue.empty():
            while not output_queue.empty():
                rsp_text = output_queue.get()
                print(Fore.CYAN + rsp_text + Style.RESET_ALL, end="", flush=True)
                response_text += rsp_text
        print()
        thread.join()
        reset_stdin()
        responses.append(f"AI: {response_text}\n\n\n")


if __name__ == "__main__":
    mainrun()
