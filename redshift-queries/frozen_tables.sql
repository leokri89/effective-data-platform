with tables as (
	select
		data_colecao,
		schema_name,
		table_name,
		(schema_name || '.' || table_name) full_table_name,
		table_size,
		lag(table_size) over(partition by schema_name, table_name order by data_colecao) prev_table_size,
		table_rows,
		lag(table_rows) over(partition by schema_name, table_name order by data_colecao) prev_table_rows
	from dax_tools.dax_table_size_history
	order by schema_name, table_name
), table_change_test as (
	select *,
		(table_size = prev_table_size) is_table_size_equal,
		(table_rows = prev_table_rows) is_table_rows_equal,,
		case
			when (table_size = prev_table_size) and (table_rows = prev_table_rows) then true
			else false
		end is_table_equal
	from tables
), calculate_equal_days as (
	select *,
		sum((case when is_table_equal and date(data_colecao) > current_date -7 then 1 end)) over(partition by full_table_name) is_table_equal_7days,
		sum((case when is_table_equal and date(data_colecao) > current_date -15 then 1 end)) over(partition by full_table_name) is_table_equal_15days,
		sum((case when is_table_equal and date(data_colecao) > current_date -30 then 1 end)) over(partition by full_table_name) is_table_equal_30days,
		sum((case when is_table_equal and date(data_colecao) > current_date -45 then 1 end)) over(partition by full_table_name) is_table_equal_45days,
		sum((case when is_table_equal and date(data_colecao) > current_date -60 then 1 end)) over(partition by full_table_name) is_table_equal_60days
	from table_change_test
	where full_table_name in (select full_table_name from tables where date(data_colecao) = current_date)
)
select * from calculate_equal_days
where date(data_colecao) =  (select date(max(data_colecao)) from tables);
