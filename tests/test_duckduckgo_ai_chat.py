from duckduckgo_ai_chat import cli


def test_create_parser():
    
    parser = cli.create_parser()
    result = parser.parse_args(["hello"])
    assert result.name == "hello"

