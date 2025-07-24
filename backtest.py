# backtest.py

import pandas as pd
import numpy as np
from improved_project.utils import calculate_stop_reward
from strategy import TradingStrategy
from logger import log

results = []
strategy = TradingStrategy()

data = pd.read_csv("eurusd_prices_multiip.csv", parse_dates=["timestamp"], index_col="timestamp")
data['status'] = np.where(data['open'] > data['close'], 'bearish', 'bullish')

# آماده‌سازی اندیس
timestamps = data.index.tolist()
total_profit = 0
win, loss = 0, 0

for i in range(100, len(data)):
    current_data = data.iloc[:i+1]
    strategy.update_legs(current_data)

    if len(strategy.legs) < 3:
        continue

    swing_type, is_swing = strategy.handle_swing(current_data)

    # فقط در صورتی که معامله انجام شود
    if strategy.true_position:
        entry_price = current_data.iloc[-1]['close']
        stop, reward = calculate_stop_reward(entry_price, strategy.fib_levels, swing_type)

        # شبیه‌سازی رسیدن قیمت به stop یا reward
        for j in range(i+1, min(i+50, len(data))):  # فقط 50 کندل بعدی بررسی می‌شود
            future = data.iloc[j]
            if swing_type == 'bullish':
                if future['low'] <= stop:
                    profit = stop - entry_price
                    loss += 1
                    break
                elif future['high'] >= reward:
                    profit = reward - entry_price
                    win += 1
                    break
            elif swing_type == 'bearish':
                if future['high'] >= stop:
                    profit = entry_price - stop
                    loss += 1
                    break
                elif future['low'] <= reward:
                    profit = entry_price - reward
                    win += 1
                    break
        else:
            profit = 0  # پوزیشن نامشخص

        total_profit += profit
        results.append({
            'entry_time': current_data.iloc[-1].name,
            'swing': swing_type,
            'profit': profit
        })
        
        strategy.reset_state()  # پاک کردن وضعیت برای ورود بعدی

print("\n=== Backtest Result ===")
print(f"✅ Win: {win}, ❌ Loss: {loss}")
print(f"📈 Total Profit: {round(total_profit, 5)}")
print(f"📊 Win Rate: {round((win/(win+loss))*100, 2)}%" if (win+loss) else "0%")

df_result = pd.DataFrame(results)
df_result.to_csv("backtest_results.csv", index=False)
