import httpx
import json
import sys
from typing import Dict, Any, Optional

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def _fetch_data(ex_ch: str) -> Optional[Dict[str, Any]]:
    url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={ex_ch}&json=1&delay=0"
    try:
        response = httpx.get(url, headers={"User-Agent": USER_AGENT}, timeout=10.0, verify=False)
        response.raise_for_status()
        data = response.json()
        
        if "msgArray" in data and len(data["msgArray"]) > 0:
            return data["msgArray"][0]
        return None
    except Exception as e:
        sys.stderr.write(f"Error fetching {ex_ch}: {e}\n")
        return None

def get_stock_price(symbol: str) -> Dict[str, Any]:
    """
    Get real-time stock info from TWSE/TPEx.
    Symbol can be '2330' (defaults to TSE) or 'tse_2330.tw'.
    """
    # 1. Handle TAIEX special case
    if symbol.lower() in ["taiex", "tse", "大盤"]:
        symbol = "t00"

    # 2. Normalize symbol
    target_ex_ch = []
    if "_" in symbol:
         target_ex_ch.append(symbol) # Already formatted
    else:
        # Try TSE first, then OTC
        target_ex_ch.append(f"tse_{symbol}.tw")
        target_ex_ch.append(f"otc_{symbol}.tw")

    for ch in target_ex_ch:
        raw_data = _fetch_data(ch)
        if raw_data:
            # Parse readable fields
            # Keys: 
            # n: Name
            # z: Current Price
            # tv: Total Volume (shares? usually lots)
            # v: Volume (lots)
            # o: Open
            # h: High
            # l: Low
            # y: Yesterday Close
            # t: Time
            
            try:
                name = raw_data.get("n", "Unknown")
                price = raw_data.get("z", "-")
                if price == "-": price = raw_data.get("b", "-").split("_")[0] # Bid price if no trade
                
                change = "0.0"
                pct_change = "0.0%"
                
                try:
                    curr = float(price)
                    prev = float(raw_data.get("y", 0))
                    diff = curr - prev
                    change = f"{diff:.2f}"
                    pct_change = f"{(diff/prev)*100:.2f}%"
                except:
                    pass

                return {
                    "symbol": raw_data.get("c", symbol),
                    "name": name,
                    "price": price,
                    "change": change,
                    "change_percent": pct_change,
                    "open": raw_data.get("o", "-"),
                    "high": raw_data.get("h", "-"),
                    "low": raw_data.get("l", "-"),
                    "volume": raw_data.get("v", "0"),
                    "time": raw_data.get("t", "-"),
                    "raw_code": ch
                }
            except Exception as e:
                sys.stderr.write(f"Error parsing data: {e}\n")
                continue
    
    return {"error": f"Stock symbol {symbol} not found or no data available."}

if __name__ == "__main__":
    # Test
    print(get_stock_price("2330"))
    print(get_stock_price("t00"))
