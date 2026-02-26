# Travel Agent MCP

A lightweight hotel booking MCP (Model Context Protocol) server built with [FastMCP](https://gofastmcp.com). It exposes tools that let any MCP-compatible AI client (e.g. Claude Desktop) create and list hotel bookings.

## Features

- **Create booking** – register a hotel stay (name, city, nights)
- **List bookings** – retrieve all saved bookings
- Bookings are persisted locally in `bookings.json`

## Requirements

- Python 3.10+
- [fastmcp](https://gofastmcp.com) >= 3.0.0

## Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install fastmcp
```

## Running the server

```bash
python server.py
```

The MCP server starts and listens for tool calls from a connected client.

## Tools

| Tool | Description | Parameters |
|---|---|---|
| `create_booking` | Registers a new hotel booking | `hotel_name: str`, `city: str`, `nights: int` |
| `list_bookings` | Retrieves all current bookings | _(none)_ |

## How It Works

### FastMCP
FastMCP turns plain Python functions into MCP tools instantly — no boilerplate, no protocol wiring needed. It runs **entirely on your local machine** and does not require internet access.

### Keyword Extraction & Natural Language Parsing
FastMCP itself does **not** parse natural language. Here is the full flow:

```
"Book me a room at Marriott in Paris for 3 nights"
        ↓
  Claude Desktop (LLM)
  - Reads your tool definitions (tool name + param names + docstrings)
  - Understands natural language using its built-in LLM capabilities
  - Extracts: hotel_name="Marriott", city="Paris", nights=3
        ↓
  JSON-RPC call to your local server.py
  { "tool": "create_booking", "arguments": { "hotel_name": "Marriott", "city": "Paris", "nights": 3 } }
        ↓
  FastMCP (server.py) receives the structured call
  - Matches tool name → create_booking()
  - Passes extracted params to your Python function
        ↓
  bookings.json (saved locally)
```

### How Claude Knows What to Extract
Claude reads your **function signature and docstring** from `server.py`:

```python
@mcp.tool()
def create_booking(hotel_name: str, city: str, nights: int):
    """Create a hotel booking"""
```

- **Param names** (`hotel_name`, `city`, `nights`) tell Claude what values to look for
- **Types** (`str`, `int`) tell Claude what format to send
- **Docstrings** help Claude understand when to call which tool

> Internet is only needed for the **Claude LLM API** — FastMCP itself runs fully offline.

### Component Summary

| Component | Runs where | Needs internet? |
|---|---|---|
| Claude Desktop (AI client) | Local app | Yes (Anthropic API) |
| FastMCP server (`server.py`) | Local Python process | No |
| NLP / keyword extraction | Done by Claude (LLM) | Yes (Claude API) |
| Tool execution | Local FastMCP | No |

## Connecting to Claude Desktop

### 1. Find your project path

```bash
pwd
# e.g. /Users/alice/projects/travel-agent-mcp
```

### 2. Note your Python interpreter path

```bash
source .venv/bin/activate
which python
# e.g. /Users/alice/projects/travel-agent-mcp/.venv/bin/python
```

### 3. Edit the Claude Desktop config

Open (or create) the config file:

| OS | Path |
|---|---|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

Add the `travel-agent` entry under `mcpServers`, replacing the paths with your actual values from steps 1 and 2:

```json
{
  "mcpServers": {
    "travel-agent": {
      "command": "/Users/alice/projects/travel-agent-mcp/.venv/bin/python",
      "args": ["/Users/alice/projects/travel-agent-mcp/server.py"]
    }
  }
}
```

### 4. Restart Claude Desktop

Quit and reopen Claude Desktop so it picks up the new config.

### 5. Verify the connection

Open a new conversation in Claude Desktop. The travel-agent tools should appear in the tool picker (hammer icon). If not, check **Settings → Developer → MCP Servers** for error logs.

### 6. Test with natural language

Try these prompts:

```
Book me a room at Marriott in Paris for 3 nights.
```

```
Show me all my current hotel bookings.
```

Claude will automatically call `create_booking` or `list_bookings` and return the result.

## Project Structure

```
travel-agent-mcp/
├── server.py        # FastMCP server with booking tools
├── bookings.json    # Local booking database (auto-created)
└── README.md
```

## License

MIT
