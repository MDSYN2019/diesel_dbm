
      
        
        
        delete from "fresh_segments"."analytics"."dbt_seeds" as DBT_INTERNAL_DEST
        where (unique_id) in (
            select distinct unique_id
            from "dbt_seeds__dbt_tmp205105889197" as DBT_INTERNAL_SOURCE
        );

    

    insert into "fresh_segments"."analytics"."dbt_seeds" ("unique_id", "alias", "checksum", "tags", "meta", "owner", "database_name", "schema_name", "description", "name", "package_name", "original_path", "path", "generated_at", "metadata_hash", "group_name")
    (
        select "unique_id", "alias", "checksum", "tags", "meta", "owner", "database_name", "schema_name", "description", "name", "package_name", "original_path", "path", "generated_at", "metadata_hash", "group_name"
        from "dbt_seeds__dbt_tmp205105889197"
    )
  