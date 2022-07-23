

  create  table
    `DWH`.`dim_type__dbt_tmp`
  as (
    
with warehouse_data as (
    select * from `DWH`.`elt`
),
final as (
    SELECT distinct
    md5(cars) as Id,
    cars FROM warehouse_data
)
select * from final
  )
