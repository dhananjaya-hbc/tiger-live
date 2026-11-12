# Tiger Live: real-time streaming analytics

A simulator streams IoT-style sensor events into a Tiger Data (TimescaleDB) hypertable.
A Streamlit dashboard queries it every 2 seconds with `time_bucket` aggregations,
latest-reading lookups and a threshold alert counter, all in plain SQL.

## Run
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export TIGER_URL="postgres://USER:PASSWORD@HOST:PORT/tsdb?sslmode=require"   # from the Tiger console
python simulator.py          # terminal 1
streamlit run app.py         # terminal 2
```

Built for MLH Global Hack Week: Builders Week, Challenge 4.
