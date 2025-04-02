from alpaca_connector import get_option_data, store_data_in_csv
from binomial_model import american_slow_tree, update_daily
import schedule
import time as t
import datetime
from datetime import datetime, timedelta
from functools import wraps
import numpy as np



if __name__ == "__main__":
    # Retrieve option data for the symbol "SPY"
    option_data = get_option_data("SPY")
    store_data_in_csv(option_data)
    
    # Extract parameters for pricing
    S0 = option_data["S0"]
    K = option_data["K"]
    T = option_data["T"]
    opttype = option_data["opttype"]
    
    # Set additional parameters for the binomial model
    r = 0.06      # Risk-free rate (annual)
    N = 3         # Number of time steps (for demonstration; increase for better accuracy)
    u = 1.1       # Up-factor
    d = 1 / u     # Down-factor (ensures a recombining tree)
    
    # Compute the American option fair price using the binomial model
    fair_price = american_slow_tree(K, T, S0, r, N, u, d, opttype=opttype)
    print("American Option Fair Price:", fair_price)
    
    # Schedule the job to run at 09:31 every day
    # Schedule the update_daily() job to run every day at 09:31.
    schedule.every().day.at("09:31").do(update_daily)   
    print("Scheduler started. Waiting for 09:31 to run the update job...")
    while True:
        schedule.run_pending()
        t.sleep(1)
