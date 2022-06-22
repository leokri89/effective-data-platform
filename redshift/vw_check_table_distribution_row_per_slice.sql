WITH query AS (
    SELECT tb1.id,
        node,
        tb1.slice,
        tb3."schema" schema_name,
        tb1.name table_name,
        tb3.diststyle,
        sum(rows) as n_rows,
        round(max(size) / max(tbl_rows)*sum(rows),2) estimated_node_size,
        max(tbl_rows) tbl_rows,
        max(size) total_size,
        sysdate dat_load
    FROM STV_TBL_PERM tb1, STV_SLICES tb2, SVV_TABLE_INFO tb3
    WHERE tb1.slice = tb2.slice
        AND tb1.id = tb3.table_id
        AND schema_name not like 'pg_temp_%'
    GROUP BY tb1.id,
        node,
        tb3."schema",
        tb1.name,
        tb3.diststyle,
        tb1.slice
)
SELECT *
FROM query
