# Archi RoomAI - UML Diagrams

This document outlines the architecture, data models, and sequence workflows of the **Archi RoomAI** application using Mermaid UML.

## 1. Component Architecture
This diagram shows the high-level system architecture and how different components interact.

```mermaid
graph TD
    Client[Frontend Client<br/>demo.html] --> API[FastAPI Backend<br/>app/main.py]
    API --> Endpoints[Route Handlers<br/>app/api/endpoints.py]
    Endpoints --> Models[Pydantic Schemas<br/>app/models/schemas.py]
    
    Endpoints --> Validation[Room Validation logic]
    Validation -->|Google GenAI| Gemini[Gemini 1.5 Flash]
    
    Endpoints --> GenTask[Background GenTask]
    GenTask -->|Google GenAI| Imagen[Imagen 3.0]
    GenTask --> Models
```

## 2. Sequence Workflow (Main Application Flow)
This sequence diagram models the lifecycle of a user uploading an image, the system validating it, and asynchronously generating design styles.

```mermaid
sequenceDiagram
    actor User
    participant Frontend as Frontend App (HTML/JS)
    participant FastAPI as API Backend
    participant Gemini as Google Gemini (Validation)
    participant Imagen as Google Imagen (Generation)

    User->>Frontend: Upload Room Image
    Frontend->>FastAPI: POST /api/v1/upload
    FastAPI-->>Frontend: UploadResponse (image_url)

    User->>Frontend: "Validate Room"
    Frontend->>FastAPI: POST /api/v1/validate-room
    FastAPI->>Gemini: Verify if image is a room
    Gemini-->>FastAPI: Validation boolean
    FastAPI-->>Frontend: Is Valid Room?

    User->>Frontend: Click "Generate Design"
    Frontend->>FastAPI: POST /api/v1/generate
    FastAPI->>FastAPI: Spawn background task
    FastAPI-->>Frontend: GenerateResponse (generation_id, PENDING)

    loop Polling (every 2-3s)
        Frontend->>FastAPI: GET /api/v1/generations/{id}
        alt Generating
            FastAPI-->>Frontend: status: IN_PROGRESS
        end
        opt Background Processing
            FastAPI->>Imagen: Send prompt for interior design
            Imagen-->>FastAPI: Generated Render URLs & details
        end
        alt Complete
            FastAPI-->>Frontend: GenerationStatusResponse (SUCCESS, GenerationResultData)
        end
    end
    Frontend->>User: Display Interactive Renders & Budget Estimation
```

## 3. Class Diagram (Data Transfer Objects)
This class diagram illustrates the Pydantic schemas used for API requests and responses.

```mermaid
classDiagram
    class UploadResponse {
        +bool success
        +str image_url
    }
    class GenerateRequest {
        +str image_url
        +str room_type
        +str design_style
        +dict design_preferences
    }
    class GenerateResponse {
        +bool success
        +str generation_id
        +str status
    }
    class BudgetItem {
        +str item_name
        +float estimated_cost
        +str currency_symbol
    }
    class GenerationResultData {
        +List~str~ result_image_urls
        +str explanation
        +List~str~ color_palette
        +List~str~ recommendations
    }
    class GenerationStatusResponse {
        +bool success
        +str status
    }

    GenerationResultData *-- BudgetItem : contains -> budget_estimates
    GenerationStatusResponse *-- GenerationResultData : contains -> data
```
