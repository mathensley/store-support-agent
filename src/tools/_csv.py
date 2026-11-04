import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

def read_rows(filename: str) -> list[dict[str, str]]:
    with (DATA_DIR / filename).open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))