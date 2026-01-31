import httpx
import json
import asyncio
import sys

# TWSE Real-time API
BASE_URL = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp"

async def fetch_stock_data(symbol: str):
    """
    Fetch real-time stock data for a given symbol.
    Tries TSE first, then OTC.
    """
    # Try TSE first (most common)
    tse_key = f"tse_{symbol}.tw"
    otc_key = f"otc_{symbol}.tw"
    
    # We can request both at once to be efficient or one by one.
    # The API supports multiple ex_ch separated by pipe, but let's do simple requests.
    
    # Try TSE
    url = f"{BASE_URL}?ex_ch={tse_key}"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=10.0)
            data = resp.json()
            
            if data.get("msgArray") and len(data["msgArray"]) > 0:
                return _parse_stock_data(data["msgArray"][0])
            
            # If TSE empty, try OTC
            url_otc = f"{BASE_URL}?ex_ch={otc_key}"
            resp_otc = await client.get(url_otc, timeout=10.0)
            data_otc = resp_otc.json()
            
            if data_otc.get("msgArray") and len(data_otc["msgArray"]) > 0:
                return _parse_stock_data(data_otc["msgArray"][0])
                
            return {"error": "Stock symbol not found in TSE or OTC."}
            
    except Exception as e:
        return {"error": f"Network error: {str(e)}"}

async def fetch_market_index():
    """
    Fetch the TAIEX (Weighted Index).
    """
    key = "tse_t00.tw" # TAIEX
    otc_key = "otc_o00.tw" # OTC Index
    
    url = f"{BASE_URL}?ex_ch={key}|{otc_key}"
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=10.0)
            data = resp.json()
            
            results = {}
            if data.get("msgArray"):
                for item in data["msgArray"]:
                    parsed = _parse_stock_data(item)
                    if item["c"] == "t00":
                        results["TAIEX"] = parsed
                    elif item["c"] == "o00":
                        results["OTC_Index"] = parsed
            
            return results
    except Exception as e:
        return {"error": f"Network error: {str(e)}"}

def _parse_stock_data(item):
    """
    Parse the raw TWSE JSON item into a readable dictionary.
    Ref: http://jstutorial.medium.com/how-to-get-real-time-stock-data-from-twse-api-5e26306764
    """
    try:
        return {
            "symbol": item.get("c"),
            "name": item.get("n"),
            "fullname": item.get("nf"),
            "price": item.get("z", "-"), # Recent transaction price
            "open": item.get("o", "-"),
            "high": item.get("h", "-"),
            "low": item.get("l", "-"),
            "volume": item.get("v", "-"), # Total volume
            "time": item.get("t", "-"), # Time of last trade
            "best_bid_price": item.get("b", "_").split("_")[0],
            "best_ask_price": item.get("a", "_").split("_")[0],
            "yesterday_close": item.get("y", "-"),
            "change": _calculate_change(item.get("z"), item.get("y"))
        }
    except Exception as e:
        return {"raw": item, "parse_error": str(e)}

def _calculate_change(current, yesterday):
    if not current or not yesterday or current == "-" or yesterday == "-":
        return "-"
    try:
        c = float(current)
        y = float(yesterday)
        diff = c - y
        pct = (diff / y) * 100
        return f"{diff:.2f} ({pct:.2f}%)"
    except:
        return "-"

if __name__ == "__main__":
    # Test logic
    print(asyncio.run(fetch_stock_data("2330")))
