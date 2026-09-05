# Factory-to-Customer Shipping Route Efficiency Analysis

### Nassau Candy Distributor

## Problem Statement

This project analyses shipping-route efficiency to understand delivery performance across customer routes, geographic areas, and shipping methods. The goal is to provide a clear operational view of route performance and identify areas that may require further attention.

The analysis supports route comparison, delivery-time monitoring, geographic performance review, and shipping-mode evaluation through a Streamlit dashboard.

## Dataset

The dataset contains **10,194 shipment records and 18 fields** covering order information, shipment dates, customer geography, product information, sales, units, gross profit, and cost.

**Dataset:** [Download / View Dataset](Nassau%20Candy%20Distributor.csv)

For the complete field-level description, see the [Data Dictionary](data_dictionary_updated.md).

## Key Findings & Recommendations

The KPI results show an **Average Shipping Lead Time of 1320.8 days**, an **Average Lead Time of 1137.1 days**, and **10,194 orders** in the analysed dataset. The **Delay Frequency is 100.0%** using the defined threshold of more than 5 days, while the **Average Route Efficiency Score is 0.62** on a 0-to-1 scale.

These results provide a high-level operational reference for the dashboard. Route-level, geographic, and ship-mode views can be used to compare performance and focus attention on routes or areas with relatively weaker efficiency.

## Key Performance Indicators (KPIs)

| KPI | Value | Description |
|---|---:|---|
| Average Shipping Lead Time | **1320.8 days** | Overall shipping lead-time KPI |
| Average Lead Time | **1137.1 days** | Mean shipping duration per route |
| Route Volume | **10,194 orders** | Number of orders |
| Delay Frequency | **100.0%** | Percentage of shipments exceeding 5 days |
| Average Route Efficiency Score | **0.62** | Normalised lead-time performance on a 0-to-1 scale |

### KPI Definitions

| KPI | Definition |
|---|---|
| Shipping Lead Time | Ship Date − Order Date |
| Average Lead Time | Mean shipping duration per route |
| Route Volume | Number of orders per route |
| Delay Frequency | % of shipments exceeding threshold |
| Route Efficiency Score | Normalised lead-time performance |

## Method

The analysis covers data validation, shipping lead-time calculation, route grouping, efficiency benchmarking, geographic performance analysis, and ship-mode comparison. Detailed implementation remains in the Jupyter Notebook rather than being repeated here.

## Visualization

**Image:** `Cost-Time Tradeoff by Ship Mode.png`

![Cost-Time Tradeoff by Ship Mode](./Cost-Time%20Tradeoff%20by%20Ship%20Mode.png)

The chart compares shipping modes using delivery time and cost. It provides a quick view of the time-cost trade-off between available shipping methods.

## Streamlit Web Application Requirements

The project includes a Streamlit application for interactive exploration of shipping-route performance.

### Dashboard Modules

#### Route Efficiency Overview
- Average lead time by route
- Route performance leaderboard

#### Geographic Shipping Map
- US heatmap of shipping efficiency
- Regional bottleneck visualisation

#### Ship Mode Comparison
- Lead time comparison by shipping method

#### Route Drill-Down
- State-level performance insights
- Order-level shipment timelines

### User Capabilities

- Date range filter
- Region / State selector
- Ship mode filter
- Lead-time threshold slider

## Dashboard Tabs

The dashboard can be organised into four main tabs: **Route Efficiency Overview**, **Geographic Shipping Map**, **Ship Mode Comparison**, and **Route Drill-Down**. These tabs move from an overall route-performance view to geographic analysis, shipping-method comparison, and detailed state/order-level insights.

The KPI section provides the main operational summary, while the interactive filters allow users to narrow the dashboard by date range, region or state, ship mode, and lead-time threshold.

## Project Structure

```text
Nassau-Candy-Shipping-Route-Efficiency/
│
├── README.md
├── data_dictionary.md
├── Nassau_Candy_Shipping_Route_Efficiency_Analysis (1).ipynb
├── streamlit_app.py
├── requirements.txt
├── dataset.csv
└── Cost-Time Tradeoff by Ship Mode.png
```

### File Purpose

- `README.md` — project documentation and deployment guidance.
- `data_dictionary.md` — dataset field definitions.
- `Nassau_Candy_Shipping_Route_Efficiency_Analysis (1).ipynb` — detailed analysis notebook.
- `streamlit_app.py` — Streamlit application entry point.
- `requirements.txt` — Python dependencies required by the Streamlit app.
- `dataset.csv` — source dataset used by the application.
- `Cost-Time Tradeoff by Ship Mode.png` — project visualisation used in the README.

## How to Run

### Jupyter Notebook

Open the notebook in Jupyter Notebook, JupyterLab, or VS Code and run the cells in order.

### Streamlit Application

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run streamlit_app.py
```

The application will open in your browser.

## Files Needed to Publish on Streamlit Community Cloud

For the Streamlit Community Cloud deployment, keep the application and all files that it reads inside the GitHub repository. The expected project files are:

- `streamlit_app.py`
- `requirements.txt`
- `dataset.csv`
- `data_dictionary.md`
- `Cost-Time Tradeoff by Ship Mode.png` (only if referenced by the app or documentation)

The Jupyter Notebook and README are useful project documentation but are not required for Streamlit to start the application unless the app depends on them.

## Publish on Streamlit Community Cloud

1. Create a GitHub repository and upload the project files.
2. Confirm that `streamlit_app.py` is in the repository and is the main application file.
3. Confirm that `requirements.txt` lists every Python package imported by `streamlit_app.py`.
4. Make sure dataset, image, and other resources are referenced with repository-relative paths.
5. Open Streamlit Community Cloud and sign in with GitHub.
6. Create a new app and select the repository, branch, and `streamlit_app.py` as the main file.
7. Deploy the application.

After deployment, Streamlit Community Cloud builds the environment from `requirements.txt` and runs `streamlit_app.py`.

## Jupyter Notebook

**Notebook:** [Nassau_Candy_Shipping_Route_Efficiency_Analysis (1).ipynb](./Nassau_Candy_Shipping_Route_Efficiency_Analysis%20%281%29.ipynb)

The notebook contains the detailed analytical workflow for data validation, feature engineering, route definition and aggregation, efficiency benchmarking, geographic bottleneck analysis, and ship-mode performance analysis. 

## Dataset Dictionary

See [data_dictionary.md](./data_dictionary.md) for the complete field-level documentation.

## Author

**Satyaranjan Jena**  
**MCA**
## LinkedIn

[LinkedIn Profile](https://www.linkedin.com/in/satyaranjan-jena09/)

