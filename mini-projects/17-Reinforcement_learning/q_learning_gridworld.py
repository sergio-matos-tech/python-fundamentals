"""
Q-Learning visual demo: a robot learns to reach the treasure (*) while avoiding traps (X).
Slow, step-by-step version: you can watch every single decision change the agent's "weights".

What you see:
  - LEFT  : the grid. Each cell is split into 4 triangles (up / right / down / left).
            The color + number of a triangle is Q(cell, direction) = how good the agent
            thinks it is to move in that direction from that cell.
            The blue-outlined triangle is the weight that was JUST updated.
  - RIGHT (top)   : probability of choosing each direction in the current cell.
                    It comes straight from the weights:  P(a) = softmax(Q(s, a) / tau)
                    -> higher weight = higher probability.
  - RIGHT (middle): the Q-learning update with the real numbers of the last step.
  - RIGHT (bottom): learning curve (total reward per episode) and temperature tau.

Controls (click the window first):
  SPACE   pause / resume
  UP/DOWN faster / slower
  F       fast-forward on/off (trains quickly, skips the step-by-step animation)

Run:  python q_learning_gridworld.py
"""

import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle, Circle, Polygon

# ============================================================
# 1. ENVIRONMENT (the world the agent lives in)
# ============================================================
ROWS, COLS = 5, 6
START = (0, 0)
N_TRAPS = 6
MIN_GOAL_DISTANCE = 5  # treasure at least this many steps (Manhattan) from the start

ACTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left
ACTION_NAMES = ["UP", "RIGHT", "DOWN", "LEFT"]
ACTION_ARROWS = ["\u2191", "\u2192", "\u2193", "\u2190"]


def is_reachable(goal, traps):
    """Breadth-first search: can we walk from START to goal without stepping on a trap?"""
    frontier, seen = [START], {START}
    while frontier:
        r, c = frontier.pop(0)
        if (r, c) == goal:
            return True
        for dr, dc in ACTIONS:
            nxt = (r + dr, c + dc)
            if 0 <= nxt[0] < ROWS and 0 <= nxt[1] < COLS and nxt not in traps and nxt not in seen:
                seen.add(nxt)
                frontier.append(nxt)
    return False


def random_world():
    """Place the treasure and traps at random, retrying until the treasure is reachable."""
    world_rng = np.random.default_rng()
    cells = [(r, c) for r in range(ROWS) for c in range(COLS) if (r, c) != START]
    while True:
        goal_options = [p for p in cells if abs(p[0] - START[0]) + abs(p[1] - START[1]) >= MIN_GOAL_DISTANCE]
        goal = goal_options[world_rng.integers(len(goal_options))]
        others = [p for p in cells if p != goal]
        idx = world_rng.choice(len(others), size=N_TRAPS, replace=False)
        traps = {others[i] for i in idx}
        if is_reachable(goal, traps):
            return goal, traps


GOAL, TRAPS = random_world()  # new map every run

REWARD_GOAL = 10
REWARD_TRAP = -10
REWARD_STEP = -0.1  # small penalty per step -> encourages shorter paths
MAX_STEPS = 50


def step(state, action):
    """Apply an action and return (new_state, reward, done)."""
    r, c = state
    dr, dc = ACTIONS[action]
    # Bumping into the border = stay in place
    new_state = (min(max(r + dr, 0), ROWS - 1), min(max(c + dc, 0), COLS - 1))

    if new_state == GOAL:
        return new_state, REWARD_GOAL, True
    if new_state in TRAPS:
        return new_state, REWARD_TRAP, True
    return new_state, REWARD_STEP, False


# ============================================================
# 2. AGENT (Q-learning with softmax exploration)
# ============================================================
EPISODES = 80
ALPHA = 0.5    # learning rate: how much new info overrides old
GAMMA = 0.9    # discount: how much future rewards matter
TAU_START, TAU_MIN, TAU_DECAY = 2.0, 0.1, 0.95  # temperature: high = explore, low = exploit

