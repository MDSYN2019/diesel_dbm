"""Airflow DAGs for orchestrating the Fresh Segments dbt project.

The DAGs assume dbt is installed in the Airflow worker/scheduler environment and
that a valid dbt profile is available via ``DBT_PROFILES_DIR`` or the default
``~/.dbt`` location.
"""

from __future__ import annotations

import os
import shlex
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

REPO_ROOT = os.environ.get("DIESEL_DBM_REPO_ROOT", "/workspace/diesel_dbm")
DBT_PROJECT_DIR = os.environ.get(
    "DBT_FRESH_SEGMENTS_PROJECT_DIR",
    os.path.join(REPO_ROOT, "dbt_fresh_segments"),
)
DBT_PROFILES_DIR = os.environ.get("DBT_PROFILES_DIR", os.path.expanduser("~/.dbt"))
DBT_TARGET = os.environ.get("DBT_TARGET", "dev")
DBT_SELECT = os.environ.get("DBT_SELECT", "")
DBT_EXCLUDE = os.environ.get("DBT_EXCLUDE", "")


def dbt_command(command: str, *, include_selectors: bool = True) -> str:
    """Build a dbt CLI command with common project/profile arguments."""
    select_clause = f" --select {shlex.quote(DBT_SELECT)}" if include_selectors and DBT_SELECT else ""
    exclude_clause = f" --exclude {shlex.quote(DBT_EXCLUDE)}" if include_selectors and DBT_EXCLUDE else ""

    return (
        f"cd {shlex.quote(DBT_PROJECT_DIR)} && "
        f"dbt {command} "
        f"--project-dir {shlex.quote(DBT_PROJECT_DIR)} "
        f"--profiles-dir {shlex.quote(DBT_PROFILES_DIR)} "
        f"--target {shlex.quote(DBT_TARGET)}"
        f"{select_clause}{exclude_clause}"
    )


DEFAULT_ARGS = {
    "owner": "data-platform",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

DBT_ENV = {
    "DBT_PROFILES_DIR": DBT_PROFILES_DIR,
    "DBT_TARGET": DBT_TARGET,
    **os.environ,
}

with DAG(
    dag_id="fresh_segments_dbt_daily",
    description="Run and test the Fresh Segments dbt project every day.",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["dbt", "fresh_segments", "analytics"],
) as daily_dbt_dag:
    dbt_deps = BashOperator(
        task_id="dbt_deps",
        bash_command=dbt_command("deps", include_selectors=False),
        env=DBT_ENV,
    )

    dbt_debug = BashOperator(
        task_id="dbt_debug",
        bash_command=dbt_command("debug", include_selectors=False),
        env=DBT_ENV,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=dbt_command("run"),
        env=DBT_ENV,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=dbt_command("test"),
        env=DBT_ENV,
    )

    dbt_deps >> dbt_debug >> dbt_run >> dbt_test

with DAG(
    dag_id="fresh_segments_dbt_compile_check",
    description="Compile the Fresh Segments dbt project on a lightweight schedule.",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2026, 1, 1),
    schedule="0 */6 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["dbt", "fresh_segments", "validation"],
) as compile_check_dag:
    BashOperator(
        task_id="dbt_compile",
        bash_command=dbt_command("compile --target-path airflow_compile_target --no-partial-parse"),
        env=DBT_ENV,
    )
