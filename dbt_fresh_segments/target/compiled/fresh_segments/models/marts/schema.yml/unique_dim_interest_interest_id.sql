
    
    

select
    interest_id as unique_field,
    count(*) as n_records

from "fresh_segments"."analytics_analytics"."dim_interest"
where interest_id is not null
group by interest_id
having count(*) > 1


