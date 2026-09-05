"""
Factory-to-Customer Shipping Route Efficiency Analysis
Nassau Candy Distributor - Streamlit Dashboard

Run this app with:
    streamlit run streamlit_app.py

Make sure "Nassau_Candy_Distributor.csv" is in the same folder as this file,
or update DATA_FILE below.
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# ============================================================
# PAGE CONFIGURATION
# ============================================================
# This must be the first Streamlit command in the app.
st.set_page_config(
    page_title="Nassau Candy | Shipping Route Efficiency",
    layout="wide",
)

DATA_FILE = "Nassau Candy Distributor.csv"

# Maps full US state names (as they appear in the dataset) to the
# 2-letter codes Plotly needs to draw a US choropleth map.
US_STATE_ABBREVIATIONS = {
    "Alabama": "AL", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "District Of Columbia": "DC", "District of Columbia": "DC", "Florida": "FL",
    "Georgia": "GA", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN",
    "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
    "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI",
    "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
    "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
    "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
}


# ============================================================
# DATA LOADING & CLEANING
# ============================================================
# @st.cache_data means Streamlit only re-runs this function when the input
# file changes, instead of reloading and re-cleaning the data on every
# filter click. This keeps the app fast.
@st.cache_data
def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)

    # --- Validate date formats (dayfirst=True: dates are DD-MM-YYYY) ---
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce", dayfirst=True)
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce", dayfirst=True)

    # --- Handle missing shipment records ---
    df = df[~(df["Order Date"].isna() | df["Ship Date"].isna())].copy()

    # --- Calculate Shipping Lead Time and remove negative (invalid) values ---
    df["Lead Time Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df = df[df["Lead Time Days"] >= 0].copy()

    # --- Standardise geographic + categorical fields ---
    for col in ["City", "State/Province", "Region", "Country/Region", "Ship Mode"]:
        df[col] = df[col].astype(str).str.strip().str.title()

    # --- Define Factory and build route labels ---
    df["Factory"] = "Nassau Candy Distribution Center"
    df["Route State"] = df["Factory"] + " → " + df["State/Province"]
    df["Route Region"] = df["Factory"] + " → " + df["Region"]

    # --- Add US state abbreviation, needed for the choropleth map ---
    df["State Code"] = df["State/Province"].map(US_STATE_ABBREVIATIONS)

    return df


df = load_and_clean_data(DATA_FILE)


# ============================================================
# SIDEBAR - USER FILTERS
# ============================================================
st.sidebar.header("Filters")

# --- Date range filter ---
min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()
date_range = st.sidebar.date_input(
    "Order date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)
# date_input returns a single date until the user picks a second one -
# this guards against errors while the user is still choosing.
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# --- Region / State selector ---
region_options = sorted(df["Region"].unique())
selected_regions = st.sidebar.multiselect(
    "Region", options=region_options, default=region_options
)

state_options = sorted(df["State/Province"].unique())
selected_states = st.sidebar.multiselect(
    "State / Province", options=state_options, default=state_options
)

# --- Ship mode filter ---
ship_mode_options = sorted(df["Ship Mode"].unique())
selected_ship_modes = st.sidebar.multiselect(
    "Ship mode", options=ship_mode_options, default=ship_mode_options
)

# --- Lead-time threshold slider ---
# Used both to filter the map/table view and to calculate the
# Delay Frequency KPI ("% of shipments exceeding threshold").
max_possible_lead_time = int(df["Lead Time Days"].max())
delay_threshold = st.sidebar.slider(
    "Delay threshold (days) - shipments taking longer than this count as delayed",
    min_value=0,
    max_value=max_possible_lead_time,
    value=5,
)

# --- Apply all filters together ---
filtered_df = df[
    (df["Order Date"].dt.date >= start_date)
    & (df["Order Date"].dt.date <= end_date)
    & (df["Region"].isin(selected_regions))
    & (df["State/Province"].isin(selected_states))
    & (df["Ship Mode"].isin(selected_ship_modes))
].copy()

if filtered_df.empty:
    st.warning("No shipments match the selected filters. Try widening your filter selections.")
    st.stop()


# ============================================================
# ROUTE-LEVEL AGGREGATION (used across multiple modules)
# ============================================================
route_summary = filtered_df.groupby("Route State").agg(
    Route_Volume=("Lead Time Days", "count"),
    Avg_Lead_Time=("Lead Time Days", "mean"),
    Lead_Time_Variability=("Lead Time Days", "std"),
).reset_index().round(2)

# Delay Frequency per route: % of shipments exceeding the sidebar threshold
delay_frequency = filtered_df.groupby("Route State")["Lead Time Days"].apply(
    lambda x: (x > delay_threshold).mean() * 100
).reset_index(name="Delay_Frequency_%").round(2)

route_summary = route_summary.merge(delay_frequency, on="Route State")

# Route Efficiency Score: min-max normalised Avg_Lead_Time, inverted
# so that 1 = fastest route, 0 = slowest route.
min_lead = route_summary["Avg_Lead_Time"].min()
max_lead = route_summary["Avg_Lead_Time"].max()
if max_lead > min_lead:
    route_summary["Route_Efficiency_Score"] = (
        1 - (route_summary["Avg_Lead_Time"] - min_lead) / (max_lead - min_lead)
    ).round(2)
else:
    # If every route has the same average lead time, score them all equally
    route_summary["Route_Efficiency_Score"] = 1.0

route_summary = route_summary.sort_values("Route_Efficiency_Score", ascending=False)


# ============================================================
# TOP-LEVEL KPI CARDS
# ============================================================
st.title("Factory-to-Customer Shipping Route Efficiency")
st.caption("Nassau Candy Distributor")

# Custom KPI cards (instead of st.metric) so that:
# - the full label text is kept and wraps onto multiple lines, no truncation
# - every card is the same height, however many lines its label takes
# - each card gets an accent color and a caption line with added context
st.markdown("""
<style>
.kpi-card {
    background-color: #3d3d3d;
    border-radius: 10px;
    border-top: 4px solid var(--accent-color, #4C78A8);
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    padding: 16px 14px;
    min-height: 110px;      /* keeps every card the same height */
    display: flex;
    flex-direction: column;
    justify-content: center;
    background-color: #3d3d3d;
}
.kpi-label {
    font-size: 0.82rem;
    font-weight: 600;
    color: #e0e0e0;
    white-space: normal;    /* lets the full label wrap instead of truncating */
    line-height: 1.25;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.02em;
}
.kpi-value {
    font-size: 1.9rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.1;
}
</style>
""", unsafe_allow_html=True)


def kpi_card(column, label, value, accent_color):
    """Render one full-height KPI card with a wrapping label and value."""
    column.markdown(f"""
    <div class="kpi-card" style="--accent-color: {accent_color};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

kpi_card(
    kpi1, "Average Shipping Lead Time (in days)",
    f"{filtered_df['Lead Time Days'].mean():.1f}",
    "#4C78A8",
)
kpi_card(
    kpi2, "Average Lead Time (in days)",
    f"{route_summary['Avg_Lead_Time'].min():.1f}",
    "#54A24B",
)
kpi_card(
    kpi3, "Route Volume (of orders)",
    f"{filtered_df.shape[0]:,}",
    "#F58518",
)
kpi_card(
    kpi4, f"Delay Frequency (over {delay_threshold} days)",
    f"{(filtered_df['Lead Time Days'] > delay_threshold).mean() * 100:.1f}%",
    "#E45756",
)
kpi_card(
    kpi5, "Average Route Efficiency Score (0 to 1)",
    f"{route_summary['Route_Efficiency_Score'].mean():.2f}",
    "#72B7B2",
)

st.divider()


# ============================================================
# DASHBOARD MODULES (as tabs)
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "Route Efficiency Overview",
    "Geographic Shipping Map",
    "Ship Mode Comparison",
    "Route Drill-Down",
])

