"""Project metadata used across the framework."""
from __future__ import annotations

from .colors import style


PROJECT_NAME = "Mercury Framework"
PROJECT_SLUG = "mercury-framework"
PROJECT_VERSION = "3.0.0"
PROJECT_VERSION_TAG = "v3.0"
AUTHOR = "voltsparx"
CONTACT_EMAIL = "voltsparx@gmail.com"
LICENSE = "MIT"
TAGLINE = "Advanced safe simulation framework for authorized security labs."


def summary_line() -> str:
    return (
        f"{PROJECT_NAME} {PROJECT_VERSION_TAG} | "
        f"author: {AUTHOR} | contact: {CONTACT_EMAIL}"
    )


def colored_summary(*, theme: str = "mercury") -> str:
    return (
        f"{style(PROJECT_NAME, 'primary', bold=True, theme=theme)} "
        f"{style(PROJECT_VERSION_TAG, 'accent', bold=True, theme=theme)} "
        f"{style(f'author={AUTHOR}', 'muted', theme=theme)} "
        f"{style(f'contact={CONTACT_EMAIL}', 'muted', theme=theme)}"
    )


def as_dict() -> dict[str, str]:
    return {
        "project_name": PROJECT_NAME,
        "project_slug": PROJECT_SLUG,
        "project_version": PROJECT_VERSION,
        "project_version_tag": PROJECT_VERSION_TAG,
        "author": AUTHOR,
        "contact_email": CONTACT_EMAIL,
        "license": LICENSE,
        "tagline": TAGLINE,
    }
