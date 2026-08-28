"""Local HK/US research nodes for skill-tqx-research.

This file holds the core node logic for:
CodeControl -> StockBacktestControl -> BackTestResultControl
CodeControl -> FactorAnalysisControl -> FactorAnalysisChartControl
"""

from __future__ import annotations

import inspect
import os
from pathlib import Path
from math import sqrt
from dataclasses import dataclass, field
from typing import Any, Iterable

import numpy as np
import pandas as pd
from dotenv import load_dotenv

_SKILL_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(_SKILL_ROOT / ".env", override=False)


def _chunked(values: list[str], size: int) -> list[list[str]]:
    return [values[i : i + size] for i in range(0, len(values), size)]


def _default_hk_universe(limit: int = 50) -> list[str]:
    import tqx_data

    try:
        idx = tqx_data.get_index_component(market="hk", index_symbol="HSI", stock_symbol="")
        if isinstance(idx, pd.DataFrame) and not idx.empty and "stock_symbol" in idx.columns:
            symbols = [str(x) for x in idx["stock_symbol"].dropna().astype(str).tolist()]
            if symbols:
                return symbols[:limit]
    except Exception:
        pass

    try:
        detail = tqx_data.get_stock_detail(symbol="", market="hk", fields=["symbol"], status=1)
        if isinstance(detail, pd.DataFrame) and not detail.empty and "symbol" in detail.columns:
            symbols = [str(x) for x in detail["symbol"].dropna().astype(str).tolist()]
            if symbols:
                return symbols[:limit]
    except Exception:
        pass

    try:
        detail = tqx_data.get_stock_detail(symbol="", market="hk", fields=["symbol"], status=None)
        if isinstance(detail, pd.DataFrame) and not detail.empty and "symbol" in detail.columns:
            symbols = [str(x) for x in detail["symbol"].dropna().astype(str).tolist()]
            if symbols:
                return symbols[:limit]
    except Exception:
        pass

    return []


def _load_hk_daily_panel(
    start_date: str,
    end_date: str,
    symbols: list[str] | None,
    fields: list[str] | None,
) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    symbol_list = [str(s) for s in symbols or [] if str(s).strip()]
    chunks = _chunked(symbol_list, 50) if symbol_list else [None]
    for chunk in chunks:
        kwargs: dict[str, Any] = {"start_date": start_date, "end_date": end_date, "fields": fields}
        if chunk:
            kwargs["symbol"] = chunk
        try:
            frame = load_daily_data("hk", **kwargs)
        except Exception:
            continue
        if isinstance(frame, pd.DataFrame) and not frame.empty:
            frames.append(frame)
    if not frames:
        return pd.DataFrame()
    out = pd.concat(frames, ignore_index=True)
    if "date" in out.columns and "symbol" in out.columns:
        out["date"] = out["date"].astype(str).str.replace("-", "")
        out["symbol"] = out["symbol"].astype(str)
        out = out.sort_values(["symbol", "date"]).drop_duplicates(["symbol", "date"], keep="last")
    return out.reset_index(drop=True)


def _as_yyyymmdd(value: Any) -> str:
    text = "" if value is None else str(value)
    digits = "".join(ch for ch in text if ch.isdigit())
    return digits[:8]


def _finite_float(value: Any) -> float | None:
    try:
        number = float(value)
    except Exception:
        return None
    return number if np.isfinite(number) else None


def _safe_corr(left: pd.Series, right: pd.Series) -> float | None:
    pair = pd.concat([left, right], axis=1).dropna()
    if len(pair) < 2:
        return None
    value = pair.iloc[:, 0].corr(pair.iloc[:, 1])
    return None if pd.isna(value) else float(value)


def _annualized_sharpe(daily_returns: pd.Series) -> float | None:
    values = pd.to_numeric(daily_returns, errors="coerce").dropna()
    if len(values) < 2:
        return None
    std = float(values.std(ddof=1))
    if std <= 0:
        return None
    return float(values.mean() / std * sqrt(252))


def _max_drawdown(equity: pd.Series) -> float | None:
    values = pd.to_numeric(equity, errors="coerce").dropna()
    if values.empty:
        return None
    peak = values.cummax()
    drawdown = values / peak - 1.0
    return float(drawdown.min())


