#!/usr/bin/env python3
"""
MCP Client implementation using FastMCP
"""
from fastmcp.client import Client
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("mcp-client")

class MCPDemoClient:
    def __init__(self, server_url="http://localhost:8000"):
        self.server_url = server_url
        self.client = Client(self.server_url)
        
    async def get_greeting(self):
        """Get the greeting from the server"""
        logger.info("Requesting greeting resource")
        result = await self.client.get("greeting")
        logger.info(f"Received greeting: {result}")
        return result
    
    async def get_status(self):
        """Get the server status"""
        logger.info("Requesting status resource")
        result = await self.client.get("status")
        logger.info(f"Received status: {result}")
        return result
    
    async def get_info(self):
        """Get server information"""
        logger.info("Requesting info resource")
        result = await self.client.get("info")
        logger.info(f"Received info: {result}")
        return result
    
    async def get_counter(self):
        """Get the current counter value"""
        logger.info("Requesting counter resource")
        result = await self.client.get("counter")
        logger.info(f"Received counter: {result}")
        return result
    
    async def increment_counter(self, value=None):
        """Increment the counter or set to a specific value"""
        logger.info(f"Incrementing counter with value: {value}")
        result = await self.client.put("counter", value)
        logger.info(f"Counter updated to: {result}")
        return result
    
    async def run_demo(self):
        """Run a demonstration of client capabilities"""
        try:
            # Get greeting
            greeting = await self.get_greeting()
            print(f"Greeting: {greeting}")
            
            # Get server information
            info = await self.get_info()
            print(f"Server Info: {info}")
            
            # Get initial counter value
            counter = await self.get_counter()
            print(f"Initial Counter: {counter}")
            
            # Increment counter a few times
            for _ in range(3):
                counter = await self.increment_counter()
                print(f"Counter after increment: {counter}")
            
            # Set counter to specific value
            counter = await self.increment_counter(10)
            print(f"Counter after setting to 10: {counter}")
            
            # Get server status
            status = await self.get_status()
            print(f"Server Status: {status}")
            
        except Exception as e:
            logger.error(f"Error during demo: {e}")

async def main():
    """Main entry point for the client"""
    client = MCPDemoClient()
    try:
        await client.run_demo()
    except KeyboardInterrupt:
        logger.info("Client shutting down")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
