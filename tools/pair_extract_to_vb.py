#!/usr/bin/env python3
"""
Extract sequential (x y) number pairs from an SVG path string and output VB6
SpaceObject angle/radius assignments. This is a best-effort extractor for paths
dominated by explicit coordinate pairs (M, L commands).
"""
import argparse
import math
import re


def extract_pairs(path):
    # find all occurrences of two numbers separated by whitespace or comma
    matches = re.findall(r"(-?\d*\.?\d+)[,\s]+(-?\d*\.?\d+)", path)
    pts = [(float(a), float(b)) for a,b in matches]
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
    # remove consecutive duplicates
    filtered = []
    last = None
    for a,r in out:
        if last is None or (a != last[0] or r != last[1]):
            filtered.append((a,r))
            last = (a,r)
    return filtered[:max_points]


def rotate_to_tip(pairs):
    # find the pair with the maximum radius and rotate angles so it becomes 0
    if not pairs:
        return pairs
    max_idx = max(range(len(pairs)), key=lambda i: pairs[i][1])
    rot = pairs[max_idx][0]
    rotated = [((a - rot) % 360, r) for a, r in pairs]
    return rotated


def print_vb(pairs, obj=0, start=10):
    idx = start
    for a,r in pairs:
        print(f"SpaceObject({obj}, {idx}) = {a}")
        print(f"SpaceObject({obj}, {idx+1}) = {r}")
        idx += 2
    print(f"SpaceObject({obj}, {idx}) = -1")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--path', required=False)
    ap.add_argument('--path-file', required=False, help='Read SVG path string from a file')
    ap.add_argument('--scale', type=float, default=1.1)
    ap.add_argument('--obj', type=int, default=0)
    ap.add_argument('--start', type=int, default=10)
    ap.add_argument('--max-points', type=int, default=40)
    ap.add_argument('--align-tip', action='store_true', help='Rotate polygon so largest-radius vertex is at angle 0')
    args = ap.parse_args()

    path_str = args.path
    if args.path_file:
        with open(args.path_file, 'r', encoding='utf-8') as f:
            path_str = f.read()
    if not path_str:
        print("' No path provided")
        return
    pts = extract_pairs(path_str)
    if not pts:
        print("' No coordinate pairs found")
        return
    cx, cy = centroid(pts)
    pairs = to_polar(pts, (cx, cy), scale=args.scale, max_points=args.max_points)
    if args.align_tip:
        pairs = rotate_to_tip(pairs)
    print(f"' Center used: {cx:.2f}, {cy:.2f}")
    print_vb(pairs, obj=args.obj, start=args.start)


if __name__ == '__main__':
    main()
