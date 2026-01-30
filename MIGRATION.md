# Migration Guide: xAI API Endpoint Changes

## Overview

The xAI `/v1/messages` endpoint is being deprecated on **February 20, 2026**. This guide helps you migrate to the new endpoints.

## What's Changed

### New Endpoints
- **Chat Completions**: `/v1/chat/completions` (OpenAI-compatible)
- **Responses**: `/v1/responses` (xAI-specific)

### Deprecated Endpoint
- **Messages**: `/v1/messages` (will return 410 Gone after Feb 20, 2026)

## Migration Steps

### 1. Update Your Code

**Before (Deprecated):**
```python
from manager import Manager

m = Manager()
payload = m.render_chat_with_tools(
    "grok-beta",
    [{"role": "user", "content": "Hello"}],
    [{"type": "web_search", "name": "web_search"}]
)
```

**After (New Chat Completions):**
```python
from manager import Manager

m = Manager()
payload = m.render_chat_completions(
    "grok-4",
    [{"role": "user", "content": "Hello"}],
    [{"type": "function", "function": {"name": "web_search"}}]
)
```

**After (New Responses):**
```python
from manager import Manager

m = Manager()
payload = m.render_responses(
    [{"role": "user", "content": "Hello"}],
    [{"type": "function", "function": {"name": "web_search"}}]
)
```

### 2. Update Tool Format

**Old Format:**
```python
tools = [{"type": "web_search", "name": "web_search"}]
```

**New Format:**
```python
tools = [{
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the web for information"
    }
}]
```

### 3. Update CLI Usage

**Before:**
```bash
manager-cli --message "Hello" --model grok-beta
```

**After:**
```bash
manager-cli --message "Hello" --model grok-4 --endpoint chat_completions
# or
manager-cli --message "Hello" --endpoint responses
```

## Backward Compatibility

The old `render_chat_with_tools()` method still works but shows deprecation warnings. It automatically uses the new chat completions endpoint.

## Key Differences

| Feature | Messages (Deprecated) | Chat Completions | Responses |
|---------|----------------------|------------------|-----------|
| Endpoint | `/v1/messages` | `/v1/chat/completions` | `/v1/responses` |
| Model param | Required | Required | Not used |
| Input field | `messages` | `messages` | `input` |
| Tool format | Simple | OpenAI-compatible | xAI-specific |
| Compatibility | xAI only | OpenAI-compatible | xAI only |

## Timeline

- **Now**: Both old and new endpoints work
- **February 20, 2026**: `/v1/messages` returns 410 Gone
- **Recommended**: Migrate immediately to avoid disruption

## Need Help?

Check the [examples/migration_example.py](examples/migration_example.py) for complete working examples.
