
import json
import pytest
import requests
from unittest import mock

from fastmcp import Client
from fastmcp.exceptions import ToolError

import jnpr_pathfinder_mcp
from jnpr_pathfinder_mcp.server.feature_explorer import mcp

class ResponseMock():
    def __init__(self, ok=True, content="", status_code=200):
        # emulate requests.Response: .content (bytes) and .text and .ok and .json()
        if isinstance(content, (dict, list)):
            self.content = json.dumps(content).encode("utf-8")
            self.text = json.dumps(content)
        else:
            # allow passing raw text
            self.content = content.encode("utf-8") if isinstance(content, str) else content
            self.text = content if isinstance(content, str) else ""
        self.ok = ok
        self.status_code = status_code

    def json(self):
        if not (self.text or self.content):
            raise ValueError("No content")
        if self.text:
            return json.loads(self.text)
        return json.loads(self.content.decode("utf-8"))

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("Raising for status.")

@pytest.mark.asyncio
async def test_software_releases_success():
    async with Client(mcp) as client:
        result = await client.call_tool("software_releases")
        assert result.structured_content.get('success')
        assert result.structured_content.get('response')

@pytest.mark.asyncio
async def test_software_releases_requests_error_raises():
    async with Client(mcp) as client:
        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "post", side_effect=requests.exceptions.RequestException):
            with pytest.raises(ToolError):
                await client.call_tool("software_releases")

@pytest.mark.asyncio
async def test_software_releases_not_ok():
    async with Client(mcp) as client:
        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "post", return_value=ResponseMock(False, "Failed")):
            result = await client.call_tool("software_releases")
            assert not result.structured_content.get('success')
            assert result.structured_content.get('error')
            assert not result.structured_content.get('response')

@pytest.mark.asyncio
async def test_software_releases_empty_response():
    async with Client(mcp) as client:
        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "post", return_value=ResponseMock(True, "")):
            result = await client.call_tool("software_releases")
            assert not result.structured_content.get('success')
            assert result.structured_content.get('error')
            assert 'Empty response' in (result.structured_content.get('error') or '') or 'Empty response' in (result.structured_content.get('error') or '')

@pytest.mark.asyncio
async def test_models_for_release_success_and_errors():
    async with Client(mcp) as client:
        payload = {"platforms": ["ACX710", "EX4300"]}
        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "get", return_value=ResponseMock(True, payload)):
            result = await client.call_tool("models_compatible_with_release", {"junos_os_type": "Junos OS", "junos_version": "25.2R1"})
            assert result.structured_content.get('success')
            assert result.structured_content.get('response') == payload

        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "get", side_effect=requests.exceptions.RequestException):
            with pytest.raises(ToolError):
                await client.call_tool("models_compatible_with_release", {"junos_os_type": "Junos OS", "junos_version": "25.2R1"})

        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "get", return_value=ResponseMock(False, "Failed")):
            result = await client.call_tool("models_compatible_with_release", {"junos_os_type": "Junos OS", "junos_version": "25.2R1"})
            assert not result.structured_content.get('success')

        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "get", return_value=ResponseMock(True, "")):
            result = await client.call_tool("models_compatible_with_release", {"junos_os_type": "Junos OS", "junos_version": "25.2R1"})
            assert not result.structured_content.get('success')

        with pytest.raises(ToolError):
            result = await client.call_tool("models_compatible_with_release", {"junos_os_type": "Junos OS BadName", "junos_version": "25.2R1"})
            assert not result.structured_content.get('success')

        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "get", return_value=ResponseMock(True, "")):
            result = await client.call_tool("models_compatible_with_release", {"junos_os_type": "Junos OS", "junos_version": "25.2R1"})
            assert not result.structured_content.get('success')

@pytest.mark.asyncio
async def test_releases_compatible_with_model_success_and_errors():
    async with Client(mcp) as client:
        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer, "_build_platform_catalog", return_value={"mx10008": {"product_key": 11320008}}):
            result = await client.call_tool("releases_compatible_with_model", {"model": "MX10008"})
            assert result.structured_content.get('success')

        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "get", side_effect=requests.exceptions.RequestException):
            with pytest.raises(ToolError):
                result = await client.call_tool("releases_compatible_with_model", {"model": "MX10008"})

        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer, "_build_platform_catalog", return_value={"mx10008": {"product_key": 11320008}}):
            with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "get", return_value=ResponseMock(False, "Failed")):
                result = await client.call_tool("releases_compatible_with_model", {"model": "MX10008"})
                assert not result.structured_content.get('success')

        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer, "_build_platform_catalog", return_value={"mx10008": {"product_key": 11320008}}):
            with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "get", return_value=ResponseMock(True, "")):
                result = await client.call_tool("releases_compatible_with_model", {"model": "MX10008"})
                assert not result.structured_content.get('success')

