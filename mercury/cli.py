"""CLI entrypoint for installed package usage."""
from __future__ import annotations

from .launcher import main as launcher_main


def main(argv=None):
    return launcher_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
