# Data Dictionary

This document describes the fields included in the Nassau Candy shipping dataset used for the Shipping Route Efficiency Analysis.

| Field | Description |
|---|---|
| Row ID | Unique row identifier |
| Order ID | Unique order identifier |
| Order Date | Date of order |
| Ship Date | Date of shipment |
| Ship Mode | Shipping method of order |
| Customer ID | Unique customer identifier |
| Country/Region | Country or region of customer |
| City | City of customer |
| State/Province | State/province of customer |
| Postal Code | Postal code / ZIP code of customer |
| Division | Product division |
| Region | Region of customer |
| Product ID | Unique product identifier |
| Product Name | Product long name |
| Sales | Total sales value of order |
| Units | Total units of order |
| Gross Profit | Gross profit of order (Sales - Cost) |
| Cost | Cost to manufacture |

## Related Calculated Metrics

| Metric | Description |
|---|---|
| Shipping Lead Time | Ship Date − Order Date |
| Average Lead Time | Mean shipping duration per route |
| Route Volume | Number of orders per route |
| Delay Frequency | Percentage of shipments exceeding the defined threshold |
| Route Efficiency Score | Normalised lead-time performance |
