# Wedding-Data- Marriage Trends Dashboard
An interactive Dash dashboard that visualizes U.S. marriage patterns over time, including median age at first marriage, wedding costs and guest counts, and state‑level marriage rates. The dashboard uses data from the U.S. Census Bureau, The Knot, and Zola.

## Files

"01_median_age_first_marriage.csv" - Median age at first marriage for men and women (1890–2024)
"02_marital_status_by_state.csv" - Percentage of population aged 15+ who are married, by state and year (2015–2022)
"00_MASTER_wedding_research.csv" - Wedding costs, guest counts, remarriage statistics, and divorce risk (2000–2024)

## Install

```bash
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import math



## Required CSV location for Dash app

This location:
data_folder = "/Users/BlushingButterfly/MY_PYTHON/VIRTUAL/py311/DataVis/Final Project/Data/wedding_data/"



