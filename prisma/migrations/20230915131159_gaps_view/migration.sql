-- ohlcv 1 day gaps report

CREATE OR REPLACE VIEW ohlcv_1day_gaps AS
WITH date_series AS (
    SELECT generate_series(
        date_trunc('day', now() - interval '1 year')::date,
        date_trunc('day', now())::date,
        interval '1 day'
    )::date AS date_series
)

SELECT
    ds.date_series,
    COALESCE(ohlcv.exchange, pairs.exchange) AS exchange,
    COALESCE(ohlcv.token, pairs.token) AS token
FROM date_series ds
CROSS JOIN (
    SELECT DISTINCT exchange, token
    FROM one_day_ohlcv_data
) AS pairs
LEFT JOIN one_day_ohlcv_data ohlcv
    ON ds.date_series = date_trunc('day', ohlcv."updatedAt")::date
    AND ohlcv.exchange = pairs.exchange
    AND ohlcv.token = pairs.token
WHERE ohlcv."updatedAt" IS NULL
ORDER BY exchange, token, date_series;


-- ohlcv 1 hour gaps report

CREATE OR REPLACE VIEW ohlcv_1hour_gaps AS
WITH date_series AS (
    SELECT generate_series(
        date_trunc('hour', now() - interval '1 month')::timestamp,
        date_trunc('hour', now())::timestamp,
        interval '1 hour'
    ) AS date_series
)

SELECT
    ds.date_series,
    COALESCE(ohlcv.exchange, pairs.exchange) AS exchange,
    COALESCE(ohlcv.token, pairs.token) AS token
FROM date_series ds
CROSS JOIN (
    SELECT DISTINCT exchange, token
    FROM one_hour_ohlcv_data
) AS pairs
LEFT JOIN one_hour_ohlcv_data ohlcv
    ON ds.date_series = date_trunc('hour', ohlcv."updatedAt")::timestamp
    AND ohlcv.exchange = pairs.exchange
    AND ohlcv.token = pairs.token
WHERE ohlcv."updatedAt" IS NULL
ORDER BY exchange, token, date_series;

-- ohlcv 1 minute gaps report
CREATE OR REPLACE VIEW ohlcv_1min_gaps AS
WITH date_series AS (
    SELECT generate_series(
        date_trunc('minute', now() - interval '1 day')::timestamp,
        date_trunc('minute', now())::timestamp,
        interval '1 minute'
    ) AS date_series
)

SELECT
    ds.date_series,
    COALESCE(ohlcv.exchange, pairs.exchange) AS exchange,
    COALESCE(ohlcv.token, pairs.token) AS token
FROM date_series ds
CROSS JOIN (
    SELECT DISTINCT exchange, token
    FROM one_min_ohlcv_data
) AS pairs
LEFT JOIN one_min_ohlcv_data ohlcv
    ON ds.date_series = date_trunc('minute', ohlcv."updatedAt")::timestamp
    AND ohlcv.exchange = pairs.exchange
    AND ohlcv.token = pairs.token
WHERE ohlcv."updatedAt" IS NULL
ORDER BY exchange, token, date_series;
