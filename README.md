# RoomAI - Virtual Interior Consultant

RoomAI is an AI-powered web application that lets users upload a room photo, add dimensions, and receive a spatially aware layout proposal with a budget estimate and theme palette. It targets students and homeowners who need fast, professional-grade layout guidance without expensive interior design services.

## Quick Start (TL;DR) ⚡

### 1) Clone

```bash
git clone <YOUR_REPO_URL>
cd room-organizer
```

### 2) Backend (Python 3.11, CPU-only PyTorch)

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
python3.11 -m pip install --upgrade pip
python3.11 -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
python3.11 -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3) Frontend (new terminal)

```bash
cd ../frontend
printf "VITE_API_URL=http://localhost:8000\n" > .env
npm install
npm run dev
```

Open:

- Frontend: http://localhost:5173
- Backend docs: http://localhost:8000/docs

## Requirements ✅

- Python 3.10 or 3.11 only
- Do not use Python 3.12+ (some ML wheels will fail to install)
- Node.js 18+
- Virtual environment required (use `python3.11 -m venv .venv`)

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
- YOLOv8 via ultralytics
- OpenCV + Pillow for image handling
- MiDaS depth estimation via PyTorch (optional but enabled in requirements)

## Project Structure 📁

```text
backend/            FastAPI service + YOLOv8 inference
  app/main.py       FastAPI entrypoint
frontend/           React UI (shadcn/ui)
Problem Statement_.docx
P1_PROMPT.txt
```

## Setup (Detailed)

### Backend (Python + ML)

1. Create and activate a virtual environment (Python 3.11):

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
```

2. Upgrade pip:

```bash
python3.11 -m pip install --upgrade pip
```

3. Install CPU-only PyTorch first (prevents CUDA downloads):

```bash
python3.11 -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

4. Install the remaining backend dependencies:

```bash
python3.11 -m pip install -r requirements.txt
```

5. Run the API:

```bash
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
printf "VITE_API_URL=http://localhost:8000\n" > .env
npm install
npm run dev
```

### Environment Variables

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

If `VITE_API_URL` is missing, the UI uses mock data.

## Verify Setup ✅

1. Open http://localhost:8000/docs
2. You should see the FastAPI Swagger UI with the `GET /health` and `POST /analyze` endpoints.

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
- `depth_summary` (if MiDaS is available)

## Constraints & Notes

- GPU recommended for YOLOv8 inference. CPU works but is slow.
- Single-image depth estimation is approximate. Dimension inputs are used to scale layout.
- Depth models download at first run via `torch.hub`.
- Budget estimates come from `backend/data/catalog.json`. Replace with a real catalog or vendor API as needed.

## Troubleshooting 🛠️

### ModuleNotFoundError: No module named 'app'

- Run the backend from the `backend/` directory.
- Make sure the virtual environment is activated.

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### Port already in use

- Change the port for the backend or frontend.

```bash
uvicorn app.main:app --reload --port 8001
# Update VITE_API_URL to http://localhost:8001
```

### Slow install or CUDA-related errors

- You are likely installing GPU wheels. Use the CPU-only command:

```bash
python3.11 -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### First-run model download

- On first request, YOLOv8 and MiDaS weights are downloaded automatically.
- This can take a few minutes depending on network speed.

## Next Steps

1. Upgrade depth estimation (Depth-Anything / Stereo) for better spatial mapping.
2. Replace budget catalog with live pricing APIs.
3. Expand the layout editor with constraints, snapping presets, and collaborative editing.
4. Add persistence (S3 uploads, project history, user accounts).