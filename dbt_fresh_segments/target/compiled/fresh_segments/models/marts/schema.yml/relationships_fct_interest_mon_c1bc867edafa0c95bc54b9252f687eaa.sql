
    
    

with child as (
    select interest_id as from_field
    from "fresh_segments"."analytics_analytics"."fct_interest_monthly_performance"
    where interest_id is not null
),

parent as (
    select interest_id as to_field
    from "fresh_segments"."analytics_analytics"."dim_interest"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