@pytest.mark.asyncio
async def test_features_for_model_on_release_success_and_errors():
    async with Client(mcp) as client:
        payload = {"features": ["f1", "f2"]}
        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "post", return_value=ResponseMock(True, payload)):
            result = await client.call_tool("features_for_model_on_junos_version", {"junos_os_type": "Junos OS", "junos_version": "25.2R1", "model": "ACX710"})
            assert result.structured_content.get('success')
            assert result.structured_content.get('response') == payload

        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "post", side_effect=requests.exceptions.RequestException):
            with pytest.raises(ToolError):
                await client.call_tool("features_for_model_on_junos_version", {"junos_os_type": "Junos OS", "junos_version": "25.2R1", "model": "ACX710"})

        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "post", return_value=ResponseMock(False, "Failed")):
            result = await client.call_tool("features_for_model_on_junos_version", {"junos_os_type": "Junos OS", "junos_version": "25.2R1", "model": "ACX710"})
            assert not result.structured_content.get('success')

        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "post", return_value=ResponseMock(True, "")):
            result = await client.call_tool("features_for_model_on_junos_version", {"junos_os_type": "Junos OS", "junos_version": "25.2R1", "model": "ACX710"})
            assert not result.structured_content.get('success')

@pytest.mark.asyncio
async def test_feature_tree_and_details_and_product_keys():
    async with Client(mcp) as client:
        # feature_tree
        tree_payload = {"tree": []}
        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "get", return_value=ResponseMock(True, tree_payload)):
            result = await client.call_tool("feature_tree")
            assert result.structured_content.get('success')
            assert result.structured_content.get('response') == tree_payload

        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "get", return_value=ResponseMock(False, tree_payload)):
            result = await client.call_tool("feature_tree")
            assert not result.structured_content.get('success')

        # feature_details
        details_payload = {"detail": {"k": "v"}}
        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "get", return_value=ResponseMock(True, details_payload)):
            result = await client.call_tool("feature_details", {"feature_key": "12345"})
            assert result.structured_content.get('success')
            assert result.structured_content.get('response') == details_payload

        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "get", return_value=ResponseMock(False, details_payload)):
            result = await client.call_tool("feature_details", {"feature_key": "12345"})
            assert not result.structured_content.get('success')

        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer.requests, "get", side_effect=Exception("boom")):
            jnpr_pathfinder_mcp.server.feature_explorer._build_platform_catalog.cache_clear()
            result = await client.call_tool("product_keys")
            assert not result.structured_content.get('success')

        # simulate failure in building catalog
        with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer, "_build_platform_catalog", side_effect=Exception("boom")):
            with pytest.raises(ToolError):
                result = await client.call_tool("product_keys")

@pytest.mark.asyncio
async def test_product_keys_with_real_get():
    async with Client(mcp) as client:
        jnpr_pathfinder_mcp.server.feature_explorer._build_platform_catalog.cache_clear()
        result = await client.call_tool("product_keys")
        assert result.structured_content.get('success')
        assert result.structured_content.get('response')

def test_snake_returns_on_false():
    assert jnpr_pathfinder_mcp.server.feature_explorer._snake(False) == False
    assert jnpr_pathfinder_mcp.server.feature_explorer._snake("") == ""

def test_snake_snakes():
    assert jnpr_pathfinder_mcp.server.feature_explorer._snake(" A Long-Name With Many  Spaces ") == "a_long-name_with_many_spaces"

def test__get_pid_for_model():
    with mock.patch.object(jnpr_pathfinder_mcp.server.feature_explorer, "_build_platform_catalog", return_value={"mx10008": {"product_key": 11320008}}):
        assert jnpr_pathfinder_mcp.server.feature_explorer._get_pid_for_model("MX10008") == 11320008
        assert jnpr_pathfinder_mcp.server.feature_explorer._get_pid_for_model("MX10008-FAKE") == 11320008
        assert jnpr_pathfinder_mcp.server.feature_explorer._get_pid_for_model("MX10008-FAKE-AFO") == 11320008


