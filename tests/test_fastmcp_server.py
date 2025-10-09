import sys
from argparse import Namespace
from unittest import mock
from unittest.mock import Mock, patch

import pytest

from jnpr_pathfinder_mcp import server
from jnpr_pathfinder_mcp.__main__ import main, parse_args, run_cli


def test_default_transport():
    test_args = ["jnpr_pathfinder_mcp"]
    with patch.object(sys, "argv", test_args):
        args = parse_args()
        assert args.transport == "stdio"
        assert args.host is None
        assert args.port is None


def test_http_transport():
    test_args = [
        "jnpr_pathfinder_mcp",
        "--transport",
        "http",
        "--host",
        "example.com",
        "--port",
        "8080",
    ]
    with patch.object(sys, "argv", test_args):
        args = parse_args()
        assert args.transport == "http"
        assert args.host == "example.com"
        assert args.port == 8080


def test_invalid_transport_combination():
    test_args = [
        "jnpr_pathfinder_mcp",
        "--transport",
        "stdio",
        "--host",
        "example.com",
        "--port",
        "8080",
    ]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(ValueError):
            args = parse_args()
            run_cli(args)


def test_run_cli_with_stdio_and_host_or_port():
    # This should raise a ValueError because host and port are not allowed with stdio transport.
    with pytest.raises(ValueError, match="host/port cannot be used with stdio transport"):
        args = Namespace(transport="stdio", host="localhost", port=8080)
        run_cli(args)


def test_main_with_valid_stdio():
    # Valid case for stdio
    with mock.patch("jnpr_pathfinder_mcp.server.run") as mock_run:
        with mock.patch(
            "jnpr_pathfinder_mcp.__main__.parse_args",
            return_value=Namespace(transport="stdio", host=None, port=None),
        ):
            main()
            mock_run.assert_called_once_with(transport="stdio", host=None, port=None)


def test_run_cli_with_valid_stdio():
    # Valid case for stdio
    with mock.patch("jnpr_pathfinder_mcp.server.run") as mock_run:
        args = Namespace(transport="stdio", host=None, port=None)
        run_cli(args)
        mock_run.assert_called_once_with(transport="stdio", host=None, port=None)


def test_run_cli_with_valid_http():
    # Valid case for http
    with mock.patch("jnpr_pathfinder_mcp.server.run") as mock_run:
        args = Namespace(transport="http", host="localhost", port=8080)
        run_cli(args)
        mock_run.assert_called_once_with(transport="http", host="localhost", port=8080)


def test_run_invalid_transport():
    with pytest.raises(ValueError, match="transport must be 'stdio' or 'http'"):
        server.run(transport="invalid")


def test_run_http_mounts_and_run_called(monkeypatch):
    # Replace the module mcp with a Mock
    fake_mcp = Mock()
    # mount should return None (or whatever your real mcp returns)
    fake_mcp.mount.return_value = None
    fake_mcp.run.return_value = None

    monkeypatch.setattr(server, "mcp", fake_mcp)

    # call the run function with http transport and custom host/port
    server.run(transport="http", host="127.0.0.1", port=12345)

    # check mount calls contain the expected prefixes and objects
    # mount was likely called 3 times; check each call args
    assert fake_mcp.mount.call_count == 3

    # simpler: assert mount called with those modules and prefixes (order matters)
    fake_mcp.mount.assert_any_call(server.hct_mcp, prefix="juniper_hardware_compatibility_tool")
    fake_mcp.mount.assert_any_call(server.cli_explorer_mcp, prefix="juniper_cli_explorer")
    fake_mcp.mount.assert_any_call(server.feature_explorer_mcp, prefix="juniper_feature_explorer")

    # verify run was called with kwargs
    fake_mcp.run.assert_called_once_with(transport="http", host="127.0.0.1", port=12345)


def test_run_stdio_disallows_host_or_port(monkeypatch):
    fake_mcp = Mock()
    monkeypatch.setattr(server, "mcp", fake_mcp)

    # stdio with host should raise ValueError
    try:
        server.run(transport="stdio", host="127.0.0.1")
        raised = False
    except ValueError:
        raised = True
    assert raised

    # stdio with port should raise ValueError
    try:
        server.run(transport="stdio", port=9999)
        raised2 = False
    except ValueError:
        raised2 = True
    assert raised2

    # plain stdio call should call mcp.run with transport stdio
    server.run(transport="stdio")
    fake_mcp.run.assert_called_with(transport="stdio")


@patch.object(server.mcp, "mount")
@patch.object(server.mcp, "run")
def test_run_http_transport_with_host_and_port(mock_run, mock_mount):
    # Test with both host and port
    server.run(transport="http", host="127.0.0.1", port=8080)
    # Assertions for mcp.run method
    mock_run.assert_called_once_with(transport="http", host="127.0.0.1", port=8080)


@patch.object(server.mcp, "mount")
@patch.object(server.mcp, "run")
def test_run_http_transport_with_only_host(mock_run, mock_mount):
    # Test with only host
    server.run(transport="http", host="127.0.0.1")

    # Assertions for mcp.run method
    mock_run.assert_called_once_with(transport="http", host="127.0.0.1")


@patch.object(server.mcp, "mount")
@patch.object(server.mcp, "run")
def test_run_http_transport_with_only_port(mock_run, mock_mount):
    # Test with only port
    server.run(transport="http", port=8080)

    # Assertions for mcp.run method
    mock_run.assert_called_once_with(transport="http", port=8080)


@patch.object(server.mcp, "mount")
@patch.object(server.mcp, "run")
def test_run_http_transport_without_host_and_port(mock_run, mock_mount):
    # Test without host and port
    server.run(transport="http")

    # Assertions for mcp.run method
    mock_run.assert_called_once_with(transport="http")
