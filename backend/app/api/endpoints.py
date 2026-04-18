import asyncio
import uuid
import os
from PIL import Image, ImageEnhance, ImageOps
from io import BytesIO
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, status

# Load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional; env vars can be set manually

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
from app.models.schemas import (
    UploadResponse, 
    GenerateRequest, 
    GenerateResponse, 
    GenerationStatusResponse, 
    GenerationResultData
)

router = APIRouter(prefix="/api/v1")

# Mock database to store generation status
MOCK_DB = {}

@router.post("/upload", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File Too Large")
        
    try:
        img = Image.open(BytesIO(content))
        if img.width < 1280 or img.height < 720:
            print(f"Low Quality Warning: Image resolution {img.width}x{img.height} is below 720p. Results may be blurry.")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image format")

    # Save the file to static/uploads
    os.makedirs("static/uploads", exist_ok=True)
    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join("static/uploads", filename)
    with open(filepath, "wb") as buffer:
        buffer.write(content)
    
    file_url = f"http://127.0.0.1:8001/static/uploads/{filename}"
    return UploadResponse(success=True, image_url=file_url)


@router.post("/validate-room")
async def validate_room(file: UploadFile = File(...)):
    """
    Uses Google Gemini vision to determine whether the uploaded image
    contains an interior room (living room, bedroom, kitchen, bathroom, etc.).
    Returns:  { is_room: bool, confidence: float (0-1), reason: str }
    """
    content = await file.read()

    # Basic format guard
    try:
        img = Image.open(BytesIO(content))
        img.verify()           # raises if corrupt
    except Exception:
        return {"is_room": False, "confidence": 0.0, "reason": "invalid_image"}

    # Re-open after verify (verify() closes the file pointer)
    img = Image.open(BytesIO(content)).convert("RGB")

    # ── Gemini Vision Check ──────────────────────────────────────────────────
    api_key = GOOGLE_API_KEY
    try:
        import google.generativeai as genai
        from google.generativeai.types import HarmCategory, HarmBlockThreshold

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Convert to JPEG bytes for the inline image part
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=85)
        image_bytes = buf.getvalue()

        prompt = (
            "You are a room-detection classifier. Analyse the image and decide "
            "whether it shows an INTERIOR ROOM (e.g. living room, bedroom, kitchen, "
            "bathroom, dining room, office, hallway, etc.).\n\n"
            "Reply with ONLY a JSON object — no markdown, no extra text:\n"
            '{"is_room": true|false, "confidence": 0.0-1.0, "reason": "<code>"}\n\n'
            "Allowed reason codes:\n"
            "  indoor_room        – is a valid interior room\n"
            "  no_indoor_scene    – no interior scene visible\n"
            "  outdoor_scene      – clearly an outdoor photo\n"
            "  face_or_person     – selfie or portrait; room not the subject\n"
            "  no_room_features   – interior but lacks room features (e.g. close-up of object)\n"
            "  low_confidence     – cannot determine clearly\n"
        )

        response = model.generate_content(
            [
                {"mime_type": "image/jpeg", "data": image_bytes},
                prompt,
            ],
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT:        HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH:       HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )

        raw = response.text.strip()
        # Strip any accidental markdown fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        import json as _json
        result = _json.loads(raw)
        return {
            "is_room":    bool(result.get("is_room", False)),
            "confidence": float(result.get("confidence", 0.0)),
            "reason":     str(result.get("reason", "low_confidence")),
        }

    except ImportError:
        # SDK not installed – fall back to permissive
        print("[validate-room] google-generativeai not installed. Skipping AI check.")
        return {"is_room": True, "confidence": 0.5, "reason": "sdk_missing"}
    except Exception as e:
        print(f"[validate-room] Gemini error: {e}")
        # On any API error, be permissive so users aren't blocked
        return {"is_room": True, "confidence": 0.5, "reason": "api_error"}



def _finalize_generation(job_id, result_urls, prefs):
    country = "US"
    if prefs and "country" in prefs:
        country = prefs["country"]

    currency_map = {
        "IN": ("₹", 83.0),
        "UK": ("£", 0.79),
        "US": ("$", 1.0)
    }
    
    symbol, multiplier = currency_map.get(country, ("$", 1.0))

    try:
        budget_limit = float(prefs.get("budget", 5000)) if prefs else 5000.0
    except:
        budget_limit = 5000.0
        
    budget_limit_usd = budget_limit / multiplier

    if budget_limit_usd < 500:
        base_items = [
            ("DIY Terracotta Paint Kit", 80),
            ("Thrifted Accent Chair", 150),
            ("Basic Slate Throw Pillows", 45),
            ("Warm Amber Bulb (4-pack)", 25)
        ]
        recs = [
            "Use DIY terracotta painting techniques on an accent wall to save costs.",
            "Thrift for mid-century modern seating and simply wash or reupholster.",
            "Swap out existing bulbs for amber or warm white to improve the ambiance."
        ]
    elif budget_limit_usd < 2000:
        base_items = [
            ("Terracotta Accent Chair", 450),
            ("Matte Slate Coffee Table", 250),
            ("Neutral Sand Area Rug", 180),
            ("LED Light Strips (50ft)", 60)
        ]
        recs = [
            "Implement LED strip lighting behind the TV or bed for an upgraded look without rewiring.",
            "Invest in a centerpiece terracotta accent chair.",
            "Use a neutral sand rug to anchor the matte slate furniture pieces together."
        ]
    else:
        base_items = [
            ("Premium Terracotta Velvet Lounge Chair", 1250),
            ("Custom Brushed Slate Coffee Table", 850),
            ("Handwoven Sand Area Rug", 580),
            ("Architectural Hidden LED Lighting System", 420)
        ]
        recs = [
            "Install an architectural hidden LED lighting system in the ceiling coves.",
            "Utilize pure terracotta velvet for the main accent lounge chair.",
            "Choose custom matte black or dark slate hardware for all cabinet fixtures."
        ]

    total_base = sum(cost for _, cost in base_items)
    scale = (budget_limit_usd * 0.95) / total_base if total_base > 0 else 1.0

    budget_estimates = []
    for name, base_usd in base_items:
        adjusted_usd = base_usd * scale
        budget_estimates.append({
            "item_name": name,
            "estimated_cost": int(adjusted_usd * multiplier),
            "currency_symbol": symbol
        })
    
    # Update mock DB with completed status and payload
    res = GenerationStatusResponse(
        success=True,
        status="completed",
        data=GenerationResultData(
            result_image_urls=result_urls,
            explanation=f"To achieve the designated look within your {symbol}{int(budget_limit):,} budget, we introduced soft edges, plush seating, and warm ambient lighting. The color palette revolves around our signature hues.",
            color_palette=["#0f172a", "#1e293b", "#475569", "#c25c42", "#e2e8f0"],
            recommendations=recs,
            budget_estimates=budget_estimates
        )
    )
    MOCK_DB[job_id] = res
    return res

