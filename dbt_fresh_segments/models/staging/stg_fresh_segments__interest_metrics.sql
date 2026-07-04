


with source as (
    select *
    from {{ source('fresh_segments', 'interest_metrics') }}
),

cleaned as (
    select
        nullif(_month, 'NULL')::integer as month_number,
        nullif(_year, 'NULL')::integer as year_number,
	month_year as month_start_date,
	nullif(interest_id, 'NULL')::integer as interest_id,
        composition::numeric(10, 4) as composition,
        index_value::numeric(10, 4) as index_value,
        ranking::integer as ranking,
        percentile_ranking::numeric(10, 4) as percentile_ranking
    from source
    where month_year is not null
)

select *
from cleaned
where interest_id is not null
