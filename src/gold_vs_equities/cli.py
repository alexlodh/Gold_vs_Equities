"""Simple CLI entry points for the package.

Usage: python -m gold_vs_equities.cli [command]
Available commands: preprocess, plot
"""
import sys
from . import preprocess, eda


def _help():
    print("Usage: python -m gold_vs_equities.cli [command]")
    print("Commands:\n  preprocess   Fetch and prepare aligned CSV\n  plot <path>  Plot the aligned CSV file")


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        _help()
        return 1
    cmd = argv[0]
    if cmd == "preprocess":
        preprocess.main()
        return 0
    if cmd == "plot":
        if len(argv) < 2:
            print("Missing path for plot command")
            return 2
        eda.plot_gold_sp500(argv[1])
        return 0
    print(f"Unknown command: {cmd}")
    _help()
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
