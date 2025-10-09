import json
from unittest import mock

import pytest
import requests
from fastmcp import Client
from fastmcp.exceptions import ToolError

import jnpr_pathfinder_mcp
from jnpr_pathfinder_mcp.server.cli_explorer import mcp


class ResponseMock:
    def __init__(self, ok=True, content=""):
        self.content = self.text = content
        self.ok = ok

    def ok(self):
        return self.ok

    def json(self):
        return json.loads(self.content)


@pytest.mark.asyncio
async def test_topic_reference():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        result = await client.call_tool("topic_reference")
        assert result.structured_content.get("success")
        assert result.structured_content.get("response")
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            side_effect=requests.exceptions.RequestException,
        ):
            with pytest.raises(ToolError):
                await client.call_tool("topic_reference")

        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(False, "Failed."),
        ):
            result = await client.call_tool("topic_reference")
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert not result.structured_content.get("response")

        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(True, ""),
        ):
            result = await client.call_tool("topic_reference")
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert "Empty response from API" in result.structured_content.get("error")


@pytest.mark.asyncio
async def test_topic_hierarchy():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        result = await client.call_tool("topic_hierarchy")
        assert result.structured_content.get("success")
        assert result.structured_content.get("response")

        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "post",
            side_effect=requests.exceptions.RequestException,
        ):
            with pytest.raises(ToolError):
                await client.call_tool("topic_hierarchy")

        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "post",
            return_value=ResponseMock(False, "Failed."),
        ):
            result = await client.call_tool("topic_hierarchy")
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert not result.structured_content.get("response")
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "post",
            return_value=ResponseMock(True, ""),
        ):
            result = await client.call_tool("topic_hierarchy")
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert "Empty response from API" in result.structured_content.get("error")


@pytest.mark.asyncio
async def test_topic_search():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        result = await client.call_tool(
            "search", {"query": "bgp peers", "page_number": 0, "page_size": 10}
        )
        assert result.structured_content.get("success")
        assert result.structured_content.get("response")

        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "post",
            side_effect=requests.exceptions.RequestException,
        ):
            with pytest.raises(ToolError):
                await client.call_tool(
                    "search", {"query": "bgp peers", "page_number": 0, "page_size": 10}
                )

        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "post",
            return_value=ResponseMock(False, "Failed."),
        ):
            result = await client.call_tool(
                "search", {"query": "bgp peers", "page_number": 0, "page_size": 10}
            )
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert not result.structured_content.get("response")
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "post",
            return_value=ResponseMock(True, ""),
        ):
            result = await client.call_tool(
                "search", {"query": "bgp peers", "page_number": 0, "page_size": 10}
            )
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert "Empty response from API" in result.structured_content.get("error")
