#!/usr/bin/env python3
"""
gen_specs.py — generate a port's concrete file(s) from palette.json.

The port defines *its* shape. The generator looks up the semantic tokens
the port needs and emits the target format. We only ship one format here
(CSS :root variables) as the reference implementation — expand with
`if fmt == "json": ...` branches as ports come online.

Per-port input:
  ports/<tool>/meta.yaml
    name: vscode            # human name (matches port folder)
    format: css             # css | json | ansi | ... (extend as needed)
    generated: dist/theme.css   # relative to the port's folder here
    map:
      background: surface.background
      border: structure.border
      accent: structure.accent
      ...

`map` is the key — each key in the map is a *variable name in the port's
concrete format*; the value is a *dotted token path* into palette.json.

Usage:
    python3 scripts/gen_specs.py --port vscode
    python3 scripts/gen_specs.py      # every port
    python3 scripts/gen_specs.py --port vscode --emit       # actually write
"""
import argparse
import json
import sys
import pathlib


def load_palette(root: pathlib.Path):
    with (root / "palette.json").open() as f:
        return json.load(f)


def resolve(data, dotted: str):
    cur = data
    for part in dotted.split("."):
        cur = cur.get(part)
        if cur is None:
            return None
    return cur


def read_meta(ports_root: pathlib.Path, port: str):
    meta_path = ports_root / port / "meta.yaml"
    if not meta_path.exists():
        raise FileNotFoundError(meta_path)
    # minimal YAML-ish parse: we only need top-level scalars + a `map:` dict
    meta = {"name": port, "format": "css", "generated": "dist/theme.css", "map": {}}
    in_map = False
    for raw in meta_path.read_text().splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.strip().startswith("map:"):
            in_map = True
            continue
        if in_map:
            if line.startswith("  ") and ":" in line:
                k, v = line.strip().split(":", 1)
                meta["map"][k.strip()] = v.strip()
                continue
            in_map = False
        # top-level key
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta


def render_css(meta, palette):
    lines = [":root {"]
    for var_name, token_path in meta["map"].items():
        v = resolve(palette, f"colors.{token_path}") if not token_path.startswith(("ansi.", "fonts.")) else resolve(palette, token_path)
        if isinstance(v, dict):
            v = v.get("hex", v.get("family") or "")
        lines.append(f"  --{var_name}: {v};")
    lines.append("}")
    return "\n".join(lines) + "\n"


def render_port(root: pathlib.Path, port: str, emit: bool):
    meta = read_meta(root / "ports", port)
    palette = load_palette(root)
    if meta["format"] == "css":
        text = render_css(meta, palette)
    else:
        print(f"  (format '{meta['format']}' not implemented yet — skipping {port})")
        return None
    out = root / "ports" / port / meta["generated"]
    out.parent.mkdir(parents=True, exist_ok=True)
    if emit:
        out.write_text(text)
    print(f"  {port}: would write {out.relative_to(root)} (emit={'yes' if emit else 'no'})")
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port")
    ap.add_argument("--root", default=str(pathlib.Path(__file__).parent.parent))
    ap.add_argument("--emit", action="store_true", help="actually write files")
    args = ap.parse_args()

    root = pathlib.Path(args.root)
    ports_root = root / "ports"
    if not ports_root.is_dir():
        print("ok: no ports/ directory")
        return

    if args.port:
        names = [args.port]
    else:
        names = sorted(p.name for p in ports_root.iterdir()
                       if p.is_dir() and (p / "meta.yaml").exists())

    for name in names:
        render_port(root, name, args.emit)


if __name__ == "__main__":
    main()
