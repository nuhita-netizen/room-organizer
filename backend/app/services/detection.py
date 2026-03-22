from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from PIL import Image

try:
  from ultralytics import YOLO
except ImportError:  # pragma: no cover - handled at runtime
  YOLO = None


@dataclass
class Detection:
  label: str
  confidence: float
  width: float
  height: float
  x: float
  y: float


_model: Any | None = None


def _load_model() -> Any:
  global _model
  if _model is not None:
    return _model
  if YOLO is None:
    raise RuntimeError("ultralytics is not installed")
  _model = YOLO("yolov8n.pt")
  return _model


def detect_objects(image: Image.Image) -> list[Detection]:
  model = _load_model()
  img_array = np.array(image.convert("RGB"))
  results = model.predict(img_array, verbose=False)
  detections: list[Detection] = []

  for result in results:
    if result.boxes is None:
      continue
    for box in result.boxes:
      cls_id = int(box.cls[0])
      label = result.names.get(cls_id, "object")
      confidence = float(box.conf[0])
      x1, y1, x2, y2 = box.xyxy[0].tolist()
      width = max(0.0, x2 - x1)
      height = max(0.0, y2 - y1)
      x = x1 + width / 2
      y = y1 + height / 2
      detections.append(
        Detection(
          label=label,
          confidence=confidence,
          width=width,
          height=height,
          x=x,
          y=y,
        )
      )

  return detections
