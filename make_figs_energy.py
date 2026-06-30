# -*- coding: utf-8 -*-
"""Ⅵ. 에너지 전환과 보존 모의고사용 그림 생성 (matplotlib)
images/ 폴더에 e_*.png 저장"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle, Arc

FONT_PATH = "/root/.fonts/NanumGothic.ttf"
fm.fontManager.addfont(FONT_PATH)
FP = fm.FontProperties(fname=FONT_PATH)
plt.rcParams["font.family"] = FP.get_name()
plt.rcParams["axes.unicode_minus"] = False

IMG = "images"
os.makedirs(IMG, exist_ok=True)
DPI = 200


def save(fig, name):
    fig.savefig(os.path.join(IMG, name), dpi=DPI, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print("저장:", name)


def freefall_energy():
    """Q7: 낙하 거리에 따른 위치/운동/역학적 에너지"""
    fig, ax = plt.subplots(figsize=(4.0, 3.0))
    d = np.linspace(0, 10, 100)
    E = 10
    ax.plot(d, [E] * len(d), color="#444444", lw=2, label="A")
    ax.plot(d, E - d, color="#1f77b4", lw=2, label="B")
    ax.plot(d, d, color="#d62728", lw=2, label="C")
    ax.text(7.2, E + 0.3, "A", color="#444444", fontproperties=FP, fontsize=12)
    ax.text(8.4, E - 8.4 + 0.4, "B", color="#1f77b4", fontproperties=FP, fontsize=12)
    ax.text(8.4, 8.4 + 0.4, "C", color="#d62728", fontproperties=FP, fontsize=12)
    ax.set_xlabel("낙하 거리", fontproperties=FP, fontsize=11)
    ax.set_ylabel("에너지", fontproperties=FP, fontsize=11)
    ax.set_xlim(0, 10.5); ax.set_ylim(0, 12)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    save(fig, "e_freefall_energy.png")


def height_energy():
    """Q16: 지면으로부터의 높이에 따른 위치/운동 에너지"""
    fig, ax = plt.subplots(figsize=(4.0, 3.0))
    h = np.linspace(0, 10, 100)
    E = 10
    ax.plot(h, h, color="#1f77b4", lw=2)
    ax.plot(h, E - h, color="#d62728", lw=2)
    ax.text(8.2, 8.6, "위치 에너지", color="#1f77b4", fontproperties=FP, fontsize=10)
    ax.text(0.3, 8.7, "운동 에너지", color="#d62728", fontproperties=FP, fontsize=10)
    ax.set_xlabel("지면으로부터의 높이", fontproperties=FP, fontsize=11)
    ax.set_ylabel("에너지", fontproperties=FP, fontsize=11)
    ax.set_xlim(0, 10.5); ax.set_ylim(0, 11.5)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    save(fig, "e_height_energy.png")


def pendulum():
    """Q11: 진자 A-O-B"""
    fig, ax = plt.subplots(figsize=(4.0, 3.2))
    px, py = 0.0, 3.0          # 회전축(고정점)
    L = 2.6
    # 천장
    ax.plot([-1.4, 1.4], [py, py], color="#555", lw=3)
    for x in np.linspace(-1.3, 1.3, 9):
        ax.plot([x, x - 0.18], [py, py + 0.18], color="#555", lw=1)
    ang = np.deg2rad(40)
    ax_, ay = px - L * np.sin(ang), py - L * np.cos(ang)   # A (왼쪽 최고)
    bx, by = px + L * np.sin(ang), py - L * np.cos(ang)    # B (오른쪽 최고)
    ox, oy = px, py - L                                    # O (최저)
    # 흔들림 궤적(호)
    arc = Arc((px, py), 2 * L, 2 * L, angle=0, theta1=270 - 40, theta2=270 + 40,
              color="#bbbbbb", lw=1.2, linestyle="--")
    ax.add_patch(arc)
    # 줄
    ax.plot([px, ax_], [py, ay], color="#888", lw=1, linestyle=":")
    ax.plot([px, bx], [py, by], color="#888", lw=1, linestyle=":")
    ax.plot([px, ox], [py, oy], color="#333", lw=1.5)
    # 추
    for (x, y, c) in [(ax_, ay, "#9ec5e8"), (ox, oy, "#1f77b4"), (bx, by, "#9ec5e8")]:
        ax.add_patch(Circle((x, y), 0.18, color=c, zorder=5))
    ax.add_patch(Circle((px, py), 0.06, color="#333", zorder=6))
    ax.text(ax_ - 0.15, ay + 0.28, "A", fontproperties=FP, fontsize=13, ha="center")
    ax.text(bx + 0.15, by + 0.28, "B", fontproperties=FP, fontsize=13, ha="center")
    ax.text(ox, oy - 0.42, "O", fontproperties=FP, fontsize=13, ha="center")
    # 기준면
    ax.plot([-2.4, 2.4], [oy - 0.55, oy - 0.55], color="#aaa", lw=1)
    ax.set_xlim(-2.6, 2.6); ax.set_ylim(-0.6, 3.6)
    ax.set_aspect("equal"); ax.axis("off")
    save(fig, "e_pendulum.png")


def rollercoaster():
    """Q13: 롤러코스터 A(40)-B(0)-C(20)-D(10)"""
    fig, ax = plt.subplots(figsize=(4.8, 2.9))
    # 경로 좌표 (x, 높이) — 부드러운 트랙
    xs = [0.3, 1.1, 2.0, 3.0, 3.8, 4.6, 5.3, 6.2, 7.0]
    ys = [40,  16,   0,   12,  20,  10,   4,   9,   7]
    xfine = np.linspace(xs[0], xs[-1], 300)
    yfine = np.interp(xfine, xs, ys)
    ax.plot(xfine, yfine, color="#444", lw=2.5, zorder=1)
    ax.plot([-0.2, 7.4], [0, 0], color="#aaa", lw=1)
    # 지점 표시: 점(scatter) + 위쪽 letter 라벨 + 높이 라벨(점마다 위치 지정)
    # (x, 높이, 높이라벨, letter offset, 높이라벨 offset, 높이라벨 ha)
    pts = {
        "A": (0.3, 40, "40 m", (0, 11), (14, -4), "left"),
        "B": (2.0, 0, "0 m",  (-2, 11), (0, -17), "center"),
        "C": (3.8, 20, "20 m", (0, 11), (-12, -2), "right"),
        "D": (4.6, 10, "10 m", (12, 8), (14, -8), "left"),
    }
    for name, (x, y, hlabel, loff, hoff, hha) in pts.items():
        ax.scatter([x], [y], s=90, color="#d62728", zorder=5, edgecolors="white",
                   linewidths=0.8)
        ax.annotate(name, (x, y), textcoords="offset points", xytext=loff,
                    ha="center", fontproperties=FP, fontsize=13, fontweight="bold")
        ax.annotate(hlabel, (x, y), textcoords="offset points", xytext=hoff,
                    ha=hha, fontproperties=FP, fontsize=8.5, color="#555")
    ax.set_xlim(-0.5, 7.8); ax.set_ylim(-7, 50)
    ax.axis("off")
    save(fig, "e_rollercoaster.png")


def induction():
    """Q21: 코일 + 막대자석 + 검류계"""
    fig, ax = plt.subplots(figsize=(4.6, 2.7))
    # 코일 (원통)
    cx, cy, cw, ch = 3.2, 1.0, 1.7, 1.4
    for i in range(6):
        x = cx + i * 0.28
        ax.add_patch(Arc((x, cy), 0.55, ch, angle=0, theta1=-90, theta2=90,
                         color="#b5651d", lw=2))
        ax.add_patch(Arc((x, cy), 0.55, ch, angle=0, theta1=90, theta2=270,
                         color="#b5651d", lw=2, linestyle=(0, (3, 2))))
    # 막대자석 (N/S) — 코일 왼쪽에서 다가옴
    mx, my, mw, mh = 0.7, cy - 0.32, 1.7, 0.62
    ax.add_patch(Rectangle((mx, my), mw / 2, mh, color="#cc3333"))
    ax.add_patch(Rectangle((mx + mw / 2, my), mw / 2, mh, color="#3366cc"))
    ax.text(mx + mw / 4, cy, "N", color="white", fontproperties=FP, fontsize=12,
            ha="center", va="center", fontweight="bold")
    ax.text(mx + 3 * mw / 4, cy, "S", color="white", fontproperties=FP, fontsize=12,
            ha="center", va="center", fontweight="bold")
    # 운동 방향 화살표
    ax.add_patch(FancyArrowPatch((mx + mw + 0.05, cy + 0.55), (cx - 0.15, cy + 0.55),
                                 arrowstyle="-|>", mutation_scale=14, color="#333"))
    ax.text((mx + mw + cx) / 2, cy + 0.85, "운동", fontproperties=FP, fontsize=9,
            ha="center")
    # 검류계 (원 + G)
    gx, gy = 5.7, 1.0
    ax.add_patch(Circle((gx, gy), 0.5, fill=False, color="#333", lw=1.8))
    ax.text(gx, gy, "G", fontproperties=FP, fontsize=13, ha="center", va="center")
    ax.text(gx, gy - 0.85, "검류계", fontproperties=FP, fontsize=9, ha="center")
    # 연결선 (코일 → 검류계)
    ax.plot([cx + 1.6, gx - 0.02], [cy + 0.62, gy + 0.45], color="#333", lw=1.2)
    ax.plot([cx + 1.6, gx - 0.02], [cy - 0.62, gy - 0.45], color="#333", lw=1.2)
    ax.set_xlim(0.3, 6.5); ax.set_ylim(-0.1, 2.3)
    ax.set_aspect("equal"); ax.axis("off")
    save(fig, "e_induction.png")


def hydro():
    """Q37: 수력 발전 에너지 전환 흐름도"""
    fig, ax = plt.subplots(figsize=(5.0, 1.7))
    steps = ["물의\n위치 에너지", "물의\n운동 에너지", "전기 에너지\n(발전기)", "빛 에너지\n(전등)"]
    colors = ["#cfe8cf", "#cfe0f0", "#f5e0a3", "#f5c6c6"]
    x = 0.2
    w, h = 1.05, 0.9
    for i, (s, c) in enumerate(zip(steps, colors)):
        ax.add_patch(Rectangle((x, 0.05), w, h, color=c, ec="#666"))
        ax.text(x + w / 2, 0.05 + h / 2, s, fontproperties=FP, fontsize=8.5,
                ha="center", va="center")
        if i < len(steps) - 1:
            ax.add_patch(FancyArrowPatch((x + w + 0.02, 0.5), (x + w + 0.27, 0.5),
                                         arrowstyle="-|>", mutation_scale=13, color="#333"))
        x += w + 0.29
    ax.set_xlim(0, x); ax.set_ylim(0, 1.05)
    ax.axis("off")
    save(fig, "e_hydro.png")


if __name__ == "__main__":
    freefall_energy()
    height_energy()
    pendulum()
    rollercoaster()
    induction()
    hydro()
    print("그림 생성 완료")
