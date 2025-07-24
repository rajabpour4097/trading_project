# utils.py
def calculate_stop_reward(entry, fib_levels, direction):
    if direction == 'bullish':
        stop = fib_levels['1.0'] if abs(fib_levels['0.9'] - entry) * 10000 < 2 else fib_levels['0.9']
        reward = entry + 2 * abs(entry - stop)
    else:
        stop = fib_levels['1.0'] if abs(fib_levels['0.9'] - entry) * 10000 < 2 else fib_levels['0.9']
        reward = entry - 2 * abs(entry - stop)

    return stop, reward
