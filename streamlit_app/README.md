# Streamlit Diesel DBM prototype

This Streamlit app now provides a lightweight **data modeling interface** (in the spirit of SQLDBM/Luna) while keeping this Rust/Diesel project as backend source of truth.

## What it can do

- Introspect the current Postgres schema (`information_schema.columns`).
- Prototype a table using simple form inputs.
- Generate DDL (`CREATE TABLE ...`) and apply it directly.
- Keep the original posts list/create workflow available as a simple demo.

## Usage

1. Export `DATABASE_URL` (same connection Diesel uses).
2. Install dependencies:

   ```bash
   pip install -r streamlit_app/requirements.txt
   ```

3. Run Streamlit:

   ```bash
   streamlit run streamlit_app/app.py
   ```

## Notes

- This is a pragmatic prototype and not a full SQLDBM implementation.
- For production-grade modeling, route generated DDL through Diesel migrations.
