import numpy as np
from functools import wraps
from time import time
import matplotlib.pyplot as plt
import json
from datetime import date, timedelta
import schedule
import time as t  # renamed to avoid conflict with time() above

def timing(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        ts = time()
        result = f(*args, **kwargs)
        te = time()
        print("Function %r took: %2.4f sec" % (f.__name__, te - ts))
        return result
    return wrap

@timing
def american_slow_tree(K, T, S0, r, N, u, d, opttype='P'):
    """
    Computes the American option price using a binomial tree.
    
    Parameters:
        K: strike price
        T: time to maturity (years)
        S0: initial stock price
        r: annual risk-free rate
        N: number of time steps
        u: up-factor per step
        d: down-factor per step (should be 1/u for a recombining tree)
        opttype: 'C' for call, 'P' for put
    
    Returns:
        Fair price of the American option (float)
    """
    dt = T / N
    q = (np.exp(r * dt) - d) / (u - d)
    disc = np.exp(-r * dt)
    
    # Initialize stock prices at maturity
    S = np.zeros(N + 1)
    for j in range(N + 1):
        S[j] = S0 * (u ** j) * (d ** (N - j))
    
    # Option payoff at maturity
    C = np.zeros(N + 1)
    for j in range(N + 1):
        if opttype == 'P':
            C[j] = max(0, K - S[j])
        else:
            C[j] = max(0, S[j] - K)
    
    # Backward recursion through the tree
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            stock_price = S0 * (u ** j) * (d ** (i - j))
            C[j] = disc * (q * C[j + 1] + (1 - q) * C[j])
            if opttype == 'P':
                C[j] = max(C[j], K - stock_price)
            else:
                C[j] = max(C[j], stock_price - K)
    
    return C[0]

def build_binomial_tree_json(S0, u, d, N):
    """
    Recursively builds a JSON structure representing the binomial tree.
    
    Each node includes:
      - id: a unique node identifier
      - time_step: the current step in the tree
      - price: the computed stock price at that node
      - children: a list of child nodes (empty if at final step)
    """
    def node(time_step, j):
        price = S0 * (u ** j) * (d ** (time_step - j))
        node_id = f"node_{time_step}_{j}"
        children = []
        if time_step < N:
            children.append(node(time_step + 1, j))
            children.append(node(time_step + 1, j + 1))
        return {"id": node_id, "time_step": time_step, "price": price, "children": children}
    
    return node(0, 0)

def update_daily():
    """
    This function updates the option data and binomial tree JSON.
    It:
      - Computes the remaining time to expiry T (in years) based on a fixed expiry date.
      - Calculates the American option fair price.
      - Constructs a JSON representation of the binomial tree.
      - Exports the JSON to a file.
      - (Optionally) Plots the tree for visual reference.
    """
    # --- Configuration & Dynamic Parameters ---
    S0 = 100.0    # Current underlying stock price (replace with live data as needed)
    K = 100.0     # Strike price
    r = 0.06      # Annual risk-free rate
    N = 5         # Number of time steps (can be increased for finer resolution)
    u = 1.1       # Up-factor per step
    d = 1 / u     # Down-factor (to ensure a recombining tree)
    opttype = 'C' # Option type: 'C' for Call (or 'P' for Put)
    
    # --- Compute Time to Expiry ---
    # Set a fixed expiry date (for example, one year from when the option was initiated)
    expiry_date = date(2026, 4, 2)  # Replace with your actual fixed expiry date
    today = date.today()
    T = (expiry_date - today).days / 365.0
    print(f"Today's date: {today}, Time to expiry T: {T:.4f} years")
    
    # --- Calculate Option Price ---
    option_price = american_slow_tree(K, T, S0, r, N, u, d, opttype=opttype)
    print("American Option Fair Price:", option_price)
    
    # --- Build and Export JSON for Binomial Tree ---
    tree_data = build_binomial_tree_json(S0, u, d, N)
    with open("binomial_tree.json", "w") as f:
        json.dump(tree_data, f, indent=2)
    print("Exported binomial_tree.json")
    
   




