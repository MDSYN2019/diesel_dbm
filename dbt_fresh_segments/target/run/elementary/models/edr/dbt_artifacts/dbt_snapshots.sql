
      
        
        
        delete from "fresh_segments"."analytics"."dbt_snapshots" as DBT_INTERNAL_DEST
        where (unique_id) in (
            select distinct unique_id
            from "dbt_snapshots__dbt_tmp205105926016" as DBT_INTERNAL_SOURCE
        );

    

    insert into "fresh_segments"."analytics"."dbt_snapshots" ("unique_id", "alias", "checksum", "materialization", "tags", "meta", "owner", "database_name", "schema_name", "depends_on_macros", "depends_on_nodes", "description", "name", "package_name", "original_path", "path", "patch_path", "generated_at", "metadata_hash", "unique_key", "incremental_strategy", "group_name", "access")
    (
        select "unique_id", "alias", "checksum", "materialization", "tags", "meta", "owner", "database_name", "schema_name", "depends_on_macros", "depends_on_nodes", "description", "name", "package_name", "original_path", "path", "patch_path", "generated_at", "metadata_hash", "unique_key", "incremental_strategy", "group_name", "access"
        from "dbt_snapshots__dbt_tmp205105926016"
    )
  