import argparse
from duckduckgo_ai_chat.app import mainrun, MODELS


def create_parser():
    parser = argparse.ArgumentParser(
        description="CLI to use DuckDuckGo AI Chat service from terminal",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-m",
        "--model",
        choices=MODELS.keys(),
        help="Select a model by key:\n "
        + "\n ".join(f"{k}: {v}" for k, v in MODELS.items()),
        default=None,
    )

    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="If provided, means user accept terms of service.",
    )

    return parser


def cli():
    "CLI to use DuckDuckGo AI Chat service from terminal"
    parser = create_parser()
    args = parser.parse_args()
    mycommand(args)


def mycommand(args):
    _ = mainrun(args)