def load_daily_data(market: str, **kwargs: Any) -> pd.DataFrame:
    """Thin local wrapper for tqx_data daily data.

    Use the exact tqx_data export name from the bundled references.
    """
    import tqx_data

    name = "get_hk_daily" if str(market).lower() == "hk" else "get_us_daily"
    fn = getattr(tqx_data, name)
    return fn(**kwargs)


def build_hk_momentum_factor_panel(
    start_date: str,
    end_date: str,
    symbols: list[str] | None = None,
    horizon: int = 5,
) -> pd.DataFrame:
    """Build a HK momentum factor panel from local tqx_data parquet."""
    symbol_list = [str(s) for s in symbols or [] if str(s).strip()]
    if not symbol_list:
        symbol_list = _default_hk_universe()
    df = _load_hk_daily_panel(
        start_date=start_date,
        end_date=end_date,
        symbols=symbol_list,
        fields=["date", "symbol", "close"],
    )
    if df is None or df.empty:
        return pd.DataFrame(columns=["date", "symbol", "close", "factor", f"fwd_return_{horizon}d"])

    frame = df.copy()
    frame["date"] = frame["date"].astype(str).str.replace("-", "")
    frame["symbol"] = frame["symbol"].astype(str)
    frame["close"] = pd.to_numeric(frame["close"], errors="coerce")
    frame = frame.dropna(subset=["date", "symbol", "close"])
    frame = frame.sort_values(["symbol", "date"]).reset_index(drop=True)
    frame["factor"] = frame.groupby("symbol")["close"].pct_change(horizon)
    frame = build_forward_returns(frame, horizon=horizon)
    return frame.dropna(subset=["factor", f"fwd_return_{horizon}d"]).reset_index(drop=True)


def code_control(code: str) -> str:
    """CodeControl equivalent: keep the source code string as the input payload."""
    return str(code)


@dataclass
class PendingOrder:
    symbol: str
    side: str
    qty: int
    price: float = 0.0
    reason: str = ""
    is_target_percent: bool = False
    target_percent: float | None = None


class LocalDataAccess:
    def __init__(self, history: dict[str, list[dict[str, Any]]]) -> None:
        self._history = history

    def current(self, symbol: str) -> dict[str, Any] | None:
        h = self._history.get(symbol)
        return h[-1] if h else None

    def history(self, symbol: str, field: str, n: int) -> pd.Series:
        h = self._history.get(symbol, [])
        if not h:
            return pd.Series(dtype=float)
        window = h[-n:]
        return pd.Series([float(row.get(field, np.nan)) for row in window], dtype=float)

    def __getitem__(self, symbol: str) -> dict[str, Any] | None:
        return self.current(symbol)


@dataclass
class LocalStrategyContext:
    cash: float = 10_000_000.0
    equity: float = 10_000_000.0
    fee_rate: float = 0.0003
    _positions: dict[str, int] = field(default_factory=dict)
    _avg_prices: dict[str, float] = field(default_factory=dict)
    _last_prices: dict[str, float] = field(default_factory=dict)
    _orders: list[PendingOrder] = field(default_factory=list)
    _logs: list[str] = field(default_factory=list)
    on_log: Any = None

    def order(self, symbol: str, qty: int, side: str = "buy", price: float = 0.0, reason: str = "") -> None:
        if qty > 0:
            self._orders.append(PendingOrder(symbol=symbol, side=side, qty=qty, price=price, reason=reason))

    def order_target_percent(self, symbol: str, pct: float, reason: str = "") -> None:
        pct = max(0.0, min(1.0, float(pct)))
        self._orders.append(
            PendingOrder(
                symbol=symbol,
                side="buy",
                qty=0,
                price=0.0,
                reason=reason,
                is_target_percent=True,
                target_percent=pct,
            )
        )

    def position(self, symbol: str) -> int:
        return int(self._positions.get(symbol, 0))

    def log(self, msg: str) -> None:
        self._logs.append(str(msg))
        if self.on_log:
            self.on_log(str(msg))

    def drain_orders(self) -> list[PendingOrder]:
        orders = self._orders
        self._orders = []
        return orders

    def apply_fill(self, symbol: str, side: str, qty: int, price: float, fee: float) -> None:
        cur = self._positions.get(symbol, 0)
        avg = self._avg_prices.get(symbol, 0.0)
        if side == "buy":
            new_qty = cur + qty
            self._positions[symbol] = new_qty
            self._avg_prices[symbol] = (avg * cur + price * qty) / new_qty if new_qty > 0 else 0.0
            self.cash -= price * qty + fee
        else:
            new_qty = max(0, cur - qty)
            self._positions[symbol] = new_qty
            if new_qty == 0:
                self._avg_prices[symbol] = 0.0
            self.cash += price * qty - fee

    def update_last_price(self, symbol: str, price: float) -> None:
        self._last_prices[symbol] = float(price)

    def recompute_equity(self) -> float:
        mv = sum(self._positions.get(s, 0) * self._last_prices.get(s, 0.0) for s in self._positions)
        self.equity = float(self.cash + mv)
        return self.equity


