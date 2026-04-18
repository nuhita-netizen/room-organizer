from pydantic import BaseModel
from typing import List, Optional, Any

class UploadResponse(BaseModel):
    success: bool
    image_url: str

class GenerateRequest(BaseModel):
    image_url: str
    room_type: str
    design_style: str
    design_preferences: Optional[dict] = None  # e.g. {"budget": "mid", "purpose": "relaxation"}

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

class GenerationStatusResponse(BaseModel):
    success: bool
    status: str
    data: Optional[GenerationResultData] = None
