select
    interest_id,
    interest_name,
    interest_summary,
    created_at,
    last_modified
from {{ ref('stg_fresh_segments__interest_map') }}
