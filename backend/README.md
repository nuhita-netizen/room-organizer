# RoomAI Backend

FastAPI service that runs YOLOv8 detection, estimates layout suggestions, and produces a budget summary.
Depth estimation is enabled via MiDaS (torch hub) when PyTorch is installed.

## Setup

1. Create a virtual environment
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the API:

```bash
uvicorn app.main:app --reload --port 8000
```

## API

- `GET /health` -> health check
- `POST /analyze` -> run inference and get layout + budget output

### `POST /analyze`

Multipart form fields:
- `image`: room photo (optional, but recommended)
- `room_name`: name of the room
- `length`, `width`, `height`: dimensions in meters
- `notes`: extra design notes
- `theme`: preferred theme
- `budget`: target budget (USD)
- `furniture`: existing furniture list

Response fields:
- `detected_objects`: bounding boxes from YOLOv8
- `layout_suggestions`: layout ideas
- `budget_items` + `total_budget`: auto estimate
- `theme_palette`: hex colors to guide styling
- `depth_summary`: min/max/mean depth values if MiDaS is available

## Notes

- YOLOv8 runs on the `yolov8n` weights by default. Swap to `yolov8s` or `yolov8m` for higher accuracy.
- GPU recommended for production use.
- Budget estimates come from `backend/data/catalog.json`.
- MiDaS weights download on first run.
