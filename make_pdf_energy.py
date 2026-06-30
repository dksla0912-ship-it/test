# -*- coding: utf-8 -*-
"""중3 과학 모의고사(Ⅵ. 에너지 전환과 보존) 2단 PDF 생성 (배점 없음, 그림 삽입)
docx와 동일 내용을 reportlab으로 렌더링 — 미리보기/검증용"""
import os
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Image, Table, TableStyle, FrameBreak,
                                NextPageTemplate, KeepTogether)
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

from exam_data_energy import QUESTIONS, SECTIONS, ANSWERS, EXPLANATIONS, FIGS, CONFIG

# 원숫자(①)·원문자(㉠) 글리프를 포함하는 Adobe-Korea1 기반 CID 한국어 폰트 사용
pdfmetrics.registerFont(UnicodeCIDFont("HYGothic-Medium"))
FONT = "HYGothic-Medium"
IMG_DIR = "images"

styles = getSampleStyleSheet()
def S(name, **kw):
    base = dict(fontName=FONT, leading=12)
    base.update(kw)
    return ParagraphStyle(name, **base)

st_stem = S("stem", fontSize=9.5, leading=12.5, spaceBefore=5, spaceAfter=2)
st_choice = S("choice", fontSize=9, leading=11.5, leftIndent=8)
st_sec = S("sec", fontSize=12, leading=15, textColor=colors.HexColor("#1F3A5F"),
           spaceBefore=6, spaceAfter=3)
st_bogi = S("bogi", fontSize=8.5, leading=11)
st_bogihdr = S("bogihdr", fontSize=8.5, leading=11, alignment=1)
st_title = S("title", fontSize=16, leading=20, alignment=1)
st_info = S("info", fontSize=8.5, leading=11, textColor=colors.HexColor("#606060"))
st_ans = S("ans", fontSize=10, leading=12.5, textColor=colors.HexColor("#C0392B"),
           spaceBefore=4)
st_exp = S("exp", fontSize=9, leading=12, spaceAfter=2)

COLW = 253


def img_flowable(fname, maxw=150, maxh=130):
    path = os.path.join(IMG_DIR, fname)
    with PILImage.open(path) as im:
        w, h = im.size
    ar = w / h
    ww = maxw; hh = ww / ar
    if hh > maxh:
        hh = maxh; ww = hh * ar
    img = Image(path, width=ww, height=hh)
    img.hAlign = "CENTER"
    return img


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def bogi_flowable(items):
    inner = [Paragraph("&lt; 보 기 &gt;", st_bogihdr)]
    for it in items:
        inner.append(Paragraph(esc(it), st_bogi))
    t = Table([[inner]], colWidths=[COLW-6])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EEF3FA")),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#9DB3CC")),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def data_table(headers, rows):
    cw = (COLW-4) / len(headers)
    data = [[Paragraph(esc(h), S("th", fontSize=7.6, leading=9, alignment=1)) for h in headers]]
    for row in rows:
        data.append([Paragraph(esc(c), S("td", fontSize=7.6, leading=9, alignment=1)) for c in row])
    t = Table(data, colWidths=[cw]*len(headers))
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6E6E6")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ]))
    return t


def box_flowable(lines):
    inner = [Paragraph(esc(ln), st_bogi) for ln in lines]
    t = Table([[inner]], colWidths=[COLW-6])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F4F4")),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#B0B0B0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def question_flowables(q):
    flow = [Paragraph(f"<b>{q['num']}.</b> " + esc(q['stem']), st_stem)]
    has_fig = q['num'] in FIGS
    if has_fig:
        flow.append(img_flowable(FIGS[q['num']]))
    for block in q.get('blocks', []):
        if block[0] == 'box':
            if has_fig:
                continue
            flow.append(box_flowable(block[1]))
        elif block[0] == 'table':
            flow.append(data_table(block[1], block[2]))
        elif block[0] == 'bogi':
            flow.append(bogi_flowable(block[1]))
        flow.append(Spacer(1, 2))
    for ch in q['choices']:
        flow.append(Paragraph(esc(ch), st_choice))
    flow.append(Spacer(1, 3))
    return flow


