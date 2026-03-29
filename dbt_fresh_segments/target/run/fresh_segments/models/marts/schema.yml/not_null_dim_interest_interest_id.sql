
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select interest_id
from "fresh_segments"."analytics_analytics"."dim_interest"
where interest_id is null



  
  
      
    ) dbt_internal_test