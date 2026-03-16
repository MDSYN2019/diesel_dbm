"""Starter Streamlit app for extending Diesel-backed features.

Run:
    streamlit run streamlit_app/app.py
"""

from __future__ import annotations

import streamlit as st

from backend_client import DieselDbClient

st.set_page_config(page_title="Diesel + Streamlit starter", layout="wide")
st.title("Diesel + Streamlit integration starter")

client = DieselDbClient.from_env()

st.subheader("Backend health")
if st.button("Check health"):
    st.json(client.health())

st.subheader("Create post")
with st.form("create_post"):
    title = st.text_input("Title")
    body = st.text_area("Body")
    submitted = st.form_submit_button("Create")

if submitted:
    if title.strip() and body.strip():
        created = client.create_post(title=title.strip(), body=body.strip())
        st.success(f"Created post #{created['id']}")
    else:
        st.warning("Title and body are required")

st.subheader("Posts")
if st.button("Refresh posts"):
    st.session_state["posts"] = client.list_posts()

for post in st.session_state.get("posts", []):
    st.markdown(f"### {post['title']}")
    st.write(post["body"])
    st.caption(f"id={post['id']} | published={post['published']}")
