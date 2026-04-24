from pydantic import BaseModel
from typing import List, Optional, Any

class UploadResponse(BaseModel):
    success: bool
    image_url: str

# ── Spatial Analysis ──────────────────────────────────────────────────────────
class AnalyzeRoomResponse(BaseModel):
    success: bool
    congestion_score: float          # 0 (open) – 10 (very cluttered)
    detected_items: List[str]        # e.g. ["Sofa", "Coffee Table", "Bookshelf"]
    suggestions: List[str]           # actionable AI suggestions
    spatial_summary: str             # 1-2 sentence narrative

# ── Generation ────────────────────────────────────────────────────────────────
class GenerateRequest(BaseModel):
    image_url: str
    room_type: str
    design_style: str                # "Aethelred Slate & Terracotta" | "Nordic Sage & Stone"
    design_preferences: Optional[dict] = None
    ai_suggestions: Optional[List[str]] = None   # suggestions toggled ON by user
    user_suggestion: Optional[str] = None        # free-text override from user

class GenerateResponse(BaseModel):
    success: bool
    generation_id: str
    status: str

class BudgetItem(BaseModel):
    item_name: str
    estimated_cost: float
    currency_symbol: str = "$"

class GenerationResultData(BaseModel):
    result_image_urls: List[str]
    explanation: str
    color_palette: List[str]
    recommendations: List[str]
    budget_estimates: List[BudgetItem]
    applied_suggestions: Optional[List[str]] = None   # echoed back for the UI

class GenerationStatusResponse(BaseModel):
    success: bool
    status: str
    data: Optional[GenerationResultData] = None
