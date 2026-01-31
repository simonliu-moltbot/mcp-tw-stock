# Taiwan Stock Market (TWSE) MCP Server

This is a Model Context Protocol (MCP) server that provides real-time stock data from the Taiwan Stock Exchange (TWSE).

## Features
- **Real-time Prices**: Fetch current price, bid/ask, and volume for any TSE/OTC stock.
- **Market Index**: Check the TAIEX (Weighted Index) and OTC Index status.
- **No API Key Required**: Uses public endpoints from `mis.twse.com.tw`.

## Setup

### Prerequisites
- Python 3.10+
- `pip`

### Installation
1. Clone this repository.
2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Claude Desktop
Add this to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "tw-stock": {
      "command": "/absolute/path/to/project/.venv/bin/python",
      "args": [
        "/absolute/path/to/project/src/server.py"
      ]
    }
  }
}
```

### Dive
- **Type**: `stdio`
- **Command**: `/absolute/path/to/project/.venv/bin/python`
- **Args**: `/absolute/path/to/project/src/server.py`

## Tools
- `get_stock_price(symbol)`: Get real-time data for a stock (e.g., "2330").
- `get_market_index()`: Get TAIEX and OTC index status.
