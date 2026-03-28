# Fresh Segments dbt project

This dbt project models the `fresh_segments` schema loaded by `sql/fresh_segments.sql` in Postgres.

## What is included

- **Sources** for:
  - `fresh_segments.interest_map`
  - `fresh_segments.interest_metrics`
- **Staging models** to normalize types and clean placeholder `'NULL'` strings.
- **Mart models**:
  - `dim_interest` (dimension table)
  - `fct_interest_monthly_performance` (monthly fact table)
- **Data quality tests** for nulls, uniqueness, relationships, and accepted values.

## Prerequisites

1. Install dbt with Postgres adapter:

   ```bash
   pip install dbt-postgres
   ```

2. Set a profile in `~/.dbt/profiles.yml`:

   ```yaml
   fresh_segments:
     target: dev
     outputs:
       dev:
         type: postgres
         host: "{{ env_var('PGHOST', 'localhost') }}"
         port: "{{ env_var('PGPORT', '5432') | int }}"
         user: "{{ env_var('PGUSER') }}"
         pass: "{{ env_var('PGPASSWORD') }}"
         dbname: "{{ env_var('PGDATABASE') }}"
         schema: analytics
         threads: 4
   ```

3. (Optional) If your source database differs from the target database, set:

   ```bash
   export DBT_DATABASE=your_source_database
   ```

## Run

From `dbt_fresh_segments/`:

```bash
dbt debug
dbt run
dbt test
```


## Sanity-check compiled SQL in a separate folder

Use the helper script to render Jinja templates into raw SQL without writing to the default `target/` directory:

```bash
cd dbt_fresh_segments
scripts/dbt_sanity_sql.sh
```

This compiles into `dbt_fresh_segments/sanity_sql/target/compiled/fresh_segments/models/` so you can inspect the rendered SQL separately from normal dbt artifacts.

Optional examples:

```bash
# only compile marts models
scripts/dbt_sanity_sql.sh --select marts.*

# customize output folder
SANITY_DIR=tmp/sanity_sql scripts/dbt_sanity_sql.sh
```

## Model graph

```text
fresh_segments.interest_map  ──> stg_fresh_segments__interest_map ──> dim_interest
fresh_segments.interest_metrics ─> stg_fresh_segments__interest_metrics ─> fct_interest_monthly_performance
                                                                      dim_interest ────┘
```