# ------------------------------------------------------------
# MODULE 1: Route Efficiency Overview
# ------------------------------------------------------------
with tab1:
    st.subheader("Average Lead Time by Route")
    lead_time_chart = px.bar(
        route_summary.sort_values("Avg_Lead_Time"),
        x="Avg_Lead_Time",
        y="Route State",
        orientation="h",
        labels={"Avg_Lead_Time": "Average Lead Time (days)", "Route State": ""},
        color="Avg_Lead_Time",
        color_continuous_scale="RdYlGn_r",  # red = slow, green = fast
    )
    lead_time_chart.update_layout(height=max(400, len(route_summary) * 22))
    st.plotly_chart(lead_time_chart, use_container_width=True)

    st.subheader("Route Performance Leaderboard")
    st.caption("Ranked by Route Efficiency Score (1 = fastest, 0 = slowest)")
    st.dataframe(
        route_summary[[
            "Route State", "Route_Volume", "Avg_Lead_Time",
            "Delay_Frequency_%", "Route_Efficiency_Score",
        ]].reset_index(drop=True),
        use_container_width=True,
    )

# ------------------------------------------------------------
# MODULE 2: Geographic Shipping Map
# ------------------------------------------------------------
with tab2:
    st.subheader("US Heatmap of Shipping Efficiency")

    us_only = filtered_df[filtered_df["Country/Region"] == "United States"]

    if us_only.empty:
        st.info("No US shipments in the current filter selection.")
    else:
        state_perf = us_only.groupby(["State/Province", "State Code"]).agg(
            Avg_Lead_Time=("Lead Time Days", "mean"),
            Shipment_Volume=("Lead Time Days", "count"),
        ).reset_index().round(2)

        map_fig = px.choropleth(
            state_perf,
            locations="State Code",
            locationmode="USA-states",
            color="Avg_Lead_Time",
            scope="usa",
            color_continuous_scale="RdYlGn_r",  # red = slow (inefficient), green = fast
            hover_name="State/Province",
            hover_data={"Shipment_Volume": True, "State Code": False},
            labels={"Avg_Lead_Time": "Avg Lead Time (days)"},
        )
        st.plotly_chart(map_fig, use_container_width=True)

    st.subheader("Regional Bottleneck Visualisation")
    region_perf = filtered_df.groupby("Region").agg(
        Region_Volume=("Lead Time Days", "count"),
        Avg_Lead_Time=("Lead Time Days", "mean"),
    ).reset_index().round(2)

    bottleneck_fig = px.scatter(
        region_perf,
        x="Region_Volume",
        y="Avg_Lead_Time",
        text="Region",
        size="Region_Volume",
        color="Avg_Lead_Time",
        color_continuous_scale="RdYlGn_r",
        labels={"Region_Volume": "Shipment Volume", "Avg_Lead_Time": "Average Lead Time (days)"},
    )
    bottleneck_fig.update_traces(textposition="top center")
    st.plotly_chart(bottleneck_fig, use_container_width=True)
    st.caption("Regions in the top-right (high volume + high lead time) are the biggest bottlenecks.")

