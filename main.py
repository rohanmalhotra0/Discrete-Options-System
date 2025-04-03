from alpaca_connector import get_option_data, store_data_in_csv
from binomial_model import american_slow_tree, build_binomial_tree_json
import schedule
import time as t
import datetime
import json

def run_pricing_job(symbol: str = "SPY"):
    print(f"\nRunning pricing job for {symbol} at {datetime.datetime.now()}")

    # Step 1: Get option data
    option_data = get_option_data(symbol)
    
    # Step 2: Extract relevant values
    S0 = option_data["S0"]
    K = option_data["K"]
    T = option_data["T"]
    opttype = option_data["opttype"]

    # Step 3: Parameters for binomial model
    r = 0.06      # Risk-free rate (annual)
    N = 3         # Number of time steps (for demonstration; increase for better accuracy)
    u = 1.1       # Up-factor
    d = 1 / u     # Down-factor (ensures a recombining tree)

    # Step 4: Compute fair price
    fair_price = american_slow_tree(K, T, S0, r, N, u, d, opttype=opttype)
    option_data["fair_price"] = round(fair_price, 4)
    print("American Option Fair Price:", fair_price)

    # Step 5: Log to console and CSV
    print(f"Market Price: {option_data['market_price']}")
    print(f"Fair Price:   {option_data['fair_price']}")
    store_data_in_csv(option_data, filename=f"{symbol}_option_data.csv")

    # Step 6: (Optional) Export binomial tree to JSON
    tree_data = build_binomial_tree_json(S0, u, d, N)
    with open(f"{symbol}_binomial_tree.json", "w") as f:
        json.dump(tree_data, f, indent=2)
    print(f"Binomial tree JSON exported to {symbol}_binomial_tree.json")


if __name__ == "__main__":
    # Immediate run (useful for testing)
    run_pricing_job("SPY")

    # Schedule job for daily execution at 09:31 AM
    schedule.every().day.at("09:31").do(run_pricing_job, symbol="SPY")

    print("Scheduler started. Waiting for 09:31 to run the update job...\n")
    while True:
        schedule.run_pending()
        t.sleep(1)
