# Dark Console

**One palette. Every tool.** The source of truth is one file — [`palette.json`](palette.json) — that feeds every surface: terminal, editor, app, design tool, web. Change a value here once, and every generated surface carries the change.

> **Status:** v0.1.0 — colors locked for current ports, palette still evolving as new surfaces come online.

## The palette

Every color is a *token*, not just a swatch. The token carries a **group** (surface / text / structure / semantic / bubble / composer / button), a **name** (its role in the UI), and a **hex** — that is the whole thing. No fallbacks. No stacked fonts. The hex *is* the value; the name is what the rest of the suite builds from.

### Surfaces

| Token | Hex | Role |
|---|---|---|
| `surface.background` | `#00040B` | The chat field — darkest surface |
| `surface.card` | `#0A0806` | Warm near-black, lifted — raised surfaces |
| `surface.muted` | `#141109` | Hover tints, disabled fills (warm) |
| `surface.popover` | `#12100B` | Menus, dropdowns, popovers |
| `surface.sidebar` | `#0A0806` | Working rail — reads lighter than chat |

### Text

| Token | Hex | Role |
|---|---|---|
| `text.foreground` | `#FF8300` | Amber — all body text (label / output) |
| `text.secondary` | `#A06222` | Warm dim — secondary, placeholders, tree rules |

### Structure

| Token | Hex | Role |
|---|---|---|
| `structure.border` | `#300F00` | Warm brown — all borders, idle input outlines |
| `structure.accent` | `#DB0000` | Red — focus ring, active tab, selection, cursor |
| `structure.accentDeep` | `#221102` | Accent ~12% on bg — hover fills, active nav rows |

### Semantic / User

| Token | Hex | Role |
|---|---|---|
| `semantic.danger` | `#DB0000` | Stop / error actions |
| `semantic.dangerDeep` | `#221102` | Danger hover / active |
| `bubble.userMessage` | `#300F00` | Your messages — warm brown, raised |
| `bubble.userMessageBorder` | `#213E97` | Blue line around your message bubble |
| `composer.field` | `#170700` | Composer / input field fill (maroon) |
| `composer.fieldText` | `#DB0000` | Your typed text (red) |
| `button.filled` | `#0D1A32` | Filled + secondary button background |
| `button.filledHover` | `#152E55` | Button hover |
| `button.navSelected` | `#0D1A32` | Selected nav rows |
| `button.navHover` | `#152E55` | Nav / row hover |

### Terminal (ANSI 16)

The 16-color terminal ramp, mapped from the suite.

| | Normal | Bright |
|---|---|---|
| black | `#464B59` | `#A06222` |
| red | `#E33B57` | `#E85E75` |
| green | `#25A231` | `#59D966` |
| yellow | `#B88A16` | `#EABC48` |
| blue | `#476BD7` | `#718CDC` |
| magenta | `#9E1A53` | `#E5619A` |
| cyan | `#0981B4` | `#3DBEF5` |
| white | `#C2C2C2` | `#EBEBEB` |

Cursor: `#DB0000` · Selection: `#1A3278` · Foreground: `#FF8300`

## Fonts

**Glass TTY VT220** — single face, single weight, no bold ramp (marked bold syntheses). The spec records the *real* family name only — the per-surface CSS fallback chain is a rendering detail of each tool, not a suite token. Every port respects the user's own font preference when one is set, and falls back to this family when not.

## How it stays consistent (and doesn't rot)

- **`palette.json` is the only source of truth.** Every other file in this repo and every per-tool port derives from it — by generation, not by copy-paste. The moment a `#RRGGBB` appears anywhere other than here, that's a drift bug.
- **A generator (`scripts/gen_specs.py`) is the only pathway into ports.** Each port declares *which* semantic tokens it uses, in what *shape* (CSS vars, JSON, ANSI, `.archive`); the generator emits the concrete file. The hand-authored layout lives in the port and never re-touches the palette.
- **The drift-checker (`scripts/validate.py`) runs on every push to every port.** It greps each port's generated file for hex values and asserts they all exist in `palette.json`. The green check is the *suite-level* verification, not a tool-specific CI status.
- **Adding a new tool does not mean re-building anything.** Add a `ports/<tool>.yaml` that maps semantic names to the target format; the generator emits the file; the validator picks it up.

## Status per surface

| Port | Surface | Status | Repo |
|---|---|---|---|
| `hermes` | Hermes desktop | live | `dark-console/hermes` |
| `vscode` | VS Code | live | `dark-console/vscode` |
| `obsidian` | Obsidian | live | `dark-console/obsidian` |
| `neovim` | Neovim | next | — |
| `obs` | OBS Studio | planned | — |
| `terminal` | Terminal (ANSI) | planned | — |

*See [STATUS.md](STATUS.md) for the in-flight board per port.*

## Repo layout

```
core/
  palette.json          ← source of truth (the one file)
  README.md             ← this page (swatch wall + token table + how-it-works)
  STATUS.md             ← status board per port (live/next/planned)
  design/
    settings.md         ← the "user resilient" contract
    standards.md        ← contrast, rounding, font rules
  scripts/
    validate.py         ← drift check (hex in ports ⊆ palette.json)
    gen_specs.py        ← palette.json → per-tool generated files
  ports/
    hermes/             ← template/example port (meta.yaml + generated dist/)
  screenshots/          ← generated screenshots per surface (committed)
```

## Contributing a port

1. Drop a `ports/<tool>/meta.yaml` that maps semantic tokens to the target format.
2. Ask core to add you to the port registry.
3. `gen_specs.py` emits your concrete file; `validate.py` runs against it on every push.
4. Ship the port as its own repo (`dark-console/<tool>/`) — the generated file is the *output*, never the source.

## License

MIT (draft; final license TBA — see `LICENSE`).
