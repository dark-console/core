# Dark Console — the "user resilient" contract

The suite splits the design surface into two categories. This document governs where each one lives and how it's read/written.

## 1. Fixed (suite identity — non-overridable by the user)

- **Colors.** Every token in `palette.json` is the identity of the suite. A consumer does not "theme the palette"; a consumer *applies* the palette.
- Rationale: one author, one identity. A per-user color system (Catppuccin's `flavors`) is a different product; Dark Console is the locked-palette product.

## 2. Resilient (per-user, per-surface)

Rules of thumb:

1. **A tool's font is never a palette token.** A port reads the surface's native font preference and only falls back to the suite default (`Glass TTY VT220`) when the user hasn't set one. The spec records the family name, never a CSS stack.
2. **A user-resilient value is a *setting*, declared in `ports/<tool>/meta.yaml`** — its label, type (`string` / `color` / `bool` / `select`), default, and which key of the surface's native config it maps to (e.g. `editor.fontFamily` in VS Code, the idle-font field in Obsidian, the custom-font field in Hermes).
3. **The Hermes desktop port additionally can present user overrides via the SDK's UI doors:**
   - `ctx.storage.{get,set,remove}` — persist per-plugin state (e.g. "my accent override"), survives restarts.
   - `APPEARANCE_AREAS.extra` — inject a row at the end of Settings → Appearance for a user-visible control.
   - `host.settings.*` — read/write the *existing* native appearance prefs (font, density, etc.).
4. **Resilient values are user-editable, not suite-defined.** The suite does not decide what a per-user toggle means; it only *provides* the storage and the UI.

## 3. Why this split matters (the non-rewrite rule)

A **fixed** token change (like moving `accent` from `#DB0000` to `#E33B57`) should require:
- one edit in `palette.json`,
- one commit,
- the generator re-emitting every port's generated file,
- zero hand-touched changes in any port.

A **resilient** value change (like a user choosing a different monospace face) should require:
- a user edit *inside the consuming tool*, or, if exposed, a drag in that tool's settings UI,
- zero edits in the suite,
- zero commits.

Any change that inverts this split is a design bug and should be caught in review.

## 4. Read-first, never-force

For every user-resilient value, the port's runtime contract is:
1. Read the surface preference.
2. If present, use it.
3. If absent, fall back to the suite default.
4. **Never overwrite the surface preference as a side effect of applying the theme.**

This is how users "don't get fighting themes." The suite supplies the palette; the tool keeps the pen.
