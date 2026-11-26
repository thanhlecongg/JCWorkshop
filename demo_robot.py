"""Demo: a delivery robot brings lunch across a mini campus. It goes around a cart, keeps out of a no-entry
room, and waits for a student who walks across its way. The walk is saved as an animated GIF.

Run:  python demo_robot.py
Then click  out/robot_demo.gif  in the VS Code Explorer (left bar) to watch it.

In the workshop you will build the robot's brain yourself, step by step, with an AI coding agent.
(The picture-drawing code below is a small copy of what the workshop project uses.)
"""
import os
import random
from collections import deque

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "robot_demo.gif")

# ------------------------------------------------------------------ the world
# # wall   . floor   S start   D destination (a hungry student)   R no-entry room   O parked cart
MAP = [
    "############",
    "#S....#....#",
    "#.....#..RR#",
    "#..O.......D",
    "#.....#.RR.#",
    "#.....#....#",
    "############",
]
MAP = [row.ljust(12, "#") for row in MAP]
PERSON = (7, 2, 0, 1, 3)  # (x, y, dx, dy, n): walks 3 cells down, then back up, forever (right by the door)
MOVES = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}

TILE = 64
COL = {
    "floor1": (246, 242, 234), "floor2": (240, 235, 225), "grid": (225, 219, 207), "wall": (84, 90, 104),
    "wall_hi": (112, 119, 135), "wall_lo": (58, 63, 74), "restricted": (251, 208, 208), "red": (214, 69, 65),
    "cart": (240, 150, 40), "goal": (58, 168, 96), "start": (178, 210, 247), "robot": (47, 107, 224),
    "robot_dark": (30, 78, 170), "trail": (125, 165, 238), "text": (40, 40, 48), "muted": (112, 116, 128),
    "space": (226, 214, 245), "person": (146, 88, 198), "skin": (255, 224, 189), "face": (255, 205, 60),
    "box": (250, 196, 62), "ribbon": (214, 69, 65), "good": (40, 140, 70), "header": (32, 40, 64),
}


def font(size):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # very old Pillow
        return ImageFont.load_default()


def find(symbol):
    for y, row in enumerate(MAP):
        for x, ch in enumerate(row):
            if ch == symbol:
                return x, y


def person_at(t):
    x, y, dx, dy, n = PERSON
    k = t % (2 * n)
    off = k if k <= n else 2 * n - k
    return x + dx * off, y + dy * off


def blocked(x, y):
    return not (0 <= y < len(MAP) and 0 <= x < len(MAP[0])) or MAP[y][x] in "#O"


def restricted(x, y):
    return MAP[y][x] == "R"


def too_close(cell, person):
    return abs(cell[0] - person[0]) + abs(cell[1] - person[1]) <= 1


def plan_first_move(pos, goal):
    """Shortest route that avoids walls, carts and the no-entry room (breadth-first search). Returns the first move."""
    queue, came = deque([pos]), {pos: None}
    while queue:
        cur = queue.popleft()
        if cur == goal:
            break
        for name, (dx, dy) in MOVES.items():
            nxt = (cur[0] + dx, cur[1] + dy)
            if nxt not in came and not blocked(*nxt) and not restricted(*nxt):
                came[nxt] = (cur, name)
                queue.append(nxt)
    if goal not in came:
        return None
    step = goal
    while came[step][0] != pos:
        step = came[step][0]
    return came[step][1]


