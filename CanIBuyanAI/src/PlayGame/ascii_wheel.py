import math
import argparse


def draw_ascii_wheel(values, radius=12, ring_char='o', spoke_char='|', center_char='@', label_style='short'):
    """
    Render an ASCII wheel with the provided segment values.

    - values: list of segment values around the wheel, clockwise starting at 3 o'clock
    - radius: wheel radius in characters (increase for more detail)
    - ring_char: character used for the circular ring
    - spoke_char: character used for segment boundaries
    - center_char: center mark
    - label_style: 'short' -> BK/0/numbers, 'long' -> BANKRUPT/LOSE TURN/numbers
    """
    n = len(values)
    width = 2 * radius + 20  # extra margin for labels
    height = 2 * radius + 10
    cx, cy = width // 2, height // 2

    grid = [[' ' for _ in range(width)] for _ in range(height)]

    # Draw outer ring
    for y in range(height):
        for x in range(width):
            d = math.hypot(x - cx, y - cy)
            if abs(d - radius) <= 0.6:
                grid[y][x] = ring_char

    # Draw spokes (segment boundaries)
    for i in range(n):
        ang = 2 * math.pi * (i / n)
        rr = 0.0
        while rr <= radius:
            x = int(round(cx + rr * math.cos(ang)))
            y = int(round(cy - rr * math.sin(ang)))
            if 0 <= x < width and 0 <= y < height:
                grid[y][x] = spoke_char
            rr += 0.5

    # Center mark
    if 0 <= cx < width and 0 <= cy < height:
        grid[cy][cx] = center_char

    def label_for(v):
        if label_style == 'long':
            if v == -1:
                return 'BANKRUPT'
            if v == 0:
                return 'LOSE TURN'
        else:
            if v == -1:
                return 'BK'
            if v == 0:
                return '0'
        return str(v)

    # Place labels near the outer ring at mid-angle of each segment
    for i, v in enumerate(values):
        mid = 2 * math.pi * ((i + 0.5) / n)
        lx = int(round(cx + (radius + 2) * math.cos(mid)))
        ly = int(round(cy - (radius + 2) * math.sin(mid)))
        s = label_for(v)
        start_x = lx - len(s) // 2
        for j, ch in enumerate(s):
            x = start_x + j
            if 0 <= x < width and 0 <= ly < height:
                grid[ly][x] = ch

    print('\n'.join(''.join(row).rstrip() for row in grid))


def parse_values_arg(raw):
    parts = [p.strip() for p in raw.split(',') if p.strip()]
    out = []
    for p in parts:
        if p.upper() in {'BK', 'BANKRUPT'}:
            out.append(-1)
        elif p.upper() in {'LT', 'LOSE', 'LOSETURN', 'LOSE_TURN'}:
            out.append(0)
        else:
            out.append(int(p))
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ASCII wheel renderer')
    parser.add_argument('--values', type=str, default=None,
                        help='Comma-separated values, e.g. 0,-1,500,550,... (-1 for BANKRUPT, 0 for LOSE TURN)')
    parser.add_argument('--radius', type=int, default=12, help='Wheel radius (chars)')
    parser.add_argument('--label', choices=['short', 'long'], default='short', help='Label style')

    args = parser.parse_args()

    default_values = [0,-1,500,550,600,650,700,750,800,850,900,-1,500,550,600,650,700,750,800,850,900,500,550,600]
    values = parse_values_arg(args.values) if args.values else default_values

    draw_ascii_wheel(values, radius=args.radius, label_style=args.label)
