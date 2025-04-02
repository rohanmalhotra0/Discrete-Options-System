import numpy as np
from functools import wraps
from time import time

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