# ------------------------------------------------------------------ drawing
def draw_tile(d, x, y, ch, mood):
    t = TILE
    x0, y0, x1, y1 = x, y, x + t - 1, y + t - 1
    if ch == "#":
        d.rectangle([x0, y0, x1, y1], fill=COL["wall"])
        d.rectangle([x0, y0, x1, y0 + 5], fill=COL["wall_hi"])
        d.rectangle([x0, y1 - 5, x1, y1], fill=COL["wall_lo"])
        return
    d.rectangle([x0, y0, x1, y1], fill=COL["floor1"] if ((x // t) + (y // t)) % 2 == 0 else COL["floor2"], outline=COL["grid"])
    if ch == "S":
        d.rounded_rectangle([x0 + 5, y0 + 5, x1 - 5, y1 - 5], radius=10, fill=COL["start"])
        d.text((x0 + t // 2, y1 - 10), "start", fill=COL["muted"], font=font(12), anchor="mm")
    elif ch == "D":
        d.rounded_rectangle([x0 + 3, y0 + 3, x1 - 3, y1 - 3], radius=12, fill=COL["goal"])
        cx, cy, r = x0 + t // 2, y0 + t // 2 + 2, t // 3
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=COL["face"], outline=(200, 150, 20), width=2)
        for ex in (-r // 3, r // 3):
            d.ellipse([cx + ex - 3, cy - r // 3 - 3, cx + ex + 3, cy - r // 3 + 3], fill=COL["text"])
        m = r // 2
        if mood == "happy":
            d.arc([cx - m, cy - m // 2, cx + m, cy + m], 20, 160, fill=COL["text"], width=3)
        elif mood == "sad":
            d.arc([cx - m, cy + m // 3, cx + m, cy + m * 2], 200, 340, fill=COL["text"], width=3)
        else:
            d.line([cx - m // 2, cy + m // 2, cx + m // 2, cy + m // 2], fill=COL["text"], width=3)
    elif ch == "R":
        d.rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], fill=COL["restricted"])
        for k in range(-t, t, 12):
            d.line([x0 + k, y1, x0 + k + t, y0], fill=(240, 160, 160), width=2)
        d.rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], outline=COL["red"], width=3)
        cx, cy, r = x0 + t // 2, y0 + t // 2, t // 4
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=COL["red"])
        d.rectangle([cx - r + 4, cy - 3, cx + r - 4, cy + 3], fill="white")
    elif ch == "O":
        d.rounded_rectangle([x0 + 9, y0 + 14, x1 - 9, y1 - 22], radius=5, fill=COL["cart"], outline=(170, 100, 20), width=2)
        for wx in (x0 + 20, x1 - 20):
            d.ellipse([wx - 6, y1 - 24, wx + 6, y1 - 12], fill=(60, 60, 60))
        d.text((x0 + t // 2, y0 + 28), "cart", fill="white", font=font(13), anchor="mm")


def draw_robot(d, cx, cy, happy, carrying, alert):
    # wheels and body
    for wx in (-14, 14):
        d.ellipse([cx + wx - 7, cy + 14, cx + wx + 7, cy + 28], fill=(50, 54, 64))
    d.rounded_rectangle([cx - 22, cy - 18, cx + 22, cy + 20], radius=12, fill=COL["robot"], outline=COL["robot_dark"], width=3)
    # antenna
    d.line([cx, cy - 18, cx, cy - 30], fill=COL["robot_dark"], width=3)
    d.ellipse([cx - 5, cy - 36, cx + 5, cy - 26], fill=COL["red"] if alert else (255, 224, 110))
    # face screen
    d.rounded_rectangle([cx - 16, cy - 11, cx + 16, cy + 9], radius=7, fill=(236, 244, 255))
    for ex in (-7, 7):
        if happy:
            d.arc([cx + ex - 4, cy - 6, cx + ex + 4, cy + 2], 200, 340, fill=COL["text"], width=3)
        else:
            d.ellipse([cx + ex - 3, cy - 5, cx + ex + 3, cy + 1], fill=COL["text"])
    d.arc([cx - 6, cy - 3, cx + 6, cy + 6], 20, 160, fill=COL["text"], width=2)
    if carrying:  # the lunch parcel
        d.rounded_rectangle([cx - 11, cy - 34, cx + 11, cy - 18], radius=3, fill=COL["box"], outline=(190, 140, 20), width=2)
        d.line([cx, cy - 34, cx, cy - 18], fill=COL["ribbon"], width=3)


def draw_person(d, cx, cy):
    d.rounded_rectangle([cx - 13, cy - 2, cx + 13, cy + 24], radius=9, fill=COL["person"])
    d.ellipse([cx - 10, cy - 24, cx + 10, cy - 4], fill=COL["skin"], outline=COL["person"], width=2)
    d.pieslice([cx - 11, cy - 27, cx + 11, cy - 7], 180, 360, fill=(70, 50, 40))


def bubble(d, text, cx, top, bottom, width, header):
    f = font(15)
    l, t_, r, b = d.textbbox((0, 0), text, font=f)
    w, h = r - l + 18, b - t_ + 14
    x0 = max(4, min(width - w - 4, cx - w // 2))
    above = top - h - 12 >= header + 2
    y0 = top - h - 12 if above else bottom + 12
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=9, fill="white", outline=COL["robot"], width=2)
    ty = y0 + h if above else y0
    d.polygon([(cx - 6, ty), (cx + 6, ty), (cx, ty + (10 if above else -10))], fill="white", outline=COL["robot"])
    d.line([(cx - 5, ty), (cx + 5, ty)], fill="white", width=3)
    d.text((x0 + 9, y0 + h // 2), text, fill=COL["text"], font=f, anchor="lm")


def confetti(d, width, height, seed, header):
    rnd = random.Random(seed)
    for _ in range(70):
        x, y = rnd.randrange(width), rnd.randrange(header, height)
        c = rnd.choice([(250, 196, 62), (214, 69, 65), (47, 107, 224), (58, 168, 96), (146, 88, 198)])
        if rnd.random() < 0.5:
            d.rectangle([x, y, x + 7, y + 4], fill=c)
        else:
            d.ellipse([x, y, x + 6, y + 6], fill=c)


def frame(pos, trail, person, say, caption, stats, mood, carrying, happy, alert, party=0):
    t, header, bar = TILE, 46, 74
    w, h = len(MAP[0]) * t, len(MAP) * t
    img = Image.new("RGB", (w, header + h + bar), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, header], fill=COL["header"])
    d.text((14, header // 2), "Campus Delivery Robot", fill="white", font=font(22), anchor="lm")
    d.text((w - 14, header // 2), "built on MiniGrid  |  you will build its brain", fill=(170, 180, 205), font=font(14), anchor="rm")
    world = Image.new("RGB", (w, h), "white")
    wd = ImageDraw.Draw(world)
    for y, row in enumerate(MAP):
        for x, ch in enumerate(row):
            draw_tile(wd, x * t, y * t, ch, mood)
    # the person's personal space (the robot must stay out of the purple squares)
    if person:
        px, py = person
        for ddx, ddy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            cx_, cy_ = px + ddx, py + ddy
            if 0 <= cx_ < len(MAP[0]) and 0 <= cy_ < len(MAP) and MAP[cy_][cx_] != "#":
                wd.rectangle([cx_ * t + 2, cy_ * t + 2, (cx_ + 1) * t - 3, (cy_ + 1) * t - 3], fill=COL["space"])
    pts = [(x * t + t // 2, y * t + t // 2) for x, y in trail]
    if len(pts) > 1:
        wd.line(pts, fill=COL["trail"], width=6, joint="curve")
    for x, y in pts[:-1]:
        wd.ellipse([x - 5, y - 5, x + 5, y + 5], fill=COL["trail"])
    if person:
        draw_person(wd, person[0] * t + t // 2, person[1] * t + t // 2)
    rx, ry = pos[0] * t + t // 2, pos[1] * t + t // 2
    draw_robot(wd, rx, ry, happy, carrying, alert)
    if say:
        bubble(wd, say, rx, ry - 38, ry + 30, w, 2)
    if party:
        confetti(wd, w, h, party, 0)
    img.paste(world, (0, header))
    d.text((12, header + h + 24), caption, fill=COL["good"] if "Delivered" in caption else COL["text"], font=font(20), anchor="lm")
    d.text((12, header + h + 54), stats, fill=COL["muted"], font=font(15), anchor="lm")
    return np.asarray(img)


# ------------------------------------------------------------------ the story
def stats_line(steps, waits, close, entered):
    return f"steps {steps}   waits {waits}   no-entry room entered {entered}x   too close to people {close}x"


def choose_move(pos, goal, person_next):
    """The robot's rule: take the planned step, but never END a step on or next to a person.
    If the planned step is unsafe: wait; if waiting is unsafe too: step aside. Returns (move, new_position, planned_move)."""
    planned = plan_first_move(pos, goal)
    if planned is None:
        return None, pos, None
    for move in [planned, "wait"] + [m for m in MOVES if m != planned]:
        dx, dy = MOVES.get(move, (0, 0))
        new = (pos[0] + dx, pos[1] + dy)
        if move != "wait" and (blocked(*new) or restricted(*new)):
            continue
        if not too_close(new, person_next):
            return move, new, planned
    return "wait", pos, planned


def run(person=None):
    global PERSON
    if person:
        PERSON = person
    start, goal = find("S"), find("D")
    pos, trail, steps, waits, close, entered = start, [start], 0, 0, 0, 0
    told = set()
    frames = [frame(pos, trail, person_at(0), "Lunch for a hungry student!", "Start", stats_line(0, 0, 0, 0), "sad", True, False, False)]
    for t in range(80):
        if pos == goal:
            break
        person_next = person_at(t + 1)
        move, nxt, planned = choose_move(pos, goal, person_next)
        if move is None:
            break
        say, alert = "", False
        if move != planned:
            alert = True
            say = "A student is close. I wait!" if move == "wait" else "A student is close. I step aside!"
        elif "cart" not in told and abs(nxt[0] - 3) + abs(nxt[1] - 3) <= 2:
            say = "A cart! I go around it."
            told.add("cart")
        elif "door" not in told and nxt == (6, 3):
            say = "Through the door..."
            told.add("door")
        elif "near" not in told and abs(nxt[0] - goal[0]) + abs(nxt[1] - goal[1]) <= 2:
            say = "Almost there!"
            told.add("near")
        waits += move == "wait"
        close += too_close(nxt, person_next)
        entered += restricted(*nxt)
        pos, steps = nxt, steps + 1
        trail.append(pos)
        mood = "sad" if steps < 6 else "ok" if steps < 14 else "happy"
        frames.append(frame(pos, trail, person_next, say, f"step {steps}: {move}", stats_line(steps, waits, close, entered), mood, True, False, alert))
    delivered = pos == goal
    for i in range(3):  # celebrate
        frames.append(frame(pos, trail, person_at(steps + 1), "Lunch delivered! Thank you!" if delivered else "",
                            f"Delivered in {steps} steps!" if delivered else "Something went wrong",
                            stats_line(steps, waits, close, entered), "happy", False, True, False, party=i + 1 if delivered else 0))
    return frames, delivered, steps, waits, close, entered


def make_demo(path=OUT):
    """Runs the demo and saves the GIF. Returns (pictures, delivered, steps, waits)."""
    frames, delivered, steps, waits, close, entered = run()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    imgs = [Image.fromarray(f) for f in frames]
    durations = [380] * (len(imgs) - 3) + [500, 500, 2600]
    imgs[0].save(path, save_all=True, append_images=imgs[1:], duration=durations, loop=0)
    return len(imgs), delivered and close == 0 and entered == 0, steps, waits


if __name__ == "__main__":
    n, ok, steps, waits = make_demo()
    print(f"Saved {OUT} ({n} pictures).")
    print(f"The robot delivered the lunch in {steps} steps (it waited {waits} time(s))." if ok else "The robot did NOT deliver (something is wrong).")
