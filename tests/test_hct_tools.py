import json
from unittest import mock

import pytest
import requests
from fastmcp import Client
from fastmcp.exceptions import ToolError

import jnpr_pathfinder_mcp
from jnpr_pathfinder_mcp.server.hct import mcp


class ResponseMock:
    def __init__(self, ok=True, content=""):
        self.content = self.text = content
        self.ok = ok

    def ok(self):
        return self.ok

    def json(self):
        return json.loads(self.content)


@pytest.mark.asyncio
async def test_categories():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        result = await client.call_tool("categories")
        assert result.structured_content.get("success")
        assert result.structured_content.get("response")


@pytest.mark.asyncio
async def test_categories_requests_error_raises():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            side_effect=requests.exceptions.RequestException,
        ):
            with pytest.raises(ToolError):
                await client.call_tool("categories")


@pytest.mark.asyncio
async def test_categories_request_not_ok():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(False, "Failed."),
        ):
            result = await client.call_tool("categories")
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert not result.structured_content.get("response")


@pytest.mark.asyncio
async def test_categories_request_empty_response():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(True, ""),
        ):
            result = await client.call_tool("categories")
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert "Empty response from API" in result.structured_content.get("error")


@pytest.mark.asyncio
async def test_category_components():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        result = await client.call_tool("category_components", {"category_key": 100001})
        assert result.structured_content.get("success")
        assert result.structured_content.get("response")


@pytest.mark.asyncio
async def test_category_components_requests_error_raises():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            side_effect=requests.exceptions.RequestException,
        ):
            with pytest.raises(ToolError):
                await client.call_tool("category_components", {"category_key": 100001})


@pytest.mark.asyncio
async def test_category_components_request_not_ok():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(False, "Failed."),
        ):
            result = await client.call_tool("category_components", {"category_key": 100001})
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert not result.structured_content.get("response")


@pytest.mark.asyncio
async def test_category_components_request_empty_response():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(True, ""),
        ):
            result = await client.call_tool("category_components", {"category_key": 100001})
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert "Empty response from API" in result.structured_content.get("error")


@pytest.mark.asyncio
async def test_component_details():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        result = await client.call_tool("component_details", {"component_name": "OSFP-800G-AOC-7M"})
        assert result.structured_content.get("success")
        assert result.structured_content.get("response")


@pytest.mark.asyncio
async def test_component_details_requests_error_raises():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            side_effect=requests.exceptions.RequestException,
        ):
            with pytest.raises(ToolError):
                await client.call_tool("component_details", {"component_name": "OSFP-800G-AOC-7M"})


@pytest.mark.asyncio
async def test_component_details_request_not_ok():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(False, "Failed."),
        ):
            result = await client.call_tool(
                "component_details", {"component_name": "OSFP-800G-AOC-7M"}
            )
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert not result.structured_content.get("response")


@pytest.mark.asyncio
async def test_component_details_request_empty_response():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(True, ""),
        ):
            result = await client.call_tool(
                "component_details", {"component_name": "OSFP-800G-AOC-7M"}
            )
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert "Empty response from API" in result.structured_content.get("error")


@pytest.mark.asyncio
async def test_component_supported_platforms():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        result = await client.call_tool(
            "component_supported_platforms", {"component_name": "OSFP-800G-AOC-7M"}
        )
        assert result.structured_content.get("success")
        assert result.structured_content.get("response")


@pytest.mark.asyncio
async def test_component_supported_platforms_requests_error_raises():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            side_effect=requests.exceptions.RequestException,
        ):
            with pytest.raises(ToolError):
                await client.call_tool(
                    "component_supported_platforms", {"component_name": "OSFP-800G-AOC-7M"}
                )


@pytest.mark.asyncio
async def test_component_supported_platforms_request_not_ok():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(False, "Failed."),
        ):
            result = await client.call_tool(
                "component_supported_platforms", {"component_name": "OSFP-800G-AOC-7M"}
            )
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert not result.structured_content.get("response")


@pytest.mark.asyncio
async def test_component_supported_platforms_request_empty_response():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(True, ""),
        ):
            result = await client.call_tool(
                "component_supported_platforms", {"component_name": "OSFP-800G-AOC-7M"}
            )
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert "Empty response from API" in result.structured_content.get("error")


@pytest.mark.asyncio
async def test_component_supported_models():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        result = await client.call_tool(
            "component_supported_models", {"component_name": "QFX10000-30C"}
        )
        assert result.structured_content.get("success")
        assert result.structured_content.get("response")


@pytest.mark.asyncio
async def test_component_supported_models_requests_error_raises():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            side_effect=requests.exceptions.RequestException,
        ):
            with pytest.raises(ToolError):
                await client.call_tool(
                    "component_supported_models", {"component_name": "QFX10000-30C"}
                )


