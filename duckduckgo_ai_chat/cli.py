import argparse
from duckduckgo_ai_chat.app import mainrun
def create_parser():
    parser = argparse.ArgumentParser(description="CLI to use DuckDuckGo AI Chat service from terminal")
    return parser


def cli():
    "CLI to use DuckDuckGo AI Chat service from terminal"
    parser = create_parser()
    args = parser.parse_args()
    mycommand(args)


def mycommand(args):
    _ = mainrun()