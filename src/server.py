"""
Taiwan Stock MCP Server using FastMCP.
Supports both STDIO and Streamable HTTP transport modes.
"""
import sys
import os
import argparse
import asyncio

# Add current directory to path so we can import 'logic'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastmcp import FastMCP
import logic

# Initialize FastMCP
mcp = FastMCP("mcp-tw-stock")

@mcp.tool()
async def get_stock_price(symbol: str) -> str:
    """
    Get real-time stock price and info for a Taiwan stock (TSE/OTC).
    Args:
        symbol: Stock symbol (e.g., '2330' for TSMC, '0050' for ETF).
    """
    data = await logic.fetch_stock_data(symbol)
    return str(data)

@mcp.tool()
async def get_market_index() -> str:
    """
    Get the current status of the Taiwan Weighted Index (TAIEX) and OTC Index.
    """
    data = await logic.fetch_market_index()
    return str(data)

def main():
    parser = argparse.ArgumentParser(description="Taiwan Stock MCP Server")
    parser.add_argument("--mode", choices=["stdio", "http"], default="stdio", help="Transport mode")
    parser.add_argument("--port", type=int, default=8000, help="HTTP port (only for http mode)")
    args = parser.parse_args()

    if args.mode == "stdio":
        mcp.run()
    else:
        print(f"Starting FastMCP in streamable-http mode on port {args.port}...", file=sys.stderr)
        mcp.run(
            transport="streamable-http",
            host="0.0.0.0",
            port=args.port,
            path="/mcp"
        )

if __name__ == "__main__":
    main()
