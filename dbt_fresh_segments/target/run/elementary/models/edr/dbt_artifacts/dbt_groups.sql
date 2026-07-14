
      
        
        
        delete from "fresh_segments"."analytics"."dbt_groups" as DBT_INTERNAL_DEST
        where (unique_id) in (
            select distinct unique_id
            from "dbt_groups__dbt_tmp205105182018" as DBT_INTERNAL_SOURCE
        );

    

    insert into "fresh_segments"."analytics"."dbt_groups" ("unique_id", "name", "owner_email", "owner_name", "generated_at", "metadata_hash")
    (
        select "unique_id", "name", "owner_email", "owner_name", "generated_at", "metadata_hash"
        from "dbt_groups__dbt_tmp205105182018"
    )
  