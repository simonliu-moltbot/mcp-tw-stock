import sys
import os
import asyncio
import traceback

# Import hack for logic
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    import mcp.types as types
    from mcp.server.stdio import stdio_server
except ImportError:
    sys.stderr.write("Critical: 'mcp' package not found. Install it via 'pip install mcp'.\n")
    sys.exit(1)

# Logic imports
try:
    from logic import fetch_stock_data, fetch_market_index
except ImportError as e:
    sys.stderr.write(f"Warning: Failed to import logic: {e}\n")
    # Dummy fallbacks
    async def fetch_stock_data(symbol): return {"error": "Logic import failed"}
    async def fetch_market_index(): return {"error": "Logic import failed"}

# Initialize Server
server = Server("mcp-tw-stock")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_stock_price",
            description="Get real-time stock price and info for a Taiwan stock (TSE/OTC).",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., '2330' for TSMC, '0050' for ETF)"
                    }
                },
                "required": ["symbol"]
            },
        ),
        types.Tool(
            name="get_market_index",
            description="Get the current status of the Taiwan Weighted Index (TAIEX) and OTC Index.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if not arguments:
        arguments = {}

    try:
        if name == "get_stock_price":
            symbol = arguments.get("symbol")
            if not symbol:
                return [types.TextContent(type="text", text="Error: 'symbol' is required.")]
            
            data = await fetch_stock_data(symbol)
            return [types.TextContent(type="text", text=str(data))]

        elif name == "get_market_index":
            data = await fetch_market_index()
            return [types.TextContent(type="text", text=str(data))]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        sys.stderr.write(f"Error executing tool {name}: {e}\n")
        traceback.print_exc(file=sys.stderr)
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    try:
        sys.stderr.write("Starting mcp-tw-stock server...\n")
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="mcp-tw-stock",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    except Exception as e:
        sys.stderr.write(f"Server crashed: {e}\n")
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
