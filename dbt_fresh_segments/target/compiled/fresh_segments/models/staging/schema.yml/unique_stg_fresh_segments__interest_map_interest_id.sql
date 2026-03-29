
    
    

select
    interest_id as unique_field,
    count(*) as n_records

from "fresh_segments"."analytics_analytics_staging"."stg_fresh_segments__interest_map"
where interest_id is not null
group by interest_id
having count(*) > 1


