# RoomAI - Virtual Interior Consultant

RoomAI is an AI-powered web application that lets users upload a room photo, add dimensions, and receive a spatially aware layout proposal with a budget estimate and theme palette. It targets students and homeowners who need fast, professional-grade layout guidance without expensive interior design services.

## Features (MVP)

- Upload a room image for object detection (beds, sofas, desks, etc.)
- Input room dimensions + optional furniture list
- Theme selection (minimal, Scandinavian, industrial, boho, luxury, coastal)
- Layout recommendations with collision-aware suggestions (scaffolded)
- Interactive drag-and-drop layout editor with snap-to-grid, collision guard, and JSON/SVG export
- Budget estimation from a configurable product catalog
- Depth estimation summary (MiDaS) when enabled

## Tech Stack

Frontend:
- React + Vite + TypeScript
- Tailwind CSS v3 + shadcn/ui components

Backend:
- FastAPI + Pydantic
- YOLOv8 via `ultralytics`
- OpenCV + Pillow for image handling
- MiDaS depth estimation via PyTorch (optional but enabled in requirements)

## Repo Structure

```
backend/            FastAPI service + YOLOv8 inference
frontend/           React UI (shadcn/ui)
Problem Statement_.docx
P1_PROMPT.txt
```

## Setup

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Environment Variables

Create `frontend/.env`:

```
VITE_API_URL=http://localhost:8000
```

If `VITE_API_URL` is missing, the UI uses mock data.

## API Contract

`POST /analyze` expects multipart form data:
- `image`: image file
- `room_name`, `length`, `width`, `height`
- `notes`, `theme`, `budget`, `furniture`

The response includes:
- `detected_objects` (from YOLOv8)
- `layout_suggestions`
- `budget_items` + `total_budget`
- `theme_palette`

## Constraints & Notes

- **GPU recommended** for YOLOv8 inference. CPU works but is slow.
- **Single-image depth estimation** is approximate. Dimension inputs are used to scale layout.
- **Depth models download at first run** via `torch.hub`.
- **Budget estimates** come from `backend/data/catalog.json`. Replace with a real catalog or vendor API as needed.

## Next Steps

1. Upgrade depth estimation (Depth-Anything / Stereo) for better spatial mapping
2. Replace budget catalog with live pricing APIs
3. Add drag-and-drop layout editor in the frontend
4. Add persistence (S3 uploads, project history, user accounts)
