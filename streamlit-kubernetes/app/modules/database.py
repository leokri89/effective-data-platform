import redshift_connector as rc
import streamlit as st
from pydantic import BaseModel


class DatabaseObject(BaseModel):
    schema_name: str
    object_name: str
    object_type: str


class DatabaseDataTypes(BaseModel):
    oid: str
    type_name: str


def get_tables(cursor):
    cursor.execute("""
    SELECT schema_name, table_name obj_name, table_type 
    FROM pg_catalog.svv_all_tables
    WHERE table_type = 'TABLE' and schema_name in ('dax_stage','dax_core');
    """)
    result = cursor.fetchall()
    return [DatabaseObject(schema_name=item[0], object_name=item[1], object_type=item[2]) for item in result]


def get_views(cursor):
    cursor.execute("""
    SELECT schema_name, table_name obj_name, table_type 
    FROM pg_catalog.svv_all_tables
    WHERE table_type = 'VIEW' and schema_name in ('dax_stage','dax_core');
    """)
    result = cursor.fetchall()
    return [DatabaseObject(schema_name=item[0], object_name=item[1], object_type=item[2]) for item in result]


def filter_database_type(x, database_type_list):
    for type_item in database_type_list:
        if x == int(type_item.oid):
            return type_item.type_name
    return ""


def get_database_data_types(cursor):
    cursor.execute("""SELECT oid, typname FROM pg_catalog.pg_type;""")
    database_data_types = cursor.fetchall()
    return [DatabaseDataTypes(oid=item[0], type_name=item[1]) for item in database_data_types]


def get_procedures(cursor):
    database_type_list = get_database_data_types(cursor)
    cursor.execute("""
    SELECT
        nspname schema_name,
        proname,
        proc.proargtypes,
        'PROCEDURE' as obj_type
    FROM pg_catalog.pg_proc_info proc
    JOIN pg_catalog.pg_namespace pn on proc.pronamespace = pn.oid
    WHERE nspname in ('dax_stage','dax_core');
    """
    )
    result = cursor.fetchall()
    procedure_list = []
    for item in result:
        args = []
        if len(item[2]) > 0:
            args_types_oid = [int(oid) for oid in item[2].split(" ")]
            for oid in args_types_oid:
                args.append(filter_database_type(oid, database_type_list))
            object_name = f'{item[1]}({", ".join(args)})'
        else:
            object_name = item[1]
        database_object = DatabaseObject(
            schema_name=item[0], object_name=object_name, object_type=item[3]
        )
        procedure_list.append(database_object)
    return procedure_list


def load_codebase(_database_object, _cursor):
    object_type_sql = {
        'VIEW': f'SHOW VIEW {_database_object.schema_name}.{_database_object.object_name}',
        'TABLE': f'SHOW TABLE {_database_object.schema_name}.{_database_object.object_name}',
        'PROCEDURE': f'SHOW PROCEDURE {_database_object.schema_name}.{_database_object.object_name}'
    }
    if _database_object.object_type in ['VIEW','TABLE','PROCEDURE']:
        _cursor.execute(object_type_sql[_database_object.object_type])
        code = _cursor.fetchone()[0]
    else:
        code = 'Err'
    return code


@st.cache_resource
def connect_database():
    conn = rc.connect(
        host="",
        port=5439,
        database="",
        user="",
        password="",
    )
    cursor = conn.cursor()
    return conn, cursor


@st.cache_data
def load_database_object(_cursor, object_types):
    fn_list = {
        'TABLE': get_tables,
        'VIEW': get_views,
        'PROCEDURE': get_procedures
    }
    object_list = []
    for object_type in object_types:
        object_list = object_list + fn_list[object_type](_cursor)
    return object_list


def load_dummy_database_objects():
    dummies = [('dax_core','sp_load_ent_base_active(timestamp)','PROCEDURE'),
               ('dax_stage','tmp_view', 'VIEW'),
               ('dax_core','stg_ent_transaction_chargeback_recovery_payware_fee','TABLE'),
               ('dax_core','portfolio_history','TABLE')]
    return [DatabaseObject(schema_name=item[0], object_name=item[1], object_type=item[2]) for item in dummies]

