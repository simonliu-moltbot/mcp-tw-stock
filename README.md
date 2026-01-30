# MCP Taiwan Stock Helper (mcp-tw-stock)

A Model Context Protocol (MCP) server that provides real-time stock information from the Taiwan Stock Exchange (TWSE) and Taipei Exchange (TPEx).

## 🇹🇼 Features
- **Real-time Price**: Get current price, change, and percentage for any TW stock (e.g., TSMC 2330).
- **Market Index**: Check the TAIEX (Weighted Index) status using `taiex`.
- **Zero Config**: Uses public APIs (mis.twse.com.tw), no API key required.

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/mcp-tw-stock.git
   cd mcp-tw-stock
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🛠 Configuration

### Claude Desktop
Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tw-stock": {
      "command": "/absolute/path/to/mcp-tw-stock/.venv/bin/python",
      "args": [
        "/absolute/path/to/mcp-tw-stock/src/server.py"
      ]
    }
  }
}
```

### 🛠 Dive Configuration
- **Type**: `stdio`
- **Command**: `/absolute/path/to/mcp-tw-stock/.venv/bin/python`
- **Args**: `/absolute/path/to/mcp-tw-stock/src/server.py`

## 🧩 Tools

### `get_stock_price`
Get stock information.
- `symbol` (string): The stock code (e.g., "2330", "0050") or "taiex" for the market index.

## License
MIT
