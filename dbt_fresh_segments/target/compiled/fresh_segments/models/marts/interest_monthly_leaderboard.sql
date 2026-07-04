select
    month_start_date,
    interest_id,
    interest_name,
    ranking,
    composition,
    index_value,
    percentile_ranking
from "fresh_segments"."analytics_analytics"."fct_interest_monthly_performance"
where ranking <= 10