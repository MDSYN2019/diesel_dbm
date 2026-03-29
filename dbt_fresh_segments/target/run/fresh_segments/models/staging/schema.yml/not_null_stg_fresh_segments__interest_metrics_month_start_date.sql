
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select month_start_date
from "fresh_segments"."analytics_analytics_staging"."stg_fresh_segments__interest_metrics"
where month_start_date is null



  
  
      
    ) dbt_internal_test