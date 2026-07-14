
  create view "fresh_segments"."analytics"."dbt_artifacts_hashes__dbt_tmp"
    
    
  as (
    




select
  'dbt_models' as artifacts_model,
   metadata_hash
from "fresh_segments"."analytics"."dbt_models"
 union all 

select
  'dbt_tests' as artifacts_model,
   metadata_hash
from "fresh_segments"."analytics"."dbt_tests"
 union all 

select
  'dbt_sources' as artifacts_model,
   metadata_hash
from "fresh_segments"."analytics"."dbt_sources"
 union all 

select
  'dbt_snapshots' as artifacts_model,
   metadata_hash
from "fresh_segments"."analytics"."dbt_snapshots"
 union all 

select
  'dbt_metrics' as artifacts_model,
   metadata_hash
from "fresh_segments"."analytics"."dbt_metrics"
 union all 

select
  'dbt_exposures' as artifacts_model,
   metadata_hash
from "fresh_segments"."analytics"."dbt_exposures"
 union all 

select
  'dbt_seeds' as artifacts_model,
   metadata_hash
from "fresh_segments"."analytics"."dbt_seeds"
 union all 

select
  'dbt_columns' as artifacts_model,
   metadata_hash
from "fresh_segments"."analytics"."dbt_columns"
 union all 

select
  'dbt_groups' as artifacts_model,
   metadata_hash
from "fresh_segments"."analytics"."dbt_groups"


order by metadata_hash
  );