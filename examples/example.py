# SPDX-License-Identifier: MIT

from manager import Manager

# Example usage
jinja_lib = Manager()

model = "grok-beta"
messages = [{"role": "user", "content": "Search for the latest news on AI."}]
tools = [{"type": "web_search", "name": "web_search"}]

payload = jinja_lib.render_chat_with_tools(model, messages, tools)
print(payload)
