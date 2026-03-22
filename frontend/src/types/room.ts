export type RoomTheme =
  | "minimal"
  | "scandinavian"
  | "industrial"
  | "boho"
  | "luxury"
  | "coastal"

export interface RoomInput {
  roomName: string
  length: number
  width: number
  height: number
  notes: string
  theme: RoomTheme
  budget: number
  furniture: string
}

export interface DetectedObject {
  id: string
  label: string
  confidence: number
  dimensions: {
    width: number
    height: number
    depth?: number
  }
  position: {
    x: number
    y: number
  }
}

export interface LayoutSuggestion {
  id: string
  title: string
  description: string
  items: string[]
}

export interface BudgetItem {
  id: string
  name: string
  category: string
  price: number
}

export interface AnalysisResult {
  summary: string
  detectedObjects: DetectedObject[]
  layoutSuggestions: LayoutSuggestion[]
  budgetItems: BudgetItem[]
  totalBudget: number
  themePalette: string[]
  depthSummary?: {
    min: number
    max: number
    mean: number
  } | null
}