def build_exam_pdf():
    out = CONFIG["out_exam"] + ".pdf"
    doc = BaseDocTemplate(out, pagesize=A4,
                          leftMargin=1.2*cm, rightMargin=1.2*cm,
                          topMargin=1.2*cm, bottomMargin=1.2*cm)
    pw, ph = A4
    lm, rm, tm, bm = 1.2*cm, 1.2*cm, 1.2*cm, 1.2*cm
    usable_w = pw - lm - rm
    gap = 16
    colw = (usable_w - gap) / 2
    header_h = 76
    fh = Frame(lm, ph - tm - header_h, usable_w, header_h, id="hdr",
               leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    col_h1 = (ph - tm - header_h - 4) - bm
    fL1 = Frame(lm, bm, colw, col_h1, id="L1", leftPadding=4, rightPadding=4)
    fR1 = Frame(lm + colw + gap, bm, colw, col_h1, id="R1", leftPadding=4, rightPadding=4)
    col_h = (ph - tm) - bm
    fL = Frame(lm, bm, colw, col_h, id="L", leftPadding=4, rightPadding=4)
    fR = Frame(lm + colw + gap, bm, colw, col_h, id="R", leftPadding=4, rightPadding=4)
    doc.addPageTemplates([
        PageTemplate(id="first", frames=[fh, fL1, fR1]),
        PageTemplate(id="later", frames=[fL, fR]),
    ])
    story = []
    htbl = Table([[Paragraph(CONFIG["grade_label"].replace("\n", " "),
                             S("h", fontSize=10, alignment=1)),
                   Paragraph(CONFIG["exam_title"], st_title),
                   Paragraph(CONFIG["range_label_pdf"],
                             S("h2", fontSize=8, leading=10.5, alignment=1))]],
                 colWidths=[usable_w*0.2, usable_w*0.52, usable_w*0.28])
    htbl.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1.0, colors.HexColor("#333333")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#333333")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(htbl)
    story.append(Spacer(1, 3))
    for ln in CONFIG["note_lines"]:
        story.append(Paragraph(esc(ln), st_info))
    story.append(NextPageTemplate("later"))
    story.append(FrameBreak())

    for q in QUESTIONS:
        if q['num'] in SECTIONS:
            story.append(Paragraph(SECTIONS[q['num']], st_sec))
        story.append(KeepTogether(question_flowables(q)))
    story.append(Spacer(1, 4))
    story.append(Paragraph("― 문제 끝 ―", S("end", fontSize=10, alignment=1)))
    doc.build(story)
    print("저장:", out)


def build_answers_pdf():
    out = CONFIG["out_answer"] + ".pdf"
    doc = BaseDocTemplate(out, pagesize=A4,
                          leftMargin=1.4*cm, rightMargin=1.4*cm,
                          topMargin=1.4*cm, bottomMargin=1.4*cm)
    pw, ph = A4
    frame = Frame(1.4*cm, 1.4*cm, pw-2.8*cm, ph-2.8*cm, id="full",
                  leftPadding=4, rightPadding=4)
    doc.addPageTemplates([PageTemplate(id="full", frames=[frame])])
    story = [Paragraph(CONFIG["answer_title"], st_title),
             Spacer(1, 8),
             Paragraph("빠른 정답표", st_sec)]
    headers = ["문항", "정답", "문항", "정답", "문항", "정답", "문항", "정답"]
    rows = []
    for i in range(10):
        row = []
        for j in range(4):
            num = i + 1 + j*10
            row += [str(num), ANSWERS[num]]
        rows.append(row)
    data = [headers] + rows
    t = Table(data, colWidths=[(pw-2.8*cm)/8]*8)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), FONT), ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6E6E6")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t); story.append(Spacer(1, 8))
    for n in range(1, 41):
        if n in SECTIONS:
            story.append(Paragraph(SECTIONS[n], st_sec))
        story.append(Paragraph(f"<b>{n}. 정답 {ANSWERS[n]}</b>", st_ans))
        story.append(Paragraph(esc(EXPLANATIONS[n]), st_exp))
    doc.build(story)
    print("저장:", out)


if __name__ == "__main__":
    build_exam_pdf()
    build_answers_pdf()
