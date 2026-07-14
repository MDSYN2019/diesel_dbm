
      
        
        
        delete from "fresh_segments"."analytics"."test_result_rows" as DBT_INTERNAL_DEST
        where (elementary_test_results_id) in (
            select distinct elementary_test_results_id
            from "test_result_rows__dbt_tmp205107616182" as DBT_INTERNAL_SOURCE
        );

    

    insert into "fresh_segments"."analytics"."test_result_rows" ("elementary_test_results_id", "result_row", "detected_at", "created_at")
    (
        select "elementary_test_results_id", "result_row", "detected_at", "created_at"
        from "test_result_rows__dbt_tmp205107616182"
    )
  