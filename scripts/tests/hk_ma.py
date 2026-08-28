from panda_backtest.api.api import *
from panda_backtest.api.stock_hk_api import *
import tqx_data


def initialize(context):
    # The backtest node you used is an HK stock backtest node (market=hk),
    # so we must trade HK symbols, not US (.NB) symbols.
    # Here we switch to Tencent as an example.
    context.symbol = "0700.HK"  # HK stock symbol instead of AAPL.NB

    # Parameters
    context.short_window = 5
    context.long_window = 20
    context.max_position_ratio = 0.9  # use up to 90% of cash when opening

    # State holders (no globals allowed)
    context.closes = []  # rolling close prices
    context.last_date = None  # to avoid double-counting closes within same day


def _update_closes(context, bar):
    """Maintain close-price window for MA calculation.

    Guard by trade_date so we only append one close per day.
    """
    trade_date = getattr(bar, "trade_date", None)

    # If trade_date is unavailable, just append; otherwise ensure one close per day
    if trade_date is not None:
        if context.last_date == trade_date:
            return
        context.last_date = trade_date

    context.closes.append(float(bar.close))

    # Keep only necessary window length
    max_len = max(context.short_window, context.long_window)
    if len(context.closes) > max_len:
        context.closes = context.closes[-max_len:]


def _calc_ma(series, window):
    if len(series) < window:
        return None
    return sum(series[-window:]) / window


def _get_position(account, symbol):
    if account is None:
        return None
    return account.positions.get(symbol)


def _position_size_by_cash(account, price, max_ratio):
    """Risk-aware sizing: use fraction of available cash, round down to int."""
    if account is None or price is None or price <= 0:
        return 0
    cash_to_use = account.cash * max_ratio
    qty = int(cash_to_use // price)
    return max(qty, 0)


def handle_data(context, data):
    symbol = context.symbol

    # Protect against missing bar (e.g., symbol not in this market or trading halted)
    try:
        bar = data[symbol]
    except Exception:
        return

    # Basic data validation
    if bar is None:
        return
    if bar.close is None or bar.close <= 0:
        return

    # Update rolling close list
    _update_closes(context, bar)

    # Need enough history to compute long MA
    if len(context.closes) < context.long_window:
        return

    short_ma = _calc_ma(context.closes, context.short_window)
    long_ma = _calc_ma(context.closes, context.long_window)
    if short_ma is None or long_ma is None:
        return

    account = context.stock_account_dict.get(context.account)
    position = _get_position(account, symbol)
    quantity = position.quantity if position else 0

    # Golden-cross: short MA crosses above long MA, open / increase position
    if short_ma > long_ma:
        # If no position, open a new one sized by available cash
        if quantity == 0:
            price = float(bar.close)
            buy_qty = _position_size_by_cash(account, price, context.max_position_ratio)
            if buy_qty > 0:
                order_shares(context.account, symbol, buy_qty, style=MarketOrderStyle)

    # Death-cross: short MA below long MA, fully exit
    elif short_ma < long_ma and position and position.sellable > 0:
        order_shares(context.account, symbol, -position.sellable, style=MarketOrderStyle)
