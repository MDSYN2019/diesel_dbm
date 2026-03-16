# Streamlit integration scaffold

This folder is a starter template for building Streamlit features against the
same Postgres schema managed by Diesel.

## Why this exists

- Rust (`diesel_demo`) remains the source of truth for migrations and backend logic.
- Streamlit can add UI/features quickly by reusing `DATABASE_URL` and existing tables.
- `backend_client.py` centralizes connection/query code so future functions are easy to add.

## Usage

1. Export the same `DATABASE_URL` you use for Diesel.
2. Install Python dependencies:

   ```bash
   pip install -r streamlit_app/requirements.txt
   ```

3. Run Streamlit:

   ```bash
   streamlit run streamlit_app/app.py
   ```

## Extending for future functions

- Add new methods to `DieselDbClient` for each new feature.
- Keep SQL in `backend_client.py`, keep UI in `app.py` or feature modules.
- If you add new tables, create a Diesel migration first, then consume them here.
