manager/__init__.py:26

```python
def render_chat_with_tools(self, model, messages, tools):
    self._validate_messages(messages)
    self._validate_tools(tools)
    if not isinstance(model, str):
        raise ValueError("Model must be a string")
    template = self.env.get_template("chatwithtools.jinja")
    return template.render(model=model, messages=messages, tools=tools)
```

`manager` is a Python library and CLI tool for generating robust, structured templates for **xAI API agentic tool calls**. It uses Jinja2 to produce well-formed payloads that integrate messages, tools, and model configurations.

Manager library validation, configured with input checks to prevent malformed payloads. When validation is bypassed, it can lead to runtime errors or invalid API calls.

Incorrect template construction can lead to subtle but impactful runtime issues in agentic systems, such as:

* Missing or malformed tool specifications
* Invalid message formatting
* Rendering errors due to improper Jinja2 expressions
* Payloads that omit required fields expected by the xAI API models

These issues can degrade agent behavior, cause unexpected execution failures, or — in production environments — weaken the reliability guarantees of downstream automation.

Users of this library can create custom template extensions or override defaults by supplying their own Jinja2 templates or filters.

## Installation

```
pip install -e .
```

## Usage

### As a library

```python
from manager import Manager

m = Manager()
payload = m.render_chat_with_tools(
    "grok-beta",
    [{"role": "user", "content": "Hello"}],
    [{"type": "web_search", "name": "web_search"}]
)

print(payload)
```

### CLI

```
manager-cli --message "Search for AI news" --tools web_search code_execution
```

## Common Misconfigurations

Misusing or disabling key template components can result in malformed or incomplete xAI agent payloads. Common problematic patterns include:

### **1. Missing Tool Definitions**

Failing to include required tool metadata (e.g., `"name"`, `"type"`) can prevent the agent from resolving tool calls correctly.

### **2. Incorrect Message Shape**

Improperly formatted message objects (missing `"role"` or `"content"`) can lead to API rejections or undefined agent behavior.

### **3. Bypassing Default Rendering Logic**

Overriding template defaults without ensuring compatibility may produce payloads that the xAI model cannot interpret.

### Why These Issues Matter

Well-structured agent payloads are essential for:

* Ensuring deterministic tool invocation
* Preventing silent failures during multi-step reasoning
* Maintaining clear separation between user input, model instructions, and tool environments

When these structures are weakened, the agent may misinterpret instructions, skip tools, or produce degraded responses.

## Recommendation

To reduce errors and maintain compatibility with xAI agent requirements, ensure that:

* All tool entries include the necessary fields (`type`, `name`)
* Messages follow the strict structure:
  `{ "role": "<role>", "content": "<message>" }`
* Custom templates preserve the core structure expected by the default system template
* Template overrides include appropriate Jinja2 safety guards

### Example of an Incorrect Configuration

```python
# Missing 'name' field and incorrect message structure
m.render_chat_with_tools(
    "grok-beta",
    ["Hello"],  # invalid message format
    [{"type": "web_search"}]
)
```

### Example of a Correct Configuration

```python
m.render_chat_with_tools(
    "grok-beta",
    [{"role": "user", "content": "Find recent AI news"}],
    [{"type": "web_search", "name": "web_search"}]
)
```

## Vulnerabilities

No known vulnerabilities.

| Severity | Package | Fixed Version | Link |
| -------- | ------- | ------------- | ---- |
|          |         |               |      |

## Conventional Commits

This project uses conventional commit standards.

### Setup

1. Copy the commit hook: `cp scripts/commit-msg .git/hooks/`
2. Make it executable: `chmod +x .git/hooks/commit-msg`

### Usage

Commit messages must:
- Start with a type: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`, `perf:`, `ci:`, `build:`, `revert:`
- Be lowercase
- First line ≤40 characters

Examples:
- `feat: add input validation`
- `fix: correct message format check`
- `docs: update installation instructions`
- `chore: set up CI workflow`

To rewrite existing commits: `./scripts/rewrite_msg.sh <commit-hash>`

## References

* Jinja2 Documentation
* xAI API Documentation
* Template Injection and Payload Structuring Guidelines
* CWE-112: Missing Critical Step in Template Rendering
* CWE-1021: Improper Data Formatting in Structured Outputs
* Conventional Commits Specification
