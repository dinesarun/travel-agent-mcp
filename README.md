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

## Connecting to Claude Desktop

Add the following to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "travel-agent": {
      "command": "/path/to/.venv/bin/python",
      "args": ["/path/to/travel-agent-mcp/server.py"]
    }
  }
}
```

Replace `/path/to/` with the absolute path to this project.

## Project Structure

```
travel-agent-mcp/
├── server.py        # FastMCP server with booking tools
├── bookings.json    # Local booking database (auto-created)
└── README.md
```

## License

MIT
