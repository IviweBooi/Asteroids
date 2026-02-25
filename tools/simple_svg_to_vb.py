#!/usr/bin/env python3
"""
Lightweight SVG path parser for common commands (M, L, H, V, Z) to produce
VB6 SpaceObject angle/radius pairs. No external dependencies.

Usage:
  python simple_svg_to_vb.py --path "M...Z" --scale 1.1 --obj 0
"""
import argparse
import math
import re


def tokenize_path(path):
    # Insert a separator before each command letter
    tokens = re.findall(r"[MmLlHhVvZz]|-?\d*\.?\d+", path)
    return tokens


def parse_tokens(tokens):
    pts = []
    it = iter(tokens)
    curr_x = 0.0
    curr_y = 0.0
    start_x = None
    start_y = None
    last_cmd = None
    for t in it:
        if re.match(r"[MmLlHhVvZz]", t):
            cmd = t.upper()
            last_cmd = cmd
            if cmd == 'Z':
                if start_x is not None:
                    curr_x, curr_y = start_x, start_y
                    pts.append((curr_x, curr_y))
                continue
            if cmd in ('M','L'):
                # read pairs until next command or end
                # peek ahead in tokens
                while True:
                    # try to get next token; if next is a command letter, break
                    try:
                        nxt = next(it)
                    except StopIteration:
                        break
                    if re.match(r"[MmLlHhVvZz]", nxt):
                        # push back by moving iterator one step backwards is hard; instead
                        # set last_cmd and continue outer loop by prepping nxt
                        last = nxt
                        # python iterator can't push back; so we create a new iterator including nxt
                        tokens_remaining = [nxt] + list(it)
                        it = iter(tokens_remaining)
                        break
                    # nxt should be a number (x)
                    x = float(nxt)
                    try:
                        ytok = next(it)
                    except StopIteration:
                        break
                    if re.match(r"[MmLlHhVvZz]", ytok):
                        # malformed; stop
                        tokens_remaining = [ytok] + list(it)
                        it = iter(tokens_remaining)
                        break
                    y = float(ytok)
                    curr_x, curr_y = x, y
                    if start_x is None:
                        start_x, start_y = curr_x, curr_y
                    pts.append((curr_x, curr_y))
            elif cmd == 'H':
                # horizontal lines: read numbers until next command
                while True:
                    try:
                        nxt = next(it)
                    except StopIteration:
                        break
                    if re.match(r"[MmLlHhVvZz]", nxt):
                        tokens_remaining = [nxt] + list(it)
                        it = iter(tokens_remaining)
                        break
                    curr_x = float(nxt)
                    pts.append((curr_x, curr_y))
            elif cmd == 'V':
                while True:
                    try:
                        nxt = next(it)
                    except StopIteration:
                        break
                    if re.match(r"[MmLlHhVvZz]", nxt):
                        tokens_remaining = [nxt] + list(it)
                        it = iter(tokens_remaining)
                        break
                    curr_y = float(nxt)
                    pts.append((curr_x, curr_y))
        else:
            # unexpected number without explicit command: assume continuation of last command
            if last_cmd in ('M','L'):
                # t is x, next is y
                x = float(t)
                try:
                    y = float(next(it))
                except StopIteration:
                    break
                curr_x, curr_y = x, y
                if start_x is None:
                    start_x, start_y = curr_x, curr_y
                pts.append((curr_x, curr_y))
            elif last_cmd == 'H':
                curr_x = float(t)
                pts.append((curr_x, curr_y))
            elif last_cmd == 'V':
                curr_y = float(t)
                pts.append((curr_x, curr_y))
    return pts


def centroid(pts):
    x = sum(p[0] for p in pts) / len(pts)
    y = sum(p[1] for p in pts) / len(pts)
    return x, y


def to_polar(pts, center, scale=1.0, max_points=40):
    n = len(pts)
    if n == 0:
        return []
    step = max(1, n // max_points)
    out = []
    for i in range(0, n, step):
        x, y = pts[i]
        dx = (x - center[0]) * scale
        dy = (center[1] - y) * scale
        r = math.hypot(dx, dy)
        ang = math.degrees(math.atan2(dy, dx))
        if ang < 0:
            ang += 360
        out.append((int(round(ang)) % 360, int(round(r))))
    # filter duplicates
    filtered = []
    last = None
    for a, r in out:
        if last is None or (a != last[0] or r != last[1]):
            filtered.append((a, r))
            last = (a, r)
    return filtered[:max_points]


def print_vb(pairs, obj=0, start=10):
    idx = start
    for a, r in pairs:
        print(f"SpaceObject({obj}, {idx}) = {a}")
        print(f"SpaceObject({obj}, {idx+1}) = {r}")
        idx += 2
    print(f"SpaceObject({obj}, {idx}) = -1")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--path', required=True, help='SVG path string')
    ap.add_argument('--scale', type=float, default=1.1)
    ap.add_argument('--obj', type=int, default=0)
    ap.add_argument('--start', type=int, default=10)
    ap.add_argument('--max-points', type=int, default=40)
    args = ap.parse_args()

    tokens = tokenize_path(args.path)
    pts = parse_tokens(tokens)
    if not pts:
        print("' No points parsed from path")
        return
    cx, cy = centroid(pts)
    pairs = to_polar(pts, (cx, cy), scale=args.scale, max_points=args.max_points)
    print(f"' Center used: {cx:.2f}, {cy:.2f}")
    print_vb(pairs, obj=args.obj, start=args.start)


if __name__ == '__main__':
    main()