def compile_strategy_code(code: str) -> dict[str, Any]:
    ns: dict[str, Any] = {"__name__": "tqx_strategy"}
    exec(compile(code, "<strategy>", "exec"), ns, ns)
    if "initialize" not in ns or "handle_data" not in ns:
        raise ValueError("strategy code must define initialize(context) and handle_data(context, data)")
    return ns


def _normalize_history_frame(
    df: pd.DataFrame,
    date_col: str = "date",
    symbol_col: str = "symbol",
) -> pd.DataFrame:
    frame = df.copy()
    if date_col not in frame.columns:
        raise ValueError(f"missing column: {date_col}")
    if symbol_col not in frame.columns:
        frame[symbol_col] = "SINGLE"
    frame[date_col] = frame[date_col].map(_as_yyyymmdd)
    frame = frame.dropna(subset=[date_col, symbol_col]).copy()
    frame = frame.sort_values([symbol_col, date_col]).drop_duplicates([symbol_col, date_col], keep="last")
    return frame


def _build_history(frame: pd.DataFrame, symbol_col: str = "symbol") -> dict[str, list[dict[str, Any]]]:
    history: dict[str, list[dict[str, Any]]] = {}
    for symbol, group in frame.groupby(symbol_col, sort=False):
        history[str(symbol)] = group.to_dict(orient="records")
    return history


