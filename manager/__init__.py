# SPDX-License-Identifier: MIT

import os
from jinja2 import Environment, FileSystemLoader

from ._version import __version__

__all__ = ["Manager", "__version__"]


class Manager:
    def __init__(self):
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

    def render_chat_with_tools(self, model, messages, tools):
        self._validate_messages(messages)
        self._validate_tools(tools)
        if not isinstance(model, str):
            raise ValueError("Model must be a string")
        template = self.env.get_template("chatwithtools.jinja")
        return template.render(model=model, messages=messages, tools=tools)
