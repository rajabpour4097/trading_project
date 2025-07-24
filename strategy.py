# strategy.py
from get_data_multiip import get_live_data
from get_legs import get_legs
from swing import get_swing_points
from logger import log
from utils import calculate_stop_reward
from time import sleep

class TradingStrategy:
    def __init__(self):
        self.fib_levels = None
        self.true_position = False
        self.last_touched_705_up = None
        self.last_touched_705_down = None
        self.last_swing_type = None
        self.start_index = 0
        self.legs = []

    def update_legs(self, data):
        self.legs = get_legs(data[self.start_index:])
        if len(self.legs) > 2:
            self.legs = self.legs[-3:]

    def handle_swing(self, data):
        swing_type, is_swing = get_swing_points(data, self.legs)

        if not is_swing and self.fib_levels is None:
            self.reset_state()
            return

        if is_swing:
            self.last_swing_type = swing_type
            self.handle_entry_logic(data, swing_type)
        elif self.fib_levels is not None:
            self.continue_existing_fib(data)

    def handle_entry_logic(self, data, swing_type):
        # ادامه منطق ورود به پوزیشن (buy/sell)
        # مشابه کدی که قبلاً نوشتی ولی داخل متد جداگانه با ساختار مرتب‌تر
        pass  # تکمیل می‌کنم در مرحله بعد

    def manage_position(self, data, swing_type):
        live = get_live_data()
        entry = data.iloc[-1]['close']
        stop, reward = calculate_stop_reward(entry, self.fib_levels, swing_type)

        log(f"Entry: {entry}, Stop: {stop}, Reward: {reward}", color='cyan')
        
        while True:
            live = get_live_data()
            if swing_type == 'bullish' and (live['high'] >= reward or live['low'] <= stop):
                break
            if swing_type == 'bearish' and (live['low'] <= reward or live['high'] >= stop):
                break
            sleep(0.3)

        self.reset_state()

    def reset_state(self):
        self.fib_levels = None
        self.true_position = False
        self.last_touched_705_up = None
        self.last_touched_705_down = None
        self.legs = self.legs[-2:] if len(self.legs) >= 2 else []
        if self.legs:
            self.start_index = self.legs[0]['start']
