"""Simulated contacts module - harmless contact list for testing UI and flows."""
from dataclasses import dataclass
from typing import List


@dataclass
class Contact:
    name: str
    phone: str
    email: str


def sample_contacts() -> List[Contact]:
    return [
        Contact(name="Alice Example", phone="+10000000001", email="alice@example.com"),
        Contact(name="Bob Research", phone="+10000000002", email="bob@example.com"),
    ]


if __name__ == "__main__":
    for c in sample_contacts():
        print(f"{c.name} - {c.phone} - {c.email}")
