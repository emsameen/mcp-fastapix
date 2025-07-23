#!/usr/bin/env python3
"""
MCP Client implementation using FastMCP with SSE transport
"""
from fastmcp.client import Client
from fastmcp.client.transports import SSETransport
import asyncio
import logging
import json
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("mcp-sse-client")

class MCPSSEClient:
    def __init__(self, server_url="http://localhost:8000"):
        # Create a client with SSE transport
        self.server_url = server_url
        self.transport = SSETransport(self.server_url)
        self.client = Client(transport=self.transport)
        
    async def get_resource(self, resource_name):
        """Get a resource from the server"""
        logger.info(f"Requesting resource: {resource_name}")
        result = await self.client.get(f"{self.server_url.rstrip('/')}/{resource_name}")
        logger.info(f"Received {resource_name}: {result}")
        return result
    
    async def update_resource(self, resource_name, value):
        """Update a resource on the server"""
        logger.info(f"Updating resource {resource_name} with value: {value}")
        # For PUT requests to counter, use the special update endpoint
        if resource_name == "counter":
            result = await self.client.put(f"{self.server_url.rstrip('/')}/counter/update", value)
        else:
            result = await self.client.put(f"{self.server_url.rstrip('/')}/{resource_name}", value)
        logger.info(f"Resource {resource_name} updated to: {result}")
        return result
    
    async def run_demo(self):
        """Run a demonstration of client capabilities"""
        try:
            # Print instructions
            print(f"MCP SSE Client Demo - Connected to {self.server_url}")
            print("=====================")
            print("Available commands:")
            print("  get <resource>       - Get a resource (greeting, status, info, counter)")
            print("  put counter <value>  - Update counter value")
            print("  exit                 - Exit the client")
            print()
            
            while True:
                # Get user input
                print("> ", end="", flush=True)
                command = input().strip()
                
                if command == "exit":
                    print("Exiting...")
                    break
                
                parts = command.split()
                if not parts:
                    continue
                
                if parts[0] == "get" and len(parts) == 2:
                    resource = parts[1]
                    try:
                        result = await self.get_resource(resource)
                        if isinstance(result, (dict, list)):
                            print(json.dumps(result, indent=2))
                        else:
                            print(result)
                    except Exception as e:
                        print(f"Error: {e}")
                
                elif parts[0] == "put" and parts[1] == "counter" and len(parts) == 3:
                    try:
                        value = int(parts[2])
                        result = await self.update_resource("counter", value)
                        print(f"Counter updated to: {result}")
                    except ValueError:
                        print("Error: Counter value must be an integer")
                    except Exception as e:
                        print(f"Error: {e}")
                
                else:
                    print("Unknown command. Try 'get <resource>' or 'put counter <value>'")
            
        except KeyboardInterrupt:
            logger.info("Client shutting down")
        except Exception as e:
            logger.error(f"Error during demo: {e}")

async def main():
    """Main entry point for the client"""
    # Allow specifying a custom server URL as a command-line argument
    server_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    client = MCPSSEClient(server_url)
    try:
        await client.run_demo()
    except KeyboardInterrupt:
        logger.info("Client shutting down")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
