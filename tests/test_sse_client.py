pytest_plugins = ['pytest_asyncio']

import types
import sys
from unittest.mock import AsyncMock, patch

# create dummy fastmcp modules if not installed
fastmcp_client = types.ModuleType('fastmcp.client')
fastmcp_transports = types.ModuleType('fastmcp.client.transports')

class DummyClient:
    def __init__(self, *args, **kwargs):
        pass

    async def get(self, *a, **k):
        pass

    async def put(self, *a, **k):
        pass

class DummyTransport:
    def __init__(self, url):
        self.url = url

fastmcp_client.Client = DummyClient
fastmcp_transports.SSETransport = DummyTransport
fastmcp_client.transports = fastmcp_transports

fastmcp = types.ModuleType('fastmcp')
fastmcp.client = fastmcp_client
sys.modules.setdefault('fastmcp', fastmcp)
sys.modules.setdefault('fastmcp.client', fastmcp_client)
sys.modules.setdefault('fastmcp.client.transports', fastmcp_transports)

from client.sse.client import MCPSSEClient


import pytest

@pytest.mark.asyncio
async def test_get_resource_url_prefix():
    with patch('client.sse.client.Client.get', new_callable=AsyncMock) as mock_get:
        c = MCPSSEClient('http://example.com')
        await c.get_resource('hello')
        mock_get.assert_awaited_once()
        assert mock_get.call_args[0][0].startswith('http://example.com')


@pytest.mark.asyncio
async def test_update_resource_url_prefix_counter():
    with patch('client.sse.client.Client.put', new_callable=AsyncMock) as mock_put:
        c = MCPSSEClient('http://example.com')
        await c.update_resource('counter', 5)
        mock_put.assert_awaited_once()
        assert mock_put.call_args[0][0].startswith('http://example.com')


@pytest.mark.asyncio
async def test_update_resource_url_prefix_general():
    with patch('client.sse.client.Client.put', new_callable=AsyncMock) as mock_put:
        c = MCPSSEClient('http://example.com')
        await c.update_resource('foo', 'bar')
        mock_put.assert_awaited_once()
        assert mock_put.call_args[0][0].startswith('http://example.com')
