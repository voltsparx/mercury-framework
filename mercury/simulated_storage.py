"""Simulated storage - fake file listings to emulate gallery/storage.

All filenames and metadata are synthetic and intended for UI testing only.
"""
from typing import List


def storage_listing() -> List[str]:
    return [
        "document_001_sim.txt",
        "photo_2025_12_simulated.jpg",
        "notes_meeting_sim.txt",
    ]


if __name__ == "__main__":
    for f in storage_listing():
        print(f)
