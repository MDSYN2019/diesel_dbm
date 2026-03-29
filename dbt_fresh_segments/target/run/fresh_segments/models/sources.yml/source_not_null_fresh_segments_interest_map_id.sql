
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select id
from "fresh_segments"."fresh_segments"."interest_map"
where id is null



  
  
      
    ) dbt_internal_test