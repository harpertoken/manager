# SPDX-License-Identifier: MIT

import os
from typing import Any, Dict, List

from ._version import __version__

__all__ = ["Manager", "__version__"]


class Manager:
    """Manager for generating robust JSON payloads for xAI API agentic tool calls.

    Uses Jinja2 templating to ensure well-formed outputs with built-in validation.
    Supports both chat completions and responses endpoints.
    """

    def __init__(self):
        """Initialize the Manager with Jinja2 environment."""
        from jinja2 import Environment, FileSystemLoader

        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def _validate_messages(self, messages: List[Dict[str, str]]) -> None:
        if not isinstance(messages, list):
            raise ValueError("Messages must be a list")
        for msg in messages:
            if not isinstance(msg, dict):
                raise ValueError("Each message must be a dict")
            if "role" not in msg or "content" not in msg:
                raise ValueError("Each message must have 'role' and 'content' keys")
            if not isinstance(msg["role"], str) or not isinstance(msg["content"], str):
                raise ValueError("'role' and 'content' must be strings")

    def _validate_tools(self, tools: List[Dict[str, Any]]) -> None:
        if not isinstance(tools, list):
            raise ValueError("Tools must be a list")
        for tool in tools:
            if not isinstance(tool, dict):
                raise ValueError("Each tool must be a dict")
            if "type" not in tool:
                raise ValueError("Each tool must have 'type' key")
            if tool["type"] == "function":
                if "function" not in tool:
                    raise ValueError("Function tools must have 'function' key")
                func = tool["function"]
                if "name" not in func:
                    raise ValueError("Function must have 'name' key")
            # Legacy format support
            elif "name" not in tool:
                raise ValueError("Each tool must have 'name' key")

    def render_chat_completions(
        self,
        model: str,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]] = None,
        template_name: str = "chat_completions.jinja",
        **kwargs: Any,
    ) -> str:
        """Render a JSON payload for xAI /v1/chat/completions endpoint.

        Args:
            model (str): The model name (e.g., "grok-4").
            messages (list): List of message dicts with 'role' and 'content'.
            tools (list, optional): List of tool dicts in OpenAI format.
            template_name (str): Name of the Jinja2 template to use.
            **kwargs: Additional parameters (temperature, max_tokens, stream, etc.).

        Returns:
            str: The rendered JSON payload.

        Raises:
            ValueError: If inputs do not meet validation requirements.
        """
        self._validate_messages(messages)
        if tools:
            self._validate_tools(tools)
        if not isinstance(model, str):
            raise ValueError("Model must be a string")
        template = self.env.get_template(template_name)
        return template.render(model=model, messages=messages, tools=tools, **kwargs)

    def render_responses(
        self,
        input_messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]] = None,
        template_name: str = "responses.jinja",
        **kwargs: Any,
    ) -> str:
        """Render a JSON payload for xAI /v1/responses endpoint.

        Args:
            input_messages (list): List of message dicts with 'role' and 'content'.
            tools (list, optional): List of tool dicts in xAI format.
            template_name (str): Name of the Jinja2 template to use.
            **kwargs: Additional parameters (temperature, max_tokens, stream, etc.).

        Returns:
            str: The rendered JSON payload.

        Raises:
            ValueError: If inputs do not meet validation requirements.
        """
        self._validate_messages(input_messages)
        if tools:
            self._validate_tools(tools)
        template = self.env.get_template(template_name)
        return template.render(input=input_messages, tools=tools, **kwargs)

    # Legacy method for backward compatibility
    def render_chat_with_tools(
        self,
        model: str,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        template_name: str = "chat_completions.jinja",
        **kwargs: Any,
    ) -> str:
        """Legacy method - use render_chat_completions instead.

        DEPRECATED: The /v1/messages endpoint is deprecated.
        Use render_chat_completions() for /v1/chat/completions endpoint.
        """
        import warnings

        warnings.warn(
            "render_chat_with_tools is deprecated. Use render_chat_completions() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.render_chat_completions(
            model, messages, tools, template_name, **kwargs
        )
