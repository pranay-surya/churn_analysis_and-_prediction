"""
ui.py
Shared UI helpers that render pure HTML so CSS is always reliable.
Use these instead of st.metric(), st.divider(), etc.
"""

import streamlit as st


def kpi_row(cards: list):
    """
    Render a row of KPI cards.
    cards = list of dicts: {label, value, sub, accent}
    accent is a hex colour for the top border strip.
    """
    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        accent = card.get("accent", "#0078D4")
        col.markdown(
            f"""
            <div style="
                background   : #FFFFFF;
                border       : 1px solid #EDEBE9;
                border-top   : 3px solid {accent};
                padding      : 18px 20px 16px 20px;
                font-family  : 'IBM Plex Sans', sans-serif;
            ">
                <div style="
                    font-size      : 0.65rem;
                    font-weight    : 600;
                    color          : #A19F9D;
                    text-transform : uppercase;
                    letter-spacing : 0.08em;
                    margin-bottom  : 8px;
                ">{card['label']}</div>
                <div style="
                    font-size   : 1.75rem;
                    font-weight : 700;
                    color       : #252423;
                    line-height : 1;
                    margin-bottom: 6px;
                ">{card['value']}</div>
                <div style="
                    font-size : 0.72rem;
                    color     : #A19F9D;
                ">{card.get('sub', '')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def section(title: str):
    """Render a section heading with a bottom border."""
    st.markdown(
        f"""
        <div style="
            font-family    : 'IBM Plex Sans', sans-serif;
            font-size      : 0.7rem;
            font-weight    : 700;
            color          : #605E5C;
            text-transform : uppercase;
            letter-spacing : 0.1em;
            padding-bottom : 8px;
            border-bottom  : 1px solid #EDEBE9;
            margin-bottom  : 16px;
            margin-top     : 8px;
        ">{title}</div>
        """,
        unsafe_allow_html=True,
    )


def page_title(title: str, subtitle: str = ""):
    """Render a page title with an optional subtitle."""
    st.markdown(
        f"""
        <div style="margin-bottom: 18px; font-family: 'IBM Plex Sans', sans-serif;">
            <div style="font-size:1.3rem; font-weight:700; color:#252423; line-height:1.2;">
                {title}
            </div>
            {"" if not subtitle else f'<div style="font-size:0.82rem; color:#A19F9D; margin-top:4px;">{subtitle}</div>'}
        </div>
        """,
        unsafe_allow_html=True,
    )


def divider():
    st.markdown(
        '<hr style="border:none; border-top:1px solid #EDEBE9; margin:20px 0;">',
        unsafe_allow_html=True,
    )


def caption(text: str):
    st.markdown(
        f'<p style="font-size:0.75rem; color:#A19F9D; margin-top:4px; '
        f'font-family:\'IBM Plex Sans\',sans-serif;">{text}</p>',
        unsafe_allow_html=True,
    )


def expander(title: str, content_html: str):
    """
    Pure HTML expander — works identically across all Streamlit versions.
    content_html is raw HTML for the body.
    """
    st.markdown(
        f"""
        <details style="
            border       : 1px solid #EDEBE9;
            background   : #FFFFFF;
            margin-bottom: 6px;
            font-family  : 'IBM Plex Sans', sans-serif;
        ">
          <summary style="
              padding    : 12px 16px;
              font-size  : 0.875rem;
              font-weight: 600;
              color      : #252423;
              cursor     : pointer;
              list-style : none;
          ">{title}</summary>
          <div style="padding: 12px 16px 14px 16px; border-top: 1px solid #EDEBE9;">
            {content_html}
          </div>
        </details>
        """,
        unsafe_allow_html=True,
    )


def info_box(text: str, kind: str = "info"):
    """kind: info | warning | success | error"""
    colors = {
        "info":    ("#0078D4", "#EFF6FC"),
        "warning": ("#CA5010", "#FFF4CE"),
        "success": ("#107C10", "#DFF6DD"),
        "error":   ("#A4262C", "#FDE7E9"),
    }
    border_color, bg = colors.get(kind, colors["info"])
    st.markdown(
        f"""
        <div style="
            background   : {bg};
            border-left  : 3px solid {border_color};
            padding      : 12px 16px;
            font-size    : 0.84rem;
            color        : #252423;
            font-family  : 'IBM Plex Sans', sans-serif;
            line-height  : 1.55;
            margin-bottom: 8px;
        ">{text}</div>
        """,
        unsafe_allow_html=True,
    )

    