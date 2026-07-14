
      
        
        
        delete from "fresh_segments"."analytics"."dbt_metrics" as DBT_INTERNAL_DEST
        where (unique_id) in (
            select distinct unique_id
            from "dbt_metrics__dbt_tmp205105614877" as DBT_INTERNAL_SOURCE
        );

    

    insert into "fresh_segments"."analytics"."dbt_metrics" ("unique_id", "name", "label", "model", "type", "sql", "timestamp", "filters", "time_grains", "dimensions", "depends_on_macros", "depends_on_nodes", "description", "tags", "meta", "package_name", "original_path", "path", "generated_at", "metadata_hash", "group_name")
    (
        select "unique_id", "name", "label", "model", "type", "sql", "timestamp", "filters", "time_grains", "dimensions", "depends_on_macros", "depends_on_nodes", "description", "tags", "meta", "package_name", "original_path", "path", "generated_at", "metadata_hash", "group_name"
        from "dbt_metrics__dbt_tmp205105614877"
    )
  