import streamlit as st
from modules.helpers import clear_screen_mark

st.set_page_config('Dax Tools', page_icon=':mechanic:')
st.title('Dax Tools')

clear_screen_mark()

st.markdown(body="""
A ideia dessa aplicação é auxiliar no uso e na administração do Dax.

Para isso foram desenvolvidas as seguintes aplicações:

---

### Simple Replace
Para poder migrar os objetos do projeto de Produtização dos dados do DAX

---

### Table Migration
Facilita na geração do código para migrar a tabela de um schema para o outro.
""")