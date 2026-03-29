
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ranking
from "fresh_segments"."analytics_analytics_staging"."stg_fresh_segments__interest_metrics"
where ranking is null



  
  
      
    ) dbt_internal_test