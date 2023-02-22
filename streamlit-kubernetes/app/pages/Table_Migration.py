import json
from copy import copy

import redshift_connector as rc
import streamlit as st
from modules.database import (connect_database, load_codebase,
                              load_database_object)
from modules.helpers import (clear_screen_mark, filter_object,
                             fn_unique_schemas,
                             fn_unique_table_per_schema_type)


def generate_migration_code(codebase, selected_obj, destiny_schema, destiny_table):
    if len(destiny_table) < 3:
        table_name = 'sem_nome_nao_vai'
    else:
        table_name = destiny_table
    code = codebase.replace(f'{selected_obj.schema_name}.{selected_obj.object_name}',
                            f'{destiny_schema}.{table_name}')
    insert = f"""\n\nINSERT INTO "{destiny_schema}"."{destiny_table}"\nSELECT * FROM "{selected_obj.schema_name}"."{selected_obj.object_name}";"""
    return code + insert


def main():
    st.set_page_config('Dax Tools', page_icon=':mechanic:')
    st.markdown('## Dax Tools Table Migration')
    
    clear_screen_mark()
    
    conn, cursor = connect_database()
    database_object_list = load_database_object(cursor, ['TABLE'])

    header = st.markdown(body='### Origem')

    col1, col2 = st.columns(2)
    with col1:
        unique_schemas = fn_unique_schemas(database_object_list)
        selected_schema = st.selectbox(label="Schema", options=unique_schemas, key='origin_schema_options')
    with col2:
        unique_objects = fn_unique_table_per_schema_type(
            database_object_list, selected_schema, 'TABLE'
        )
        selected_obj = st.selectbox(label="Tabela", options=unique_objects)

    header = st.markdown(body='### Destino')

    col3, col4 = st.columns(2)
    with col3:
        dst_schema = st.selectbox(label='Schema', options=unique_schemas, key='destiny_schema_options')
    with col4:
        dst_table = st.text_input(label='Tabela')


    load_codebase_button = st.button(
        label="Criar código de migração", type="primary", use_container_width=True
    )

    if load_codebase_button:
        database_object = filter_object(
            database_object_list,
            selected_schema,
            'TABLE',
            selected_obj,
        )
        st.session_state["codebase"] = load_codebase(database_object, cursor)
        st.session_state["migration_code"] = generate_migration_code(st.session_state["codebase"],
                                                                    database_object,
                                                                    dst_schema,
                                                                    dst_table)
        with st.expander(label="Clique para expandir"):
            st.code(body=st.session_state["migration_code"], language="sql")


if __name__ == '__main__':
    main()