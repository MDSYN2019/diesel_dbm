"""Streamlit data-modeling playground backed by Diesel-managed Postgres.

Run:
    streamlit run streamlit_app/app.py
"""

from __future__ import annotations

import streamlit as st

from backend_client import DieselDbClient

st.set_page_config(page_title="Diesel DBM", layout="wide")
st.title("Diesel DBM: lightweight data modeling")
st.caption("A small SQLDBM/Luna-style modeling surface using this repository as the backend.")

client = DieselDbClient.from_env()

st.subheader("1) Inspect current schema")
schema_name = st.text_input("Schema", value="public")
if st.button("Load schema"):
    rows = client.introspect_schema(schema=schema_name.strip() or "public")
    st.session_state["schema_rows"] = rows

schema_rows = st.session_state.get("schema_rows", [])
if schema_rows:
    st.dataframe(schema_rows, use_container_width=True)
else:
    st.info("No schema data loaded yet. Click 'Load schema'.")

st.subheader("2) Prototype a table")
with st.form("table_designer"):
    table_name = st.text_input("Table name", value="example_entities")
    col1_name = st.text_input("Column 1", value="name")
    col1_type = st.selectbox("Type 1", ["VARCHAR(255)", "TEXT", "INTEGER", "BOOLEAN"])
    col2_name = st.text_input("Column 2", value="description")
    col2_type = st.selectbox("Type 2", ["TEXT", "VARCHAR(255)", "INTEGER", "BOOLEAN"])
    create_btn = st.form_submit_button("Generate DDL")

if create_btn:
    if not table_name.strip() or not col1_name.strip() or not col2_name.strip():
        st.warning("Table and column names are required.")
    else:
        ddl = f"""
CREATE TABLE IF NOT EXISTS {table_name.strip()} (
    id SERIAL PRIMARY KEY,
    {col1_name.strip()} {col1_type} NOT NULL,
    {col2_name.strip()} {col2_type}
);
""".strip()
        st.session_state["generated_ddl"] = ddl

if st.session_state.get("generated_ddl"):
    st.code(st.session_state["generated_ddl"], language="sql")
    if st.button("Apply DDL to database"):
        client.apply_ddl(st.session_state["generated_ddl"])
        st.success("DDL applied. Reload schema to verify.")

st.subheader("3) Existing posts demo (from scaffold)")
if st.button("Refresh posts"):
    st.session_state["posts"] = client.list_posts()

for post in st.session_state.get("posts", []):
    st.markdown(f"### {post['title']}")
    st.write(post["body"])
    st.caption(f"id={post['id']} | published={post['published']}")
