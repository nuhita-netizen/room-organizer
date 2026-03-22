# Design System: Archi RoomAI - Organic Velvet
**Project ID:** 9230622313347280582

## 1. Visual Theme & Atmosphere
The "Organic Velvet" aesthetic is designed to feel welcoming, soft, and playful. Rooted in the user's visual reference, the design leaves behind rigid enterprise grids and embraces fluid organic shapes. It feels appetizing, casual yet highly polished, using sweeping fluid backgrounds and heavily rounded "pill-like" containers to wrap content.

## 2. Color Palette & Roles
- **Primary Rose:** `#ce6b7f` (Used for primary CTA buttons, active states, and energetic highlights)
- **Soft Blush:** `#fae5e5` (Used for large background sections, soft card backgrounds, and organic blobs)
- **Deep Maroon / Charcoal:** `#3d2327` (Used for primary text and high-contrast icons to maintain readability against soft pinks)
- **Clean White:** `#ffffff` (Used for pure card backgrounds to provide "breathing room" for content)
- **Warm Sand:** `#fbf2eb` (Used for secondary backgrounds or alternative sections to break up the pink)

## 3. Typography Rules
- **Headlines:** A rounded, playful sans-serif (e.g., Quicksand or Nunito). Must be set in Heavy/Bold weights to provide a sturdy but soft look.
- **Body:** Inter or Poppins, used primarily in medium weight.
- **Color:** Always use Deep Maroon/Charcoal for text; avoid pure `#000` black as it clashes with the soft vibe.

## 4. Component Stylings
- **Buttons (Primary):** Pill-shaped (`rounded-full`). Background is Primary Rose. Text is White. Soft colored shadow (e.g., `box-shadow: 0 8px 24px rgba(206, 107, 127, 0.3)`).
- **Cards & Containers:** Extremely rounded corners (e.g., `border-radius: 24px` or `32px`). No thick borders. Use soft, diffused shadows to lift cards off the background.
- **Layout Margins:** Generous padding inside cards (at least `24px`).
- **Tags/Pills:** Used for categories or styles. Small pill shapes with a semi-transparent blush background and rose text.

## 5. Layout Principles
- **Organic Shapes:** Backgrounds should not always be straight horizontal cuts. Use wavy top or bottom edges to delineate sections (achieved through SVG paths or CSS border-radius masking).
- **Overlapping Elements:** Let images or cards slightly break out of their containers to feel dynamic and unconstrained.
- **White Space:** High reliance on white space to avoid feeling cluttered. Every element should feel like it has room to "breathe".
