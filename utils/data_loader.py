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
