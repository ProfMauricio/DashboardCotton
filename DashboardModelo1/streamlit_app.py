import streamlit as st


custo_producao_page = st.Page("dashboard_custo_producao.py", title="Custo de Produção",
                              icon=":material/empty_dashboard:")

custo_

pg = st.navigation([custo_producao_page, st.Page("dashboard_modelo1.py")])

pg.run()
