"""
ui.py
Pure-HTML UI components.
Theme: #F3F2F1 bg · #FFFFFF cards · #EDEBE9 borders · #0078D4 blue · #252423 text
Font Awesome 6 loaded in app.py — use <i class="fa-solid ..."> freely here.
"""

import streamlit as st

_FONT   = "'DM Sans', sans-serif"
_MONO   = "'DM Mono', monospace"
_CARD   = "#FFFFFF"
_BG     = "#F3F2F1"
_BORDER = "#EDEBE9"
_TEXT   = "#252423"
_MUTED  = "#A19F9D"
_LABEL  = "#605E5C"
_BLUE   = "#0078D4"


def kpi_row(cards: list):
    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        accent = card.get("accent", _BLUE)
        col.markdown(
            f'<div style="background:{_CARD};border:1px solid {_BORDER};'
            f'border-top:3px solid {accent};padding:20px 22px 16px;'
            f'box-shadow:0 1px 4px rgba(0,0,0,0.05);">'
            f'<div style="font-size:0.61rem;font-weight:700;color:{_MUTED};'
            f'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;">'
            f'{card["label"]}</div>'
            f'<div style="font-size:1.75rem;font-weight:700;color:{_TEXT};'
            f'line-height:1;margin-bottom:10px;letter-spacing:-0.03em;'
            f'font-family:{_MONO};">{card["value"]}</div>'
            f'<div style="font-size:0.71rem;color:{_MUTED};line-height:1.45;'
            f'border-top:1px solid {_BORDER};padding-top:9px;">'
            f'{card.get("sub", "&nbsp;")}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


def page_title(title: str, subtitle: str = ""):
    sub = (
        f'<div style="font-size:0.82rem;color:{_MUTED};margin-top:5px;">{subtitle}</div>'
        if subtitle else ""
    )
    st.markdown(
        f'<div style="margin-bottom:22px;padding-bottom:16px;border-bottom:2px solid {_BORDER};">'
        f'<div style="font-size:1.3rem;font-weight:700;color:{_TEXT};'
        f'letter-spacing:-0.02em;">{title}</div>{sub}</div>',
        unsafe_allow_html=True,
    )


def section(title: str):
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;margin:24px 0 16px 0;">'
        f'<div style="width:3px;height:16px;background:{_BLUE};'
        f'border-radius:2px;flex-shrink:0;"></div>'
        f'<div style="font-size:0.67rem;font-weight:700;color:{_LABEL};'
        f'text-transform:uppercase;letter-spacing:0.12em;">{title}</div>'
        f'<div style="flex:1;height:1px;background:{_BORDER};"></div></div>',
        unsafe_allow_html=True,
    )


def divider():
    st.markdown(
        f'<div style="height:1px;background:{_BORDER};margin:24px 0;"></div>',
        unsafe_allow_html=True,
    )


def caption(text: str):
    st.markdown(
        f'<div style="font-size:0.74rem;color:{_MUTED};margin-top:6px;'
        f'line-height:1.65;padding:9px 13px;background:#F7F6F5;'
        f'border-left:3px solid {_BORDER};">{text}</div>',
        unsafe_allow_html=True,
    )


def info_box(text: str, kind: str = "info"):
    icons = {
        "info":    "fa-circle-info",
        "warning": "fa-triangle-exclamation",
        "success": "fa-circle-check",
        "error":   "fa-circle-exclamation",
    }
    palette = {
        "info":    (_BLUE,    "#EFF6FC", "#DEECF9"),
        "warning": ("#CA5010", "#FFF4CE", "#FFE6A0"),
        "success": ("#107C10", "#DFF6DD", "#C3E6C3"),
        "error":   ("#A4262C", "#FDE7E9", "#F9C5C8"),
    }
    bc, bg, border = palette.get(kind, palette["info"])
    icon = icons.get(kind, "fa-circle-info")
    st.markdown(
        f'<div style="background:{bg};border:1px solid {border};'
        f'border-left:4px solid {bc};'
        f'padding:13px 16px;font-size:0.84rem;color:{_TEXT};'
        f'line-height:1.65;margin-bottom:10px;display:flex;gap:10px;align-items:flex-start;">'
        f'<i class="fa-solid {icon}" style="color:{bc};margin-top:3px;flex-shrink:0;"></i>'
        f'<div>{text}</div></div>',
        unsafe_allow_html=True,
    )


def stat_row(items: list):
    n = len(items)
    cells = "".join(
        f'<div style="display:flex;flex-direction:column;align-items:center;'
        f'padding:0 24px;'
        f'{"" if i==n-1 else "border-right:1px solid "+_BORDER+";"}">'
        f'<div style="font-size:0.61rem;font-weight:700;color:{_MUTED};'
        f'text-transform:uppercase;letter-spacing:.1em;margin-bottom:5px;">{lbl}</div>'
        f'<div style="font-size:1.1rem;font-weight:700;color:{_TEXT};'
        f'font-family:{_MONO};">{val}</div>'
        f'</div>'
        for i, (lbl, val) in enumerate(items)
    )
    st.markdown(
        f'<div style="background:{_CARD};border:1px solid {_BORDER};'
        f'display:flex;align-items:center;padding:14px 4px;margin-bottom:12px;">'
        f'{cells}</div>',
        unsafe_allow_html=True,
    )


