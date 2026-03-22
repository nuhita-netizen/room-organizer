from __future__ import annotations

from pydantic import BaseModel


class RoomInput(BaseModel):
  room_name: str | None = None
  length: float
  width: float
  height: float
  notes: str | None = None
  theme: str | None = None
  budget: float | None = None
  furniture: str | None = None


class DetectedObject(BaseModel):
  id: str
  label: str
  confidence: float
  width: float
  height: float
  depth: float | None = None
  x: float
  y: float


class LayoutSuggestion(BaseModel):
  id: str
  title: str
  description: str
  items: list[str]


class BudgetItem(BaseModel):
  id: str
  name: str
  category: str
  price: float


class AnalysisResult(BaseModel):
  summary: str
  detected_objects: list[DetectedObject]
  layout_suggestions: list[LayoutSuggestion]
  budget_items: list[BudgetItem]
  total_budget: float
  theme_palette: list[str]
  depth_summary: dict[str, float] | None = None
