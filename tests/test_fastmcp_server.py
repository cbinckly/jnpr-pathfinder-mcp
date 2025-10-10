import sys
from argparse import Namespace
from unittest import mock
from unittest.mock import Mock, patch

import pytest

from jnpr_pathfinder_mcp.server import pathfinder
from jnpr_pathfinder_mcp.server.pathfinder import mcp as server
from jnpr_pathfinder_mcp.__main__ import main
from jnpr_pathfinder_mcp.helpers import parse_args, run_cli


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
            run_cli("prog", server)


def test_run_cli_with_stdio_and_host_or_port():
    # This should raise a ValueError because host and port are not allowed with stdio transport.
    with pytest.raises(ValueError, match="host/port cannot be used with stdio transport"):
        with mock.patch(
            "jnpr_pathfinder_mcp.helpers.parse_args",
            return_value=Namespace(transport="stdio", host="localhost", port=8080),
        ):
            run_cli("prog", server)
        mock_run.assert_called_once_with(transport="http", host="localhost", port=8080)


@patch.object(server, "run")
def test_main_with_valid_stdio(mock_run):
    # Valid case for stdio
    with mock.patch(
        "jnpr_pathfinder_mcp.helpers.parse_args",
        return_value=Namespace(transport="stdio", host=None, port=None),
    ):
        main()
        mock_run.assert_called_once_with(transport="stdio")


@patch.object(server, "run")
def test_run_cli_with_valid_stdio(mock_run):
    # Valid case for stdio
    with mock.patch(
        "jnpr_pathfinder_mcp.helpers.parse_args",
        return_value=Namespace(transport="stdio", host=None, port=None),
    ):
        run_cli("prog", server)
        mock_run.assert_called_once_with(transport="stdio")


def test_run_cli_with_valid_http():
    # Valid case for http
    with mock.patch("jnpr_pathfinder_mcp.server.pathfinder.mcp.run") as mock_run:
        with mock.patch(
            "jnpr_pathfinder_mcp.helpers.parse_args",
            return_value=Namespace(transport="http", host="localhost", port=8080)
        ):
            run_cli("prog", server)
            mock_run.assert_called_once_with(transport="http", host="localhost", port=8080)


def test_run_invalid_transport():
    with mock.patch(
        "jnpr_pathfinder_mcp.helpers.parse_args",
        return_value=Namespace(transport="invalid", host="localhost", port=8080)
    ):
        with pytest.raises(ValueError, match="transport must be 'stdio' or 'http'"):
            run_cli("prog", server)


@patch.object(server, "mount")
@patch.object(server, "run")
def test_run_http_transport_with_host_and_port(mock_run, mock_mount):
    # Test with both host and port
    server.run(transport="http", host="127.0.0.1", port=8080)
    # Assertions for mcp.run method
    mock_run.assert_called_once_with(transport="http", host="127.0.0.1", port=8080)


@patch.object(server, "mount")
@patch.object(server, "run")
def test_run_http_transport_with_only_host(mock_run, mock_mount):
    # Test with only host
    server.run(transport="http", host="127.0.0.1")

    # Assertions for mcp.run method
    mock_run.assert_called_once_with(transport="http", host="127.0.0.1")


@patch.object(server, "mount")
@patch.object(server, "run")
def test_run_http_transport_with_only_port(mock_run, mock_mount):
    # Test with only port
    server.run(transport="http", port=8080)

    # Assertions for mcp.run method
    mock_run.assert_called_once_with(transport="http", port=8080)


@patch.object(server, "mount")
@patch.object(server, "run")
def test_run_http_transport_without_host_and_port(mock_run, mock_mount):
    # Test without host and port
    server.run(transport="http")

    # Assertions for mcp.run method
    mock_run.assert_called_once_with(transport="http")
