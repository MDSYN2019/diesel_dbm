
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select interest_name
from "fresh_segments"."analytics_analytics"."dim_interest"
where interest_name is null



  
  
      
    ) dbt_internal_test