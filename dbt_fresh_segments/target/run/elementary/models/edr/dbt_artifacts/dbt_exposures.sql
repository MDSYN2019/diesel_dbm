
      
        
        
        delete from "fresh_segments"."analytics"."dbt_exposures" as DBT_INTERNAL_DEST
        where (unique_id) in (
            select distinct unique_id
            from "dbt_exposures__dbt_tmp205105215740" as DBT_INTERNAL_SOURCE
        );

    

    insert into "fresh_segments"."analytics"."dbt_exposures" ("unique_id", "name", "maturity", "type", "owner_email", "owner_name", "url", "depends_on_macros", "depends_on_nodes", "depends_on_columns", "description", "tags", "meta", "package_name", "original_path", "path", "generated_at", "metadata_hash", "label", "raw_queries")
    (
        select "unique_id", "name", "maturity", "type", "owner_email", "owner_name", "url", "depends_on_macros", "depends_on_nodes", "depends_on_columns", "description", "tags", "meta", "package_name", "original_path", "path", "generated_at", "metadata_hash", "label", "raw_queries"
        from "dbt_exposures__dbt_tmp205105215740"
    )
  