Q = np.zeros((ROWS, COLS, len(ACTIONS)))  # the agent's "weights": one per (cell, direction)
rng = np.random.default_rng()


def action_probabilities(state, tau):
    """Softmax: turns the 4 weights of a cell into 4 probabilities."""
    z = Q[state] / tau
    z = np.exp(z - z.max())  # subtract max for numerical stability
    return z / z.sum()


def choose_action(state, tau):
    probs = action_probabilities(state, tau)
    return int(rng.choice(len(ACTIONS), p=probs)), probs


# ============================================================
# 3. VISUALIZATION
# ============================================================
plt.rcParams["keymap.fullscreen"] = []  # free the "f" key for fast-forward
ctrl = {"delay": 0.6, "paused": False, "fast": False}

plt.ion()
fig = plt.figure(figsize=(16, 9))
fig.canvas.manager.set_window_title("Q-Learning - watch every decision")
gs = GridSpec(3, 2, figure=fig, width_ratios=[1.45, 1], height_ratios=[1, 0.75, 1],
              hspace=0.45, wspace=0.22)
ax_grid = fig.add_subplot(gs[:, 0])
ax_prob = fig.add_subplot(gs[0, 1])
ax_eq = fig.add_subplot(gs[1, 1])
ax_curve = fig.add_subplot(gs[2, 1])


def triangle(r, c, a):
    """Vertices of the triangle for direction `a` inside cell (r, c)."""
    tl, tr = (c - 0.5, r - 0.5), (c + 0.5, r - 0.5)
    br, bl = (c + 0.5, r + 0.5), (c - 0.5, r + 0.5)
    center = (c, r)
    return [[tl, tr, center], [tr, br, center], [br, bl, center], [bl, tl, center]][a]


# --- Grid panel: 4 colored triangles per cell ---
cells = [(r, c) for r in range(ROWS) for c in range(COLS)]
tri_keys = [(r, c, a) for (r, c) in cells for a in range(4)]
tris = PolyCollection([triangle(*k) for k in tri_keys], cmap="RdYlGn",
                      edgecolors="white", linewidths=0.6)
tris.set_clim(-10, 10)
tris.set_array(np.zeros(len(tri_keys)))
ax_grid.add_collection(tris)
fig.colorbar(tris, ax=ax_grid, fraction=0.03, pad=0.02, label="Q-value (weight of that direction)")

q_texts = {}
for (r, c, a) in tri_keys:
    if (r, c) in TRAPS or (r, c) == GOAL:
        continue
    dr, dc = ACTIONS[a]
    q_texts[(r, c, a)] = ax_grid.text(c + 0.3 * dc, r + 0.3 * dr, "0", ha="center",
                                      va="center", fontsize=8, color="gray", zorder=3)

for (r, c) in cells:  # thick cell borders
    ax_grid.add_patch(Rectangle((c - 0.5, r - 0.5), 1, 1, fill=False, edgecolor="white",
                                linewidth=2.5, zorder=2))
for (r, c) in TRAPS:
    ax_grid.add_patch(Rectangle((c - 0.5, r - 0.5), 1, 1, color="#222222", zorder=3))
    ax_grid.text(c, r, "X", color="red", ha="center", va="center", fontsize=26,
                 fontweight="bold", zorder=4)
ax_grid.add_patch(Rectangle((GOAL[1] - 0.5, GOAL[0] - 0.5), 1, 1, color="#1b7a1b", zorder=3))
ax_grid.text(GOAL[1], GOAL[0], "\u2605", color="gold", ha="center", va="center",
             fontsize=40, zorder=4)

highlight = Polygon(triangle(0, 0, 0), fill=False, edgecolor="blue", linewidth=3,
                    zorder=5, visible=False)
ax_grid.add_patch(highlight)
trail, = ax_grid.plot([], [], color="royalblue", alpha=0.6, linewidth=3, zorder=6)
agent = Circle((START[1], START[0]), 0.17, color="royalblue", ec="white", lw=2, zorder=7)
ax_grid.add_patch(agent)

