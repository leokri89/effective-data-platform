import json
from copy import copy

import streamlit as st


def clear_screen_mark():
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    return st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def fn_unique_schemas(object_list):
    return set(database_object.schema_name for database_object in object_list)


def fn_unique_type_per_schema(object_list, schema_name):
    return set(
        database_object.object_type
        for database_object in object_list
        if database_object.schema_name == schema_name
    )


def fn_unique_table_per_schema_type(object_list, schema_name, object_type):
    uniques = set()
    for database_object in object_list:
        if (database_object.schema_name == schema_name) and (
            database_object.object_type == object_type
        ):
            uniques.add(database_object.object_name)
    return uniques


def filter_object(object_list, schema_name, object_type, object_name):
    for database_object in object_list:
        if (
            (database_object.schema_name == schema_name)
            and (database_object.object_type == object_type)
            and (database_object.object_name == object_name)
        ):
            return database_object
        

def replace_codebase(codebase, replace_text):
    replaced_codebase = copy(codebase)
    replace_list = json.loads(f"[{replace_text}]".replace("'", '"'))
    for replace_item in replace_list:
        for key in replace_item:
            replaced_codebase = replaced_codebase.replace(key, replace_item[key])
    return replaced_codebase
