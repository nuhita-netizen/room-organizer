from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from PIL import Image

try:
  import torch
except ImportError:  # pragma: no cover
  torch = None


@dataclass
class DepthSummary:
  min_depth: float
  max_depth: float
  mean_depth: float


_model: Any | None = None
_transform: Any | None = None


def _load_midas() -> tuple[Any, Any] | tuple[None, None]:
  global _model, _transform
  if torch is None:
    return None, None

  if _model is None or _transform is None:
    _model = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")
    _model.eval()
    transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
    _transform = transforms.small_transform

  return _model, _transform


def estimate_depth_summary(image: Image.Image) -> DepthSummary | None:
  model, transform = _load_midas()
  if model is None or transform is None:
    return None

  img = image.convert("RGB")
  input_batch = transform(img)

  with torch.no_grad():
    prediction = model(input_batch)
    prediction = torch.nn.functional.interpolate(
      prediction.unsqueeze(1),
      size=img.size[::-1],
      mode="bicubic",
      align_corners=False,
    ).squeeze()

  depth_map = prediction.cpu().numpy()
  depth_min = float(np.min(depth_map))
  depth_max = float(np.max(depth_map))
  depth_mean = float(np.mean(depth_map))

  return DepthSummary(min_depth=depth_min, max_depth=depth_max, mean_depth=depth_mean)
