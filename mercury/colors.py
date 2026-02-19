"""Color and theme helpers for terminal output.

The module is dependency-light and uses ANSI codes by default. If `colorama`
is installed, it will initialize Windows console support automatically.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
import re
import sys
from typing import Dict

try:
    # Optional dependency: enables ANSI handling on older Windows terminals.
    from colorama import just_fix_windows_console  # type: ignore

    just_fix_windows_console()
except Exception:
    pass


ANSI_RESET = "\x1b[0m"
ANSI_BOLD = "\x1b[1m"
ANSI_UNDERLINE = "\x1b[4m"


ANSI_COLORS: Dict[str, str] = {
    "black": "\x1b[30m",
    "red": "\x1b[31m",
    "green": "\x1b[32m",
    "yellow": "\x1b[33m",
    "blue": "\x1b[34m",
    "magenta": "\x1b[35m",
    "cyan": "\x1b[36m",
    "white": "\x1b[37m",
    "bright_black": "\x1b[90m",
    "bright_red": "\x1b[91m",
    "bright_green": "\x1b[92m",
    "bright_yellow": "\x1b[93m",
    "bright_blue": "\x1b[94m",
    "bright_magenta": "\x1b[95m",
    "bright_cyan": "\x1b[96m",
    "bright_white": "\x1b[97m",
}


@dataclass(frozen=True)
class Theme:
    primary: str
    accent: str
    info: str
    success: str
    warning: str
    error: str
    muted: str


THEMES: Dict[str, Theme] = {
    "mercury": Theme(
        primary="bright_cyan",
        accent="bright_blue",
        info="cyan",
        success="bright_green",
        warning="bright_yellow",
        error="bright_red",
        muted="bright_black",
    ),
    "sunset": Theme(
        primary="bright_yellow",
        accent="bright_magenta",
        info="bright_blue",
        success="green",
        warning="yellow",
        error="red",
        muted="bright_black",
    ),
    "mono": Theme(
        primary="white",
        accent="bright_white",
        info="white",
        success="white",
        warning="white",
        error="white",
        muted="bright_black",
    ),
}


def supports_color() -> bool:
    """Return True when ANSI coloring should be enabled."""
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    return bool(sys.stdout.isatty())


def _resolve_color(token: str, theme_name: str) -> str:
    theme = THEMES.get(theme_name, THEMES["mercury"])
    theme_colors = {
        "primary": theme.primary,
        "accent": theme.accent,
        "info": theme.info,
        "success": theme.success,
        "warning": theme.warning,
        "error": theme.error,
        "muted": theme.muted,
    }
    color_name = theme_colors.get(token, token)
    return ANSI_COLORS.get(color_name, "")


def style(
    text: str,
    color: str | None = None,
    *,
    bold: bool = False,
    underline: bool = False,
    theme: str = "mercury",
) -> str:
    """Return styled text using ANSI escape sequences."""
    if not supports_color():
        return text
    prefix = ""
    if color:
        prefix += _resolve_color(color, theme)
    if bold:
        prefix += ANSI_BOLD
    if underline:
        prefix += ANSI_UNDERLINE
    if not prefix:
        return text
    return f"{prefix}{text}{ANSI_RESET}"


ANSI_PATTERN = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(text: str) -> str:
    return ANSI_PATTERN.sub("", text)


def theme_names() -> list[str]:
    return sorted(THEMES.keys())
