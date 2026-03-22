import * as React from "react"
import { Move } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import type { DetectedObject } from "@/types/room"

interface LayoutEditorProps {
  items: DetectedObject[]
  roomWidth: number
  roomLength: number
}

interface LayoutItemState {
  id: string
  label: string
  x: number
  y: number
  width: number
  height: number
}

const clamp = (value: number, min: number, max: number) =>
  Math.min(Math.max(value, min), max)

const snapToGrid = (value: number, gridSize: number) =>
  Math.round(value / gridSize) * gridSize

const intersects = (a: LayoutItemState, b: LayoutItemState) =>
  a.x < b.x + b.width &&
  a.x + a.width > b.x &&
  a.y < b.y + b.height &&
  a.y + a.height > b.y

export default function LayoutEditor({
  items,
  roomWidth,
  roomLength,
}: LayoutEditorProps) {
  const containerRef = React.useRef<HTMLDivElement | null>(null)
  const [layoutItems, setLayoutItems] = React.useState<LayoutItemState[]>([])
  const [draggingId, setDraggingId] = React.useState<string | null>(null)
  const [origin, setOrigin] = React.useState<{ x: number; y: number } | null>(
    null
  )
  const [snapEnabled, setSnapEnabled] = React.useState(true)
  const gridSize = 20

  const buildLayout = React.useCallback(() => {
    if (!containerRef.current) {
      return
    }

    const { width, height } = containerRef.current.getBoundingClientRect()
    const scaleX = width / (roomWidth || 1)
    const scaleY = height / (roomLength || 1)

    const normalized = items.map((item, index) => {
      const itemWidth = Math.max(48, Math.min(item.dimensions.width * scaleX, width * 0.5))
      const itemHeight = Math.max(
        36,
        Math.min((item.dimensions.depth ?? item.dimensions.height) * scaleY, height * 0.5)
      )
      const x = clamp(item.position.x * scaleX, 0, width - itemWidth)
      const y = clamp(item.position.y * scaleY, 0, height - itemHeight)

      return {
        id: item.id || `item-${index}`,
        label: item.label,
        x,
        y,
        width: itemWidth,
        height: itemHeight,
      }
    })

    setLayoutItems(normalized)
  }, [items, roomWidth, roomLength])

  React.useEffect(() => {
    buildLayout()
  }, [buildLayout])

  const handlePointerDown = (event: React.PointerEvent, id: string) => {
    const target = event.currentTarget as HTMLDivElement
    target.setPointerCapture(event.pointerId)
    setDraggingId(id)
    setOrigin({ x: event.clientX, y: event.clientY })
  }

  const handlePointerMove = (event: React.PointerEvent) => {
    if (!draggingId || !origin || !containerRef.current) {
      return
    }

    const deltaX = event.clientX - origin.x
    const deltaY = event.clientY - origin.y
    const { width, height } = containerRef.current.getBoundingClientRect()

    setLayoutItems((prev) =>
      prev.map((item) => {
        if (item.id !== draggingId) {
          return item
        }

        let nextX = clamp(item.x + deltaX, 0, width - item.width)
        let nextY = clamp(item.y + deltaY, 0, height - item.height)

        if (snapEnabled) {
          nextX = clamp(snapToGrid(nextX, gridSize), 0, width - item.width)
          nextY = clamp(snapToGrid(nextY, gridSize), 0, height - item.height)
        }

        const candidate = { ...item, x: nextX, y: nextY }
        const collision = prev.some(
          (other) => other.id !== item.id && intersects(candidate, other)
        )
        if (collision) {
          return item
        }

        return candidate
      })
    )

    setOrigin({ x: event.clientX, y: event.clientY })
  }

  const handlePointerUp = (event: React.PointerEvent) => {
    event.currentTarget.releasePointerCapture(event.pointerId)
    setDraggingId(null)
    setOrigin(null)
  }

  const handleReset = () => {
    buildLayout()
  }

  const exportLayout = (format: "json" | "svg") => {
    if (!containerRef.current) {
      return
    }

    const { width, height } = containerRef.current.getBoundingClientRect()

    if (format === "json") {
      const payload = {
        room: { width: roomWidth, length: roomLength },
        items: layoutItems.map((item) => ({
          id: item.id,
          label: item.label,
          x: Number(((item.x / width) * roomWidth).toFixed(2)),
          y: Number(((item.y / height) * roomLength).toFixed(2)),
          width: Number(((item.width / width) * roomWidth).toFixed(2)),
          height: Number(((item.height / height) * roomLength).toFixed(2)),
        })),
      }
      const blob = new Blob([JSON.stringify(payload, null, 2)], {
        type: "application/json",
      })
      const url = URL.createObjectURL(blob)
      const anchor = document.createElement("a")
      anchor.href = url
      anchor.download = "room-layout.json"
      anchor.click()
      URL.revokeObjectURL(url)
      return
    }

    const svgItems = layoutItems
      .map(
        (item) =>
          `<rect x="${item.x}" y="${item.y}" width="${item.width}" height="${item.height}" rx="8" ry="8" fill="#F8F5F2" stroke="#CFC6BE" />\n` +
          `<text x="${item.x + 8}" y="${item.y + 20}" font-size="12" fill="#3D2327">${item.label}</text>`
      )
      .join("\n")
    const svg = `<?xml version="1.0" encoding="UTF-8"?>\n<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg">\n<rect width="${width}" height="${height}" fill="#FFFFFF" stroke="#E5DED7" />\n${svgItems}\n</svg>`
    const svgBlob = new Blob([svg], { type: "image/svg+xml" })
    const svgUrl = URL.createObjectURL(svgBlob)
    const anchor = document.createElement("a")
    anchor.href = svgUrl
    anchor.download = "room-layout.svg"
    anchor.click()
    URL.revokeObjectURL(svgUrl)
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div>
          <p className="text-sm font-semibold">Interactive Layout Editor</p>
          <p className="text-xs text-muted-foreground">
            Drag furniture blocks to explore placements. Scaled to your room size.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button
            variant={snapEnabled ? "default" : "outline"}
            size="sm"
            onClick={() => setSnapEnabled((prev) => !prev)}
          >
            Snap {snapEnabled ? "On" : "Off"}
          </Button>
          <Button variant="outline" size="sm" onClick={() => exportLayout("json")}>
            Export JSON
          </Button>
          <Button variant="outline" size="sm" onClick={() => exportLayout("svg")}>
            Export SVG
          </Button>
          <Button variant="outline" size="sm" onClick={handleReset}>
            Reset
          </Button>
        </div>
      </div>

      <div
        ref={containerRef}
        className="relative h-[360px] w-full overflow-hidden rounded-xl border border-border/60 bg-gradient-to-br from-white to-muted/40"
        onPointerMove={handlePointerMove}
        onPointerUp={handlePointerUp}
      >
        <div className="absolute left-4 top-4 flex items-center gap-2 rounded-full bg-white/80 px-3 py-1 text-xs shadow-soft">
          <Move className="h-3 w-3" />
          Drag to rearrange
        </div>

        {layoutItems.length === 0 ? (
          <div className="flex h-full items-center justify-center text-xs text-muted-foreground">
            Run analysis to populate detected furniture blocks.
          </div>
        ) : (
          layoutItems.map((item) => (
            <div
              key={item.id}
              className="absolute rounded-lg border border-border/70 bg-white/90 p-2 text-xs shadow-sm transition"
              style={{
                width: item.width,
                height: item.height,
                transform: `translate(${item.x}px, ${item.y}px)`,
              }}
              onPointerDown={(event) => handlePointerDown(event, item.id)}
            >
              <Badge variant="secondary">{item.label}</Badge>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
