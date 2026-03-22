import type { AnalysisResult, RoomInput } from "@/types/room"
import { mockAnalysis } from "@/features/room/mock"

const API_URL = import.meta.env.VITE_API_URL

export async function analyzeRoom(
  input: RoomInput,
  image?: File | null
): Promise<AnalysisResult> {
  if (!API_URL) {
    return mockAnalysis(input)
  }

  const formData = new FormData()
  if (image) {
    formData.append("image", image)
  }
  formData.append("room_name", input.roomName)
  formData.append("length", String(input.length))
  formData.append("width", String(input.width))
  formData.append("height", String(input.height))
  formData.append("notes", input.notes)
  formData.append("theme", input.theme)
  formData.append("budget", String(input.budget))
  formData.append("furniture", input.furniture)

  const response = await fetch(`${API_URL}/analyze`, {
    method: "POST",
    body: formData,
  })

  if (!response.ok) {
    throw new Error("Failed to analyze room")
  }

  const data = await response.json()

  return {
    summary: data.summary,
    detectedObjects: (data.detected_objects ?? []).map((item: any) => ({
      id: item.id,
      label: item.label,
      confidence: item.confidence,
      dimensions: {
        width: item.width,
        height: item.height,
        depth: item.depth ?? undefined,
      },
      position: {
        x: item.x,
        y: item.y,
      },
    })),
    layoutSuggestions: (data.layout_suggestions ?? []).map((item: any) => ({
      id: item.id,
      title: item.title,
      description: item.description,
      items: item.items ?? [],
    })),
    budgetItems: (data.budget_items ?? []).map((item: any) => ({
      id: item.id,
      name: item.name,
      category: item.category,
      price: item.price,
    })),
    totalBudget: data.total_budget ?? 0,
    themePalette: data.theme_palette ?? [],
    depthSummary: data.depth_summary ?? null,
  } as AnalysisResult
}
