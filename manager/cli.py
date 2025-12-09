# SPDX-License-Identifier: MIT

import argparse
import os
import shutil
from pathlib import Path
from typing import Dict, List

from manager import Manager


def setup_hooks() -> None:
    """Setup git hooks for conventional commits."""

    hooks_dir = Path(".git/hooks")
    if not hooks_dir.exists():
        print("Git repository not found. Please run from the project root.")
        return

    commit_msg_hook = hooks_dir / "commit-msg"
    script_path = Path(__file__).resolve().parent.parent / "scripts" / "commit-msg"

    if os.path.exists(script_path):
        shutil.copy(script_path, commit_msg_hook)
        os.chmod(commit_msg_hook, 0o755)
        print("Commit message hook installed.")
    else:
        print("Hook script not found.")


def main() -> None:
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
        m: Manager = Manager()
        messages: List[Dict[str, str]] = []
        if args.system_message:
            messages.append({"role": "system", "content": args.system_message})
        for msg in args.message:
            messages.append({"role": "user", "content": msg})
        tools: List[Dict[str, str]] = [{"type": t, "name": t} for t in args.tools]
        kwargs = {
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
            "stream": args.stream,
        }
        kwargs = {k: v for k, v in kwargs.items() if v}
        payload: str = m.render_chat_with_tools(
            args.model, messages, tools, template_name=args.template, **kwargs
        )
        print(payload)


if __name__ == "__main__":
    main()
