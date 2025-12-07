# SPDX-License-Identifier: MIT

import argparse
from manager import Manager


def setup_hooks():
    """Setup git hooks for conventional commits."""
    import shutil
    import os

    hooks_dir = ".git/hooks"
    if not os.path.exists(hooks_dir):
        print("Git repository not found. Please run from the project root.")
        return

    commit_msg_hook = os.path.join(hooks_dir, "commit-msg")
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "commit-msg")

    if os.path.exists(script_path):
        shutil.copy(script_path, commit_msg_hook)
        os.chmod(commit_msg_hook, 0o755)
        print("Commit message hook installed.")
    else:
        print("Hook script not found.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate xAI API payloads using Manager"
    )
    parser.add_argument("--model", default="grok-beta", help="Model name")
    parser.add_argument(
        "--message", action="append", help="User message (can be used multiple times)"
    )
    parser.add_argument("--system-message", help="System message")
    parser.add_argument(
        "--tools", nargs="+", default=["web_search"], help="List of tool names"
    )
    parser.add_argument(
        "--template", default="chatwithtools.jinja", help="Template name"
    )
    parser.add_argument("--temperature", type=float, help="Temperature for generation")
    parser.add_argument("--max-tokens", type=int, help="Max tokens for generation")
    parser.add_argument("--stream", action="store_true", help="Enable streaming")
    parser.add_argument(
        "--setup-hooks",
        action="store_true",
        help="Setup git hooks for conventional commits",
    )

    args = parser.parse_args()

    if args.setup_hooks:
        setup_hooks()
    else:
        if not args.message:
            parser.error("--message is required unless --setup-hooks is used")
        m = Manager()
        messages = []
        if args.system_message:
            messages.append({"role": "system", "content": args.system_message})
        for msg in args.message:
            messages.append({"role": "user", "content": msg})
        tools = [{"type": t, "name": t} for t in args.tools]
        kwargs = {}
        if args.temperature is not None:
            kwargs["temperature"] = args.temperature
        if args.max_tokens is not None:
            kwargs["max_tokens"] = args.max_tokens
        if args.stream:
            kwargs["stream"] = args.stream
        payload = m.render_chat_with_tools(
            args.model, messages, tools, template_name=args.template, **kwargs
        )
        print(payload)


if __name__ == "__main__":
    main()
