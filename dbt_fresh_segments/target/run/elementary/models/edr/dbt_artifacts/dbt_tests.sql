
      
        
        
        delete from "fresh_segments"."analytics"."dbt_tests" as DBT_INTERNAL_DEST
        where (unique_id) in (
            select distinct unique_id
            from "dbt_tests__dbt_tmp205106239528" as DBT_INTERNAL_SOURCE
        );

    

    insert into "fresh_segments"."analytics"."dbt_tests" ("unique_id", "database_name", "schema_name", "name", "short_name", "alias", "test_column_name", "severity", "warn_if", "error_if", "test_params", "test_namespace", "test_original_name", "tags", "model_tags", "model_owners", "meta", "depends_on_macros", "depends_on_nodes", "parent_model_unique_id", "description", "package_name", "type", "original_path", "path", "generated_at", "metadata_hash", "quality_dimension", "group_name")
    (
        select "unique_id", "database_name", "schema_name", "name", "short_name", "alias", "test_column_name", "severity", "warn_if", "error_if", "test_params", "test_namespace", "test_original_name", "tags", "model_tags", "model_owners", "meta", "depends_on_macros", "depends_on_nodes", "parent_model_unique_id", "description", "package_name", "type", "original_path", "path", "generated_at", "metadata_hash", "quality_dimension", "group_name"
        from "dbt_tests__dbt_tmp205106239528"
    )
  