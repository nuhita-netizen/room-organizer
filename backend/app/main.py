from __future__ import annotations

from io import BytesIO
from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from app.models.schemas import AnalysisResult, DetectedObject, LayoutSuggestion
from app.services.budget import estimate_budget
from app.services.depth import estimate_depth_summary
from app.services.detection import detect_objects
from app.services.palette import palette_for_theme

app = FastAPI(title="RoomAI API")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
  return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResult)
async def analyze_room(
  image: Annotated[UploadFile | None, File()] = None,
  room_name: Annotated[str | None, Form()] = None,
  length: Annotated[float, Form()] = 0.0,
  width: Annotated[float, Form()] = 0.0,
  height: Annotated[float, Form()] = 0.0,
  notes: Annotated[str | None, Form()] = None,
  theme: Annotated[str | None, Form()] = None,
  budget: Annotated[float | None, Form()] = None,
  furniture: Annotated[str | None, Form()] = None,
) -> AnalysisResult:
  detections: list[DetectedObject] = []
  depth_summary = None

  if image is not None:
    image_bytes = await image.read()
    pil_image = Image.open(BytesIO(image_bytes))
    results = detect_objects(pil_image)
    detections = [
      DetectedObject(
        id=f"det-{idx}",
        label=result.label,
        confidence=result.confidence,
        width=result.width,
        height=result.height,
        depth=None,
        x=result.x,
        y=result.y,
      )
      for idx, result in enumerate(results)
    ]
    depth = estimate_depth_summary(pil_image)
    if depth is not None:
      depth_summary = {
        "min": depth.min_depth,
        "max": depth.max_depth,
        "mean": depth.mean_depth,
      }

  layout_suggestions = [
    LayoutSuggestion(
      id="layout-1",
      title="Clear central pathway",
      description="Shift the largest item 40cm away from the door to create a clean circulation path.",
      items=["Reposition sofa", "Add runner", "Soft overhead light"],
    ),
    LayoutSuggestion(
      id="layout-2",
      title="Functional zoning",
      description="Group storage near the tallest wall to free up the main living zone.",
      items=["Shelving", "Task lighting", "Console table"],
    ),
  ]

  budget_items, total_budget = estimate_budget(budget)

  summary = (
    f"Room {room_name or 'layout'} measured {length}m x {width}m. "
    "Detected furniture was mapped to create a balanced circulation plan. "
    "Use the theme palette to style textiles and accessories."
  )

  return AnalysisResult(
    summary=summary,
    detected_objects=detections,
    layout_suggestions=layout_suggestions,
    budget_items=budget_items,
    total_budget=total_budget,
    theme_palette=palette_for_theme(theme),
    depth_summary=depth_summary,
  )
