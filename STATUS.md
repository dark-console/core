# Ports status

Live board: which tools are building, which are next, which are planned.

| Port | Status | Notes |
|---|---|---|
| **Hermes desktop** | ✅ live | [`dark-console/hermes-desktop`](https://github.com/dark-console/hermes-desktop) — plugin ID stays `dark-studio` (compat), display label `Dark Console` |
| **VS Code** | ✅ live | `dark-console/vscode` — port built under org (upstream: `barnacker/dark-studio-vscode`) |
| **Obsidian** | ✅ live | `dark-console/obsidian` (upstream: vault `.obsidian/themes/Dark Studio`) |
| **Neovim** | 🚧 next | First port to build from scratch against `palette.json` |
| **OBS Studio** | ⏳ planned | Preset + LUT + .json project |
| **Terminal (ANSI)** | ⏳ planned | 16-ramp per-surface (generic, we no longer assume one terminal) |
| **Web (Stylus/userstyle)** | ❓ open | `dark-studio-web` v4.1 exists — needs suiting into the suite's generated path |
| **QGIS / Blender / Figma (etc.)** | ❓ open | Open request — add an issue when you start designing one |

## Status codes

- ✅ **live** — in the org, CI green, portrait on the suite page
- 🚧 **next** — design reviewed, palette tokens mapped, build not yet started
- ⏳ **planned** — acknowledged, not yet designed
- ❓ **open** — user-requested, needs a design pass
- ❌ **dropped** — removed from the suite (not actively maintained)