def _apply_pending_orders(
    ctx: LocalStrategyContext,
    orders: list[PendingOrder],
    prices: dict[str, float],
) -> list[dict[str, Any]]:
    fills: list[dict[str, Any]] = []
    for order in orders:
        last_price = float(prices.get(order.symbol, order.price or 0.0))
        if order.is_target_percent:
            target_value = ctx.equity * float(order.target_percent or 0.0)
            if last_price <= 0:
                continue
            target_qty = int(target_value // last_price)
            delta = target_qty - ctx.position(order.symbol)
            if delta == 0:
                continue
            side = "buy" if delta > 0 else "sell"
            qty = abs(delta)
        else:
            side = order.side
            qty = int(order.qty)

        if qty <= 0 or last_price <= 0:
            continue
        fee = float(last_price * qty * ctx.fee_rate)
        ctx.apply_fill(order.symbol, side, qty, last_price, fee)
        fills.append(
            {
                "symbol": order.symbol,
                "side": side,
                "qty": qty,
                "price": last_price,
                "fee": fee,
                "reason": order.reason,
            }
        )
    return fills


def run_code_backtest(
    code: str,
    df_price: pd.DataFrame,
    initial_cash: float = 10_000_000.0,
    commission_rate: float = 0.0003,
    symbol_col: str = "symbol",
    date_col: str = "date",
    price_col: str = "close",
) -> dict[str, Any]:
    """CodeControl -> StockBacktestControl."""
    frame = _normalize_history_frame(df_price, date_col=date_col, symbol_col=symbol_col)
    if price_col not in frame.columns:
        raise ValueError(f"missing column: {price_col}")
    frame[price_col] = pd.to_numeric(frame[price_col], errors="coerce")
    frame = frame.dropna(subset=[price_col]).copy()
    if frame.empty:
        return {"ok": False, "reason": "empty_input"}

    ns = compile_strategy_code(code)
    ctx = LocalStrategyContext(cash=float(initial_cash), equity=float(initial_cash), fee_rate=float(commission_rate))
    ctx.symbols = list(frame[symbol_col].astype(str).unique())  # type: ignore[attr-defined]
    ctx.date_col = date_col  # type: ignore[attr-defined]
    ctx.price_col = price_col  # type: ignore[attr-defined]
    ctx.symbol_col = symbol_col  # type: ignore[attr-defined]
    ctx.market = "hk" if any(str(s).endswith(".HK") for s in ctx.symbols) else "us"  # type: ignore[attr-defined]
    ns["initialize"](ctx)

    history: dict[str, list[dict[str, Any]]] = {str(sym): [] for sym in frame[symbol_col].astype(str).unique()}
    trades: list[dict[str, Any]] = []
    equity_curve: list[float] = []
    dates = list(dict.fromkeys(frame[date_col].astype(str).tolist()))

    for day in dates:
        day_frame = frame[frame[date_col].astype(str) == day]
        if day_frame.empty:
            continue
        for _, row in day_frame.iterrows():
            symbol = str(row[symbol_col])
            bar = row.to_dict()
            history.setdefault(symbol, []).append(bar)

        data = LocalDataAccess({sym: list(rows) for sym, rows in history.items()})
        current_prices = {
            str(row[symbol_col]): float(row[price_col])
            for _, row in day_frame.iterrows()
            if pd.notna(row[price_col])
        }
        for symbol, price in current_prices.items():
            ctx.update_last_price(symbol, price)

        before_pos = dict(ctx._positions)
        ns["handle_data"](ctx, data)
        fills = _apply_pending_orders(ctx, ctx.drain_orders(), current_prices)
        if fills:
            for fill in fills:
                trades.append({"date": day, **fill})
        ctx.recompute_equity()
        equity_curve.append(float(ctx.equity))

        # 璁板綍绌块€忓紡鑷锛氫换浣曞崟鏃ュ洖鎾ら兘涓嶅簲闈犳湭鏉ヤ环
        if not equity_curve:
            continue
        _ = before_pos  # keep local for debugging consistency

    equity_series = pd.Series(equity_curve, dtype=float)
    daily_returns = equity_series.pct_change().fillna(0.0)
    metrics = {
        "ok": True,
        "trade_count": len(trades),
        "initial_cash": float(initial_cash),
        "final_equity": float(equity_series.iloc[-1]) if not equity_series.empty else float(initial_cash),
        "total_return": float(equity_series.iloc[-1] / equity_series.iloc[0] - 1.0) if len(equity_series) >= 2 else 0.0,
        "annualized_return": _annualized_return(equity_series),
        "annualized_sharpe": _annualized_sharpe(daily_returns),
        "max_drawdown": _max_drawdown(equity_series),
        "equity_curve": equity_series.tolist(),
        "trades": trades,
    }
    return normalize_backtest_result(metrics)


def build_forward_returns(
    df: pd.DataFrame,
    horizon: int = 1,
    price_col: str = "close",
    symbol_col: str = "symbol",
    date_col: str = "date",
) -> pd.DataFrame:
    out = df.copy()
    out = out.sort_values([symbol_col, date_col])
    out[f"fwd_return_{horizon}d"] = (
        out.groupby(symbol_col)[price_col].shift(-horizon) / out[price_col] - 1.0
    )
    return out


def build_factor_panel(
    df_factor: pd.DataFrame,
    factor_col: str,
    price_col: str = "close",
    horizon: int = 1,
    date_col: str = "date",
    symbol_col: str = "symbol",
) -> pd.DataFrame:
    """Build a simple research panel with forward returns for factor analysis."""
    panel = df_factor.copy()
    if price_col in panel.columns:
        for lag in {int(horizon), 1, 3, 5, 10, 20}:
            if f"fwd_return_{lag}d" not in panel.columns:
                panel = build_forward_returns(panel, horizon=lag, price_col=price_col, date_col=date_col, symbol_col=symbol_col)
    needed = {date_col, symbol_col, factor_col, f"fwd_return_{horizon}d"}
    missing = sorted(needed - set(panel.columns))
    if missing:
        raise ValueError(f"missing columns: {missing}")
    return_cols = [
        column
        for column in panel.columns
        if column.startswith("fwd_return_") and column.endswith("d")
    ]
    panel = panel[[date_col, symbol_col, factor_col, *return_cols]].copy()
    panel = panel.dropna(subset=[date_col, symbol_col, factor_col, f"fwd_return_{horizon}d"])
    return panel


def factor_analysis_node(
    df: pd.DataFrame,
    factor_col: str,
    return_col: str | None = None,
    group_count: int = 5,
    decay_lags: Iterable[int] = (1, 3, 5, 10, 20),
    date_col: str = "date",
    symbol_col: str = "symbol",
    higher_is_better: bool = True,
) -> dict[str, Any]:
    """Minimal factor-analysis node.

    Caller must provide point-in-time visible factor and return columns.
    """
    data = df.copy()
    if return_col is None:
        return_col = "fwd_return_1d"
    data = data[[date_col, symbol_col, factor_col, return_col]].dropna()
    if data.empty:
        return {"ok": False, "reason": "empty_input"}

    ic_rows = []
    group_rows = []
    for date, day in data.groupby(date_col):
        x = pd.to_numeric(day[factor_col], errors="coerce")
        if not higher_is_better:
            x = -x
        y = pd.to_numeric(day[return_col], errors="coerce")
        valid = pd.concat([x, y], axis=1).dropna()
        if len(valid) < max(3, group_count):
            continue
        ic_rows.append({"date": date, "ic": valid.iloc[:, 0].corr(valid.iloc[:, 1])})
        ic_rows[-1]["rank_ic"] = valid.iloc[:, 0].rank().corr(valid.iloc[:, 1].rank())

        try:
            bins = pd.qcut(valid.iloc[:, 0].rank(method="first"), q=group_count, labels=False)
        except Exception:
            continue
        grouped = valid.assign(group=bins + 1).groupby("group", observed=True)[valid.columns[1]].mean()
        for group_id, group_ret in grouped.items():
            group_rows.append(
                {
                    "date": date,
                    "group": int(group_id),
                    "mean_return": float(group_ret),
                }
            )

    ic_df = pd.DataFrame(ic_rows)
    group_df = pd.DataFrame(group_rows)
    ic = None if ic_df.empty else float(ic_df["ic"].mean())
    rank_ic = None if ic_df.empty else float(ic_df["rank_ic"].mean())
    icir = None
    if ic_df.shape[0] >= 2:
        std = float(ic_df["ic"].std(ddof=1))
        if std > 0:
            icir = float(ic_df["ic"].mean() / std)

    decay: dict[int, float | None] = {}
    for lag in decay_lags:
        ret_col = f"fwd_return_{int(lag)}d"
        if ret_col in df.columns:
            decay[int(lag)] = _safe_corr(
                pd.to_numeric(df[factor_col], errors="coerce"),
                pd.to_numeric(df[ret_col], errors="coerce"),
            )
        else:
            decay[int(lag)] = None

    group_summary = {}
    if not group_df.empty:
        group_summary = (
            group_df.groupby("group", observed=True)["mean_return"]
            .mean()
            .sort_index()
            .to_dict()
        )

    confidence = {
        "sample_days": int(ic_df.shape[0]),
        "sample_rows": int(len(data)),
        "credible": bool(ic_df.shape[0] >= 30 and (icir is None or abs(icir) >= 0.5)),
    }
    return {
        "ok": True,
        "ic": ic,
        "rank_ic": rank_ic,
        "icir": icir,
        "decay": decay,
        "group_return_summary": group_summary,
        "ic_series": ic_df.to_dict(orient="records"),
        "group_rows": group_rows,
        "confidence": confidence,
    }


def run_factor_analysis(
    df_factor: pd.DataFrame,
    factor_col: str,
    return_col: str | None = None,
    group_count: int = 5,
    decay_lags: Iterable[int] = (1, 3, 5, 10, 20),
    date_col: str = "date",
    symbol_col: str = "symbol",
    higher_is_better: bool = True,
) -> dict[str, Any]:
    """Alias kept for the skill's canonical analysis entrypoint."""
    return factor_analysis_node(
        df_factor,
        factor_col=factor_col,
        return_col=return_col,
        group_count=group_count,
        decay_lags=decay_lags,
        date_col=date_col,
        symbol_col=symbol_col,
        higher_is_better=higher_is_better,
    )


def strategy_backtest_node(
    df: pd.DataFrame,
    short_window: int = 7,
    long_window: int = 20,
    initial_cash: float = 10_000_000.0,
    commission_rate: float = 0.0003,
    price_col: str = "close",
    date_col: str = "date",
) -> dict[str, Any]:
    """Minimal long-only MA cross backtest node.

    Works on one symbol or a single sorted price series.
    """
    data = df.copy()
    data = data[[date_col, price_col]].dropna().sort_values(date_col).reset_index(drop=True)
    if data.empty or len(data) < long_window + 2:
        return {"ok": False, "reason": "insufficient_data"}

    px = pd.to_numeric(data[price_col], errors="coerce")
    data["short_ma"] = px.rolling(short_window).mean()
    data["long_ma"] = px.rolling(long_window).mean()
    data["signal"] = (data["short_ma"] > data["long_ma"]).astype(int)
    data["position"] = data["signal"].shift(1).fillna(0).astype(int)
    data["ret"] = px.pct_change().fillna(0.0)
    data["strategy_ret"] = data["position"] * data["ret"]

    equity = [float(initial_cash)]
    trades: list[dict[str, Any]] = []
    holding = 0
    for i in range(1, len(data)):
        pos = int(data.loc[i, "position"])
        price = float(px.iloc[i])
        prev_price = float(px.iloc[i - 1])
        if pos != holding:
            trade_qty = 1
            fee = price * commission_rate * trade_qty
            trades.append(
                {
                    "date": data.loc[i, date_col],
                    "from": holding,
                    "to": pos,
                    "price": price,
                    "fee": fee,
                }
            )
            equity[-1] -= fee
            holding = pos
        equity.append(equity[-1] * (1.0 + float(data.loc[i, "strategy_ret"])))

    equity_series = pd.Series(equity)
    daily_returns = equity_series.pct_change().fillna(0.0)
    total_return = float(equity_series.iloc[-1] / equity_series.iloc[0] - 1.0)
    metrics = {
        "ok": True,
        "trade_count": len(trades),
        "initial_cash": float(initial_cash),
        "final_equity": float(equity_series.iloc[-1]),
        "total_return": total_return,
        "annualized_return": _annualized_return(equity_series),
        "annualized_sharpe": _annualized_sharpe(daily_returns),
        "max_drawdown": _max_drawdown(equity_series),
        "win_rate": None,
        "trades": trades,
        "equity_curve": equity_series.tolist(),
    }
    return normalize_backtest_result(metrics)


def run_backtest(
    df_price: pd.DataFrame,
    short_window: int = 7,
    long_window: int = 20,
    initial_cash: float = 10_000_000.0,
    commission_rate: float = 0.0003,
    price_col: str = "close",
    date_col: str = "date",
) -> dict[str, Any]:
    """Alias kept for the skill's canonical backtest entrypoint."""
    return strategy_backtest_node(
        df_price,
        short_window=short_window,
        long_window=long_window,
        initial_cash=initial_cash,
        commission_rate=commission_rate,
        price_col=price_col,
        date_col=date_col,
    )


def stock_backtest_control(
    df_price: pd.DataFrame,
    short_window: int = 7,
    long_window: int = 20,
    initial_cash: float = 10_000_000.0,
    commission_rate: float = 0.0003,
) -> dict[str, Any]:
    """StockBacktestControl equivalent for HK/US local research."""
    return run_backtest(
        df_price=df_price,
        short_window=short_window,
        long_window=long_window,
        initial_cash=initial_cash,
        commission_rate=commission_rate,
    )


def backtest_result_control(result: dict[str, Any]) -> dict[str, Any]:
    """BackTestResultControl equivalent for HK/US local research."""
    return {
        "status": "ok" if result.get("ok") else "error",
        "metrics": result,
    }


def factor_analysis_control(
    df_factor: pd.DataFrame,
    factor_col: str,
    return_col: str | None = None,
    group_count: int = 5,
) -> dict[str, Any]:
    """FactorAnalysisControl equivalent for HK/US local research."""
    return run_factor_analysis(
        df_factor=df_factor,
        factor_col=factor_col,
        return_col=return_col,
        group_count=group_count,
    )


def factor_analysis_workflow(
    df_factor: pd.DataFrame,
    factor_col: str,
    price_col: str = "close",
    horizon: int = 1,
    group_count: int = 5,
    decay_lags: Iterable[int] = (1, 3, 5, 10, 20),
    higher_is_better: bool = True,
) -> dict[str, Any]:
    """Canonical local factor workflow."""
    panel = build_factor_panel(
        df_factor=df_factor,
        factor_col=factor_col,
        price_col=price_col,
        horizon=horizon,
    )
    result = run_factor_analysis(
        panel,
        factor_col=factor_col,
        return_col=f"fwd_return_{horizon}d",
        group_count=group_count,
        decay_lags=decay_lags,
        higher_is_better=higher_is_better,
    )
    return factor_analysis_chart_control(result)


def factor_analysis_chart_control(result: dict[str, Any]) -> dict[str, Any]:
    """FactorAnalysisChartControl equivalent for HK/US local research."""
    return {
        "status": "ok" if result.get("ok") else "error",
        "analysis": result,
    }


def normalize_backtest_result(
    metrics: dict[str, Any],
    trades: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Normalize undefined risk metrics to None."""
    out = dict(metrics)
    trades = trades if trades is not None else out.get("trades") or []
    if not trades:
        out["trade_count"] = 0
        out["annualized_sharpe"] = None
        out["max_drawdown"] = None
    return out


def _annualized_return(equity: pd.Series, periods_per_year: int = 252) -> float | None:
    values = pd.to_numeric(equity, errors="coerce").dropna()
    if len(values) < 2 or values.iloc[0] <= 0:
        return None
    years = (len(values) - 1) / periods_per_year
    return float((values.iloc[-1] / values.iloc[0]) ** (1 / years) - 1) if years > 0 else None


def _demo_factor() -> None:
    df = pd.DataFrame(
        {
            "date": ["20250101"] * 6 + ["20250102"] * 6,
            "symbol": [f"S{i}" for i in range(6)] * 2,
            "factor": [1, 2, 3, 4, 5, 6, 2, 3, 4, 5, 6, 7],
            "fwd_return_1d": [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07],
        }
    )
    result = factor_analysis_node(df, "factor")
    assert result["ok"] is True
    assert result["confidence"]["sample_days"] == 2
    assert run_factor_analysis(df, "factor")["ok"] is True
    assert factor_analysis_workflow(df, "factor")["status"] == "ok"


def _demo_backtest() -> None:
    px = pd.DataFrame(
        {
            "date": pd.date_range("2025-01-01", periods=60, freq="D"),
            "close": np.r_[np.linspace(10, 12, 30), np.linspace(12, 9, 30)],
        }
    )
    result = strategy_backtest_node(px, short_window=5, long_window=10)
    assert result["ok"] is True
    assert "final_equity" in result
    assert run_backtest(px, short_window=5, long_window=10)["ok"] is True


def _demo_panel() -> None:
    df = pd.DataFrame(
        {
            "date": ["20250101", "20250101", "20250102", "20250102"],
            "symbol": ["A", "B", "A", "B"],
            "factor": [1.0, 2.0, 1.5, 2.5],
            "close": [10.0, 20.0, 11.0, 21.0],
        }
    )
    panel = build_factor_panel(df, "factor", horizon=1)
    assert not panel.empty
    out = factor_analysis_workflow(df, "factor")
    assert out["status"] == "ok"


if __name__ == "__main__":
    _demo_factor()
    _demo_backtest()
    _demo_panel()
    print("research_nodes self-check ok")
