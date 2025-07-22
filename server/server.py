#!/usr/bin/env python3
"""
MCP Server implementation using FastMCP
"""
from fastmcp.server import server
import asyncio
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("mcp-server")

# Sample data to serve
sample_resources = {
    "greeting": "Hello from MCP Server!",
    "status": "running",
    "info": {
        "name": "MCP FastAPI Demo Server",
        "version": "1.0.0",
        "description": "A simple MCP server implementation using FastMCP"
    },
    "counter": 0
}

class MCPDemoServer:
    def __init__(self, host="localhost", port=8000):
        self.host = host
        self.port = port
        self.server = server.FastMCP()
        self.setup_resources()
        
    def setup_resources(self):
        """Set up the resources and methods for the MCP server"""
        # Define resource handler functions
        async def get_greeting():
            logger.info("Serving greeting resource")
            return sample_resources["greeting"]
            
        async def get_status():
            logger.info("Serving status resource")
            return sample_resources["status"]
            
        async def get_info():
            logger.info("Serving info resource")
            return sample_resources["info"]
            
        async def get_counter():
            logger.info("Serving counter resource")
            return sample_resources["counter"]
            
        async def update_counter(value=None):
            if value is not None and isinstance(value, int):
                sample_resources["counter"] = value
            else:
                sample_resources["counter"] += 1
            logger.info(f"Counter updated to {sample_resources['counter']}")
            return sample_resources["counter"]
        
        # Add resources using add_resource_fn method with complete URLs
        self.server.add_resource_fn(get_greeting, uri="http://localhost:8000/greeting")
        self.server.add_resource_fn(get_status, uri="http://localhost:8000/status")
        self.server.add_resource_fn(get_info, uri="http://localhost:8000/info")
        self.server.add_resource_fn(get_counter, uri="http://localhost:8000/counter")
        
        # Add resource with PUT method - need to use a different URI to avoid conflict
        self.server.add_resource_fn(update_counter, uri="http://localhost:8000/counter/update")
        
    # Resource methods are now defined inside setup_resources using decorators
    
    async def start(self):
        """Start the MCP server"""
        logger.info(f"Starting MCP server on {self.host}:{self.port}")
        # Run both HTTP and SSE servers
        await self.server.run_async(host=self.host, port=self.port)
        logger.info("MCP server started")
        
        # Keep the server running
        while True:
            await asyncio.sleep(1)

async def main():
    """Main entry point for the server"""
    server = MCPDemoServer()
    try:
        await server.start()
    except KeyboardInterrupt:
        logger.info("Server shutting down")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
