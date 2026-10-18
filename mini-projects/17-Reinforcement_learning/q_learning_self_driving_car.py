"""
Q-Learning Highway Dodger: HUMAN vs. AI Split-Screen Race (Easy / Normal / Nightmare).

Race head-to-head against a Q-Learning agent on two side-by-side highways with the EXACT
SAME traffic waves!

Three AI Difficulty Levels (all trained via tabular Q-Learning on startup):
  [1] EASY      - Rookie AI (trained for 25 episodes, epsilon = 0.22 -> makes mistakes)
  [2] NORMAL    - Contender AI (trained for 85 episodes, epsilon = 0.06 -> solid driver)
  [3] NIGHTMARE - Optimal Master AI (trained for 500 episodes, epsilon = 0.00 -> near-flawless)

Controls (click inside the window first):
  LEFT / RIGHT (or A / D) : Steer your blue car left / right one lane
  1 / 2 / 3               : Switch AI difficulty (1=Easy, 2=Normal, 3=Nightmare) & new race
  SPACE                   : Start race / Next round / Pause
  UP / DOWN               : Speed up / Slow down game pace

Run:  python q_learning_self_driving_car.py
"""

from pathlib import Path
import time

import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.gridspec import GridSpec

HERE = Path(__file__).resolve().parent
SPRITE_DIR = HERE / "sprites"


# ============================================================
# 0. TOP-DOWN CAR SPRITE GENERATOR & LOADER (.png files)
# ============================================================
def _hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _shade(rgb, factor):
    return tuple(int(np.clip(c * factor, 0, 255)) for c in rgb)


