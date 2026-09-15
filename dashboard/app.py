import json
import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from observability.metrics import calculate_metrics, analyse_tools, load_logs
from observability.alerts import detect_incidents


st.set_page_config(
    page_title="AI Incident Response",
    layout="wide"
)

st.title("AI Incident Response Platform")
st.caption("Production AI monitoring and incident investigation")


# Load production data
logs = load_logs()
metrics = calculate_metrics(logs)
tool_metrics = analyse_tools(logs)
incidents = detect_incidents(logs)


# System status
if incidents:
    st.error("INCIDENT DETECTED")
else:
    st.success("SYSTEM HEALTHY")


# Main metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Requests",
        metrics["total_requests"]
    )

with col2:
    st.metric(
        "Error Rate",
        f'{metrics["error_rate"]}%'
    )

with col3:
    st.metric(
        "Failed Requests",
        metrics["failed_requests"]
    )

with col4:
    st.metric(
        "Average Latency",
        f'{metrics["average_latency_ms"]} ms'
    )


st.divider()


# Incidents
st.header("Detected Incidents")

if incidents:

    for incident in incidents:

        with st.expander(
            f'{incident["severity"]} — {incident["type"]}'
        ):

            st.write(
                incident["message"]
            )

            if "tool" in incident:
                st.write(
                    f'Tool: **{incident["tool"]}**'
                )

else:

    st.info("No incidents detected.")


st.divider()


# Tool performance
st.header("Tool Performance")

tool_rows = []

for tool, stats in tool_metrics.items():

    tool_rows.append({
        "Tool": tool,
        "Requests": stats["requests"],
        "Failures": stats["failures"],
        "Error Rate": f'{stats["error_rate"]}%',
        "Average Latency": f'{stats["average_latency_ms"]} ms'
    })


st.dataframe(
    tool_rows,
    use_container_width=True
)


st.divider()


# Raw logs
st.header("Production Logs")

with st.expander("View production logs"):

    st.dataframe(
        logs,
        use_container_width=True
    )


st.divider()


# AI investigation
st.header("AI Incident Investigation")

report_files = []

try:

    import os

    report_files = sorted(
        os.listdir("incidents/reports"),
        reverse=True
    )

except FileNotFoundError:

    pass


if report_files:

    selected_report = st.selectbox(
        "Select an incident report",
        report_files
    )

    with open(
        f"incidents/reports/{selected_report}",
        "r"
    ) as file:

        report_data = json.load(file)

    st.subheader("Incident")

    st.json(
        report_data["incident"]
    )

    st.subheader("AI Investigation")

    st.write(
        report_data["report"]
    )

else:

    st.info(
        "No AI incident reports have been generated yet."
    )
