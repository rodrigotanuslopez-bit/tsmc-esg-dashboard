"""
TSMC ESG Dashboard - Styling Module
Centralised colour palette and CSS for consistent branding across pages.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# TSMC brand and ESG pillar colour palette
# ---------------------------------------------------------------------------
COLORS = {
    # TSMC corporate brand
    "tsmc_red": "#C8102E",
    "tsmc_red_dark": "#8B0000",
    "tsmc_navy": "#1A2332",
    "tsmc_charcoal": "#333333",
    "tsmc_gray_light": "#F5F5F5",
    "tsmc_gray_mid": "#9E9E9E",
    "tsmc_white": "#FFFFFF",

    # ESG pillar colours
    "env_green": "#2E7D32",
    "env_green_light": "#66BB6A",
    "social_blue": "#1565C0",
    "social_blue_light": "#42A5F5",
    "gov_gold": "#B8860B",
    "gov_gold_light": "#D4A017",
    "fin_teal": "#00695C",
    "fin_teal_light": "#26A69A",

    # Status colours
    "positive": "#2E7D32",
    "negative": "#C62828",
    "neutral": "#757575",
    "warning": "#EF6C00",
}

# Pillar-to-colour map for charts
PILLAR_COLORS = {
    "E": COLORS["env_green"],
    "S": COLORS["social_blue"],
    "G": COLORS["gov_gold"],
    "Financial": COLORS["fin_teal"],
}


def apply_global_styling():
    """Inject global CSS styling for the TSMC dashboard."""
    st.markdown(
        f"""
        <style>
        /* Hide Streamlit default elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Main container */
        .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }}

        /* Headings */
        h1, h2, h3 {{
            color: {COLORS['tsmc_navy']};
            font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
        }}

        h1 {{
            border-bottom: 4px solid {COLORS['tsmc_red']};
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }}

        /* Sidebar styling */
        section[data-testid="stSidebar"] {{
            background-color: {COLORS['tsmc_navy']};
        }}

        section[data-testid="stSidebar"] * {{
            color: {COLORS['tsmc_white']} !important;
        }}

        section[data-testid="stSidebar"] .stRadio label {{
            color: {COLORS['tsmc_white']} !important;
        }}

        /* KPI metric cards */
        div[data-testid="stMetric"] {{
            background-color: {COLORS['tsmc_white']};
            border-left: 5px solid {COLORS['tsmc_red']};
            padding: 1rem 1.25rem;
            border-radius: 6px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        }}

        div[data-testid="stMetric"] label {{
            color: {COLORS['tsmc_charcoal']};
            font-weight: 600;
        }}

        div[data-testid="stMetricValue"] {{
            color: {COLORS['tsmc_navy']};
            font-size: 1.75rem;
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}

        .stTabs [data-baseweb="tab"] {{
            background-color: {COLORS['tsmc_gray_light']};
            border-radius: 6px 6px 0 0;
            padding: 8px 16px;
            font-weight: 600;
        }}

        .stTabs [aria-selected="true"] {{
            background-color: {COLORS['tsmc_red']} !important;
            color: {COLORS['tsmc_white']} !important;
        }}

        /* Info / hero banner */
        .tsmc-hero {{
            background: linear-gradient(135deg, {COLORS['tsmc_navy']} 0%, {COLORS['tsmc_red']} 100%);
            color: {COLORS['tsmc_white']};
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
        }}

        .tsmc-hero h1 {{
            color: {COLORS['tsmc_white']};
            border-bottom: none;
            margin-top: 0;
        }}

        /* Section panels */
        .panel {{
            background-color: {COLORS['tsmc_white']};
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
            margin-bottom: 1.25rem;
        }}

        /* Pillar badges */
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            color: white;
            margin-right: 6px;
        }}
        .badge-e {{ background-color: {COLORS['env_green']}; }}
        .badge-s {{ background-color: {COLORS['social_blue']}; }}
        .badge-g {{ background-color: {COLORS['gov_gold']}; }}
        .badge-f {{ background-color: {COLORS['fin_teal']}; }}

        /* Buttons */
        .stButton>button {{
            background-color: {COLORS['tsmc_red']};
            color: {COLORS['tsmc_white']};
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1.25rem;
            font-weight: 600;
        }}

        .stButton>button:hover {{
            background-color: {COLORS['tsmc_red_dark']};
            color: {COLORS['tsmc_white']};
        }}

        /* Dividers */
        hr {{
            border-top: 2px solid {COLORS['tsmc_red']};
            opacity: 0.3;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str = "", pillar: str | None = None):
    """Render a consistent page header with optional pillar badge."""
    badge_html = ""
    if pillar:
        badge_class = {"E": "badge-e", "S": "badge-s", "G": "badge-g", "F": "badge-f"}.get(
            pillar, ""
        )
        badge_label = {
            "E": "ENVIRONMENTAL",
            "S": "SOCIAL",
            "G": "GOVERNANCE",
            "F": "FINANCIAL",
        }.get(pillar, "")
        badge_html = f'<span class="badge {badge_class}">{badge_label}</span>'

    st.markdown(
        f"""
        <div style="margin-bottom: 1.5rem;">
            {badge_html}
            <h1 style="display:inline-block; margin-left: 0.5rem; border-bottom:none;">{title}</h1>
            {f'<p style="color: {COLORS["tsmc_charcoal"]}; font-size: 1.05rem; margin-top: 0.25rem;">{subtitle}</p>' if subtitle else ''}
            <hr style="margin-top: 0.5rem;"/>
        </div>
        """,
        unsafe_allow_html=True,
    )
