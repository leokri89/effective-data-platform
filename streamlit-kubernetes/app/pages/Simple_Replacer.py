import streamlit as st
from modules.database import (connect_database, load_codebase,
                              load_database_object)
from modules.helpers import (clear_screen_mark, filter_object,
                             fn_unique_schemas,
                             fn_unique_table_per_schema_type,
                             fn_unique_type_per_schema, replace_codebase)


def main():
    initialize_states()
    st.set_page_config('Dax Tools', page_icon=':mechanic:')
    st.markdown('## Dax Tools Simple Replacer')

    clear_screen_mark()
    
    conn, cursor = connect_database()
    database_object_list = load_database_object(cursor, ['VIEW','TABLE','PROCEDURE'])
    col1, col2 = st.columns(2)
    with col1:
        unique_schemas = fn_unique_schemas(database_object_list)
        selected_schema = st.selectbox(label="Schema", options=unique_schemas)
    with col2:
        unique_types = fn_unique_type_per_schema(database_object_list, selected_schema)
        selected_obj_type = st.selectbox(label="Tipo Objeto", options=unique_types)

    unique_objects = fn_unique_table_per_schema_type(
        database_object_list, selected_schema, selected_obj_type
    )
    selected_obj = st.selectbox(label="Objeto", options=unique_objects)

    load_codebase_button = st.button(
        label="Carregar código", type="primary", use_container_width=True
    )

    if load_codebase_button:
        database_object = filter_object(
            database_object_list,
            selected_schema,
            selected_obj_type,
            selected_obj,
        )
        st.session_state["codebase"] = load_codebase(database_object, cursor)
        st.session_state["codebase_loaded"] = True

    if st.session_state["codebase_loaded"]:
        with st.expander(label="Clique para expandir"):
            st.code(body=st.session_state["codebase"], language="sql")
        st.info(body="template: {'schema_original.tabela_original':'schema_novo.tabela_nova'}", icon="ℹ️")
        replace_json = st.text_area(
            label="JSON de sub stituição",
            value="{'schema_original.tabela_original':'schema_novo.tabela_nova'}",
        )
        replace_codebase_button = st.button(
            label="Substituir", type="primary", use_container_width=True
        )

        if replace_codebase_button:
            st.session_state["codebase_new"] = replace_codebase(
                st.session_state["codebase"], replace_json
            )
            with st.expander(label="Clique para expandir"):
                st.code(body=st.session_state["codebase_new"], language="sql")
            st.session_state["codebase_replaced"] = True


def initialize_states():
    if "codebase_loaded" not in st.session_state:
        st.session_state["codebase_loaded"] = False
    if "codebase_replaced" not in st.session_state:
        st.session_state["codebase_replaced"] = False
    if "codebase" not in st.session_state:
        st.session_state["codebase"] = "not_set"
    if "codebase_new" not in st.session_state:
        st.session_state["codebase_new"] = "not_set"


def clean_states():
    st.session_state["codebase_loaded"] = False
    st.session_state["codebase_replaced"] = False
    st.session_state["codebase"] = "not_set"
    st.session_state["codebase_new"] = "not_set"


def changed_object(selected_obj):
    st.session_state["codebase_loaded"] = False
    st.session_state["codebase_replaced"] = False
    st.session_state["codebase"] = "not_set"
    st.session_state["codebase_new"] = "not_set"


if __name__ == '__main__':
    main()