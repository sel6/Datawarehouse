

  create  table
    `DWH`.`fact_source__dbt_tmp`
  as (
    
with warehouse_data as (
    select * from `DWH`.`elt`
),
final as (
    SELECT cars, traveled_d, avg_speed, lat, lon, speed, lon_acc, lat_acc
    FROM warehouse_data
)
select * from final
  )
