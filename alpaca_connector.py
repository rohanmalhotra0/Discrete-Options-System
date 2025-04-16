import pandas as pd
import datetime
import os
from alpaca_trade_api.rest import REST

# Alpaca Credentials (in production, store these securely in environment variables)
api_key = ""
secret_key = ""
BASE_URL = "https://paper-api.alpaca.markets/v2"  # Paper trading URL

# Create Alpaca API instance
api = REST(api_key, secret_key, BASE_URL)

def get_option_data(symbol: str) -> dict:
    """
    Fetch option details for a given symbol, focusing on a 1-year expiry call.
    
    Currently, the option chain details are mock values.
    
    Returns:
        A dictionary with:
          - S0: underlying stock price (float)
          - K: strike price (float)
          - T: time to maturity in years (float)
          - opttype: 'C' for call or 'P' for put (str)
          - market_price: option's market price (float)
          - expiry_date: the computed expiry date (str)
          - timestamp: time of retrieval (datetime)
    """
    # Calculate expiry date ~1 year from today
    expiry_date = datetime.date.today() + datetime.timedelta(days=365)
    expiry_str = expiry_date.strftime("%Y-%m-%d")
    
    # Retrieve the underlying stock price using Alpaca's API
    try:
        # Fetch the most recent 1-minute bar using the API instance
        bars = api.get_bars(symbol, "1Min", limit=1)
        # 'bars.df' is a DataFrame; get the close price from the first row
        underlying_price = bars.df['close'].iloc[0]
    except Exception as e:
        print("Error retrieving underlying price:", e)
        underlying_price = 100.0  # Fallback value if retrieval fails
    
    # Option chain retrieval (mock values for now)
    strike_price = 100.0
    time_to_expiry = 1.0  # 1 year
    option_type = "C"
    option_market_price = 5.0

    option_data = {
        "S0": underlying_price,
        "K": strike_price,
        "T": time_to_expiry,
        "opttype": option_type,
        "market_price": option_market_price,
        "expiry_date": expiry_str,
        "timestamp": datetime.datetime.now()
    }
    return option_data

def store_data_in_csv(option_data: dict, filename: str = "option_data.csv"):
    """
    Store the option data in a CSV file.
    
    Args:
        option_data (dict): The option data to store.
        filename (str): The name of the CSV file.
    """
    df = pd.DataFrame([option_data])
    if not os.path.exists(filename):
        df.to_csv(filename, mode='w', header=True, index=False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)
    print(f"Data stored in {filename}")
