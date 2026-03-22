from __future__ import annotations

import json
from pathlib import Path

from app.models.schemas import BudgetItem

CATALOG_PATH = Path(__file__).resolve().parents[2] / "data" / "catalog.json"


def load_catalog() -> list[BudgetItem]:
  if not CATALOG_PATH.exists():
    return []
  data = json.loads(CATALOG_PATH.read_text())
  return [BudgetItem(**item) for item in data]


def estimate_budget(target_budget: float | None) -> tuple[list[BudgetItem], float]:
  catalog = load_catalog()
  if not catalog:
    return [], 0.0

  selected: list[BudgetItem] = []
  total = 0.0
  for item in catalog:
    if target_budget is None or total + item.price <= target_budget:
      selected.append(item)
      total += item.price

  return selected, total
