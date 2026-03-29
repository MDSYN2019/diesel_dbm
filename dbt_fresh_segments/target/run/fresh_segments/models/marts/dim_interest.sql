
  
    

  create  table "fresh_segments"."analytics_analytics"."dim_interest__dbt_tmp"
  
  
    as
  
  (
    select
    interest_id,
    interest_name,
    interest_summary,
    created_at,
    last_modified
from "fresh_segments"."analytics_analytics_staging"."stg_fresh_segments__interest_map"
  );
  