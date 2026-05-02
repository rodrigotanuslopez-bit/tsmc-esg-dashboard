"""
TSMC ESG Dashboard - Data Loading Utilities
Centralised, cached data access for all dashboard pages.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).parent.parent / "data"

YEARS = ["2020", "2021", "2022", "2023", "2024"]


@st.cache_data
def load_kpi_data() -> pd.DataFrame:
    """Load TSMC KPI dataset (long-format friendly)."""
    df = pd.read_csv(DATA_DIR / "tsmc_kpis.csv")
    return df


@st.cache_data
def load_kpi_long() -> pd.DataFrame:
    """Reshape KPI data from wide to long format for time-series charts."""
    df = load_kpi_data()
    long = df.melt(
        id_vars=["Pillar", "Category", "KPI", "Unit"],
        value_vars=YEARS,
        var_name="Year",
        value_name="Value",
    )
    long["Year"] = long["Year"].astype(int)
    long["Value"] = pd.to_numeric(long["Value"], errors="coerce")
    return long


@st.cache_data
def load_net_zero() -> pd.DataFrame:
    """Load net-zero trajectory scenarios (2019-2050).

    Columns: Year, BAU, NetZero, ProposedActions (all in tCO2e, S1+S2+S3 total).
    """
    return pd.read_csv(DATA_DIR / "net_zero_trajectory.csv")


@st.cache_data
def load_materiality() -> pd.DataFrame:
    """Load materiality matrix data."""
    return pd.read_csv(DATA_DIR / "materiality_matrix.csv")


def get_kpi(name: str, year: int) -> float | None:
    """Convenience helper: fetch a single KPI value for a single year."""
    df = load_kpi_long()
    match = df[(df["KPI"] == name) & (df["Year"] == year)]
    if match.empty:
        return None
    return match["Value"].iloc[0]


def yoy_change(name: str, current_year: int = 2024, prior_year: int = 2023) -> dict:
    """Return YoY change details (current value, delta, delta %)."""
    current = get_kpi(name, current_year)
    prior = get_kpi(name, prior_year)
    if current is None or prior is None or prior == 0:
        return {"current": current, "delta": None, "delta_pct": None}
    delta = current - prior
    delta_pct = (delta / prior) * 100
    return {"current": current, "delta": delta, "delta_pct": delta_pct}


def format_value(value: float, unit: str) -> str:
    """Pretty-format a KPI value for display."""
    if value is None or pd.isna(value):
        return "N/A"
    if unit == "%":
        return f"{value:.1f}%"
    if unit in ("tCO2e", "MT", "People"):
        if abs(value) >= 1_000_000:
            return f"{value/1_000_000:.2f}M"
        if abs(value) >= 1_000:
            return f"{value/1_000:.1f}K"
        return f"{value:,.0f}"
    if unit == "$M":
        if abs(value) >= 1_000:
            return f"${value/1000:.2f}B"
        return f"${value:,.0f}M"
    if unit == "GWh":
        return f"{value:,.0f} GWh"
    if unit == "Hours":
        return f"{value:.1f} hrs"
    if unit == "per 1000":
        return f"{value:.3f}"
    if unit == "Million MT":
        return f"{value:.1f}M MT"
    if unit == "tCO2e/$M":
        return f"{value:.2f}"
    return f"{value:,.2f}"

@st.cache_data
def load_peer_comparison() -> dict:
    """Peer comparison data for TSMC vs NVIDIA, ASML, Broadcom (FY2024)."""
    return {
        'ratings': {
            'TSMC': {'MSCI': 'AA', 'Sustainalytics': 13.57, 'S&P': 99, 'RepRisk': 'BB', 'Bloomberg': 5.7},
            'NVIDIA': {'MSCI': 'AA', 'Sustainalytics': 12.45, 'S&P': 93, 'RepRisk': 'CCC', 'Bloomberg': 6.6},
            'ASML': {'MSCI': 'AAA', 'Sustainalytics': 8.67, 'S&P': 96, 'RepRisk': 'AA', 'Bloomberg': 6.82},
            'Broadcom': {'MSCI': 'AA', 'Sustainalytics': 20.11, 'S&P': 57, 'RepRisk': 'BB', 'Bloomberg': 4.99}
        },
        'environmental': {
            'renewable_energy_pct': {'TSMC': 13.18, 'NVIDIA': 68.72, 'ASML': 78.68, 'Broadcom': 29.35},
            'scope1_mt': {'TSMC': 1941670, 'NVIDIA': 11896, 'ASML': 24000, 'Broadcom': 53648},
            'scope2_market_mt': {'TSMC': 10957400, 'NVIDIA': 40555, 'ASML': 9000, 'Broadcom': 166752},
            'water_recycling_pct': {'TSMC': 88.1, 'ASML': 75.0, 'Industry_Avg': 75.0},
            'waste_diversion_pct': {'TSMC': 97.0, 'ASML': 74.0}
        },
        'social': {
            'trir': {'TSMC': 0.133},
            'voluntary_turnover_pct': {'TSMC': 3.4, 'ASML': 3.9}
        },
        'governance': {
            'board_independence_pct': {'TSMC': 70, 'NVIDIA': 85, 'ASML': 87, 'Broadcom': 92, 'Peer_Median': 88},
            'women_on_board_pct_2024': {'TSMC': 20, 'NVIDIA': 27, 'ASML': 29, 'Broadcom': 25},
            'esg_linked_pay': {'TSMC': True, 'NVIDIA': True, 'ASML': True, 'Broadcom': True}
        }
    }