# ------------------------------------------------------------
# MODULE 3: Ship Mode Comparison
# ------------------------------------------------------------
with tab3:
    st.subheader("Lead Time Comparison by Shipping Method")

    ship_mode_summary = filtered_df.groupby("Ship Mode").agg(
        Shipment_Volume=("Lead Time Days", "count"),
        Avg_Lead_Time=("Lead Time Days", "mean"),
        Lead_Time_Variability=("Lead Time Days", "std"),
    ).reset_index().round(2)

    ship_mode_fig = px.bar(
        ship_mode_summary.sort_values("Avg_Lead_Time"),
        x="Ship Mode",
        y="Avg_Lead_Time",
        color="Ship Mode",
        labels={"Avg_Lead_Time": "Average Lead Time (days)"},
    )
    st.plotly_chart(ship_mode_fig, use_container_width=True)
    st.dataframe(ship_mode_summary, use_container_width=True)

# ------------------------------------------------------------
# MODULE 4: Route Drill-Down
# ------------------------------------------------------------
with tab4:
    st.subheader("State-Level Performance Insights")

    drill_state = st.selectbox("Select a state / province to drill into", state_options)
    state_df = filtered_df[filtered_df["State/Province"] == drill_state]

    if state_df.empty:
        st.info("No shipments for this state under the current filters.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Shipments", f"{state_df.shape[0]:,}")
        col2.metric("Avg Lead Time", f"{state_df['Lead Time Days'].mean():.1f} days")
        col3.metric(
            "Delay Frequency",
            f"{(state_df['Lead Time Days'] > delay_threshold).mean() * 100:.1f}%",
        )

        st.subheader("Order-Level Shipment Timeline")
        timeline_fig = px.scatter(
            state_df.sort_values("Order Date"),
            x="Order Date",
            y="Lead Time Days",
            color="Ship Mode",
            hover_data=["Order ID", "City"],
            labels={"Lead Time Days": "Lead Time (days)", "Order Date": "Order Date"},
        )
        timeline_fig.add_hline(
            y=delay_threshold, line_dash="dash", line_color="red",
            annotation_text="Delay threshold",
        )
        st.plotly_chart(timeline_fig, use_container_width=True)

        st.dataframe(
            state_df[["Order ID", "Order Date", "Ship Date", "Ship Mode", "City", "Lead Time Days"]]
            .sort_values("Order Date")
            .reset_index(drop=True),
            use_container_width=True,
        )
