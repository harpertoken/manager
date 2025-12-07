# SPDX-License-Identifier: MIT

import pytest
from manager import Manager
import subprocess
import sys


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
        m.render_chat_with_tools("model", "not a list", [])
    with pytest.raises(ValueError, match="Each message must be a dict"):
        m.render_chat_with_tools("model", ["not a dict"], [])
    with pytest.raises(ValueError, match="Each message must have 'role' and 'content'"):
        m.render_chat_with_tools("model", [{"role": "user"}], [])
    with pytest.raises(ValueError, match="'role' and 'content' must be strings"):
        m.render_chat_with_tools("model", [{"role": 123, "content": "test"}], [])


def test_validate_tools_invalid():
    m = Manager()
    with pytest.raises(ValueError, match="Tools must be a list"):
        m.render_chat_with_tools(
            "model", [{"role": "user", "content": "test"}], "not a list"
        )
    with pytest.raises(ValueError, match="Each tool must be a dict"):
        m.render_chat_with_tools(
            "model", [{"role": "user", "content": "test"}], ["not a dict"]
        )
    with pytest.raises(ValueError, match="Each tool must have 'type' and 'name'"):
        m.render_chat_with_tools(
            "model", [{"role": "user", "content": "test"}], [{"type": "test"}]
        )
    with pytest.raises(ValueError, match="'type' and 'name' must be strings"):
        m.render_chat_with_tools(
            "model",
            [{"role": "user", "content": "test"}],
            [{"type": 123, "name": "test"}],
        )


def test_validate_model_invalid():
    m = Manager()
    with pytest.raises(ValueError, match="Model must be a string"):
        m.render_chat_with_tools(
            123,
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
