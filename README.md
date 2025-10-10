# Juniper Pathfinder Model Context Protocol Server

This MCP Server allows a model to work with the data behind
the tools in the Juniper Pathfinder site (https://apps.juniper.net).

It contains tools in three namespaces:

- `juniper_hardware_compatibility_tool_`: Hardware Compatibility Tool
- `juniper_feature_explorer_`: Feature Explorer
- `juniper_cli_explorer_`: CLI Explorer

## Running the MCP Server

This MCP server is actually a composition of three MCP servers:

- `jnpr_pathfinder_mcp.server.hct`
- `jnpr_pathfinder_mcp.server.feature_explorer`
- `jnpr_pathfinder_mcp.server.cli_explorer`

with a final MCP server that mounts the others to present them all at once:

- `jnpr_pathfinder_mcp.pathfinder`

all built using [FastMCP](https://gofastmcp.com/getting-started/quickstart#run-the-server)
and support running over stdio or streamable http.

### Running the Full Server

To run all three components with a single interface, use 
[`uv`](https://docs.astral.sh/uv/getting-started/installation/)
for the simplest approach:

```bash
$ uv run --with jnpr_pathfinder_mcp -m jnpr_pathfinder_mcp --transport http --port 8888
```

This will expose tools for all supported pathfinder apps over streaming http on port 8888.

### Running a Single Server

To run all three components with a single interface, use 
[`uv`](https://docs.astral.sh/uv/getting-started/installation/)
for the simplest approach:

```bash
$ uv run --with jnpr_pathfinder_mcp -m jnpr_pathfinder_mcp.server.hct
```

This will expose tools for the Hardware Compatibility Tool only.

## Running with Docker

It may be even easier to run the MCP server using Docker:

```bash
$ docker run --rm -i -p 8888:8888 cbinckly/jnpr_pathfinder_mcp:main
```

By default we run a streaming http server on port 8888.  You can control
the command line by passing your own command and, for example, starting
only the cli_exporer server.

```bash
$ docker run --rm -i -p 8888:8888 cbinckly/jnpr_pathfinder_mcp:main \
    uv run -m jnpr_pathfinder_mcp.server.hct --transport stdio
```