ax_grid.set_xlim(-0.5, COLS - 0.5)
ax_grid.set_ylim(ROWS - 0.5, -0.5)  # row 0 on top
ax_grid.set_aspect("equal")
ax_grid.set_xticks([])
ax_grid.set_yticks([])

# --- Probability panel ---
bars = ax_prob.bar(range(4), [0.25] * 4, color="steelblue")
bar_labels = [ax_prob.text(i, 0.27, "25%", ha="center", fontsize=10) for i in range(4)]
ax_prob.set_xticks(range(4), [f"{ACTION_ARROWS[i]} {ACTION_NAMES[i]}" for i in range(4)])
ax_prob.set_ylim(0, 1.15)
ax_prob.set_ylabel("Probability")
ax_prob.set_title("Decision: P(direction) = softmax(Q / \u03c4)")

# --- Equation panel ---
ax_eq.axis("off")
eq_text = ax_eq.text(0.0, 1.0, "", va="top", ha="left", family="monospace", fontsize=10.5,
                     transform=ax_eq.transAxes)

# --- Learning-curve panel ---
ax_curve.set_title("Learning curve")
ax_curve.set_xlabel("Episode")
ax_curve.set_ylabel("Total reward")
ax_curve.set_xlim(0, EPISODES)
ax_curve.set_ylim(-16, 12)
ax_curve.axhline(0, color="gray", linewidth=0.5)
line_raw, = ax_curve.plot([], [], "o-", color="lightgray", markersize=3, label="reward per episode")
line_avg, = ax_curve.plot([], [], color="green", linewidth=2, label="moving average (10)")
ax_tau = ax_curve.twinx()
ax_tau.set_ylim(0, TAU_START * 1.05)
ax_tau.set_ylabel("\u03c4 (exploration)", color="purple")
line_tau, = ax_tau.plot([], [], "--", color="purple", label="\u03c4 (temperature)")
ax_curve.legend(handles=[line_raw, line_avg, line_tau], loc="lower right", fontsize=8)

status = fig.text(0.5, 0.01, "", ha="center", fontsize=10, color="dimgray")


def update_status():
    mode = "FAST-FORWARD" if ctrl["fast"] else f"step delay {ctrl['delay']:.2f}s"
    pause = "   [PAUSED]" if ctrl["paused"] else ""
    status.set_text(f"SPACE pause  |  \u2191/\u2193 speed  |  F fast-forward      ->  {mode}{pause}")


def on_key(event):
    if event.key == " ":
        ctrl["paused"] = not ctrl["paused"]
    elif event.key == "up":
        ctrl["delay"] = max(0.02, ctrl["delay"] / 1.5)
    elif event.key == "down":
        ctrl["delay"] = min(5.0, ctrl["delay"] * 1.5)
    elif event.key == "f":
        ctrl["fast"] = not ctrl["fast"]
    update_status()
    fig.canvas.draw_idle()


fig.canvas.mpl_connect("key_press_event", on_key)
update_status()


def window_open():
    return plt.fignum_exists(fig.number)


def wait(seconds):
    """Sleep while keeping the window responsive; honors pause; exits if window closed."""
    end = time.time() + seconds
    while True:
        if not window_open():
            raise SystemExit
        plt.pause(0.001 if seconds < 0.02 else 0.02)
        if not ctrl["paused"] and time.time() >= end:
            break


def draw_q():
    tris.set_array(np.array([Q[k] for k in tri_keys]))
    for (r, c, a), txt in q_texts.items():
        v = Q[r, c, a]
        txt.set_text("0" if v == 0 else f"{v:.1f}")
        txt.set_color("gray" if v == 0 else "black")


def draw_probs(probs, chosen=None):
    for i, (bar, lbl) in enumerate(zip(bars, bar_labels)):
        bar.set_height(probs[i])
        bar.set_color("darkorange" if i == chosen else "steelblue")
        lbl.set_position((i, probs[i] + 0.02))
        lbl.set_text(f"{probs[i] * 100:.0f}%")


