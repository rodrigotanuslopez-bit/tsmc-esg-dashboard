# TSMC ESG Dashboard

> Director-level ESG decision-support dashboard for Taiwan Semiconductor Manufacturing Company (TSMC), built in Streamlit and structured around double-materiality principles.

This dashboard summarises TSMC's environmental, social, governance, and financial performance across FY2020-FY2024, with an explicit Net-Zero 2050 trajectory view aligned with TSMC's published commitment.

## Features

- **Executive overview** with company profile, eight headline KPIs, and strategic narrative panels (leading / lagging / board actions)
- **Double Materiality Matrix** - interactive bubble chart isolating Quadrant I priority topics (Climate & Energy, Sustainable Supply Chain, Innovation Management, etc.) following the TDDM Protocol aligned with ESRS and GRI
- **Net-Zero 2050 trajectory** chart overlaying historical Scope 1+2 actuals against the committed reduction pathway, with 2030, 2040, and 2050 milestones
- **Environmental** subsection - Scope 1/2/3 emissions, carbon intensity, energy mix vs RE60/RE100 targets, water, waste, detailed Net-Zero pathway
- **Social** subsection - workforce growth, women in workforce vs senior management, TRIR safety trend, training intensity
- **Governance** subsection - board independence, women on board, governance structure, ESG ratings (MSCI, DJSI, CDP, ISS, Sustainalytics)
- **Financial** subsection - revenue, EBITDA, capex/R&D, ESG-financial linkage including revenue-vs-emissions decoupling analysis

## Project Structure

```
tsmc-esg-dashboard/
├── app.py                          # Main entry: company info, materiality matrix, net-zero
├── pages/
│   ├── 1_Environmental.py
│   ├── 2_Social.py
│   ├── 3_Governance.py
│   └── 4_Financial.py
├── data/
│   ├── tsmc_kpis.csv               # FY2020-2024 KPI data (E/S/G/Financial)
│   ├── net_zero_trajectory.csv     # 2025-2050 Net-Zero commitment pathway
│   └── materiality_matrix.csv      # Double-materiality matrix data
├── utils/
│   ├── __init__.py
│   ├── data_loader.py              # Cached pandas data loaders
│   └── styling.py                  # TSMC palette + global CSS injection
├── assets/
│   ├── favicon.png
│   └── favicon.svg
├── .streamlit/
│   └── config.toml                 # TSMC-branded Streamlit theme
├── requirements.txt
├── .gitignore
└── README.md
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/tsmc-esg-dashboard.git
cd tsmc-esg-dashboard
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate           # Windows PowerShell
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`. Use the sidebar to navigate between Overview, Environmental, Social, Governance, and Financial pages.

## Deploy to Streamlit Community Cloud

1. Push this repository to GitHub (public or private).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select the repository, branch (`main`), and main file path (`app.py`).
4. Click **Deploy**. Streamlit Cloud will install `requirements.txt` automatically and serve the app at `https://<your-app>.streamlit.app`.

The `.streamlit/config.toml` is honoured by Cloud, so the TSMC red / navy theme deploys automatically.

### Optional: secrets

This dashboard reads only from local CSVs and does not require any secrets. If you later add database, API, or auth integrations, store credentials in `.streamlit/secrets.toml` (gitignored) and corresponding entries in the Cloud **Secrets** management UI.

## Data Sources

All KPIs derive from the **TSMC 2024 Sustainability Report** and the supplementary KPI workbook prepared for SAM 503 ESG Analytics Lab 4. Specifically:

- Scope 1, 2, 3 GHG emissions, energy, water, waste figures - Sustainability Report sections 4-6
- Workforce, diversity, safety, training - Section 7
- Board composition and ESG ratings - Section 8 (Operations and Governance)
- Financial performance - Section 8 (Financial Performance) and TSMC FY2024 results
- Net-Zero trajectory - TSMC's published commitment (return to 2020 levels by 2030, Net-Zero by 2050)

Third-party assurance for E/S data is provided by DNV Business Assurance Co., Ltd.

## Design Notes

**Colour palette** (defined in `utils/styling.py`):

| Use | Hex | Rationale |
| --- | --- | --- |
| TSMC red (primary) | `#C8102E` | Corporate brand |
| TSMC navy | `#1A2332` | Headers, sidebar |
| Environmental | `#2E7D32` | Green for E pillar |
| Social | `#1565C0` | Blue for S pillar |
| Governance | `#B8860B` | Gold for G pillar |
| Financial | `#00695C` | Teal for finance pillar |

**Audience:** TSMC directors and board-level decision-makers. The dashboard prioritises:

- KPI cards with explicit YoY deltas (red/green semantics flipped for emissions, turnover, TRIR where lower is better)
- Target overlays (RE60 by 2030, RE100 by 2040, Net-Zero 2050)
- Director commentary panels under each chart for fast scanning
- Quadrant I materiality isolation to prioritise board agenda topics

## License

Internal academic / educational use. Data is publicly disclosed by TSMC; this dashboard is an analytical visualisation, not an official TSMC product.

## Authorship

Built for SAM 503 ESG Analytics Lab 4 - Dashboard Creation, Illinois Tech Stuart Business School.
