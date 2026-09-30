#!/usr/bin/env python3
"""
validate.py — drift check for the Dark Console suite.

Invariant: every hex value that appears in a *port's generated file* exists
in `palette.json`. A `#RRGGBB` or `#rgb` that surfaces outside `palette.json`
means a token is out of sync and the generation was bypassed.

Usage:
    python3 scripts/validate.py                 # check whole suite (all ports)
    python3 scripts/validate.py --port vscode   # check one port
    python3 scripts/validate.py --verbose       # print the diff

Exit codes:
    0  all good
    1  at least one hex not in palette.json
    2  missing or invalid palette.json
"""
import argparse
import json
import re
import sys
import pathlib

HEX_RE = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
HEX3_TO_6 = lambda h: "".join(c * 2 for c in h)


def load_palette(root: pathlib.Path) -> set[str] | None:
    p = root / "palette.json"
    if not p.exists():
        return None
    with p.open() as f:
        data = json.load(f)
    out = set()

    def walk(o):
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str):
            for m in HEX_RE.finditer(o):
                out.add(HEX3_TO_6(m.group(1)).upper())

    walk(data)
    return out


def generated_file_for(root: pathlib.Path, port: str) -> pathlib.Path | None:
    """
    Convention: each port declares its generated file at
    ports/<tool>/meta.yaml → `generated:` (relative to the *port's repo
    root*; if the port lives here under `ports/<tool>/`, resolve locally).

    A port with no `generated` field contributes nothing validatable.
    """
    meta = root / "ports" / port / "meta.yaml"
    if not meta.exists():
        return None
    # Minimal YAML parse: look for the `generated:` key (first scalar value)
    for line in meta.read_text().splitlines():
        if line.strip().startswith("generated:"):
            val = line.split(":", 1)[1].strip().strip('"').strip("'")
            if not val:
                return None
            local = (root / "ports" / port / val).resolve()
            if local.exists():
                return local
            return None
    return None


def check_port(root: pathlib.Path, port: str, palette: set[str], verbose: bool) -> list[str]:
    gfile = generated_file_for(root, port)
    if gfile is None:
        return []
    text = gfile.read_text(errors="replace")
    drift = []
    for m in HEX_RE.finditer(text):
        h = HEX3_TO_6(m.group(1)).upper()
        if h not in palette:
            drift.append(h)
            if verbose:
                line_no = text.count("\n", 0, m.start()) + 1
                print(f"    DRIFT {port}  {gfile.name}:{line_no}  #{h}")
    return sorted(set(drift))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", help="only check this port name (e.g. vscode)")
    ap.add_argument("--root", default=str(pathlib.Path(__file__).parent.parent),
                    help="root of the core repo")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    root = pathlib.Path(args.root)
    palette = load_palette(root)
    if palette is None:
        print(f"error: {root / 'palette.json'} missing", file=sys.stderr)
        sys.exit(2)

    ports_root = root / "ports"
    if not ports_root.is_dir():
        print(f"ok: no ports/ directory (nothing to validate)")
        sys.exit(0)

    if args.port:
        port_names = [args.port]
    else:
        port_names = sorted(p.name for p in ports_root.iterdir()
                            if p.is_dir() and (p / "meta.yaml").exists())

    all_drift = {}
    for name in port_names:
        d = check_port(root, name, palette, args.verbose)
        if d:
            all_drift[name] = d

    if all_drift:
        print(f"FAIL: {len(all_drift)} port(s) drifted from palette.json")
        for name, hs in all_drift.items():
            print(f"  {name}:")
            for h in hs:
                print(f"    #{h}")
        sys.exit(1)

    print(f"ok: {len(port_names)} port(s) validated against {len(palette)} palette tokens")


if __name__ == "__main__":
    main()
