CREATE TABLE IF NOT EXISTS sensor_events (
  time        TIMESTAMPTZ NOT NULL,
  sensor_id   TEXT NOT NULL,
  temperature DOUBLE PRECISION,
  humidity    DOUBLE PRECISION
);

SELECT create_hypertable('sensor_events', 'time', if_not_exists => TRUE);
