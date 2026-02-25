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

## How FastMCP Works

FastMCP turns plain Python functions into MCP tools instantly — no boilerplate, no protocol wiring needed. Your AI client calls them like remote functions over a standard JSON-RPC transport.

## How the MCP Server Extracts Keywords

When you say *"Book me a room at Marriott in Paris for 3 nights"*, Claude (the client) reads your sentence and pulls out the key values — `hotel_name`, `city`, `nights` — then calls the matching tool with those extracted arguments automatically.

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
