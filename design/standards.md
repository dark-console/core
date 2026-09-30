# Dark Console — Design Standards

The rules that hold across every port, in every simulation.

## Color

- **One pallete file.** `palette.json` at the root is the only place hex values may be written. Every other file — port CSS, terminal ramp, editor JSON, OBS .extendboard — is *generated* from it.
- **Named tokens, not positions.** Every color has a *role* (`background`, `accent`, `danger`, `bubble.border`, …) that tells you what it paints, not a number. The role is the contract; the hex is a rendering detail.
- **Warm bias (posture).** The darkroom identity is *warm near-black*. Surfaces lift from `surface.background` by raising the warm channel slightly, never by raising the blue channel. A cool-grey lift breaks the suite's temperature.
- **No invented grays.** The only "gray" is `#A06222` (warm dim) for secondary text. If you find yourself writing a `#888` or `#777`, that is a red flag.

## Typography

- **One face, Glass TTY VT220.** The suite ships one font family. It is single-weight; **marked bold is synthesized** by the surface, not drawn from a bold TTF. The spec records the family name — *not* a fallback stack.
- **Single-weight posture.** A port does not introduce a second font family or a weight matrix. If a port needs "code" vs "UI," it does it in *context* (same family, different CSS class), not in family.

## Rounding / Stroke

- **`--radius: 6px`** default (covers inputs, bubbles, buttons, cards).
- **`--radius-sm: 4px`** smaller controls (chips, badges, inline code).
- **`--stroke: 1px`** for idle borders; a `--stroke-active: 2px` pass for focus / selection is allowed but not required.

## Spacing / Density

- **Baseline rhythm 4px.** All paddings, gaps, margins are integers on a 4px grid (4, 8, 12, 16, 20, 24, …). No 5px, no 7px.
- **Density is a per-user resilient value** (see `settings.md`) for surfaces that expose it (Obsidian, VS Code). The suite does not force a density.

## Motion

- **No motion as a rule.** The suite does not ship animations. If a surface has native motion (Hermes's streaming cursor, a terminal bell), that is the surface's behavior, not the suite's.
- **Accent-driven selection is the only motion the suite *deifies*.** (Selected row → `button.navSelected`, cursor → `structure.accent`.) Nothing else moves for the palette.

## Contrast floor

- Body text on `surface.background` ≥ 4.5:1 (WCAG AA). This is the floor, not the target.
- The palette currently clears it at `#FF8300` on `#00040B` (compute the exact ratio in `validate.py`; CI gates on it).

## Anti-rules

- Do not add a `light` mode. Fix the *dark* mode properly.
- Do not add a per-user accent *by default*. An accent override is a project, not a setting.
- Do not invent a "code token" family — the ANSI 16 is the code ramp, and it is derived from the same palette, not an abstracted sibling.
