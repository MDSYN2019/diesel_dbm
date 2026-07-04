# Airflow dbt pipelines

This directory contains Airflow DAGs for running the `dbt_fresh_segments` project on a schedule.

## DAGs

- `fresh_segments_dbt_daily` runs daily at `06:00 UTC`:
  1. `dbt deps`
  2. `dbt debug`
  3. `dbt run`
  4. `dbt test`
- `fresh_segments_dbt_compile_check` runs every 6 hours and executes `dbt compile` into a separate `airflow_compile_target/` folder.

Both DAGs are defined in `python/dags/dbt_fresh_segments.py`.

## Prerequisites

Install Airflow and dbt in the Python environment used by your Airflow scheduler and workers:

```bash
pip install "apache-airflow>=2.8" dbt-postgres
```

Create or mount a dbt profile that matches the `fresh_segments` dbt project. By default, Airflow will look in `~/.dbt/profiles.yml`:

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

## Configuration

The DAG reads these environment variables when Airflow parses the DAG file:

| Variable | Default | Purpose |
| --- | --- | --- |
| `DIESEL_DBM_REPO_ROOT` | `/workspace/diesel_dbm` | Repository path available to Airflow. |
| `DBT_FRESH_SEGMENTS_PROJECT_DIR` | `$DIESEL_DBM_REPO_ROOT/dbt_fresh_segments` | dbt project directory. |
| `DBT_PROFILES_DIR` | `~/.dbt` | Directory containing `profiles.yml`. |
| `DBT_TARGET` | `dev` | dbt target name. |
| `DBT_SELECT` | unset | Optional dbt selector passed to `run`, `test`, and `compile`. |
| `DBT_EXCLUDE` | unset | Optional dbt exclusion selector. |
| `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE` | unset | Postgres connection values consumed by the dbt profile. |
| `DBT_DATABASE` | target database | Optional source database override used by `dbt_fresh_segments/models/sources.yml`. |

> Note: if you set `DBT_SELECT` or `DBT_EXCLUDE`, it is appended to the `run`, `test`, and `compile` commands. Leave both unset for full-project runs.

## Local Airflow quick start

From the repository root:

```bash
export AIRFLOW_HOME="$PWD/.airflow"
export AIRFLOW__CORE__DAGS_FOLDER="$PWD/python/dags"
export DIESEL_DBM_REPO_ROOT="$PWD"
export DBT_PROFILES_DIR="$HOME/.dbt"
export DBT_TARGET=dev

# Set these to match your Postgres database.
export PGHOST=localhost
export PGPORT=5432
export PGUSER=postgres
export PGPASSWORD=mypassword
export PGDATABASE=fresh_segments

# Initialize Airflow metadata and start Airflow locally.
airflow db migrate
airflow standalone
```

Open the Airflow UI URL printed by `airflow standalone`, enable the DAG you want, and trigger it manually or wait for the next scheduled run.

## Command-line validation

Before enabling the DAG, validate the dbt project directly:

```bash
cd dbt_fresh_segments
dbt deps --profiles-dir "$DBT_PROFILES_DIR" --target "$DBT_TARGET"
dbt debug --profiles-dir "$DBT_PROFILES_DIR" --target "$DBT_TARGET"
dbt run --profiles-dir "$DBT_PROFILES_DIR" --target "$DBT_TARGET"
dbt test --profiles-dir "$DBT_PROFILES_DIR" --target "$DBT_TARGET"
```

You can also check that Airflow can parse the DAG file:

```bash
airflow dags list | grep fresh_segments
```