def result_card(risk_pct: float, segment: str, monthly: float):
    if risk_pct > 70:
        rc, rbg, rb, rl, icon = "#A4262C", "#FDE7E9", "#F9C5C8", "High Risk",   "fa-triangle-exclamation"
    elif risk_pct > 40:
        rc, rbg, rb, rl, icon = "#CA5010", "#FFF4CE", "#FFE6A0", "Medium Risk", "fa-circle-exclamation"
    else:
        rc, rbg, rb, rl, icon = "#107C10", "#DFF6DD", "#C3E6C3", "Low Risk",    "fa-circle-check"

    st.markdown(
        f'<div style="background:{_CARD};border:1px solid {_BORDER};'
        f'border-top:4px solid {rc};padding:22px 24px;margin-bottom:14px;">'

        f'<div style="display:flex;justify-content:space-between;'
        f'align-items:flex-start;margin-bottom:18px;">'
        f'<div>'
        f'<div style="font-size:0.61rem;font-weight:700;color:{_MUTED};'
        f'text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px;">Churn Probability</div>'
        f'<div style="font-size:2.8rem;font-weight:700;color:{rc};'
        f'line-height:1;letter-spacing:-.04em;font-family:{_MONO};">{risk_pct:.1f}%</div>'
        f'</div>'
        f'<div style="background:{rbg};border:1px solid {rb};color:{rc};padding:5px 12px;'
        f'font-size:0.73rem;font-weight:700;letter-spacing:.04em;display:flex;gap:6px;align-items:center;">'
        f'<i class="fa-solid {icon}"></i>{rl}</div>'
        f'</div>'

        f'<div style="background:{_BG};height:7px;margin-bottom:18px;">'
        f'<div style="background:{rc};height:7px;width:{min(round(risk_pct),100)}%;"></div></div>'

        f'<div style="display:flex;gap:30px;">'
        f'<div>'
        f'<div style="font-size:0.61rem;font-weight:700;color:{_MUTED};'
        f'text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px;">'
        f'<i class="fa-solid fa-tag" style="margin-right:4px;"></i>Segment</div>'
        f'<div style="font-size:0.93rem;font-weight:600;color:{_TEXT};">{segment}</div></div>'
        f'<div>'
        f'<div style="font-size:0.61rem;font-weight:700;color:{_MUTED};'
        f'text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px;">'
        f'<i class="fa-solid fa-file-invoice-dollar" style="margin-right:4px;"></i>Monthly Bill</div>'
        f'<div style="font-size:0.93rem;font-weight:700;color:{_TEXT};'
        f'font-family:{_MONO};">${monthly:.2f}</div></div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )


def driver_cards(items: list):
    icons  = ["fa-file-contract", "fa-wifi", "fa-credit-card"]
    colors = [_BLUE, "#107C10", "#CA5010"]
    cols   = st.columns(len(items))
    for i, (col, (heading, body)) in enumerate(zip(cols, items)):
        color = colors[i % len(colors)]
        icon  = icons[i % len(icons)]
        col.markdown(
            f'<div style="background:{_CARD};border:1px solid {_BORDER};'
            f'border-left:3px solid {color};padding:16px 18px;">'
            f'<div style="font-size:0.82rem;font-weight:700;color:{_TEXT};'
            f'margin-bottom:8px;display:flex;align-items:center;gap:8px;">'
            f'<i class="fa-solid {icon}" style="color:{color};font-size:0.8rem;"></i>{heading}</div>'
            f'<div style="font-size:0.78rem;color:{_LABEL};line-height:1.7;">{body}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


def segment_badge_row(seg_counts: dict, seg_colors: dict):
    cells = "".join(
        f'<div style="display:flex;flex-direction:column;align-items:center;'
        f'padding:0 22px;min-width:110px;'
        f'{"" if i==len(seg_counts)-1 else "border-right:1px solid "+_BORDER+";"}">'
        f'<div style="width:10px;height:10px;border-radius:50%;background:{color};'
        f'margin-bottom:8px;"></div>'
        f'<div style="font-size:0.67rem;font-weight:600;color:{_LABEL};'
        f'text-align:center;margin-bottom:5px;">{seg}</div>'
        f'<div style="font-size:1.1rem;font-weight:700;color:{_TEXT};'
        f'font-family:{_MONO};">{count:,}</div>'
        f'</div>'
        for i, (seg, (count, color)) in enumerate(
            {k: (seg_counts.get(k, 0), seg_colors[k]) for k in seg_colors}.items()
        )
    )
    st.markdown(
        f'<div style="background:{_CARD};border:1px solid {_BORDER};'
        f'display:flex;justify-content:center;align-items:center;'
        f'padding:18px 4px;margin-bottom:16px;">{cells}</div>',
        unsafe_allow_html=True,
    )


def expander(title: str, content_html: str):
    st.markdown(
        f'<details style="border:1px solid {_BORDER};background:{_CARD};margin-bottom:6px;">'
        f'<summary style="padding:13px 16px;font-size:0.875rem;font-weight:600;'
        f'color:{_TEXT};cursor:pointer;list-style:none;display:flex;align-items:center;gap:8px;">'
        f'<i class="fa-solid fa-chevron-right" style="font-size:0.65rem;color:{_MUTED};"></i>'
        f'{title}</summary>'
        f'<div style="padding:13px 16px 15px;border-top:1px solid {_BORDER};">'
        f'{content_html}</div></details>',
        unsafe_allow_html=True,
    )