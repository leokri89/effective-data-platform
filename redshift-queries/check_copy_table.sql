with base as (
	select date($data) data, count(1) registros, '1' origin
	from $schema1.$tabela
	group by 1
	union all
	select date($data) data, count(1) registros, '2' origin
	from $schema2.$tabela
	group by 1
), agg_base as (
	select data,
		max(case when origin = '1' then registros end) origin_schema1,
		max(case when origin = '2' then registros end) origin_schema2
	from base
	group by 1
)
select *, (origin_schema1 - origin_schema2) count_diff
from agg_base
where (origin_schema1 - origin_schema2) != 0