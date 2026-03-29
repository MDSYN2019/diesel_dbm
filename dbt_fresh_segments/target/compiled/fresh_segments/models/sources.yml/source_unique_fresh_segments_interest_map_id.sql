
    
    

select
    id as unique_field,
    count(*) as n_records

from "fresh_segments"."fresh_segments"."interest_map"
where id is not null
group by id
having count(*) > 1


