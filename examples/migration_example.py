#!/usr/bin/env python3
"""
Example demonstrating the new xAI API endpoints.
Shows migration from deprecated /v1/messages to new endpoints.
"""

from manager import Manager


def main():
    m = Manager()

    # Example messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's the weather like in San Francisco?"},
    ]

    # Example tools in new format
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "default": "fahrenheit",
                        },
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    print("=== Chat Completions Endpoint (/v1/chat/completions) ===")
    chat_payload = m.render_chat_completions(
        model="grok-4", messages=messages, tools=tools, temperature=0.7, max_tokens=1000
    )
    print(chat_payload)
    print()

    print("=== Responses Endpoint (/v1/responses) ===")
    responses_payload = m.render_responses(
        input_messages=messages, tools=tools, temperature=0.7, max_tokens=1000
    )
    print(responses_payload)
    print()

    print("=== Legacy Method (with deprecation warning) ===")
    # This will show a deprecation warning
    legacy_payload = m.render_chat_with_tools(
        model="grok-4", messages=messages, tools=tools, temperature=0.7
    )
    print(legacy_payload)


if __name__ == "__main__":
    main()
