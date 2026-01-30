 manager/__init__.py:46

```python
def render_chat_with_tools(
    self,
    model: str,
    messages: List[Dict[str, str]],
    tools: List[Dict[str, str]],
    template_name: str = "chatwithtools.jinja",
    **kwargs: Any
) -> str:
    """Render a JSON payload for xAI API chat completions with tools.

    Args:
        model (str): The model name (e.g., "grok-beta").
        messages (List[Dict[str, str]]): List of message dicts with 'role' and 'content'.
        tools (List[Dict[str, str]]): List of tool dicts with 'type' and 'name'.
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
```

`manager` is a Python library and CLI tool for generating robust, structured templates for **xAI API agentic tool calls**. It uses Jinja2 to produce well-formed payloads that integrate messages, tools, and model configurations. 

**🚨 IMPORTANT**: The xAI `/v1/messages` endpoint is deprecated and will be removed on February 20, 2026. This library now supports the new `/v1/chat/completions` and `/v1/responses` endpoints. See [MIGRATION.md](MIGRATION.md) for upgrade instructions.

Supports multiple endpoints and templates for basic and advanced use cases, including additional parameters like temperature and max_tokens.

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

## API Reference

### Manager Class

#### `Manager()`
Initializes the Manager with Jinja2 environment for template rendering.

#### `render_chat_completions(model: str, messages: List[Dict[str, str]], tools: List[Dict[str, Any]] = None, template_name: str = "chat_completions.jinja", **kwargs: Any) -> str`
Renders a JSON payload for xAI `/v1/chat/completions` endpoint (OpenAI-compatible).

- **Parameters:**
  - `model: str`: The model name (e.g., "grok-4").
  - `messages: List[Dict[str, str]]`: List of message dicts with 'role' and 'content'.
  - `tools: List[Dict[str, Any]]`: List of tool dicts in OpenAI format.
  - `template_name: str`: Name of the Jinja2 template to use. Default: "chat_completions.jinja".
  - `**kwargs: Any`: Additional parameters (temperature, max_tokens, stream, tool_choice).

- **Returns:** str: The rendered JSON payload.

- **Raises:** ValueError: If inputs do not meet validation requirements.

#### `render_responses(input_messages: List[Dict[str, str]], tools: List[Dict[str, Any]] = None, template_name: str = "responses.jinja", **kwargs: Any) -> str`
Renders a JSON payload for xAI `/v1/responses` endpoint.

- **Parameters:**
  - `input_messages: List[Dict[str, str]]`: List of message dicts with 'role' and 'content'.
  - `tools: List[Dict[str, Any]]`: List of tool dicts in xAI format.
  - `template_name: str`: Name of the Jinja2 template to use. Default: "responses.jinja".
  - `**kwargs: Any`: Additional parameters (temperature, max_tokens, stream, tool_choice).

- **Returns:** str: The rendered JSON payload.

- **Raises:** ValueError: If inputs do not meet validation requirements.

#### CLI

The `manager-cli` command provides a command-line interface for generating payloads.

- `--model`: Model name (default: "grok-4")
- `--message`: User message (can be used multiple times)
- `--system-message`: System message
- `--tools`: List of tool names (default: ["web_search"])
- `--template`: Template name (default: "chat_completions.jinja")
- `--endpoint`: API endpoint to target ("chat_completions" or "responses", default: "chat_completions")
- `--temperature`: Temperature for generation
- `--max-tokens`: Max tokens for generation
- `--stream`: Enable streaming
- `--setup-hooks`: Setup git hooks for conventional commits

## Usage

### As a library

```python
from manager import Manager

m = Manager()

# Basic usage with new chat completions endpoint
payload = m.render_chat_completions(
    "grok-4",
    [{"role": "user", "content": "Hello"}],
    [{"type": "function", "function": {"name": "web_search"}}]
)

print(payload)
```

#### Advanced Usage

```python
# Multiple messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Search for AI news"},
    {"role": "user", "content": "Summarize the results"}
]

# Using responses endpoint
payload = m.render_responses(
    messages,
    [{"type": "function", "function": {"name": "web_search"}}],
    temperature=0.7,
    max_tokens=1000,
    stream=True
)

print(payload)
```

### CLI

```
# Basic usage
manager-cli --message "Search for AI news" --tools web_search code_execution

# Multiple messages and system message
manager-cli --system-message "You are a helpful assistant." --message "Hello" --message "How can I help?" --tools web_search

# Using responses endpoint
manager-cli --message "Generate a story" --endpoint responses --temperature 0.8 --max-tokens 500 --stream

# Setup git hooks
manager-cli --setup-hooks
```

### Advanced Examples

#### Custom Tools
```python
from manager import Manager

m = Manager()

tools = [
    {"type": "function", "function": {"name": "web_search"}},
    {"type": "function", "function": {"name": "code_execution"}},
    {"type": "function", "function": {"name": "file_read"}}
]

payload = m.render_chat_completions(
    "grok-4",
    [{"role": "user", "content": "Analyze this codebase and suggest improvements"}],
    tools
)
```

#### Error Handling
```python
try:
    payload = m.render_chat_completions(
        "grok-4",
        [{"role": "user", "content": "Hello"}],  # Valid
        [{"type": "function"}]  # Missing 'function' key
    )
except ValueError as e:
    print(f"Validation error: {e}")
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
# Missing 'function' field and incorrect message structure
m.render_chat_completions(
    "grok-4",
    ["Hello"],  # invalid message format
    [{"type": "function"}]  # missing function details
)
```

### Example of a Correct Configuration

```python
m.render_chat_completions(
    "grok-4",
    [{"role": "user", "content": "Find recent AI news"}],
    [{"type": "function", "function": {"name": "web_search"}}]
)
```

## Vulnerabilities

No known vulnerabilities.

| Severity | Package | Fixed Version | Link |
| -------- | ------- | ------------- | ---- |
|          |         |               |      |

## Contributing

We welcome contributions! Please review our [Contributing Guidelines](CONTRIBUTING.md) and sign the [Contributor License Agreement](CLA.md) before submitting pull requests.

For project architecture details, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Conventional Commits

This project uses conventional commit standards.

### Setup

Run the setup command to install the commit hook:

```
manager-cli --setup-hooks
```

Or manually:

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
