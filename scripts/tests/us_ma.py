from panda_backtest.api.api import *
from panda_backtest.api.stock_us_api import *
import tqx_data


def initialize(context):
    """Initialize US stock moving-average strategy for Tesla.

    - Symbol: TSLA.NB
    - Fast MA: 1-day, Slow MA: 12-day
    - Entry: fast MA > slow MA and no position
    - Exit: fast MA < slow MA and have position
    """
    # Account ID (set according to your backtest configuration)
    context.account = "15032863"

    # Trading universe: use Tesla only
    context.stock_universe = ["TSLA.NB"]

    # Moving average parameters
    context.fast_window = 4
    context.slow_window = 12

    # Risk management
    context.max_position_ratio = 0.9  # max 90% of total equity in one stock

    # Cache for signals / logs
    context.today_trades = []

    # Maintain close history manually to avoid relying on bar.close_array
    context.close_history = {symbol: [] for symbol in context.stock_universe}


def before_trading(context):
    """Daily pre-open hook: reset intraday state and optionally log account info."""
    context.today_trades = []

    account = context.stock_account_dict.get(context.account)
    if account is not None:
        print(
            f"[US before_trading] date={context.now}, total_value={account.total_value:.2f}, cash={account.cash:.2f}"
        )


def _compute_ma(series, window):
    """Simple helper to compute moving average from a list-like of prices."""
    if series is None:
        return None
    if len(series) < window:
        return None
    # Use the last `window` values
    window_vals = series[-window:]
    # Filter out non-positive values just in case
    window_vals = [x for x in window_vals if x is not None and x > 0]
    if len(window_vals) < window:
        return None
    return sum(window_vals) / float(window)


def handle_data(context, data):
    """Main bar handler implementing a moving-average strategy on Tesla.

    Optimizations / robustness:
      - Maintain our own close-history in context.close_history
      - Do not rely on bar.close_array
      - Minimal repeated lookups and clear logging when trades happen
    """
    account = context.stock_account_dict.get(context.account)
    if account is None:
        return

    for symbol in context.stock_universe:
        # Defensive check: ensure symbol exists in data and bar is not None
        try:
            bar = data[symbol]
        except (KeyError, TypeError, AttributeError):
            continue
        if bar is None:
            # No bar for this symbol at this time; skip safely
            continue

        # Update and maintain our own close history
        # Guard against missing/None close field
        close_val = getattr(bar, "close", None)
        if close_val is None:
            continue

        close_price = float(close_val)
        if close_price <= 0:
            continue

        history = context.close_history.setdefault(symbol, [])
        history.append(close_price)

        # Limit history length to avoid unbounded growth
        max_len = max(context.fast_window, context.slow_window) * 5
        if len(history) > max_len:
            history[:] = history[-max_len:]

        # Need at least slow_window data points for MA calculation
        if len(history) < context.slow_window:
            continue

        # Compute current moving averages
        curr_fast = _compute_ma(history, context.fast_window)
        curr_slow = _compute_ma(history, context.slow_window)

        if curr_fast is None or curr_slow is None:
            continue

        # Current position in this symbol (if any)
        position = account.positions.get(symbol)
        quantity = 0 if position is None else position.quantity
        sellable = 0 if position is None else position.sellable

        # Rules:
        #   - If fast MA > slow MA and no position -> open long
        #   - If fast MA < slow MA and have position -> close position
        should_buy = curr_fast > curr_slow and quantity == 0
        should_sell = curr_fast < curr_slow and quantity > 0 and sellable > 0

        if should_buy:
            cash = account.cash
            if cash <= 0:
                continue

            max_invest_cash = cash * context.max_position_ratio
            buy_qty = int(max_invest_cash // close_price)
            if buy_qty <= 0:
                continue

            order_shares(context.account, symbol, buy_qty, style=MarketOrderStyle)
            context.today_trades.append(
                {
                    "symbol": symbol,
                    "side": "BUY",
                    "qty": buy_qty,
                    "price": close_price,
                    "fast_ma": curr_fast,
                    "slow_ma": curr_slow,
                }
            )

        elif should_sell:
            order_shares(context.account, symbol, -sellable, style=MarketOrderStyle)
            context.today_trades.append(
                {
                    "symbol": symbol,
                    "side": "SELL",
                    "qty": sellable,
                    "price": close_price,
                    "fast_ma": curr_fast,
                    "slow_ma": curr_slow,
                }
            )


def after_trading(context):
    """Daily post-close hook: summarize trades and account status."""
    account = context.stock_account_dict.get(context.account)
    if account is None:
        return

    print(
        f"[US after_trading] date={context.now}, total_value={account.total_value:.2f}, cash={account.cash:.2f}"
    )

    if context.today_trades:
        print("Today's MA trades:")
        for t in context.today_trades:
            print(
                f"  {t['symbol']} {t['side']} {t['qty']} @ {t['price']:.2f} "
                f"(fast={t['fast_ma']:.2f}, slow={t['slow_ma']:.2f})"
            )
    else:
        print("No trades today.")