@pytest.mark.asyncio
async def test_component_supported_models_request_not_ok():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(False, "Failed."),
        ):
            result = await client.call_tool(
                "component_supported_models", {"component_name": "QFX10000-30C"}
            )
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert not result.structured_content.get("response")


@pytest.mark.asyncio
async def test_component_supported_models_request_empty_response():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(True, ""),
        ):
            result = await client.call_tool(
                "component_supported_models", {"component_name": "QFX10000-30C"}
            )
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert "Empty response from API" in result.structured_content.get("error")


@pytest.mark.asyncio
async def test_platforms_by_family():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        result = await client.call_tool("platforms_by_family")
        assert result.structured_content.get("success")
        assert result.structured_content.get("response")


@pytest.mark.asyncio
async def test_platforms_by_family_requests_error_raises():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            side_effect=requests.exceptions.RequestException,
        ):
            with pytest.raises(ToolError):
                await client.call_tool("platforms_by_family")


@pytest.mark.asyncio
async def test_platforms_by_family_request_not_ok():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(False, "Failed."),
        ):
            result = await client.call_tool("platforms_by_family")
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert not result.structured_content.get("response")


@pytest.mark.asyncio
async def test_platforms_by_family_request_empty_response():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(True, ""),
        ):
            result = await client.call_tool("platforms_by_family")
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert "Empty response from API" in result.structured_content.get("error")


@pytest.mark.asyncio
async def test_components_for_platform():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        result = await client.call_tool("components_for_platform", {"platform": "EX4000"})
        assert result.structured_content.get("success")
        assert result.structured_content.get("response")


@pytest.mark.asyncio
async def test_components_for_platform_requests_error_raises():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            side_effect=requests.exceptions.RequestException,
        ):
            with pytest.raises(ToolError):
                await client.call_tool("components_for_platform", {"platform": "EX4000"})


@pytest.mark.asyncio
async def test_components_for_platform_request_not_ok():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(False, "Failed."),
        ):
            result = await client.call_tool("components_for_platform", {"platform": "EX4000"})
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert not result.structured_content.get("response")


@pytest.mark.asyncio
async def test_components_for_platform_request_empty_response():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(True, ""),
        ):
            result = await client.call_tool("components_for_platform", {"platform": "EX4000"})
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert "Empty response from API" in result.structured_content.get("error")


@pytest.mark.asyncio
async def test_platform_hardware_details():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        result = await client.call_tool("platform_hardware_details", {"platform": "EX4000"})
        assert result.structured_content.get("success")
        assert result.structured_content.get("response")


@pytest.mark.asyncio
async def test_platform_hardware_details_requests_error_raises():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "post",
            side_effect=requests.exceptions.RequestException,
        ):
            with pytest.raises(ToolError):
                await client.call_tool("platform_hardware_details", {"platform": "EX4000"})


@pytest.mark.asyncio
async def test_platform_hardware_details_request_not_ok():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "post",
            return_value=ResponseMock(False, "Failed."),
        ):
            result = await client.call_tool("platform_hardware_details", {"platform": "EX4000"})
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert not result.structured_content.get("response")


@pytest.mark.asyncio
async def test_platform_hardware_details_request_empty_response():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "post",
            return_value=ResponseMock(True, ""),
        ):
            result = await client.call_tool("platform_hardware_details", {"platform": "EX4000"})
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert "Empty response from API" in result.structured_content.get("error")


@pytest.mark.asyncio
async def test_platform_information():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        result = await client.call_tool("platform_information", {"platform": "ACX710"})
        assert result.structured_content.get("success")
        assert result.structured_content.get("response")


@pytest.mark.asyncio
async def test_platform_information_requests_error_raises():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            side_effect=requests.exceptions.RequestException,
        ):
            with pytest.raises(ToolError):
                await client.call_tool("platform_information", {"platform": "EX4000"})


@pytest.mark.asyncio
async def test_platform_information_request_not_ok():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(False, "Failed."),
        ):
            result = await client.call_tool("platform_information", {"platform": "EX4000"})
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert not result.structured_content.get("response")


@pytest.mark.asyncio
async def test_platform_information_request_empty_response():
    """Test content and structure of workspace info command."""
    async with Client(mcp) as client:
        with mock.patch.object(
            jnpr_pathfinder_mcp.server.cli_explorer.requests,
            "get",
            return_value=ResponseMock(True, ""),
        ):
            result = await client.call_tool("platform_information", {"platform": "EX4000"})
            assert not result.structured_content.get("success")
            assert result.structured_content.get("error")
            assert "Empty response from API" in result.structured_content.get("error")
