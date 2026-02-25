#!/usr/bin/env python3
"""
Symmetrize VB6 SpaceObject angle/radius assignments in a Form1.frm file.
It finds SpaceObject(obj, start..)= pairs until -1, mirrors angles across the vertical axis
(angle -> (360 - angle) % 360), averages radii for matching pairs, and writes
symmetrized assignments to stdout.
"""
import re
import argparse


def read_pairs_from_file(frm_path, obj=0, start=10):
    with open(frm_path, 'r', encoding='utf-8') as f:
        text = f.read()
    pattern = re.compile(rf"SpaceObject\({obj},\s*({start}|{start+2}|{start+4}|\d+)\)\s*=\s*(-?\d+)")
    # Simpler: find the block starting at exact start index for this object
    block_pattern = re.compile(rf"SpaceObject\({obj},\s*{start}\)\s*=\s*-?\d+(.+?)SpaceObject\({obj},\s*\d+\)\s*=\s*-1", re.S)
    m = block_pattern.search(text)
    if not m:
        # fallback: collect sequential pairs starting from start until -1 encountered
        vals = {}
        idx = start
        while True:
            pat = re.search(rf"SpaceObject\({obj},\s*{idx}\)\s*=\s*(-?\d+)", text)
            if not pat:
                break
            v = int(pat.group(1))
            if v == -1:
                break
            vals[idx] = v
            idx += 1
        # convert to pairs
        pairs = []
        i = start
        while i in vals:
            a = vals.get(i)
            b = vals.get(i+1)
            if a is None or b is None:
                break
            pairs.append((int(a)%360, int(b)))
            i += 2
        return pairs
    block = m.group(0)
    # extract all angle/radius from block
    pairs = []
    for pm in re.finditer(rf"SpaceObject\({obj},\s*(\d+)\)\s*=\s*(-?\d+)", m.group(0)):
        idx = int(pm.group(1))
        val = int(pm.group(2))
        pairs.append((idx, val))
    # sort by index and pair them
    pairs.sort()
    out = []
    i = 0
    while i < len(pairs):
        idx, a = pairs[i]
        if a == -1:
            break
        if i+1 < len(pairs):
            _, r = pairs[i+1]
            out.append((a%360, r))
            i += 2
        else:
            break
    return out


def symmetrize(pairs):
    # map angles to radii (choose average if duplicates)
    ad = {}
    for a, r in pairs:
        a = a % 360
        if a in ad:
            ad[a].append(r)
        else:
            ad[a] = [r]
    for k in list(ad.keys()):
        ad[k] = sum(ad[k]) / len(ad[k])
    # ensure mirrored pairs
    for a in list(ad.keys()):
        m = (-a) % 360
        if m not in ad:
            ad[m] = ad[a]
        else:
            avg = (ad[a] + ad[m]) / 2
            ad[a] = avg
            ad[m] = avg
    # convert back to sorted list of ints
    items = sorted(((int(round(a))%360, int(round(r))) for a,r in ad.items()), key=lambda x: x[0])
    # ensure angle 0 is first
    items.sort(key=lambda x: (0 if x[0]==0 else 1, x[0]))
    return items


def print_vb(pairs, obj=0, start=10, max_points=None):
    idx = start
    count = 0
    for a,r in pairs:
        if max_points and count>=max_points:
            break
        print(f"SpaceObject({obj}, {idx}) = {a}")
        print(f"SpaceObject({obj}, {idx+1}) = {r}")
        idx += 2
        count += 1
    print(f"SpaceObject({obj}, {idx}) = -1")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--frm', default='Form1.frm')
    ap.add_argument('--obj', type=int, default=0)
    ap.add_argument('--start', type=int, default=10)
    ap.add_argument('--max-points', type=int, default=48)
    args = ap.parse_args()

    pairs = read_pairs_from_file(args.frm, obj=args.obj, start=args.start)
    if not pairs:
        print("' No pairs found")
        return
    sym = symmetrize(pairs)
    print("' Symmetrized polygon")
    print_vb(sym, obj=args.obj, start=args.start, max_points=args.max_points)

if __name__ == '__main__':
    main()
