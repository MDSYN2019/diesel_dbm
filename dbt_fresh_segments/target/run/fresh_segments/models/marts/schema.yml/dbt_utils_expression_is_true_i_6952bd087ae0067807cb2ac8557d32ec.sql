
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  



select
    1
from "fresh_segments"."analytics_analytics"."interest_monthly_leaderboard"

where not(ranking > 0)


  
  
      
    ) dbt_internal_test