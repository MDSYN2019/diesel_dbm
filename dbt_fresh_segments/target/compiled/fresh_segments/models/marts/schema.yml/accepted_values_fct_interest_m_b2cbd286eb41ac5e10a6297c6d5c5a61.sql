
    
    

with all_values as (

    select
        ranking_bucket as value_field,
        count(*) as n_records

    from "fresh_segments"."analytics_analytics"."fct_interest_monthly_performance"
    group by ranking_bucket

)

select *
from all_values
where value_field not in (
    'top_10','top_100','long_tail'
)


