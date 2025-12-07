# SPDX-License-Identifier: MIT

import argparse
from manager import Manager


def main():
    parser = argparse.ArgumentParser(
        description="Generate xAI API payloads using Manager"
    )
    parser.add_argument("--model", default="grok-beta", help="Model name")
    parser.add_argument("--message", required=True, help="User message")
    parser.add_argument(
        "--tools", nargs="+", default=["web_search"], help="List of tools"
    )
    args = parser.parse_args()

    m = Manager()
    messages = [{"role": "user", "content": args.message}]
    tools = [{"type": t, "name": t} for t in args.tools]
    payload = m.render_chat_with_tools(args.model, messages, tools)
    print(payload)


if __name__ == "__main__":
    main()
