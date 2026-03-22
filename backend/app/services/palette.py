from __future__ import annotations

THEME_PALETTES = {
  "minimal": ["#F6F2EE", "#EDE7E2", "#C7C1B8"],
  "scandinavian": ["#F4EFEA", "#DAD2C7", "#BFAF9B"],
  "industrial": ["#E1DCDC", "#B7B0AA", "#5E5956"],
  "boho": ["#D5A37C", "#C46B4F", "#F6EFE8"],
  "luxury": ["#2B1E2F", "#C9A46B", "#F4EFEA"],
  "coastal": ["#EAF6F8", "#CBE4E7", "#8FB7C1"],
}


def palette_for_theme(theme: str | None) -> list[str]:
  if not theme:
    return THEME_PALETTES["minimal"]
  return THEME_PALETTES.get(theme.lower(), THEME_PALETTES["minimal"])
