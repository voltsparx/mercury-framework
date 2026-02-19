"""Terminal UI helpers for banners, status lines, and prompts."""
from __future__ import annotations

import random
from typing import Iterable, Optional

from .colors import style


BANNERS = [
    r"""
 __  __                      __
|  \/  | ___ _ __ ___ _   _ / _|_   _
| |\/| |/ _ \ '__/ __| | | | |_| | | |
| |  | |  __/ | | (__| |_| |  _| |_| |
|_|  |_|\___|_|  \___|\__,_|_|  \__, |
                                 |___/
""",
    r"""
+----------------------------------------------+
|   __  __                                     |
|  |  \/  | ___ _ __ ___ _   _ _ __ _   _      |
|  | |\/| |/ _ \ '__/ __| | | | '__| | | |     |
|  | |  | |  __/ | | (__| |_| | |  | |_| |     |
|  |_|  |_|\___|_|  \___|\__,_|_|   \__, |     |
|                                   |___/      |
+----------------------------------------------+
""",
    r"""
 __  __                                 _
|  \/  | ___ _ __ ___ _   _ _ __ _   _| |
| |\/| |/ _ \ '__/ __| | | | '__| | | | |
| |  | |  __/ | | (__| |_| | |  | |_| |_|
|_|  |_|\___|_|  \___|\__,_|_|   \__, (_)
                                  |___/
""",
]


QUOTES = [
    "Learn, build, defend.",
    "Safe simulations beat risky shortcuts.",
    "Isolate first, automate second.",
]


def clear_terminal(*, force: bool = False) -> None:
    """Clear terminal using ANSI escape sequences."""
    # Always emit when force=True; in CI/non-interactive shells this is still safe.
    if force:
        print("\x1b[2J\x1b[H", end="")
        return
    print("\x1b[2J\x1b[H", end="")


def color_text(
    text: str,
    color: Optional[str] = None,
    *,
    bold: bool = False,
    underline: bool = False,
    theme: str = "mercury",
) -> str:
    return style(text, color=color, bold=bold, underline=underline, theme=theme)


def display_banner(*, theme: str = "mercury", index: int | None = None) -> None:
    if index is None:
        banner = random.choice(BANNERS)
    else:
        banner = BANNERS[index % len(BANNERS)]
    quote = random.choice(QUOTES)
    print(color_text(banner.rstrip("\n"), "accent", theme=theme))
    print(color_text(f"  {quote}", "muted", theme=theme))
    print()


def print_status(level: str, message: str, *, theme: str = "mercury") -> None:
    palette = {
        "info": "info",
        "ok": "success",
        "warn": "warning",
        "error": "error",
    }
    label = level.upper()
    color = palette.get(level, "primary")
    print(color_text(f"[{label}] ", color, theme=theme) + message)


def print_menu(title: str, options: Iterable[str], *, theme: str = "mercury") -> None:
    print(color_text(title, "primary", bold=True, theme=theme))
    for idx, line in enumerate(options, start=1):
        print(color_text(f"  {idx}) ", "accent", theme=theme) + line)
    print()


def prompt(msg: str = "") -> str:
    try:
        return input(msg)
    except (KeyboardInterrupt, EOFError):
        raise
