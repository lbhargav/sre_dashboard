import streamlit as st
import pandas as pd
from datetime import datetime

# Sample data
data = [
    {
        "dataset_name": "vendor_a",
        "ingestion_time": "2025-04-29 09:00:00",
        "status": "Success",
        "log_url": "https://logs.example.com/vendor_a/20250429"
    },
    {
        "dataset_name": "vendor_b",
        "ingestion_time": "2025-04-29 10:00:00",
        "status": "Failed",
        "log_url": "https://logs.example.com/vendor_b/20250429"
    },
    {
        "dataset_name": "vendor_c",
        "ingestion_time": "2025-04-29 11:00:00",
        "status": "In Progress",
        "log_url": "https://logs.example.com/vendor_c/20250429"
    },
]

# Create DataFrame
df = pd.DataFrame(data)
df["ingestion_time"] = pd.to_datetime(df["ingestion_time"])
df["date"] = df["ingestion_time"].dt.date

# UI title
st.title("📊 Pipeline Status Dashboard")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- Column filters ---
col1, col2, col3 = st.columns(3)

with col1:
    dataset_filter = st.multiselect(
        "Filter by Dataset", options=sorted(df["dataset_name"].unique()), default=list(df["dataset_name"].unique())
    )

with col2:
    status_filter = st.multiselect(
        "Filter by Status", options=sorted(df["status"].unique()), default=list(df["status"].unique())
    )

with col3:
    date_filter = st.date_input(
        "Filter by Date", value=None, min_value=df["date"].min(), max_value=df["date"].max()
    )

# Apply filters
filtered_df = df[
    (df["dataset_name"].isin(dataset_filter)) &
    (df["status"].isin(status_filter))
]
if date_filter:
    filtered_df = filtered_df[filtered_df["date"] == date_filter]

# Add HTML formatting
def make_clickable(val):
    return f'<a href="{val}" target="_blank">🔍 View Logs</a>'

def color_status(val):
    if val == "Success":
        return '<span style="background-color:#28a745;color:white;padding:4px 10px;border-radius:8px;font-size:90%;">✅ Success</span>'
    elif val == "Failed":
        return '<span style="background-color:#dc3545;color:white;padding:4px 10px;border-radius:8px;font-size:90%;">❌ Failed</span>'
    elif val == "In Progress":
        return '<span style="background-color:#ffc107;color:black;padding:4px 10px;border-radius:8px;font-size:90%;">⏳ In Progress</span>'
    else:
        return val

df_display = filtered_df.copy()
df_display["Status"] = df_display["status"].apply(color_status)
df_display["Log Link"] = df_display["log_url"].apply(make_clickable)
df_display = df_display.drop(columns=["status", "log_url", "date"])
df_display = df_display.rename(columns={"dataset_name": "Dataset", "ingestion_time": "Ingestion Time"})

# Show table
st.write("### Filtered Pipeline Runs")
if not df_display.empty:
    st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.warning("No data matches the selected filters.")

