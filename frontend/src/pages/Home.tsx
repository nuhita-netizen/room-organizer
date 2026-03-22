import * as React from "react"
import {
  ArrowRight,
  CheckCircle2,
  ImagePlus,
  Loader2,
  Sparkles,
} from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"
import LayoutEditor from "@/components/LayoutEditor"
import { analyzeRoom } from "@/features/room/api"
import type { AnalysisResult, RoomInput, RoomTheme } from "@/types/room"

const defaultInput: RoomInput = {
  roomName: "Studio A",
  length: 4.2,
  width: 3.6,
  height: 2.8,
  notes: "I want soft lighting and more storage for books.",
  theme: "scandinavian",
  budget: 600,
  furniture: "Bed, Sofa, Desk",
}

const themeOptions: { value: RoomTheme; label: string }[] = [
  { value: "minimal", label: "Minimal" },
  { value: "scandinavian", label: "Scandinavian" },
  { value: "industrial", label: "Industrial" },
  { value: "boho", label: "Boho" },
  { value: "luxury", label: "Luxury" },
  { value: "coastal", label: "Coastal" },
]

export default function Home() {
  const [input, setInput] = React.useState<RoomInput>(defaultInput)
  const [image, setImage] = React.useState<File | null>(null)
  const [preview, setPreview] = React.useState<string | null>(null)
  const [analysis, setAnalysis] = React.useState<AnalysisResult | null>(null)
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)

  React.useEffect(() => {
    if (!image) {
      setPreview(null)
      return
    }
    const url = URL.createObjectURL(image)
    setPreview(url)
    return () => URL.revokeObjectURL(url)
  }, [image])

  const handleInputChange = (
    key: keyof RoomInput,
    value: string | number
  ) => {
    setInput((prev) => ({ ...prev, [key]: value }))
  }

  const handleAnalyze = async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await analyzeRoom(input, image)
      setAnalysis(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(250,229,229,0.8),_transparent_55%),radial-gradient(circle_at_bottom,_rgba(251,242,235,0.9),_transparent_45%)]">
      <header className="flex items-center justify-between px-6 py-6 lg:px-12">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-deep-maroon text-white shadow-rose">
            <Sparkles className="h-5 w-5" />
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.3em] text-muted-foreground">RoomAI</p>
            <p className="text-lg font-semibold">Virtual Interior Consultant</p>
          </div>
        </div>
        <div className="hidden items-center gap-3 lg:flex">
          <Badge variant="secondary">YOLOv8 Ready</Badge>
          <Badge variant="outline">Budget Guardrails</Badge>
        </div>
      </header>

      <main className="px-6 pb-20 lg:px-12">
        <section className="grid gap-10 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="space-y-6">
            <div className="space-y-4">
              <Badge className="bg-primary-rose text-white">AI Room Planner</Badge>
              <h1 className="text-4xl font-semibold leading-tight lg:text-5xl">
                Upload your room, add dimensions, and get a fully costed layout.
              </h1>
              <p className="max-w-xl text-base text-muted-foreground">
                RoomAI analyzes your room photo with YOLOv8, maps spatial
                constraints, and proposes a styled arrangement plus a realistic
                budget breakdown.
              </p>
            </div>

            <div className="grid gap-4 sm:grid-cols-3">
              {[
                { title: "Object Detection", desc: "Detects beds, sofas, desks" },
                { title: "Space Mapping", desc: "Builds a 3D room canvas" },
                { title: "Budget Sheet", desc: "Live cost estimation" },
              ].map((item) => (
                <Card key={item.title} className="bg-white/70 backdrop-blur">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-base">{item.title}</CardTitle>
                    <CardDescription>{item.desc}</CardDescription>
                  </CardHeader>
                </Card>
              ))}
            </div>

            <Card className="overflow-hidden border-none bg-white shadow-soft">
              <CardHeader>
                <CardTitle>Room Snapshot</CardTitle>
                <CardDescription>
                  Upload a photo so the system can detect furniture and open
                  space.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <label className="group flex cursor-pointer flex-col items-center justify-center gap-3 rounded-lg border border-dashed border-border bg-background/60 p-8 text-center transition hover:border-primary">
                  <input
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={(event) =>
                      setImage(event.target.files ? event.target.files[0] : null)
                    }
                  />
                  {preview ? (
                    <img
                      src={preview}
                      alt="Room preview"
                      className="h-48 w-full rounded-md object-cover"
                    />
                  ) : (
                    <div className="flex flex-col items-center gap-2">
                      <ImagePlus className="h-8 w-8 text-muted-foreground" />
                      <p className="text-sm text-muted-foreground">
                        Drag and drop or browse an image
                      </p>
                    </div>
                  )}
                </label>
                <div className="flex flex-wrap gap-2 text-xs text-muted-foreground">
                  <span>Supports JPG, PNG</span>
                  <span>Recommended: 1200px wide</span>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card className="h-fit border-none bg-white shadow-soft">
            <CardHeader>
              <CardTitle>Room Parameters</CardTitle>
              <CardDescription>
                Provide dimensions, desired theme, and any furniture changes.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="room-name">Room name</Label>
                <Input
                  id="room-name"
                  value={input.roomName}
                  onChange={(event) =>
                    handleInputChange("roomName", event.target.value)
                  }
                />
              </div>
              <div className="grid gap-4 sm:grid-cols-3">
                <div className="space-y-2">
                  <Label htmlFor="length">Length (m)</Label>
                  <Input
                    id="length"
                    type="number"
                    value={input.length}
                    onChange={(event) =>
                      handleInputChange("length", Number(event.target.value))
                    }
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="width">Width (m)</Label>
                  <Input
                    id="width"
                    type="number"
                    value={input.width}
                    onChange={(event) =>
                      handleInputChange("width", Number(event.target.value))
                    }
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="height">Height (m)</Label>
                  <Input
                    id="height"
                    type="number"
                    value={input.height}
                    onChange={(event) =>
                      handleInputChange("height", Number(event.target.value))
                    }
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label>Theme</Label>
                <Select
                  value={input.theme}
                  onValueChange={(value) => handleInputChange("theme", value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Pick a theme" />
                  </SelectTrigger>
                  <SelectContent>
                    {themeOptions.map((option) => (
                      <SelectItem key={option.value} value={option.value}>
                        {option.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="budget">Budget (USD)</Label>
                <Input
                  id="budget"
                  type="number"
                  value={input.budget}
                  onChange={(event) =>
                    handleInputChange("budget", Number(event.target.value))
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="furniture">Furniture to keep or add</Label>
                <Input
                  id="furniture"
                  value={input.furniture}
                  onChange={(event) =>
                    handleInputChange("furniture", event.target.value)
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="notes">Notes / preferences</Label>
                <Textarea
                  id="notes"
                  value={input.notes}
                  onChange={(event) =>
                    handleInputChange("notes", event.target.value)
                  }
                />
              </div>
            </CardContent>
            <CardFooter className="flex flex-col gap-3">
              <Button className="w-full" onClick={handleAnalyze} disabled={loading}>
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Analyzing room
                  </>
                ) : (
                  <>
                    Generate layout
                    <ArrowRight className="h-4 w-4" />
                  </>
                )}
              </Button>
              {error ? (
                <p className="text-sm text-destructive">{error}</p>
              ) : (
                <p className="text-xs text-muted-foreground">
                  Results will appear below. If API is not configured, mock data is used.
                </p>
              )}
            </CardFooter>
          </Card>
        </section>

        <section className="mt-12 grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
          <Card className="border-none bg-white shadow-soft">
            <CardHeader>
              <CardTitle>Analysis Output</CardTitle>
              <CardDescription>
                Detected objects and layout recommendations.
              </CardDescription>
            </CardHeader>
            <CardContent>
              {analysis ? (
                <div className="space-y-6">
                  <div className="rounded-lg bg-muted/60 p-4 text-sm text-muted-foreground">
                    {analysis.summary}
                  </div>

                  <Tabs defaultValue="objects">
                    <TabsList>
                      <TabsTrigger value="objects">Detected</TabsTrigger>
                      <TabsTrigger value="layouts">Layouts</TabsTrigger>
                      <TabsTrigger value="palette">Palette</TabsTrigger>
                      <TabsTrigger value="depth">Depth</TabsTrigger>
                    </TabsList>
                    <TabsContent value="objects">
                      <div className="grid gap-4 sm:grid-cols-2">
                        {analysis.detectedObjects.map((obj) => (
                          <Card key={obj.id} className="border border-border/50">
                            <CardHeader className="pb-2">
                              <CardTitle className="text-base">{obj.label}</CardTitle>
                              <CardDescription>
                                Confidence {(obj.confidence * 100).toFixed(0)}%
                              </CardDescription>
                            </CardHeader>
                            <CardContent className="text-xs text-muted-foreground">
                              {obj.dimensions.width}m x {obj.dimensions.depth ?? obj.dimensions.height}m
                            </CardContent>
                          </Card>
                        ))}
                      </div>
                    </TabsContent>
                    <TabsContent value="layouts">
                      <div className="space-y-4">
                        {analysis.layoutSuggestions.map((layout) => (
                          <div key={layout.id} className="rounded-lg border border-border/60 p-4">
                            <div className="flex items-center gap-2">
                              <CheckCircle2 className="h-4 w-4 text-primary" />
                              <p className="font-medium">{layout.title}</p>
                            </div>
                            <p className="mt-2 text-sm text-muted-foreground">
                              {layout.description}
                            </p>
                            <div className="mt-3 flex flex-wrap gap-2">
                              {layout.items.map((item) => (
                                <Badge key={item} variant="secondary">
                                  {item}
                                </Badge>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    </TabsContent>
                    <TabsContent value="palette">
                      <div className="flex gap-3">
                        {analysis.themePalette.map((color) => (
                          <div
                            key={color}
                            className="flex h-16 w-16 flex-col items-center justify-center rounded-lg border border-border text-[10px]"
                            style={{ backgroundColor: color }}
                          >
                            {color}
                          </div>
                        ))}
                      </div>
                    </TabsContent>
                    <TabsContent value="depth">
                      {analysis.depthSummary ? (
                        <div className="grid gap-3 rounded-lg border border-border/60 p-4 text-sm text-muted-foreground">
                          <div>Min depth: {analysis.depthSummary.min.toFixed(2)}</div>
                          <div>Max depth: {analysis.depthSummary.max.toFixed(2)}</div>
                          <div>Mean depth: {analysis.depthSummary.mean.toFixed(2)}</div>
                        </div>
                      ) : (
                        <div className="rounded-lg border border-dashed border-border p-4 text-sm text-muted-foreground">
                          Depth estimation not available. Install the depth model to enable it.
                        </div>
                      )}
                    </TabsContent>
                  </Tabs>
                </div>
              ) : (
                <div className="rounded-lg border border-dashed border-border p-6 text-sm text-muted-foreground">
                  Run the analysis to see detection data, layout ideas, and palette.
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="border-none bg-white shadow-soft">
            <CardHeader>
              <CardTitle>Layout Editor</CardTitle>
              <CardDescription>
                Drag the detected furniture blocks to explore a new placement.
              </CardDescription>
            </CardHeader>
            <CardContent>
              {analysis ? (
                <LayoutEditor
                  items={analysis.detectedObjects}
                  roomWidth={input.width}
                  roomLength={input.length}
                />
              ) : (
                <div className="rounded-lg border border-dashed border-border p-6 text-sm text-muted-foreground">
                  Run the analysis first to populate the layout editor.
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="border-none bg-white shadow-soft">
            <CardHeader>
              <CardTitle>Budget Forecast</CardTitle>
              <CardDescription>
                Auto-generated estimate based on selected furniture.
              </CardDescription>
            </CardHeader>
            <CardContent>
              {analysis ? (
                <div className="space-y-4">
                  {analysis.budgetItems.map((item) => (
                    <div key={item.id} className="flex items-center justify-between text-sm">
                      <div>
                        <p className="font-medium">{item.name}</p>
                        <p className="text-xs text-muted-foreground">{item.category}</p>
                      </div>
                      <p className="font-semibold">${item.price}</p>
                    </div>
                  ))}
                  <div className="border-t border-border/60 pt-4 text-sm">
                    <div className="flex items-center justify-between">
                      <span>Total estimated spend</span>
                      <span className="text-lg font-semibold text-primary">
                        ${analysis.totalBudget}
                      </span>
                    </div>
                    <p className="mt-2 text-xs text-muted-foreground">
                      Budget target: ${input.budget}
                    </p>
                  </div>
                </div>
              ) : (
                <div className="rounded-lg border border-dashed border-border p-6 text-sm text-muted-foreground">
                  Budget breakdown will appear after analysis.
                </div>
              )}
            </CardContent>
          </Card>
        </section>
      </main>
    </div>
  )
}
