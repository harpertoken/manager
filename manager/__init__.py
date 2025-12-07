# SPDX-License-Identifier: MIT

import os

from ._version import __version__

__all__ = ["Manager", "__version__"]


class Manager:
    """Manager for generating robust JSON payloads for xAI API agentic tool calls.

    Uses Jinja2 templating to ensure well-formed outputs with built-in validation.
    """

    def __init__(self):
        """Initialize the Manager with Jinja2 environment."""
        from jinja2 import Environment, FileSystemLoader

        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def _validate_messages(self, messages):
        if not isinstance(messages, list):
            raise ValueError("Messages must be a list")
        for msg in messages:
            if not isinstance(msg, dict):
                raise ValueError("Each message must be a dict")
            if "role" not in msg or "content" not in msg:
                raise ValueError("Each message must have 'role' and 'content' keys")
            if not isinstance(msg["role"], str) or not isinstance(msg["content"], str):
                raise ValueError("'role' and 'content' must be strings")

    def _validate_tools(self, tools):
        if not isinstance(tools, list):
            raise ValueError("Tools must be a list")
        for tool in tools:
            if not isinstance(tool, dict):
                raise ValueError("Each tool must be a dict")
            if "type" not in tool or "name" not in tool:
                raise ValueError("Each tool must have 'type' and 'name' keys")
            if not isinstance(tool["type"], str) or not isinstance(tool["name"], str):
                raise ValueError("'type' and 'name' must be strings")

    def render_chat_with_tools(
        self, model, messages, tools, template_name="chatwithtools.jinja", **kwargs
    ):
        """Render a JSON payload for xAI API chat completions with tools.

        Args:
            model (str): The model name (e.g., "grok-beta").
            messages (list): List of message dicts with 'role' and 'content'.
            tools (list): List of tool dicts with 'type' and 'name'.
            template_name (str): Name of the Jinja2 template to use.
            **kwargs: Additional parameters to pass to the template (e.g., temperature, max_tokens).

        Returns:
            str: The rendered JSON payload.

        Raises:
            ValueError: If inputs do not meet validation requirements.
        """
        self._validate_messages(messages)
        self._validate_tools(tools)
        if not isinstance(model, str):
            raise ValueError("Model must be a string")
        template = self.env.get_template(template_name)
        return template.render(model=model, messages=messages, tools=tools, **kwargs)