def draw_agent(state, path):
    agent.center = (state[1], state[0])
    trail.set_data([p[1] for p in path], [p[0] for p in path])


# ============================================================
# 4. TRAINING LOOP
# ============================================================
rewards, avg_rewards, tau_hist = [], [], []
tau = TAU_START

for ep in range(EPISODES):
    state, path, total = START, [START], 0.0

    for t in range(MAX_STEPS):
        # ---- 1) Decide: weights -> probabilities -> sample a direction ----
        action, probs = choose_action(state, tau)
        new_state, reward, done = step(state, action)

        # ---- 2) Learn: the Q-learning update ----
        r, c = state
        old = Q[r, c, action]
        best_next = 0.0 if done else Q[new_state].max()
        target = reward + GAMMA * best_next
        Q[r, c, action] = old + ALPHA * (target - old)
        new = Q[r, c, action]

        # ---- 3) Show it ----
        if not ctrl["fast"]:
            draw_q()
            draw_probs(probs, chosen=action)
            highlight.set_xy(triangle(r, c, action))
            highlight.set_visible(True)
            draw_agent(new_state, path + [new_state])
            outcome = "  (TREASURE!)" if new_state == GOAL else "  (TRAP!)" if new_state in TRAPS else ""
            eq_text.set_text(
                f"Cell {state} -> chose {ACTION_ARROWS[action]} {ACTION_NAMES[action]}"
                f"  (prob {probs[action] * 100:.0f}%)\n"
                f"Reward r = {reward:+.1f}{outcome}\n"
                f"Best weight in next cell: max Q(s') = {best_next:.2f}\n\n"
                f"Q(s,a) <- Q(s,a) + \u03b1 * [ r + \u03b3 * maxQ(s') - Q(s,a) ]\n"
                f"       =  {old:.2f} + {ALPHA} * [ {reward:+.1f} + {GAMMA} * {best_next:.2f} - {old:.2f} ]\n"
                f"       =  {new:.2f}    (change: {new - old:+.2f})"
            )
            ax_grid.set_title(f"Episode {ep + 1}/{EPISODES}   |   step {t + 1}   |   "
                              f"\u03c4 = {tau:.2f}", fontsize=13)
            wait(ctrl["delay"] * (3 if done else 1))  # hold longer at the end of an episode

        state = new_state
        path.append(state)
        total += reward
        if done:
            break

    rewards.append(total)
    avg_rewards.append(np.mean(rewards[-10:]))
    tau_hist.append(tau)
    tau = max(TAU_MIN, tau * TAU_DECAY)

    x = range(1, len(rewards) + 1)
    line_raw.set_data(x, rewards)
    line_avg.set_data(x, avg_rewards)
    line_tau.set_data(x, tau_hist)

    if ctrl["fast"]:  # in fast mode, refresh once per episode
        draw_q()
        draw_agent(state, path)
        highlight.set_visible(False)
        ax_grid.set_title(f"Episode {ep + 1}/{EPISODES} (fast-forward)   |   \u03c4 = {tau:.2f}",
                          fontsize=13)
        wait(0.05)

# ============================================================
# 5. FINAL DEMO: follow the learned policy (always pick the highest weight)
# ============================================================
ctrl["fast"] = False
update_status()
draw_q()
highlight.set_visible(False)
state, path = START, [START]
for t in range(MAX_STEPS):
    probs = action_probabilities(state, TAU_MIN)
    action = int(np.argmax(Q[state]))
    draw_probs(probs, chosen=action)
    state, _, done = step(state, action)
    path.append(state)
    draw_agent(state, path)
    eq_text.set_text("Training finished.\nNow the agent always picks the direction\nwith the highest weight (no exploration).")
    ax_grid.set_title(f"Learned policy (greedy)   |   step {t + 1}", fontsize=13)
    wait(0.5)
    if done:
        break

result = "reached the treasure!" if state == GOAL else "did not reach the goal"
ax_grid.set_title(f"Done: agent {result} in {len(path) - 1} steps", fontsize=13)
plt.ioff()
plt.show()
