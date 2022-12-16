select *
from stl_return
where query in (select query from stl_query where pid = $1 and xid = $2) and
  slice not in (select slice from stv_slices)
 order by slice asc;  
