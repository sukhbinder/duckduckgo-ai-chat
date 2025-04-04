import pytest
from unittest.mock import patch, Mock
from queue import Queue
import tempfile
import os
from unittest.mock import patch, mock_open
from datetime import datetime
from duckduckgo_ai_chat.app import (
    accept_terms_of_service,
    choose_model,
    fetch_vqd,
    fetch_response,
    process_stream,
    save_session,
    mainrun,
)

from duckduckgo_ai_chat import cli


def test_create_parser():
    parser = cli.create_parser()
    assert parser is not None

    args = parser.parse_args(["-m", "1", "--yes"])
    assert args.model == "1"
    assert args.yes is True


# Test accept_terms_of_service
@patch("builtins.input", side_effect=["yes"])
def test_accept_terms_of_service_yes(mock_input):
    result = accept_terms_of_service()
    assert result is True


@patch("builtins.input", side_effect=["no"])
def test_accept_terms_of_service_no(mock_input):
    result = accept_terms_of_service()
    assert result is False


@patch("builtins.input", side_effect=["invalid", "yes"])
def test_accept_terms_of_service_invalid_then_yes(mock_input):
    result = accept_terms_of_service()
    assert result is True


# Test choose_model
@patch("builtins.input", side_effect=["1"])
def test_choose_model_valid(mock_input):
    result = choose_model()
    assert result == "gpt-4o-mini"


@patch("builtins.input", side_effect=["invalid", "2"])
def test_choose_model_invalid_then_valid(mock_input):
    result = choose_model()
    assert result == "claude-3-haiku-20240307"


# Test fetch_vqd
@patch("requests.get")
def test_fetch_vqd_success(mock_get):
    mock_get.return_value = Mock(status_code=200, headers={"x-vqd-4": "vqd_value"})
    result, _ = fetch_vqd()
    assert result == "vqd_value"


@patch("requests.get")
def test_fetch_vqd_failure(mock_get):
    mock_get.return_value = Mock(status_code=500, text="Internal Server Error")
    with pytest.raises(
        Exception, match="Failed to initialize chat: 500 Internal Server Error"
    ):
        fetch_vqd()


# Test fetch_response
@patch("requests.post")
def test_fetch_response_success(mock_post):
    mock_response = Mock(
        status_code=200,
        iter_lines=Mock(
            return_value=[b'data: {"message": "Test message"}', b"data: [DONE]"]
        ),
    )
    mock_post.return_value = mock_response

    chat_url = "https://dummy-chat-url.com"
    vqd = "dummy_vqd"
    vqd_hash_1 = "dummy"
    model = "dummy_model"
    messages = [{"content": "Test message", "role": "user"}]
    response = fetch_response(chat_url, vqd, vqd_hash_1, model, messages)

    assert response.status_code == 200


@patch("requests.post")
def test_fetch_response_failure(mock_post):
    mock_post.return_value = Mock(status_code=500, text="Internal Server Error")
    chat_url = "https://dummy-chat-url.com"
    vqd = "dummy_vqd"
    vqd_hash_1 = "dummy"
    model = "dummy_model"
    messages = [{"content": "Test message", "role": "user"}]
    with pytest.raises(
        Exception, match="Failed to send message: 500 Internal Server Error"
    ):
        fetch_response(chat_url, vqd, vqd_hash_1, model, messages)


# Test process_stream
def test_process_stream():
    response = Mock()
    response.iter_lines.return_value = [
        b'data: {"message": "First message"}',
        b'data: {"message": "Second message"}',
        b"data: [DONE]",
    ]
    output_queue = Queue()

    process_stream(response, output_queue)

    # Check if messages are processed correctly
    assert output_queue.get() == "First message"
    assert output_queue.get() == "Second message"
    assert output_queue.empty()


@patch("duckduckgo_ai_chat.app.get_download_folder", return_value=tempfile.gettempdir())
@patch("duckduckgo_ai_chat.app.open", new_callable=mock_open)
@patch("duckduckgo_ai_chat.app.datetime")
def test_save_session(mock_datetime, mock_open_func, mock_get_download_folder):
    mock_now = datetime(2025, 3, 25, 12, 30, 45)
    mock_datetime.now.return_value = mock_now
    mock_datetime.strftime.return_value = "2025_03_25_12_30_45"

    responses = ["User: Hello\n", "AI: Hi there!\n\n"]
    save_session(responses)

    filename = f"duckchat_2025_03_25_12_30_45.txt"
    expected_path = os.path.join(tempfile.gettempdir(), filename)

    mock_open_func.assert_called_once_with(expected_path, "w")
    handle = mock_open_func()
    handle.writelines.assert_called_once_with(responses)


@patch("builtins.input", side_effect=["/save", "exit"])
@patch("duckduckgo_ai_chat.app.save_session")
@patch("duckduckgo_ai_chat.app.fetch_vqd", return_value=("dummy_vqd", "dummy_hash"))
@patch("duckduckgo_ai_chat.app.checkquery", return_value="")
@patch("duckduckgo_ai_chat.app.choose_model", return_value="gpt-4")
@patch("duckduckgo_ai_chat.app.accept_terms_of_service", return_value=True)
@patch("duckduckgo_ai_chat.app.print_banner")
def test_mainrun_save(
    mock_print_banner,
    mock_accept_tos,
    mock_choose_model,
    mock_checkquery,
    mock_fetch_vqd,
    mock_save_session,
    mock_input,
):
    class Args:
        yes = True
        model = None

    mainrun(Args())
    mock_save_session.assert_called_once()
