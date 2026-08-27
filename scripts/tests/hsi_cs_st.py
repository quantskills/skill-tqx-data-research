from panda_backtest.api.api import *
from panda_backtest.api.stock_hk_api import *
import tqx_data

import pandas as pd
import numpy as np


def initialize(context):
    """Initialize strategy context for HK cross-sectional strategy.

    - Universe: Hang Seng Index (HSI) constituents.
    - Fundamental hard filters: revenue growth > 20%, gross margin > 20%, operating cash flow > 0
      (implemented via context.df_factor-style DataFrame if available; otherwise placeholder pass-through).
    - Rebalance: every 5 trading days.
    - On each rebalance: among filtered HSI members, pick top 5 stocks by 5-day momentum and rebalance equal-weight.
    """
    # --- account ---
    context.account = '15032863'

    # --- strategy parameters ---
    context.rebalance_period = 5  # rebalance every 5 trading days
    context.top_n = 5  # select top 5 by 5-day momentum
    context.max_position_ratio = 0.95  # use up to 95% of equity

    # --- universe: Hang Seng Index constituents ---
    # If engine provides HSI constituents via context (e.g., context.hsi_constituents), prefer that.
    # Otherwise, use a static fallback list of common HSI names; you can replace this with full index membership.
    hsi_fallback = [
        "1810.HK", "3690.HK",
    ]

    # Try to refine universe using tqx_data.get_stock_detail with market="hk"
    try:
        df_symbols = tqx_data.get_stock_detail(
            symbol="",
            fields=["symbol", "rcs_asset_category_name"],
            market="hk",
            status=1,
        )
        all_syms = set(df_symbols["symbol"].astype(str).tolist())
        stock_universe = [s for s in hsi_fallback if s in all_syms]
        if len(stock_universe) == 0:
            stock_universe = hsi_fallback
        context.stock_universe = stock_universe
    except Exception:
        context.stock_universe = hsi_fallback

    # --- trading calendar cache (for 5-day interval logic) ---
    try:
        calendar_df = tqx_data.get_trading_calendar(
            start_date="20000101",
            end_date="20991231",
            market="hk",
        )
        # Try to detect the date column
        if "date" in calendar_df.columns:
            cal_date_col = "date"
        elif "trade_date" in calendar_df.columns:
            cal_date_col = "trade_date"
        else:
            cal_date_col = calendar_df.columns[0]
        calendar_df[cal_date_col] = calendar_df[cal_date_col].astype(str).str.replace("-", "")
        context.trading_calendar = calendar_df[[cal_date_col]].rename(columns={cal_date_col: "date"})
    except Exception:
        context.trading_calendar = pd.DataFrame(columns=["date"])

    # --- order lot: use a generic 100-share lot; you may override per symbol via get_stock_detail ---
    context.order_lot = 100

    # --- potential fundamental factor DataFrame (optional) ---
    # If the engine passes a factor DataFrame via context.df_factor, normalize it for later use.
    if hasattr(context, "df_factor") and isinstance(context.df_factor, pd.DataFrame):
        df_factor = context.df_factor.copy()
        # Normalize symbol/date columns if present
        if "symbol" in df_factor.columns:
            df_factor["symbol"] = df_factor["symbol"].astype(str)
        if "date" in df_factor.columns:
            df_factor["date"] = df_factor["date"].astype(str).str.replace("-", "")
        context.df_factor = df_factor
    else:
        context.df_factor = None

    # --- state caches ---
    context.last_rebalance_date = None
    context.selected_symbols_today = []


def before_trading(context):
    """Reset daily state before market open."""
    context.selected_symbols_today = []