def make_car_png(path, body_hex, is_racer=False):
    """Draw a detailed top-down car (tires, shadows, contoured body, glass, lights) and save as RGBA PNG."""
    W, H = 160, 280
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    base = _hex_rgb(body_hex)
    dark = _shade(base, 0.62)
    light = _shade(base, 1.22)

    # 1) Drop shadow
    d.rounded_rectangle([24, 18, W - 16, H - 10], radius=34, fill=(0, 0, 0, 90))

    # 2) Four tires
    for ty in (42, H - 92):
        d.rounded_rectangle([10, ty, 30, ty + 48], radius=7, fill=(22, 22, 26, 255), outline=(60, 60, 65, 255), width=2)
        d.rounded_rectangle([W - 30, ty, W - 10, ty + 48], radius=7, fill=(22, 22, 26, 255), outline=(60, 60, 65, 255), width=2)

    # 3) Side mirrors
    d.polygon([(22, 96), (8, 104), (10, 116), (24, 114)], fill=dark)
    d.polygon([(W - 22, 96), (W - 8, 104), (W - 10, 116), (W - 24, 114)], fill=dark)

    # 4) Main chassis
    d.rounded_rectangle([20, 12, W - 20, H - 14], radius=34, fill=dark, outline=(25, 25, 30, 255), width=3)
    d.rounded_rectangle([26, 18, W - 26, H - 20], radius=28, fill=base)

    # 5) Hood & racing stripes for Human / AI racers
    d.rounded_rectangle([36, 26, W - 36, 92], radius=16, fill=light)
    if is_racer:
        d.rectangle([W // 2 - 16, 16, W // 2 - 5, H - 18], fill=(245, 245, 250, 235))
        d.rectangle([W // 2 + 5, 16, W // 2 + 16, H - 18], fill=(245, 245, 250, 235))

    # 6) Cabin (windshield, roof, rear window)
    d.polygon([(32, 88), (W - 32, 88), (W - 28, 212), (32, 212)], fill=(25, 32, 48, 255))
    d.polygon([(35, 92), (W - 35, 92), (W - 42, 126), (42, 126)], fill=(58, 86, 118, 255))
    d.polygon([(42, 95), (72, 95), (62, 122), (45, 122)], fill=(135, 175, 210, 130))
    d.rounded_rectangle([40, 128, W - 40, 182], radius=10, fill=base, outline=dark, width=2)
    if is_racer:
        d.rectangle([W // 2 - 14, 128, W // 2 - 5, 182], fill=(245, 245, 250, 235))
        d.rectangle([W // 2 + 5, 128, W // 2 + 14, 182], fill=(245, 245, 250, 235))
    d.polygon([(42, 186), (W - 42, 186), (W - 36, 208), (36, 208)], fill=(45, 68, 96, 255))

    # 7) Headlights & taillights
    d.rounded_rectangle([30, 13, 56, 24], radius=5, fill=(255, 250, 190, 255))
    d.rounded_rectangle([W - 56, 13, W - 30, 24], radius=5, fill=(255, 250, 190, 255))
    d.rounded_rectangle([30, H - 24, 58, H - 15], radius=4, fill=(255, 35, 35, 255))
    d.rounded_rectangle([W - 58, H - 24, W - 30, H - 15], radius=4, fill=(255, 35, 35, 255))

    img.save(path)


def _tilted_set(pil_img):
    return {
        0: np.asarray(pil_img),
        -1: np.asarray(pil_img.rotate(12, resample=Image.BICUBIC, expand=False)),
        1: np.asarray(pil_img.rotate(-12, resample=Image.BICUBIC, expand=False)),
    }


def load_sprites():
    """Ensure `.png` sprites exist in `sprites/` and load them as RGBA arrays."""
    SPRITE_DIR.mkdir(exist_ok=True)
    ai_path = SPRITE_DIR / "player_car.png"
    human_path = SPRITE_DIR / "human_car.png"
    if not ai_path.exists():
        make_car_png(ai_path, "#e6192e", is_racer=True)      # Crimson Red AI racer
    if not human_path.exists():
        make_car_png(human_path, "#1d63ff", is_racer=True)   # Electric Blue Human racer

    traffic_specs = [
        ("traffic_cyan.png", "#00b4d8"),
        ("traffic_gold.png", "#ffbe0b"),
        ("traffic_lime.png", "#70e000"),
        ("traffic_purple.png", "#9d4edd"),
        ("traffic_orange.png", "#ff6d00"),
        ("traffic_silver.png", "#adb5bd"),
    ]
    traffic_imgs = []
    for fname, col in traffic_specs:
        p = SPRITE_DIR / fname
        if not p.exists():
            make_car_png(p, col, is_racer=False)
        traffic_imgs.append(np.asarray(Image.open(p).convert("RGBA")))

    human_sprites = _tilted_set(Image.open(human_path).convert("RGBA"))
    ai_sprites = _tilted_set(Image.open(ai_path).convert("RGBA"))
    return human_sprites, ai_sprites, traffic_imgs


HUMAN_SPRITES, AI_SPRITES, TRAFFIC_SPRITES = load_sprites()

# ============================================================
# 1. GAME ENVIRONMENT & SYNCHRONIZED OBSTACLE GENERATOR
# ============================================================
N_LANES = 4
HIGHWAY_LEN = 26.0
PLAYER_Y = 3.2
CAR_W, CAR_L = 0.62, 2.0
HIT_MARGIN = 1.65
SPEED = 1.0
SPAWN_EVERY = 7
GOAL_DODGED = 50            # first to dodge 50 cars (or outlast the opponent) wins!
MAX_STEPS = 420

ACTIONS = [-1, 0, 1]        # left, stay, right
ACTION_NAMES = ["\u2190 LEFT", "\u2191 STAY", "\u2192 RIGHT"]

REWARD_SURVIVE = 0.2
REWARD_DODGE = 1.5
PENALTY_SWERVE = -0.15
REWARD_CRASH = -25.0

rng = np.random.default_rng()


def make_wave(wave_rng, y_base, prev_open):
    """
    Create one wave of 1-3 traffic cars that ALWAYS blocks `prev_open` (so nobody can
    camp in one lane) while guaranteeing a reachable new `open_lane` within <= 2 lanes.
    """
    n_cars = int(wave_rng.choice([1, 2, 2, 3]))
    reachable = [l for l in range(N_LANES) if abs(l - prev_open) <= 2 and l != prev_open]
    open_lane = int(wave_rng.choice(reachable))

    candidates = [l for l in range(N_LANES) if l != open_lane]
    # Always block the previous open lane so both Human and AI must keep weaving!
    chosen = [prev_open]
    others = [l for l in candidates if l != prev_open]
    if n_cars > 1:
        chosen += list(wave_rng.choice(others, size=n_cars - 1, replace=False))

    cars = []
    for l in chosen:
        jitter = float(wave_rng.uniform(-0.22, 0.22))
        s_idx = int(wave_rng.integers(len(TRAFFIC_SPRITES)))
        cars.append({"lane": int(l), "y": y_base + jitter, "sprite": s_idx, "passed": False})
    return cars, open_lane


class HighwayGame:
    def __init__(self, start_lane=1, initial_waves=None, is_human=False):
        self.lane = int(start_lane)
        self.prev_lane = self.lane
        self.is_human = is_human
        self.traffic = []
        self.dodged = 0
        self.scroll = 0.0
        self.step_count = 0
        self.crashed = False
        self.won = False
        self.last_open = self.lane
        if initial_waves is not None:
            self.traffic = [dict(c) for c in initial_waves]
        else:
            for y in (12.0, 19.0, 26.0):
                self.add_wave_from_rng(rng, y)

    def add_wave_from_rng(self, wave_rng, y_base):
        cars, self.last_open = make_wave(wave_rng, y_base, self.last_open)
        self.traffic.extend(cars)

    def add_cloned_wave(self, cars):
        self.traffic.extend(dict(c) for c in cars)

    def step(self, action_idx, auto_spawn=True):
        """Advance by 1 step. Return (reward, crashed, won)."""
        if self.crashed or self.won:
            return 0.0, self.crashed, self.won

        self.prev_lane = self.lane
        dlane = ACTIONS[action_idx]
        new_lane = self.lane + dlane
        self.step_count += 1
        self.scroll += SPEED

        # For AI training, hitting the guardrail is a crash; for Human player, clamp to road edge
        if new_lane < 0 or new_lane >= N_LANES:
            self.lane = int(np.clip(new_lane, 0, N_LANES - 1))
            if not self.is_human:
                self.crashed = True
                return REWARD_CRASH, True, False
            dlane = 0
        else:
            self.lane = new_lane

        newly_dodged = 0
        for car in self.traffic:
            car["y"] -= SPEED
            if car["lane"] == self.lane and abs(car["y"] - PLAYER_Y) < HIT_MARGIN:
                self.crashed = True
            if not car["passed"] and car["y"] <= PLAYER_Y - HIT_MARGIN:
                car["passed"] = True
                newly_dodged += 1

        self.traffic = [c for c in self.traffic if c["y"] > -3.0]
        if auto_spawn and self.step_count % SPAWN_EVERY == 0:
            self.add_wave_from_rng(rng, HIGHWAY_LEN - 1.0)

        if self.crashed:
            return REWARD_CRASH, True, False

        self.dodged += newly_dodged
        reward = REWARD_SURVIVE + newly_dodged * REWARD_DODGE + (PENALTY_SWERVE if dlane != 0 else 0.0)
        if self.dodged >= GOAL_DODGED:
            self.won = True
        return reward, False, self.won


# ============================================================
# 2. SENSORS & STATE (what the AI sees)
# ============================================================
RADAR_RANGE = 18.0
DIST_BINS = [SPEED + 0.05, 5.5 * SPEED]
BIN_NAMES = ["DANGER", "CLOSE", "CLEAR"]
ESCAPE_NAMES = ["GO LEFT", "STAY", "GO RIGHT"]
STATE_SHAPE = (3, 3, 3, 3)  # 81 states


def lane_clearances(game):
    dists = np.full(N_LANES, RADAR_RANGE)
    for car in game.traffic:
        if car["y"] - SPEED > PLAYER_Y - HIT_MARGIN:
            clearance = max(0.05, car["y"] - (PLAYER_Y + HIT_MARGIN))
            if clearance < dists[car["lane"]]:
                dists[car["lane"]] = clearance
    return dists


def sense_state(game):
    all_dists = lane_clearances(game)
    lane = game.lane

    left_d = 0.0 if lane == 0 else all_dists[lane - 1]
    front_d = all_dists[lane]
    right_d = 0.0 if lane == N_LANES - 1 else all_dists[lane + 1]

    left_bin = 0 if lane == 0 else int(np.digitize(left_d, DIST_BINS))
    front_bin = int(np.digitize(front_d, DIST_BINS))
    right_bin = 0 if lane == N_LANES - 1 else int(np.digitize(right_d, DIST_BINS))

    best_lane = int(np.argmax(all_dists))
    if all_dists[best_lane] <= front_d + 0.5:
        escape = 1
    elif best_lane < lane:
        escape = 0
    else:
        escape = 2

    return (left_d, front_d, right_d), (left_bin, front_bin, right_bin, escape)


# ============================================================
# 3. TRAIN THE 3 AI DIFFICULTY LEVELS (Easy, Normal, Nightmare)
# ============================================================
ALPHA = 0.25
GAMMA = 0.92

DIFFICULTY_SPECS = {
    "EASY": {
        "key": "1",
        "episodes": 45,
        "play_eps": 0.035,  # ~15-20 cars dodged before a rookie mistake
        "color": "#ff9f1c",
        "desc": "Rookie AI (45 train eps, 3.5% mistake rate)",
    },
    "NORMAL": {
        "key": "2",
        "episodes": 110,
        "play_eps": 0.012,  # ~30-40 cars dodged -> competitive match!
        "color": "#00b4d8",
        "desc": "Contender AI (110 train eps, 1.2% mistake rate)",
    },
    "NIGHTMARE": {
        "key": "3",
        "episodes": 400,
        "play_eps": 0.00,   # 0% mistakes -> pure optimal policy!
        "color": "#e6192e",
        "desc": "Optimal Master AI (400 train eps, 0% mistakes)",
    },
}


def train_model(n_episodes):
    """Train a Q-table for `n_episodes` and return (Q_table, moving_avg_curve)."""
    q_tab = np.zeros(STATE_SHAPE + (len(ACTIONS),))
    eps = 1.0
    decay = (0.01 / 1.0) ** (1.0 / max(1, n_episodes))
    scores, avg_curve = [], []

    for _ in range(n_episodes):
        g = HighwayGame(start_lane=int(rng.integers(N_LANES)))
        _, s = sense_state(g)
        for _ in range(MAX_STEPS):
            if rng.random() < eps:
                a = int(rng.integers(len(ACTIONS)))
            else:
                q_row = q_tab[s]
                a = int(rng.choice(np.flatnonzero(q_row == q_row.max())))
            r, crashed, won = g.step(a, auto_spawn=True)
            _, s_next = sense_state(g)
            sa = s + (a,)
            q_tab[sa] += ALPHA * (r + (0.0 if (crashed or won) else GAMMA * q_tab[s_next].max()) - q_tab[sa])
            s = s_next
            if crashed or won:
                break
        scores.append(g.dodged)
        avg_curve.append(float(np.mean(scores[-15:])))
        eps = max(0.01, eps * decay)
    return q_tab, avg_curve


MODELS = {}
CURVES = {}
for diff_name, spec in DIFFICULTY_SPECS.items():
    MODELS[diff_name], CURVES[diff_name] = train_model(spec["episodes"])


def ai_choose_action(diff_name, state):
    """Select an action using the chosen difficulty's Q-table and mistake rate."""
    q_tab = MODELS[diff_name]
    play_eps = DIFFICULTY_SPECS[diff_name]["play_eps"]
    if rng.random() < play_eps:
        # Pick a random non-wall action when making a mistake
        return int(rng.integers(len(ACTIONS))), True
    q_row = q_tab[state]
    return int(rng.choice(np.flatnonzero(q_row == q_row.max()))), False


# ============================================================
# 4. SPLIT-SCREEN VISUALIZATION (Human Highway | AI Highway | Brain)
# ============================================================
for k in ("keymap.fullscreen", "keymap.save", "keymap.back", "keymap.forward"):
    plt.rcParams[k] = []

ctrl = {
    "difficulty": "NORMAL",
    "delay": 0.055,         # comfortable human reaction speed (~18 steps/sec)
    "paused": False,
    "started": False,       # waits for key press on very first launch so window is focused
    "new_race": False,
    "human_queue": [],      # queued left/right taps from keyboard
    "wins_human": 0,
    "wins_ai": 0,
}
CMAP = plt.get_cmap("RdYlGn")

plt.ion()
fig = plt.figure(figsize=(17.5, 9.2))
fig.canvas.manager.set_window_title("Q-Learning Highway Dodger - YOU vs. AI Split-Screen Race")
gs = GridSpec(3, 3, figure=fig, width_ratios=[1.05, 1.05, 1.25], height_ratios=[0.95, 1.05, 1.0],
              hspace=0.48, wspace=0.20)

ax_human = fig.add_subplot(gs[:, 0])
ax_ai = fig.add_subplot(gs[:, 1])
ax_sens = fig.add_subplot(gs[0, 2])
ax_q = fig.add_subplot(gs[1, 2])
ax_curve = fig.add_subplot(gs[2, 2])


def setup_highway_axis(ax, player_sprites, border_col, show_radar=False):
    ax.set_facecolor("#2d6a3e")
    ax.axvspan(-0.5, N_LANES - 0.5, color="#2b2d34", zorder=0)
    ax.axvspan(-0.68, -0.5, color="#d90429", zorder=1)
    ax.axvspan(N_LANES - 0.5, N_LANES - 0.32, color="#d90429", zorder=1)

    l_lines = [ax.plot([], [], "--", color="white", alpha=0.55, linewidth=1.7, zorder=2)[0]
               for _ in range(1, N_LANES)]
    curbs = PolyCollection([], facecolors="white", edgecolors="none", zorder=2)
    ax.add_collection(curbs)
    trees, = ax.plot([], [], "o", color="#1b4332", markersize=13, zorder=2)

    r_lines = [ax.plot([], [], linewidth=2.3, alpha=0.85, zorder=3)[0] for _ in range(3)] if show_radar else []
    r_dots = ax.plot([], [], "o", color="white", markersize=5.5, zorder=4)[0] if show_radar else None

    p_img = ax.imshow(player_sprites[0], extent=[0, 1, 0, 1], aspect="auto", zorder=7)
    t_imgs = [
        ax.imshow(TRAFFIC_SPRITES[0], extent=[0, 1, 0, 1], aspect="auto", zorder=6, visible=False)
        for _ in range(16)
    ]
    hud = ax.text(0.5, 0.985, "", transform=ax.transAxes, ha="center", va="top",
                  fontsize=10, fontweight="bold", color="white", family="monospace",
                  bbox=dict(boxstyle="round,pad=0.35", facecolor="#111111", alpha=0.88, edgecolor=border_col),
                  zorder=10)
    banner = ax.text(0.5, 0.52, "", transform=ax.transAxes, ha="center", va="center",
                     fontsize=12.5, fontweight="bold", color="white",
                     bbox=dict(boxstyle="round,pad=0.6", facecolor="#111111", alpha=0.92, edgecolor="gold", lw=2),
                     zorder=12, visible=False)

    ax.set_xlim(-1.05, N_LANES + 0.05)
    ax.set_ylim(0, HIGHWAY_LEN)
    ax.set_xticks(range(N_LANES), [f"Lane {i + 1}" for i in range(N_LANES)])
    ax.set_yticks([])
    return {
        "ax": ax, "sprites": player_sprites, "lane_lines": l_lines, "curbs": curbs,
        "trees": trees, "radar_lines": r_lines, "radar_dots": r_dots,
        "player_img": p_img, "traffic_imgs": t_imgs, "hud": hud, "banner": banner,
    }


human_view = setup_highway_axis(ax_human, HUMAN_SPRITES, "#1d63ff", show_radar=False)
ai_view = setup_highway_axis(ax_ai, AI_SPRITES, "#e6192e", show_radar=True)

# --- Right top panel: AI Radar sensors ---
sens_names = ["LEFT LANE", "FRONT (AI)", "RIGHT LANE"]
sens_bars = ax_sens.barh(range(3), [0] * 3, color="gray", height=0.55)
sens_labels = [ax_sens.text(0, i, "", va="center", ha="left", fontsize=9, fontweight="bold")
               for i in range(3)]
ax_sens.set_yticks(range(3), sens_names)
ax_sens.invert_yaxis()
ax_sens.set_xlim(0, RADAR_RANGE * 1.25)
ax_sens.set_xlabel("AI clearance distance ahead")
for thresh in DIST_BINS:
    ax_sens.axvline(thresh, color="gray", linestyle=":", linewidth=0.9)

# --- Right middle panel: AI Q-values ---
q_bars = ax_q.bar(range(3), [0] * 3, color="steelblue", width=0.5)
q_labels = [ax_q.text(i, 0, "", ha="center", fontsize=9.5, fontweight="bold") for i in range(3)]
ax_q.set_xticks(range(3), ACTION_NAMES)
ax_q.set_ylim(-28, 16)
ax_q.axhline(0, color="gray", linewidth=0.6)
ax_q.set_ylabel("Q(s, a) weight")
eq_box = ax_q.text(0.02, 0.04, "", transform=ax_q.transAxes, fontsize=8.2, family="monospace",
                   va="bottom", ha="left",
                   bbox=dict(boxstyle="round,pad=0.28", facecolor="#f8f9fa", edgecolor="lightgray"))

# --- Right bottom panel: Training curves of Easy / Normal / Nightmare ---
ax_curve.set_title("How the 3 AI Difficulty Models Were Trained", fontsize=10.5)
ax_curve.set_xlabel("Training Episodes (log-scaled view)")
ax_curve.set_ylabel("Avg Cars Dodged")
ax_curve.set_ylim(-2, GOAL_DODGED + 5)
ax_curve.axhline(GOAL_DODGED, color="gold", linestyle=":", linewidth=1.2)
curve_lines = {}
for d_name, spec in DIFFICULTY_SPECS.items():
    c_data = CURVES[d_name]
    ln, = ax_curve.plot(range(1, len(c_data) + 1), c_data, color=spec["color"],
                        linewidth=2.0, alpha=0.85, label=f"[{spec['key']}] {d_name} ({spec['episodes']} ep)")
    curve_lines[d_name] = ln
ax_curve.set_xscale("log")
ax_curve.set_xlim(1, 550)
ax_curve.legend(loc="lower right", fontsize=8)

status = fig.text(0.5, 0.01, "", ha="center", fontsize=10, fontweight="bold", color="#222222")


def update_status():
    d_name = ctrl["difficulty"]
    spec = DIFFICULTY_SPECS[d_name]
    pause = "   [PAUSED]" if ctrl["paused"] else ""
    status.set_text(
        f"STEER: \u2190 / \u2192 (or A / D)   |   DIFFICULTY: [1] Easy  [2] Normal  [3] Nightmare "
        f"(Active: {d_name})   |   SPACE: Next Race / Pause   |   \u2191/\u2193: Speed{pause}"
    )
    for name, ln in curve_lines.items():
        ln.set_linewidth(3.2 if name == d_name else 1.4)
        ln.set_alpha(1.0 if name == d_name else 0.45)


def on_key(event):
    k = (event.key or "").lower()
    if k in ("left", "a"):
        ctrl["started"] = True
        if len(ctrl["human_queue"]) < 2:
            ctrl["human_queue"].append(0)   # LEFT
    elif k in ("right", "d"):
        ctrl["started"] = True
        if len(ctrl["human_queue"]) < 2:
            ctrl["human_queue"].append(2)   # RIGHT
    elif k in ("1", "2", "3"):
        ctrl["difficulty"] = {"1": "EASY", "2": "NORMAL", "3": "NIGHTMARE"}[k]
        ctrl["started"] = True
        ctrl["new_race"] = True
        ctrl["paused"] = False
    elif k in (" ", "enter", "return"):
        if not ctrl["started"]:
            ctrl["started"] = True
        elif ctrl["new_race"]:
            pass
        else:
            ctrl["paused"] = not ctrl["paused"]
    elif k == "up":
        ctrl["delay"] = max(0.015, ctrl["delay"] / 1.35)
    elif k == "down":
        ctrl["delay"] = min(0.15, ctrl["delay"] * 1.35)
    update_status()
    fig.canvas.draw_idle()


fig.canvas.mpl_connect("key_press_event", on_key)
update_status()


def window_open():
    return plt.fignum_exists(fig.number)


def wait(seconds):
    end = time.time() + seconds
    while True:
        if not window_open():
            raise SystemExit
        plt.pause(0.001 if seconds < 0.012 else 0.01)
        if not ctrl["paused"] and time.time() >= end:
            break


def rect_poly(x, y, w, h):
    return [[x - w / 2, y - h / 2], [x + w / 2, y - h / 2],
            [x + w / 2, y + h / 2], [x - w / 2, y + h / 2]]


def render_highway(view, game, player_x, scroll_val, tilt, action, dists=None):
    offset = -(scroll_val % 2.0)
    for l_idx, line in enumerate(view["lane_lines"], start=1):
        line.set_data([l_idx - 0.5, l_idx - 0.5], [offset - 2, HIGHWAY_LEN + 2])

    stripes = []
    for y in np.arange(offset, HIGHWAY_LEN + 2, 2.0):
        stripes.append(rect_poly(-0.59, y, 0.18, 1.0))
        stripes.append(rect_poly(N_LANES - 0.41, y, 0.18, 1.0))
    view["curbs"].set_verts(stripes)

    tree_y = np.arange(-(scroll_val % 4.0), HIGHWAY_LEN + 2, 4.0)
    tree_x = np.concatenate([np.full_like(tree_y, -0.9), np.full_like(tree_y, N_LANES - 0.1)])
    view["trees"].set_data(tree_x, np.tile(tree_y, 2))

    view["player_img"].set_data(view["sprites"][tilt])
    view["player_img"].set_extent([player_x - CAR_W / 2, player_x + CAR_W / 2,
                                   PLAYER_Y - CAR_L / 2, PLAYER_Y + CAR_L / 2])

    y_shift = game.scroll - scroll_val
    for idx, artist in enumerate(view["traffic_imgs"]):
        if idx < len(game.traffic):
            c = game.traffic[idx]
            cy = c["y"] + y_shift
            artist.set_data(TRAFFIC_SPRITES[c["sprite"]])
            artist.set_extent([c["lane"] - CAR_W / 2, c["lane"] + CAR_W / 2,
                               cy - CAR_L / 2, cy + CAR_L / 2])
            artist.set_visible(True)
        else:
            artist.set_visible(False)

    if view["radar_lines"] and dists is not None:
        hit_x, hit_y = [], []
        for i, dl in enumerate([-1, 0, 1]):
            target_lane = game.lane + dl
            d = dists[i]
            if 0 <= target_lane < N_LANES and not game.crashed:
                x0, y0 = player_x, PLAYER_Y + CAR_L / 2
                x1, y1 = target_lane, min(HIGHWAY_LEN - 0.5, PLAYER_Y + CAR_L / 2 + d)
                view["radar_lines"][i].set_data([x0, x1], [y0, y1])
                view["radar_lines"][i].set_color(CMAP(min(d / RADAR_RANGE, 1.0)))
                hit_x.append(x1)
                hit_y.append(y1)
            else:
                view["radar_lines"][i].set_data([], [])
        view["radar_dots"].set_data(hit_x, hit_y)

    state_tag = "CRASHED!" if game.crashed else ("FINISHED!" if game.won else ACTION_NAMES[action])
    view["hud"].set_text(f"DODGED: {game.dodged:02d}/{GOAL_DODGED}   |   {state_tag}")


def render_ai_brain(game, dists, state, action, explored):
    d_name = ctrl["difficulty"]
    q_tab = MODELS[d_name]
    for i, (bar, lbl) in enumerate(zip(sens_bars, sens_labels)):
        d = dists[i]
        bar.set_width(d)
        bar.set_color(CMAP(min(d / RADAR_RANGE, 1.0)))
        tag = "WALL!" if ((i == 0 and game.lane == 0) or (i == 2 and game.lane == N_LANES - 1)) else BIN_NAMES[state[i]]
        lbl.set_position((d + 0.4, i))
        lbl.set_text(f"{d:.1f} ({tag})")
    ax_sens.set_title(
        f"SCOREBOARD:  YOU {ctrl['wins_human']}  -  {ctrl['wins_ai']} AI\n"
        f"AI State s = ({BIN_NAMES[state[0]]}, {BIN_NAMES[state[1]]}, {BIN_NAMES[state[2]]}, {ESCAPE_NAMES[state[3]]})",
        fontsize=10,
    )

    q = q_tab[state]
    for i, (bar, lbl) in enumerate(zip(q_bars, q_labels)):
        bar.set_height(q[i])
        bar.set_color("darkorange" if i == action else "steelblue")
        y_pos = q[i] + 0.8 if q[i] >= 0 else q[i] - 2.4
        lbl.set_position((i, y_pos))
        lbl.set_text(f"{q[i]:+.1f}")
    mode_str = "MISTAKE (random)" if explored else "OPTIMAL Q-VALUE"
    ax_q.set_title(f"{d_name} AI Decision: {ACTION_NAMES[action]}  [{mode_str}]", fontsize=10.5)
    eq_box.set_text(f"{DIFFICULTY_SPECS[d_name]['desc']}\n"
                    f"Weights: LEFT={q[0]:+.1f}  STAY={q[1]:+.1f}  RIGHT={q[2]:+.1f}")


# ============================================================
# 5. MAIN RACE LOOP (Synchronized Human vs. AI Race)
# ============================================================
round_num = 1

while window_open():
    ctrl["new_race"] = False
    ctrl["human_queue"].clear()
    d_name = ctrl["difficulty"]

    # Create identical initial traffic waves for both screens
    wave_rng = np.random.default_rng()
    start_lane = 1
    init_cars = []
    last_open = start_lane
    for y_init in (13.0, 20.0, 27.0):
        w_cars, last_open = make_wave(wave_rng, y_init, last_open)
        init_cars.extend(w_cars)

    human_game = HighwayGame(start_lane=start_lane, initial_waves=init_cars, is_human=True)
    ai_game = HighwayGame(start_lane=start_lane, initial_waves=init_cars, is_human=False)
    human_game.last_open = last_open
    ai_game.last_open = last_open

    ai_dists, ai_state = sense_state(ai_game)
    render_highway(human_view, human_game, float(human_game.lane), 0.0, 0, 1)
    render_highway(ai_view, ai_game, float(ai_game.lane), 0.0, 0, 1, ai_dists)
    render_ai_brain(ai_game, ai_dists, ai_state, 1, False)

    ax_human.set_title(f"🧑 YOU (HUMAN)  —  Use \u2190 / \u2192 or A / D", fontsize=13, fontweight="bold", color="#1d63ff")
    ax_ai.set_title(f"🤖 AI ({d_name})  —  Press 1 / 2 / 3 to change", fontsize=13, fontweight="bold",
                    color=DIFFICULTY_SPECS[d_name]["color"])
    ai_view["banner"].set_visible(False)

    # On very first launch, wait for player to click window & press a key so they are ready!
    if not ctrl["started"]:
        human_view["banner"].set_text(
            "CLICK THIS WINDOW\n&\nPRESS SPACE (or \u2190 / \u2192)\nTO START THE RACE!\n\n"
            "[1] Easy   [2] Normal   [3] Nightmare"
        )
        human_view["banner"].set_visible(True)
        while window_open() and not ctrl["started"]:
            plt.pause(0.02)
        human_view["banner"].set_visible(False)
        if ctrl["new_race"]:
            continue

    # Race loop
    step_num = 0
    while window_open() and not ctrl["new_race"]:
        step_num += 1
        d_name = ctrl["difficulty"]
        ax_ai.set_title(f"🤖 AI ({d_name})  —  Press 1 / 2 / 3 to change", fontsize=13, fontweight="bold",
                        color=DIFFICULTY_SPECS[d_name]["color"])

        # 1) Human action (consume 1 queued key press, or STAY in lane)
        if ctrl["human_queue"]:
            h_action = ctrl["human_queue"].pop(0)
        else:
            h_action = 1  # STAY

        # 2) AI action from its trained Q-table
        ai_dists, ai_state = sense_state(ai_game)
        if not ai_game.crashed and not ai_game.won:
            ai_action, ai_explored = ai_choose_action(d_name, ai_state)
        else:
            ai_action, ai_explored = 1, False

        h_old_lane, h_old_scroll = human_game.lane, human_game.scroll
        ai_old_lane, ai_old_scroll = ai_game.lane, ai_game.scroll

        # 3) Step both games without auto-spawning, then spawn the EXACT SAME wave into both!
        human_game.step(h_action, auto_spawn=False)
        ai_game.step(ai_action, auto_spawn=False)

        if step_num % SPAWN_EVERY == 0:
            shared_wave, last_open = make_wave(wave_rng, HIGHWAY_LEN - 1.0, last_open)
            if not human_game.crashed and not human_game.won:
                human_game.add_cloned_wave(shared_wave)
            if not ai_game.crashed and not ai_game.won:
                ai_game.add_cloned_wave(shared_wave)

        new_ai_dists, new_ai_state = sense_state(ai_game)

        # Show status banner if one driver crashed while the other is still driving
        if human_game.crashed and not ai_game.crashed:
            human_view["banner"].set_text(
                f"💥 YOU CRASHED AT {human_game.dodged} CARS!\n\n"
                f"Watching {d_name} AI finish...\n(Press 1/2/3 or SPACE for new race)"
            )
            human_view["banner"].set_visible(True)
        if ai_game.crashed and not human_game.crashed:
            ai_view["banner"].set_text(
                f"💥 {d_name} AI CRASHED\nAT {ai_game.dodged} CARS!\n\n"
                f"KEEP DRIVING TO EXTEND YOUR WIN!"
            )
            ai_view["banner"].set_visible(True)

        # 4) Smooth 2-subframe animation
        for frac in (0.5, 1.0):
            hx = h_old_lane + frac * (human_game.lane - h_old_lane)
            hs = h_old_scroll + frac * (human_game.scroll - h_old_scroll)
            htilt = ACTIONS[h_action] if (frac < 1.0 and human_game.lane != h_old_lane) else 0

            ax_x = ai_old_lane + frac * (ai_game.lane - ai_old_lane)
            ax_s = ai_old_scroll + frac * (ai_game.scroll - ai_old_scroll)
            atilt = ACTIONS[ai_action] if (frac < 1.0 and ai_game.lane != ai_old_lane) else 0

            render_highway(human_view, human_game, hx, hs, htilt, h_action)
            render_highway(ai_view, ai_game, ax_x, ax_s, atilt, ai_action, new_ai_dists)
            render_ai_brain(ai_game, new_ai_dists, ai_state, ai_action, ai_explored)
            wait(ctrl["delay"] * 0.5)

        # If Human crashed and pressed SPACE/1/2/3 to restart early, break out
        if human_game.crashed and ctrl["paused"]:
            ctrl["paused"] = False
            break

        # 5) Check if the race round is over
        both_done = (human_game.crashed or human_game.won) and (ai_game.crashed or ai_game.won)
        someone_hit_goal = human_game.won or ai_game.won
        if both_done or someone_hit_goal:
            if human_game.dodged > ai_game.dodged or (human_game.won and not ai_game.won):
                ctrl["wins_human"] += 1
                result_msg = f"🏆 YOU BEAT THE {d_name} AI!\n({human_game.dodged} vs {ai_game.dodged} cars)"
            elif ai_game.dodged > human_game.dodged or (ai_game.won and not human_game.won):
                ctrl["wins_ai"] += 1
                result_msg = f"🤖 {d_name} AI WINS!\n({ai_game.dodged} vs {human_game.dodged} cars)"
            else:
                result_msg = f"⚡ PHOTO-FINISH TIE!\n(Both dodged {human_game.dodged} cars!)"

            human_view["banner"].set_text(f"{result_msg}\n\nStarting next race in 2.5s...")
            human_view["banner"].set_visible(True)
            render_ai_brain(ai_game, new_ai_dists, ai_state, ai_action, ai_explored)
            wait(2.5)
            human_view["banner"].set_visible(False)
            ai_view["banner"].set_visible(False)
            round_num += 1
            break
