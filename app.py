"""Live dashboard over Tiger Data. Run: TIGER_URL="postgres://..." streamlit run app.py"""
import os

import pandas as pd
import psycopg2
import streamlit as st

ALERT_TEMP = 30.0

st.set_page_config(page_title="Live Sensor Analytics", layout="wide")
st.title("Live sensor analytics on Tiger Data")
st.caption("Events stream in via simulator.py; every query below is plain SQL on a hypertable.")


@st.cache_resource
def get_conn():
    conn = psycopg2.connect(os.environ["TIGER_URL"])
    conn.autocommit = True
    return conn


def query(sql, params=None):
    return pd.read_sql(sql, get_conn(), params=params)


@st.fragment(run_every=2)
def dashboard():
    stats = query(
        """
        SELECT count(*) AS events_5m,
               round(avg(temperature)::numeric, 2) AS avg_temp,
               count(*) FILTER (WHERE temperature > %(t)s) AS alerts
        FROM sensor_events WHERE time > now() - interval '5 minutes'
        """,
        {"t": ALERT_TEMP},
    ).iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Events (last 5 min)", int(stats.events_5m))
    c2.metric("Avg temperature (C)", stats.avg_temp if stats.avg_temp is not None else "-")
    c3.metric(f"Alerts (> {ALERT_TEMP} C)", int(stats.alerts))

    ts = query(
        """
        SELECT time_bucket('10 seconds', time) AS bucket, sensor_id,
               avg(temperature) AS temperature
        FROM sensor_events
        WHERE time > now() - interval '5 minutes'
        GROUP BY bucket, sensor_id ORDER BY bucket
        """
    )
    if ts.empty:
        st.info("No data yet. Start simulator.py.")
        return
    st.subheader("Temperature by sensor (10s buckets)")
    st.line_chart(ts.pivot(index="bucket", columns="sensor_id", values="temperature"))

    st.subheader("Latest reading per sensor")
    st.dataframe(
        query(
            """
            SELECT DISTINCT ON (sensor_id) sensor_id, time, temperature, humidity
            FROM sensor_events ORDER BY sensor_id, time DESC
            """
        ),
        hide_index=True,
    )


dashboard()
