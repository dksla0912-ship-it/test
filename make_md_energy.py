# -*- coding: utf-8 -*-
"""중3 과학 모의고사(Ⅵ. 에너지 전환과 보존) Markdown 생성 (GitHub/미리보기용)"""
from exam_data_energy import QUESTIONS, SECTIONS, ANSWERS, EXPLANATIONS, FIGS, CONFIG

IMG_DIR = "images"


def render_blocks(q, lines):
    has_fig = q['num'] in FIGS
    if has_fig:
        lines.append("")
        lines.append(f"![문항 {q['num']} 그림]({IMG_DIR}/{FIGS[q['num']]})")
    for block in q.get('blocks', []):
        kind = block[0]
        if kind == 'box':
            if has_fig:
                continue
            lines.append("")
            lines.append("> " + "  \n> ".join(block[1]))
        elif kind == 'bogi':
            lines.append("")
            lines.append("> **< 보기 >**  ")
            lines.append("> " + "  \n> ".join(block[1]))
        elif kind == 'table':
            headers, rows = block[1], block[2]
            lines.append("")
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
            for r in rows:
                lines.append("| " + " | ".join(r) + " |")
    lines.append("")


def build_exam_md():
    lines = []
    lines.append(f"# {CONFIG['exam_title']} ({CONFIG['grade_label'].replace(chr(10), ' ')})")
    lines.append("")
    lines.append(f"**{CONFIG['answer_subtitle']}**")
    lines.append("")
    for ln in CONFIG["note_lines"]:
        lines.append(ln + "  ")
    lines.append("")
    lines.append("---")
    for q in QUESTIONS:
        if q['num'] in SECTIONS:
            lines.append("")
            lines.append(f"## {SECTIONS[q['num']]}")
        lines.append("")
        lines.append(f"**{q['num']}.** {q['stem']}")
        render_blocks(q, lines)
        for ch in q['choices']:
            lines.append(ch + "  ")
    lines.append("")
    lines.append("― 문제 끝 ―")
    out = CONFIG["out_exam"] + ".md"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("저장:", out)


def build_answers_md():
    lines = []
    lines.append(f"# {CONFIG['answer_title']}")
    lines.append("")
    lines.append("## 빠른 정답표")
    lines.append("")
    lines.append("| 문항 | 정답 | 문항 | 정답 | 문항 | 정답 | 문항 | 정답 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for i in range(10):
        cells = []
        for j in range(4):
            num = i + 1 + j*10
            cells += [str(num), ANSWERS[num]]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("---")
    for n in range(1, 41):
        if n in SECTIONS:
            lines.append("")
            lines.append(f"## {SECTIONS[n]}")
        lines.append("")
        lines.append(f"**{n}. 정답 {ANSWERS[n]}**  ")
        lines.append(EXPLANATIONS[n])
    out = CONFIG["out_answer"] + ".md"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("저장:", out)


if __name__ == "__main__":
    build_exam_md()
    build_answers_md()
