# SPDX-License-Identifier: MIT

import pytest
from manager import Manager
import subprocess
import sys
from unittest.mock import patch
from pathlib import Path


def test_render_chat_with_tools():
    m = Manager()
    result = m.render_chat_with_tools(
        "test-model",
        [{"role": "user", "content": "test"}],
        [{"type": "test", "name": "test"}],
    )
    assert '"model": "test-model"' in result
    assert '"content": "test"' in result


def test_validate_messages_invalid():
    m = Manager()
    with pytest.raises(ValueError, match="Messages must be a list"):
        m.render_chat_with_tools("model", "not a list", [])  # type: ignore
    with pytest.raises(ValueError, match="Each message must be a dict"):
        m.render_chat_with_tools("model", ["not a dict"], [])  # type: ignore
    with pytest.raises(ValueError, match="Each message must have 'role' and 'content'"):
        m.render_chat_with_tools("model", [{"role": "user"}], [])
    with pytest.raises(ValueError, match="'role' and 'content' must be strings"):
        m.render_chat_with_tools("model", [{"role": 123, "content": "test"}], [])  # type: ignore


def test_validate_tools_invalid():
    m = Manager()
    with pytest.raises(ValueError, match="Tools must be a list"):
        m.render_chat_with_tools(
            "model",
            [{"role": "user", "content": "test"}],
            "not a list",  # type: ignore
        )
    with pytest.raises(ValueError, match="Each tool must be a dict"):
        m.render_chat_with_tools(
            "model",
            [{"role": "user", "content": "test"}],
            ["not a dict"],  # type: ignore
        )
    with pytest.raises(ValueError, match="Each tool must have 'type' and 'name'"):
        m.render_chat_with_tools(
            "model", [{"role": "user", "content": "test"}], [{"type": "test"}]
        )
    with pytest.raises(ValueError, match="'type' and 'name' must be strings"):
        m.render_chat_with_tools(
            "model",
            [{"role": "user", "content": "test"}],
            [{"type": 123, "name": "test"}],  # type: ignore
        )


def test_validate_model_invalid():
    m = Manager()
    with pytest.raises(ValueError, match="Model must be a string"):
        m.render_chat_with_tools(
            123,  # type: ignore
            [{"role": "user", "content": "test"}],
            [{"type": "test", "name": "test"}],
        )


def test_cli_output():
    # Test CLI with basic args
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from manager.cli import main; import sys; sys.argv = ['cli', '--message', 'Test message', '--tools', 'web_search']; main()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    output = result.stdout.strip()
    assert '"model": "grok-beta"' in output
    assert '"content": "Test message"' in output
    assert '"type": "web_search"' in output


def test_cli_missing_message():
    # Test CLI with missing required message
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from manager.cli import main; import sys; sys.argv = ['cli', '--tools', 'web_search']; main()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0  # Should fail due to missing --message


def test_render_with_custom_template():
    m = Manager()
    result = m.render_chat_with_tools(
        "test-model",
        [{"role": "user", "content": "test"}],
        [{"type": "test", "name": "test"}],
        template_name="advanced.jinja",
        temperature=0.5,
        max_tokens=100,
    )
    assert '"model": "test-model"' in result
    assert '"temperature": 0.5' in result
    assert '"max_tokens": 100' in result


def test_render_multiple_messages():
    m = Manager()
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"},
        {"role": "user", "content": "How are you?"},
    ]
    result = m.render_chat_with_tools(
        "test-model", messages, [{"type": "web_search", "name": "web_search"}]
    )
    assert '"role": "system"' in result
    assert '"content": "Hello"' in result
    assert '"content": "How are you?"' in result


def test_edge_cases():
    m = Manager()
    # Empty tools
    result = m.render_chat_with_tools(
        "model", [{"role": "user", "content": "test"}], []
    )
    assert '"tools": []' in result
    # Large content (simulate)
    long_content = "test " * 1000
    result = m.render_chat_with_tools(
        "model",
        [{"role": "user", "content": long_content}],
        [{"type": "test", "name": "test"}],
    )
    assert len(result) > 1000  # Should handle large payloads


def test_setup_hooks():
    from manager.cli import setup_hooks

    with (
        patch("pathlib.Path.exists") as mock_exists,
        patch("shutil.copy") as mock_copy,
        patch("os.chmod") as mock_chmod,
        patch("builtins.print") as mock_print,
    ):
        # Test when .git/hooks exists and script exists
        mock_exists.return_value = True
        setup_hooks()
        mock_copy.assert_called_once()
        mock_chmod.assert_called_once_with(Path(".git/hooks/commit-msg"), 0o755)
        mock_print.assert_called_with("Commit message hook installed.")

        # Test when .git/hooks does not exist
        mock_exists.return_value = False
        setup_hooks()
        mock_print.assert_called_with(
            "Git repository not found. Please run from the project root."
        )


def test_cli_main_basic():
    # Test basic CLI output via subprocess (already exists, but ensure it works)
    # The existing test_cli_output covers this
    pass


def test_cli_missing_message_error():
    # Test CLI with missing message
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from manager.cli import main; import sys; sys.argv = ['cli', '--tools', 'web_search']; main()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0  # Should fail due to missing --message


def test_cli_with_system_message():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from manager.cli import main; import sys; sys.argv = ['cli', '--system-message', 'You are helpful', '--message', 'Hello']; main()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    output = result.stdout.strip()
    assert '"role": "system"' in output
    assert '"content": "You are helpful"' in output
    assert '"content": "Hello"' in output


def test_render_with_invalid_template():
    m = Manager()
    with pytest.raises(Exception):  # Jinja2.TemplateNotFound or similar
        m.render_chat_with_tools(
            "model",
            [{"role": "user", "content": "test"}],
            [{"type": "test", "name": "test"}],
            template_name="nonexistent.jinja",
        )


def test_render_with_empty_messages():
    m = Manager()
    # Empty messages are allowed
    result = m.render_chat_with_tools("model", [], [])
    assert '"messages": []' in result


def test_render_with_empty_tools():
    m = Manager()
    result = m.render_chat_with_tools(
        "model", [{"role": "user", "content": "test"}], []
    )
    assert '"tools": []' in result


def test_render_with_kwargs():
    m = Manager()
    result = m.render_chat_with_tools(
        "model",
        [{"role": "user", "content": "test"}],
        [{"type": "test", "name": "test"}],
        template_name="advanced.jinja",
        temperature=0.5,
    )
    assert '"temperature": 0.5' in result
