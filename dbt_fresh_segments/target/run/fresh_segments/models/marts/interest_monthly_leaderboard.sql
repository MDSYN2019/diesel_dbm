
  
    

  create  table "fresh_segments"."analytics_analytics"."interest_monthly_leaderboard__dbt_tmp"
  
  
    as
  
  (
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
  );
  