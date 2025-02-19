from duckduckgo_ai_chat import cli


def test_create_parser():
    parser = cli.create_parser()
    assert parser is not None
