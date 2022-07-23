{{ config(materialized='table') }}
with source_data as (
    select * from {{ source('traffic_source', 'elt') }}
),
final as (
    SELECT cars, traveled_d, avg_speed, lat, lon, speed, lon_acc, lat_acc
    FROM source_data
)
select * from final