async def simulate_yolov8_segmentation(job_id, image_path):
    print(f"[{job_id}] Initiating YOLOv8 Architecture for Semantic Segmentation...")
    await asyncio.sleep(1)
    print(f"[{job_id}] YOLOv8: Features detected (Wall: 0.98, Surface: 0.85)")
    print(f"[{job_id}] Geometric Calibration Complete. Forwarding to Generative Pipeline...")
    return True

async def simulate_generation(job_id: str, image_url: str, prefs: dict = None):
    """Background task to simulate AI generation process."""
    await asyncio.sleep(2)  # Simulate a 2-second generation time
    
    if "/static/uploads/" in image_url:
        filename = image_url.split("/static/uploads/")[-1]
        input_path = os.path.join("static/uploads", filename)
        
        await simulate_yolov8_segmentation(job_id, input_path)
        
        # --- NANO BANANA (GEMINI) API INTEGRATION ---
        api_key = GOOGLE_API_KEY
        if api_key and os.path.exists(input_path):
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                print(f"[{job_id}] Connecting to Nano Banana (Gemini/Imagen) API for Generation...")
                
                room_type = prefs.get("room_type", "Living Room") if prefs else "Living Room"
                base_prompt = f"A highly detailed, photorealistic 4k interior design render of a {room_type}. "
                
                opt1_prompt = base_prompt + "Aethelred style plush lounge. Warm terracotta velvet seating, slate grey accent walls, ambient hidden LED lighting, modern architecture."
                opt2_prompt = base_prompt + "Aethelred style stripped minimalist. Stark matte slate furniture, neutral sand rug, bright daylight, architectural."
                
                model = genai.ImageGenerationModel("imagen-3.0-generate-001")
                
                os.makedirs("static/results", exist_ok=True)
                opt1_filename = f"dynamic_{job_id}_opt1.png"
                opt2_filename = f"dynamic_{job_id}_opt2.png"
                opt1_path = os.path.join("static/results", opt1_filename)
                opt2_path = os.path.join("static/results", opt2_filename)
                
                print("Generating Option 1 via API...")
                resp1 = model.generate_images(prompt=opt1_prompt, number_of_images=1, aspect_ratio="4:3")
                if resp1.images:
                    Image.open(BytesIO(resp1.images[0].image.image_bytes)).save(opt1_path)
                
                print("Generating Option 2 via API...")
                resp2 = model.generate_images(prompt=opt2_prompt, number_of_images=1, aspect_ratio="4:3")
                if resp2.images:
                    Image.open(BytesIO(resp2.images[0].image.image_bytes)).save(opt2_path)
                
                print("Nano Banana Generation Successful!")
                result_urls = [
                    f"http://127.0.0.1:8001/static/results/{opt1_filename}",
                    f"http://127.0.0.1:8001/static/results/{opt2_filename}"
                ]
                
                # Success
                return _finalize_generation(job_id, result_urls, prefs)
            except ImportError:
                print("google-generativeai SDK not installed. Falling back to local simulation.")
            except Exception as e:
                print(f"Nano Banana API Error (Falling back to local simulation): {e}")

    # Fallback if API fails or no API key, use out pre-generated realistic mock images
    result_urls = [
        "http://127.0.0.1:8001/static/results/mock_opt1.png",
        "http://127.0.0.1:8001/static/results/mock_opt2.png"
    ]
    _finalize_generation(job_id, result_urls, prefs)

@router.post("/generate", response_model=GenerateResponse)
async def generate_design(request: GenerateRequest, background_tasks: BackgroundTasks):
    job_id = f"gen_{uuid.uuid4().hex[:8]}"
    
    # Merge room_type into design_preferences so simulate_generation can use it
    prefs = dict(request.design_preferences or {})
    prefs["room_type"] = request.room_type
    prefs["design_style"] = request.design_style

    # Initialize job in Mock DB as processing
    MOCK_DB[job_id] = GenerationStatusResponse(
        success=True,
        status="processing",
        data=None
    )
    
    # Trigger background task
    background_tasks.add_task(simulate_generation, job_id, request.image_url, prefs)
    
    return GenerateResponse(success=True, generation_id=job_id, status="processing")

@router.get("/generations/{id}", response_model=GenerationStatusResponse)
async def get_generation_status(id: str):
    job = MOCK_DB.get(id)
    if job:
        return job
    return GenerationStatusResponse(success=False, status="failed", data=None)
