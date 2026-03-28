# diesel_dbm

A small Rust + Diesel project for managing a Postgres schema, with a companion Streamlit UI for lightweight data modeling.

## What this repository does

- Defines a Diesel-backed `posts` model and schema in Rust.
- Exposes helper functions to:
  - connect to Postgres (`DATABASE_URL`),
  - list posts,
  - create posts.
- Includes migration utilities in Rust to:
  - generate Diesel-style migration folders (`up.sql`/`down.sql`),
  - generate simple version-to-version SQL schema diff files.
- Provides a Streamlit prototype app that can:
  - check DB health,
  - introspect schema metadata,
  - generate and apply basic `CREATE TABLE` DDL,
  - view and create posts.

## Project structure

- `src/lib.rs` – primary Rust library API (connection + post CRUD helpers).
- `src/models.rs` – Diesel structs for `Post` and `NewPost`.
- `src/schema.rs` – Diesel table schema.
- `src/migrations.rs` – migration/scaffold helper utilities.
- `migrations/` – SQL migrations tracked in source control.
- `streamlit_app/` – Python Streamlit frontend and DB client.
- `dbt_fresh_segments/` – dbt project for modeling `fresh_segments` source tables into analytics marts.

## Prerequisites

- Rust toolchain (edition 2024 project)
- PostgreSQL database
- `DATABASE_URL` environment variable set to your Postgres connection string
- (Optional for UI) Python 3 and pip

## Rust usage

Run tests:

```bash
cargo test
```

Use the library from Rust code:

```rust
use diesel_demo::{create_post, establish_connection, list_posts};

fn main() {
    let mut conn = establish_connection();
    let _ = create_post(&mut conn, "Hello", "Created from Rust");
    let posts = list_posts(&mut conn).expect("list posts");
    println!("{} posts found", posts.len());
}
```

## Streamlit UI

See `streamlit_app/README.md` for detailed UI setup. Quick start:

```bash
pip install -r streamlit_app/requirements.txt
streamlit run streamlit_app/app.py
```

## Notes

- The Streamlit app is a pragmatic modeling prototype and complements (not replaces) Diesel migrations.
- The migration helper module is useful for generating migration artifacts programmatically when needed.
