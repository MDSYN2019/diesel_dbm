
  create view "fresh_segments"."analytics_analytics_staging"."stg_fresh_segments__interest_metrics__dbt_tmp"
    
    
  as (
    with source as (
    select *
    from "fresh_segments"."fresh_segments"."interest_metrics"
),

cleaned as (
    select
        nullif(_month, 'NULL')::integer as month_number,
        nullif(_year, 'NULL')::integer as year_number,
        case
            when month_year = 'NULL' then null
            else to_date(month_year, 'MM-YYYY')
        end as month_start_date,
        nullif(interest_id, 'NULL')::integer as interest_id,
        composition::numeric(10, 4) as composition,
        index_value::numeric(10, 4) as index_value,
        ranking::integer as ranking,
        percentile_ranking::numeric(10, 4) as percentile_ranking
    from source
)

select *
from cleaned
where interest_id is not null
  );