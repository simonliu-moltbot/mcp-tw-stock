import sys
import os
import asyncio
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server

# Import Hack for local execution
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from logic import get_stock_price

server = Server("mcp-tw-stock")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_stock_price",
            description="Get real-time stock price and info from Taiwan Stock Exchange (TWSE/TPEx). Supports stock code (e.g. '2330') or 'taiex' for market index.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., '2330', '0050', 'taiex')",
                    }
                },
                "required": ["symbol"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name == "get_stock_price":
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Error: Missing 'symbol' argument")]
        
        data = get_stock_price(symbol)
        
        if "error" in data:
             return [types.TextContent(type="text", text=f"Error: {data['error']}")]

        # Format output nicely
        text = (
            f"📈 Stock: {data['name']} ({data['symbol']})\n"
            f"💰 Price: {data['price']} (Change: {data['change']} / {data['change_percent']})\n"
            f"📊 OHLC: O:{data['open']} H:{data['high']} L:{data['low']}\n"
            f"📦 Volume: {data['volume']} lots\n"
            f"⏰ Time: {data['time']}"
        )
        return [types.TextContent(type="text", text=text)]

    raise ValueError(f"Unknown tool: {name}")

async def main():
    # Run the server using stdin/stdout streams
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

if __name__ == "__main__":
    asyncio.run(main())