def _is_rebalance_day(context):
    """Check if today is a rebalance day based on a 5-trading-day interval.

    Uses context.trading_calendar to find the index of today and rebalance every `rebalance_period` days.
    """
    if context.trading_calendar is None or len(context.trading_calendar) == 0:
        return False

    today = str(context.now)
    cal = context.trading_calendar
    if today not in set(cal["date"]):
        return False

    cal_sorted = cal.sort_values("date").reset_index(drop=True)
    idx_map = {d: i for i, d in enumerate(cal_sorted["date"].tolist())}
    today_idx = idx_map.get(today)
    if today_idx is None:
        return False

    if context.last_rebalance_date is None:
        context.last_rebalance_date = today
        return True

    last_idx = idx_map.get(str(context.last_rebalance_date))
    if last_idx is None:
        context.last_rebalance_date = today
        return True

    if today_idx - last_idx >= context.rebalance_period:
        context.last_rebalance_date = today
        return True
    return False


def _get_recent_daily_close(symbol_list, end_date, lookback_days):
    """Fetch last `lookback_days` daily bars up to `end_date` for given symbols via stock_api_quotation.

    Returns DataFrame with columns [date, symbol, close].
    """
    if not symbol_list:
        return pd.DataFrame(columns=["date", "symbol", "close"])

    # end_date is expected as YYYYMMDD
    try:
        end_int = int(end_date)
    except Exception:
        end_int = int(str(end_date).replace("-", ""))
    # subtract ~30 calendar days to ensure we cover at least 5 trading days
    start_int = max(20000101, end_int - 30)
    start_date = str(start_int)

    df = stock_api_quotation(
        symbol_list=symbol_list,
        start_date=start_date,
        end_date=end_date,
        fields=["date", "symbol", "close"],
        period="1d",
    )
    if df is None or len(df) == 0:
        return pd.DataFrame(columns=["date", "symbol", "close"])

    df["date"] = df["date"].astype(str).str.replace("-", "")
    df = df.sort_values(["symbol", "date"])
    df = df.groupby("symbol").tail(lookback_days).reset_index(drop=True)
    return df


def _compute_5day_momentum(daily_df):
    """Compute 5-day momentum = close(last) / close(first) - 1 for each symbol.

    Assumes daily_df contains up to `rebalance_period` rows per symbol sorted by date.
    """
    if daily_df is None or len(daily_df) == 0:
        return pd.Series(dtype=float)

    momentum_list = []
    for symbol, sub in daily_df.groupby("symbol"):
        sub_sorted = sub.sort_values("date")
        if len(sub_sorted) < 2:
            continue
        first_close = float(sub_sorted.iloc[0]["close"])
        last_close = float(sub_sorted.iloc[-1]["close"])
        if first_close <= 0:
            continue
        mom = last_close / first_close - 1.0
        momentum_list.append((symbol, mom))

    if not momentum_list:
        return pd.Series(dtype=float)

    symbols, moms = zip(*momentum_list)
    return pd.Series(data=moms, index=list(symbols))


def _apply_fundamental_filters(context, universe):
    """Apply hard fundamental filters to HSI universe:

    - revenue growth > 20%
    - gross margin > 20%
    - operating cash flow > 0

    Implementation:
    - If context.df_factor exists and contains the required fields, filter by them.
    - Otherwise, return the universe unchanged (placeholder), so code remains executable.

    Expected optional columns in context.df_factor:
    - 'date' (YYYYMMDD string)
    - 'symbol' (e.g., '0700.HK')
    - 'revenue_growth' (float)
    - 'gross_margin' (float)
    - 'operating_cash_flow' (float)
    """
    if not universe:
        return []

    df_factor = getattr(context, "df_factor", None)
    if df_factor is None or not isinstance(df_factor, pd.DataFrame):
        # No fundamental data wired, pass through
        return list(universe)

    required_cols = {"date", "symbol", "revenue_growth", "gross_margin", "operating_cash_flow"}
    if not required_cols.issubset(set(df_factor.columns)):
        # Missing required fields, cannot apply filters robustly
        return list(universe)

    today = str(context.now)
    df_today = df_factor[df_factor["date"] == today]
    if len(df_today) == 0:
        return list(universe)

    cond = (
        (df_today["revenue_growth"] > 0.20)
        & (df_today["gross_margin"] > 0.20)
        & (df_today["operating_cash_flow"] > 0.0)
    )
    df_filtered = df_today[cond]
    if len(df_filtered) == 0:
        return []

    allowed_symbols = set(df_filtered["symbol"].astype(str).tolist())
    return [s for s in universe if s in allowed_symbols]


