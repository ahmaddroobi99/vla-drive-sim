#!/usr/bin/env python3
from pathlib import Path
import math
from PIL import Image, ImageDraw

OUT = Path(__file__).parent / "gifs"
OUT.mkdir(exist_ok=True)
W, H = 640, 280

def path(take_exit, which, n=180):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = 24 + t * 592
        y = 168 + math.sin(t * math.pi * 1.4) * 12
        if take_exit and which == 1 and 0.38 < t < 0.78:
            u = (t - 0.38) / 0.4
            y -= math.sin(u * math.pi) * 78
        if take_exit and which == 2 and 0.58 < t < 0.96:
            u = (t - 0.58) / 0.38
            y -= math.sin(u * math.pi) * 86
        pts.append((x, y))
    return pts

STRAIGHT = path(False, 0)
EXIT1 = path(True, 1)
EXIT2 = path(True, 2)

def nearest(pts, p):
    best, d2 = 0, 1e18
    for i, q in enumerate(pts):
        v = (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2
        if v < d2:
            d2, best = v, i
    return best

def heading(pts, i):
    a = pts[max(0, i)]
    b = pts[min(len(pts) - 1, i + 3)]
    return math.atan2(b[1] - a[1], b[0] - a[0])

def draw_frame(car, label, steer):
    im = Image.new("RGB", (W, H), (7, 8, 12))
    d = ImageDraw.Draw(im)
    def stroke(path, color, width):
        d.line(path, fill=color, width=width, joint="curve")
    stroke(STRAIGHT, (26, 35, 48), 36)
    stroke(EXIT1, (26, 35, 48), 28)
    stroke(EXIT2, (26, 35, 48), 28)
    stroke(STRAIGHT, (201, 214, 232), 2)
    d.text((16, 12), label, fill=(233, 168, 255))
    d.text((16, H - 22), f"steer {steer:+.1f} deg   v {(car['v']*3.6):.1f} km/h", fill=(201, 214, 232))
    x, y, yaw = car["x"], car["y"], car["yaw"]
    ca, sa = math.cos(yaw), math.sin(yaw)
    body = [(-16, -8), (16, -8), (20, 0), (16, 8), (-16, 8)]
    poly = [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in body]
    d.polygon(poly, outline=(214, 195, 106), fill=(28, 26, 14))
    return im

def simulate(target, label, name, frames=48):
    car = {"x": 40.0, "y": 168.0, "yaw": 0.0, "v": 7.0}
    imgs = []
    for _ in range(frames):
        i = nearest(target, (car["x"], car["y"]))
        want = heading(target, min(len(target) - 1, i + 6))
        err = (want - car["yaw"] + math.pi) % (2 * math.pi) - math.pi
        steer = max(-26, min(26, err * 42))
        dt = 0.08
        car["v"] = max(4.0, min(12.0, car["v"] + 1.4 * dt))
        car["yaw"] += (car["v"] / 2.6) * math.tan(math.radians(steer)) * dt
        car["x"] += math.cos(car["yaw"]) * car["v"] * dt * 7.2
        car["y"] += math.sin(car["yaw"]) * car["v"] * dt * 7.2
        imgs.append(draw_frame(car, label, steer))
    dest = OUT / name
    imgs[0].save(dest, save_all=True, append_images=imgs[1:], duration=70, loop=0, optimize=True)
    print("wrote", dest)

if __name__ == "__main__":
    simulate(EXIT2, "take the second exit", "take-second-exit.gif")
    simulate(EXIT1, "take the first exit", "take-first-exit.gif")
    simulate(STRAIGHT, "stay in lane", "stay-in-lane.gif")
