"""Compare runtime tqx_data exports with documented names."""
from __future__ import annotations

import argparse
import inspect
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", type=Path, required=True)
    args = parser.parse_args()
    try:
        import tqx_data  # type: ignore
    except Exception as exc:
        print(f"IMPORT_FAILED: {type(exc).__name__}: {exc}")
        return 2
    text = args.doc.read_text(encoding="utf-8")
    documented = set(re.findall(r"(?:tqx_data\.|Method name: `?|\u65b9\u6cd5\u540d\uff1a`?)([A-Za-z_][A-Za-z0-9_]*)", text))
    exports = {
        n: getattr(tqx_data, n)
        for n in getattr(tqx_data, "__all__", dir(tqx_data))
        if hasattr(tqx_data, n) and not n.startswith("_")
    }
    callable_names = {n for n, value in exports.items() if callable(value)}
    getters = {n for n in callable_names if n.startswith("get_")}
    documented_getters = {n for n in documented if n.startswith("get_")}
    print(f"RUNTIME_CALLABLES={len(callable_names)}")
    print(f"RUNTIME_GETTERS={len(getters)}")
    print(f"DOCUMENTED_GETTERS={len(documented_getters)}")
    print("RUNTIME_ONLY=" + ",".join(sorted(callable_names - documented)))
    print("DOCUMENTED_ONLY=" + ",".join(sorted(documented_getters - callable_names)))
    print("SIGNATURES:")
    for name in sorted(callable_names):
        try:
            print(f"{name}{inspect.signature(exports[name])}")
        except (TypeError, ValueError):
            print(f"{name}<signature unavailable>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
