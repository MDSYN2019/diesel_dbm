
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select interest_name
from "fresh_segments"."fresh_segments"."interest_map"
where interest_name is null



  
  
      
    ) dbt_internal_test