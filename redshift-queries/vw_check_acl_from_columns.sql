with schema_list as (
	select
		oid schema_id,
		nspname schema_name,
		nspacl schema_acl,
		nspowner schema_owner
	from pg_catalog.pg_namespace
	where oid = 16386
), table_list as (
	select
		oid table_id,
		relname table_name,
		relnamespace schema_id,
		case relkind
			when 'r' then 'ordinary table'
			when 'i' then 'index'
			when 's' then 'sequence'
			when 'v' then 'view'
			when 'c' then 'composite type'
			when 's' then 'special'
			when 't' then 'TOAST table'
			else 'other'
		end type_obj,
		relacl table_acl
	from pg_class
	where oid = 16392
), column_list as (
	select
		attrelid table_id,
		attname column_name,
		atttypid type_id,
		attacl column_acl,
		attnotnull not_null,
		pt.typname column_type
	from pg_catalog.pg_attribute_info pa
	join pg_catalog.pg_type pt on pa.atttypid = pt."oid" and pt.typname not in ('oid','tid','xid','cid')
)
select *
from schema_list
left join table_list using(schema_id)
left join column_list using(table_id)

/*
r = SELECT: LARGE OBJECT, SEQUENCE, TABLE (and table-like objects), table column
a = INSERT: TABLE, table column
w = UPDATE: LARGE OBJECT, SEQUENCE, TABLE, table column
d = DELETE: TABLE
D = TRUNCATE: TABLE
x = REFERENCES: TABLE, table column
t = TRIGGER: TABLE
C = CREATE: DATABASE, SCHEMA, TABLESPACE
c = CONNECT: DATABASE
T = TEMPORARY: DATABASE
X = EXECUTE: FUNCTION, PROCEDURE
U = USAGE: DOMAIN, FOREIGN DATA WRAPPER, FOREIGN SERVER, LANGUAGE, SCHEMA, SEQUENCE, TYPE
*/