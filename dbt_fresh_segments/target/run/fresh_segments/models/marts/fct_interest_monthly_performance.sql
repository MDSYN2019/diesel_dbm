
  
    

  create  table "fresh_segments"."analytics_analytics"."fct_interest_monthly_performance__dbt_tmp"
  
  
    as
  
  (
    with metrics as (
    select *
    from "fresh_segments"."analytics_analytics_staging"."stg_fresh_segments__interest_metrics"
),

interest as (
    select *
    from "fresh_segments"."analytics_analytics"."dim_interest"
)

select
    m.month_start_date,
    m.year_number,
    m.month_number,
    m.interest_id,
    i.interest_name,
    i.interest_summary,
    m.composition,
    m.index_value,
    m.ranking,
    m.percentile_ranking,
    case
        when m.ranking <= 10 then 'top_10'
        when m.ranking <= 100 then 'top_100'
        else 'long_tail'
    end as ranking_bucket
from metrics as m
left join interest as i
    on m.interest_id = i.interest_id
  );
  