-- Feature Engineering Query using JOINs, CTEs, and Window Functions
-- Target: Calculate price volatility, month-over-month price changes, and aggregate features per client

WITH monthly_price_changes AS (
    SELECT 
        id,
        price_date,
        price_off_peak_var,
        price_peak_var,
        price_off_peak_fix,
        -- Window Function 1: Get previous month's off-peak variable price
        LAG(price_off_peak_var, 1) OVER (
            PARTITION BY id 
            ORDER BY price_date
        ) AS prev_off_peak_var,
        -- Window Function 2: Calculate average off-peak variable price across all recorded months per client
        AVG(price_off_peak_var) OVER (
            PARTITION BY id
        ) AS avg_off_peak_var,
        -- Window Function 3: Calculate price variance over the 12-month window
        MAX(price_off_peak_var) OVER (PARTITION BY id) - MIN(price_off_peak_var) OVER (PARTITION BY id) AS price_range_off_peak_var
    FROM price_data
),

dec_jan_prices AS (
    SELECT 
        id,
        -- Extract January price (first month of year)
        MAX(CASE WHEN strftime('%m', price_date) = '01' THEN price_off_peak_var END) AS jan_off_peak_var,
        MAX(CASE WHEN strftime('%m', price_date) = '01' THEN price_off_peak_fix END) AS jan_off_peak_fix,
        -- Extract December price (last month of year)
        MAX(CASE WHEN strftime('%m', price_date) = '12' THEN price_off_peak_var END) AS dec_off_peak_var,
        MAX(CASE WHEN strftime('%m', price_date) = '12' THEN price_off_peak_fix END) AS dec_off_peak_fix
    FROM price_data
    GROUP BY id
)

SELECT 
    c.id,
    c.channel_sales,
    c.cons_12m,
    c.cons_gas_12m,
    c.cons_last_month,
    c.net_margin,
    c.num_years_antig AS tenure_years,
    c.churn,
    -- Price differences calculated from Dec and Jan prices (Estelle's hypothesis)
    (p.dec_off_peak_var - p.jan_off_peak_var) AS offpeak_diff_dec_jan_energy,
    (p.dec_off_peak_fix - p.jan_off_peak_fix) AS offpeak_diff_dec_jan_power,
    -- Aggregated window stats
    m.avg_off_peak_var,
    m.price_range_off_peak_var
FROM client_data c
LEFT JOIN dec_jan_prices p ON c.id = p.id
LEFT JOIN (
    SELECT id, avg_off_peak_var, price_range_off_peak_var 
    FROM monthly_price_changes 
    GROUP BY id
) m ON c.id = m.id;