{{ config(materialized='table') }}
with source_data as (
    select * from {{ source('traffic_source', 'elt') }}
),
final as (
    SELECT distinct
    md5(cars) as Id,
    cars FROM source_data
)
select * from final
