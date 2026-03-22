import type { AnalysisResult, RoomInput } from "@/types/room"

export function mockAnalysis(input: RoomInput): AnalysisResult {
  const detectedObjects = [
    {
      id: "obj-1",
      label: "Bed",
      confidence: 0.92,
      dimensions: { width: 2.0, height: 0.6, depth: 2.2 },
      position: { x: 1.2, y: 2.4 },
    },
    {
      id: "obj-2",
      label: "Sofa",
      confidence: 0.88,
      dimensions: { width: 1.8, height: 0.8, depth: 0.9 },
      position: { x: 3.4, y: 1.2 },
    },
    {
      id: "obj-3",
      label: "Desk",
      confidence: 0.81,
      dimensions: { width: 1.2, height: 0.75, depth: 0.6 },
      position: { x: 0.8, y: 4.1 },
    },
  ]

  const layoutSuggestions = [
    {
      id: "layout-1",
      title: "Open circulation spine",
      description:
        "Shift the sofa 40cm closer to the window to open the central pathway from door to bed.",
      items: ["Move sofa", "Add runner", "Wall-mounted lighting"],
    },
    {
      id: "layout-2",
      title: "Zoned relaxation corner",
      description:
        "Anchor a reading nook next to the desk with a floor lamp and accent chair.",
      items: ["Accent chair", "Floor lamp", "Side table"],
    },
  ]

  const budgetItems = [
    { id: "budget-1", name: "Arched floor lamp", category: "Lighting", price: 95 },
    { id: "budget-2", name: "Neutral area rug", category: "Textiles", price: 160 },
    { id: "budget-3", name: "Oak side table", category: "Furniture", price: 120 },
    { id: "budget-4", name: "Soft linen curtains", category: "Decor", price: 80 },
  ]

  const totalBudget = budgetItems.reduce((sum, item) => sum + item.price, 0)

  return {
    summary: `Room ${input.roomName || "layout"} looks balanced with clear space for movement. We can keep the bed in place and shift storage to the left wall to improve flow.`,
    detectedObjects,
    layoutSuggestions,
    budgetItems,
    totalBudget,
    themePalette: input.theme === "boho"
      ? ["#D5A37C", "#C46B4F", "#F6EFE8"]
      : input.theme === "luxury"
        ? ["#2B1E2F", "#C9A46B", "#F4EFEA"]
        : ["#EAC9C2", "#EEDFD5", "#FCF6F1"],
    depthSummary: {
      min: 0.12,
      max: 0.98,
      mean: 0.54,
    },
  }
}
