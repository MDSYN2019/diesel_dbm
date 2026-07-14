with source as (
    select *
    from "fresh_segments"."fresh_segments"."interest_map"
),

renamed as (
    select
        id::integer as interest_id,
        trim(interest_name) as interest_name,
        nullif(trim(interest_summary), '') as interest_summary,
        created_at::timestamp as created_at,
        last_modified::timestamp as last_modified
    from source
)

select *
from renamed