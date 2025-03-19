# DLIS Data Explorer
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]([https://your-streamlit-app-url](https://dlis-data-explorer-xayxzoajcnaqzedrn8sqs8.streamlit.app/))
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

 A Streamlit-based application for geoscientists to visualize and export data from DLIS files to LAS format.

## Features
- Explore Logical Files, Origins, Frames, and Channels from DLIS files.
- Visualize well log data with interactive plots and statistics.
- Select curves from multiple Logical Files and export them to a single LAS file.
- Convert depth units (meters to feet or vice-versa) during export.
- Remove unwanted curves before exporting.

## How to Use
1. **Upload a DLIS File**: Go to the "Home" page and upload your DLIS file.
2. **Explore Data**: Use the "General Information" page to view details about Logical Files, Origins, Frames, and Channels.
3. **Visualize Data**: Go to the "Data Visualization" page to select a Logical File, Frame, and channels. Visualize the data and select curves for export.
4. **Export to LAS**: On the "Export to LAS" page, review your selected curves, choose the depth unit (meters or feet), and download the LAS file.

## Installation
To run locally, clone this repository and install the dependencies:
```bash
pip install -r requirements.txt
streamlit run app.py
````

