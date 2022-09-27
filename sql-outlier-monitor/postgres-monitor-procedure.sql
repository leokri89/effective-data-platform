create or replace procedure sp_value_check(sql_cmd text)
language plpgsql
as $$
begin
	DROP TABLE IF EXISTS tmp_chk_table;	
	EXECUTE 'create temporary table tmp_chk_table as ' || sql_cmd;
	
	create temporary table zscore_table as
	WITH data AS (
	    SELECT
	        "data",
	        value
	    from tmp_chk_table
	), data_with_stddev as (
	    select
	        "data",
	        value,
	        (value - avg(value) over ()) / (stddev(value) over ()) as zscore
	    from data
	    order by 1
	)
	select 
	    "data",
	    value,
	    zscore,
	    case
	        when abs(zscore) >= 1.645 then 'Outlier'
	        else 'Normal'
	    end test_result
	from data_with_stddev
	order by "data" desc;
	
	if exists (select * from zscore_table where test_result = 'Outlier') then 
		raise 'Encontrado Outlier';
	
	end if;
end;
$$