def _select_target_symbols(context):
    """Select top-N symbols by 5-day momentum within HSI universe under fundamental filters."""
    universe = _apply_fundamental_filters(context, context.stock_universe)
    if not universe:
        return []

    today = str(context.now)
    daily_df = _get_recent_daily_close(universe, end_date=today, lookback_days=context.rebalance_period)
    if len(daily_df) == 0:
        return []

    mom_series = _compute_5day_momentum(daily_df)
    if len(mom_series) == 0:
        return []

    mom_series = mom_series.sort_values(ascending=False)
    top_symbols = list(mom_series.index[: context.top_n])
    return top_symbols


def _rebalance_portfolio(context, data, target_symbols):
    """Rebalance portfolio into `target_symbols` equally weighted up to max_position_ratio.

    - Sell symbols not in target.
    - Buy target names to equal weights.
    - Respect a generic order lot size for HK (context.order_lot).
    """
    account = context.stock_account_dict.get(context.account)
    if account is None:
        return

    # --- sell positions not in target ---
    current_positions = account.positions
    target_set = set(target_symbols)
    for symbol, position in list(current_positions.items()):
        if position.quantity > 0 and symbol not in target_set and position.sellable > 0:
            order_shares(context.account, symbol, -position.sellable, style=MarketOrderStyle)

    # Refresh account snapshot after sells
    account = context.stock_account_dict.get(context.account)
    if account is None:
        return

    if not target_symbols:
        return

    total_equity = float(account.total_value)
    max_equity_for_positions = total_equity * context.max_position_ratio
    target_value_each = max_equity_for_positions / float(len(target_symbols)) if len(target_symbols) > 0 else 0.0

    for symbol in target_symbols:
        try:
            bar = data[symbol]
        except (KeyError, TypeError, AttributeError):
            continue
        if bar is None:
            continue
        price = float(bar.close)
        if price <= 0:
            continue

        pos = account.positions.get(symbol)
        current_mv = float(pos.market_value) if pos is not None else 0.0
        desired_mv = target_value_each
        diff_mv = desired_mv - current_mv
        if diff_mv <= price:
            continue

        raw_qty = int(diff_mv // price)
        # Apply HK order lot rounding
        lot = int(getattr(context, "order_lot", 100))
        qty = int(raw_qty / lot) * lot
        if qty <= 0:
            continue

        # Ensure we do not exceed available cash
        if qty * price > account.cash:
            qty = int(account.cash // price)
            qty = int(qty / lot) * lot
        if qty <= 0:
            continue

        order_shares(context.account, symbol, qty, style=MarketOrderStyle)


def handle_data(context, data):
    """Main bar callback for HK cross-sectional strategy.

    - Every 5 trading days: within HSI constituents that pass fundamental filters,
      select top 5 by 5-day momentum and rebalance to equal weights.
    - On non-rebalance days: hold positions.
    """
    if not _is_rebalance_day(context):
        return

    # Avoid multiple rebalances within the same day
    if context.selected_symbols_today:
        return

    target_symbols = _select_target_symbols(context)
    context.selected_symbols_today = target_symbols

    if not target_symbols:
        return

    _rebalance_portfolio(context, data, target_symbols)


def after_trading(context):
    """Log end-of-day HK account summary and current positions."""
    account = context.stock_account_dict.get(context.account)
    if account is None:
        return

    print(f"[{context.now}] HK account summary: equity={account.total_value:.2f}, cash={account.cash:.2f}")
    for symbol, position in account.positions.items():
        if position.quantity > 0:
            print(
                f"  {symbol}: qty={position.quantity}, sellable={position.sellable}, "
                f"mv={position.market_value:.2f}, pnl={position.pnl:.2f}"
            )
