
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select month_start_date
from "fresh_segments"."analytics_analytics"."interest_monthly_leaderboard"
where month_start_date is null



  
  
      
    ) dbt_internal_test