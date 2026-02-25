#!/usr/bin/env python3
"""
Convert an SVG path (or SVG file) into VB6 `SpaceObject` angle/radius pairs.

Requires: svgpathtools (pip install svgpathtools)

Example:
  python svg_to_vb_angles.py --svg-file ship.svg --scale 1.1 --samples 400

You can paste your path string with --path "M...Z" instead of --svg-file.
The script prints VB6 assignment lines you can paste into `Form1.frm`.
"""
import argparse
import math
import sys
from svgpathtools import svg2paths, parse_path


def sample_path_from_file(svg_file, samples=400):
    paths, attributes = svg2paths(svg_file)
    if not paths:
        raise ValueError('No paths found in SVG')
    # join all paths into one polyline by sampling each
    pts = []
    per_path = max(10, samples // len(paths))
    for p in paths:
        for i in range(per_path):
            t = i / float(per_path)
            pt = p.point(t)
            pts.append((pt.real, pt.imag))
    return pts


def sample_path_from_string(path_str, samples=400):
    p = parse_path(path_str)
    pts = []
    for i in range(samples):
        t = i / float(samples)
        pt = p.point(t)
        pts.append((pt.real, pt.imag))
    return pts


def centroid(pts):
    x = sum(p[0] for p in pts) / len(pts)
    y = sum(p[1] for p in pts) / len(pts)
    return x, y


def to_polar(pts, center, scale=1.0, max_points=40):
    # reduce to roughly max_points by sampling uniformly
    n = len(pts)
    if n == 0:
        return []
    step = max(1, n // max_points)
    out = []
    for i in range(0, n, step):
        x, y = pts[i]
        dx = (x - center[0]) * scale
        dy = (center[1] - y) * scale  # flip Y (SVG y-down -> Cartesian y-up)
        r = math.hypot(dx, dy)
        ang = math.degrees(math.atan2(dy, dx))
        if ang < 0:
            ang += 360
        out.append((int(round(ang)) % 360, int(round(r))))
    # ensure unique consecutive angles and limit size
    filtered = []
    last = None
    for a, r in out:
        if last is None or (a != last[0] or r != last[1]):
            filtered.append((a, r))
            last = (a, r)
    return filtered[:max_points]


def print_vb_assignments(pairs, obj_index=0, start_index=10):
    lines = []
    idx = start_index
    for ang, rad in pairs:
        lines.append(f"SpaceObject({obj_index}, {idx}) = {ang}")
        lines.append(f"SpaceObject({obj_index}, {idx+1}) = {rad}")
        idx += 2
    lines.append(f"SpaceObject({obj_index}, {idx}) = -1")
    print('\n'.join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--svg-file', help='SVG file to read')
    ap.add_argument('--path', help='SVG path string (use quotes)')
    ap.add_argument('--scale', type=float, default=1.1, help='Scale factor to enlarge the shape')
    ap.add_argument('--samples', type=int, default=800, help='Number of samples to take along the path(s)')
    ap.add_argument('--obj', type=int, default=0, help='SpaceObject index to generate for')
    ap.add_argument('--start', type=int, default=10, help='Start property index for angle/radius pairs')
    args = ap.parse_args()

    if not args.svg_file and not args.path:
        ap.error('Either --svg-file or --path must be provided')

    if args.svg_file:
        pts = sample_path_from_file(args.svg_file, samples=args.samples)
    else:
        pts = sample_path_from_string(args.path, samples=args.samples)

    cx, cy = centroid(pts)
    pairs = to_polar(pts, (cx, cy), scale=args.scale)
    print(f"' Center used: {cx:.2f}, {cy:.2f}")
    print_vb_assignments(pairs, obj_index=args.obj, start_index=args.start)


if __name__ == '__main__':
    main()
