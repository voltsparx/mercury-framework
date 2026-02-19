"""Allow `python -m mercury`."""
from .launcher import main


if __name__ == "__main__":
    raise SystemExit(main())
