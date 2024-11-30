import argparse

def create_parser():
    parser = argparse.ArgumentParser(description="CLI to use DuckDuckGo AI Chat service from terminal")
    parser.add_argument("name", type=str, help="Dummy argument")
    return parser


def cli():
    "CLI to use DuckDuckGo AI Chat service from terminal"
    parser = create_parser()
    args = parser.parse_args()
    mycommand(args)


def mycommand(args):
    print(args)