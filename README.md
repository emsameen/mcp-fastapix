# MCP FastAPI Demo

A simple implementation of MCP (Meta-Object Communication Protocol) client and server using FastMCP with multiple client transport options (stdio and SSE).

## Project Structure

```text
mcp-fastapi/
├── client/
│   ├── stdio/
│   │   └── client.py     # MCP client implementation using stdio transport
│   └── sse/
│       └── client.py     # MCP client implementation using SSE transport
├── server/
│   └── server.py         # MCP server implementation
├── .venv/                # Python virtual environment (uv)
├── requirements.txt      # Project dependencies
└── README.md             # This file
```

## Prerequisites

- Python 3.8+
- uv package manager

## Installation

The project is already set up with a virtual environment and the required dependencies installed using uv.

To activate the virtual environment:

```bash
source .venv/bin/activate
```

If you need to install or update dependencies:

```bash
uv pip install -r requirements.txt
```

## Usage

### Starting the Server

1. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

2. Run the server:

   ```bash
   python server/server.py
   ```

The server will start on `localhost:8000` and provide both HTTP and SSE endpoints.

### Running the Clients

#### SSE Client

1. In a separate terminal, activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

2. Run the SSE client:
   ```bash
   python client/sse/client.py
   ```

   You can also specify a custom server URL:

   ```bash
   python client/sse/client.py http://localhost:8000
   ```

#### Stdio Client

1. In a separate terminal, activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

2. Run the stdio client:

   ```bash
   python client/stdio/client.py
   ```

Both clients provide an interactive interface to interact with the MCP server.

## Available Resources

The MCP server provides the following resources:

- `greeting`: A simple greeting message
- `status`: The current server status
- `info`: Information about the server
- `counter`: A counter that can be incremented or set to a specific value

## Client Operations

Both clients provide an interactive command-line interface with the following commands:

- `get <resource>` - Get a resource (greeting, status, info, counter)
- `put counter <value>` - Update the counter to a specific value
- `exit` - Exit the client

Examples:

```bash
> get greeting
Hello from MCP Server!

> get info
{
  "name": "MCP FastAPI Demo Server",
  "version": "1.0.0",
  "description": "A simple MCP server implementation using FastMCP"
}

> get counter
0

> put counter 10
Counter updated to: 10
```

## Extending the Project

To add new resources or methods:

1. In `server.py`, add new resources to the `sample_resources` dictionary
2. Add new resource methods in the `setup_resources` method using the `@server.resource()` decorator
3. In the client implementations, add corresponding methods to interact with the new resources

### Transport Options

FastMCP supports multiple transport options:

- **SSE Transport**: Used for browser-based or HTTP clients
- **Stdio Transport**: Used for command-line or terminal-based clients
- **WebSocket Transport**: For real-time bidirectional communication
- **HTTP Transport**: For standard HTTP clients

This project demonstrates both SSE and stdio transport options.
