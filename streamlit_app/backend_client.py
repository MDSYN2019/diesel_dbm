"""Helpers for writing Streamlit features against the Diesel-managed Postgres schema.

This module keeps DB access in one place so future Streamlit functions can be
added without touching connection/query plumbing.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import psycopg
from psycopg.rows import dict_row


@dataclass(frozen=True)
class DieselDbClient:
    """Simple Postgres client that targets the same tables Diesel uses."""

    database_url: str

    @classmethod
    def from_env(cls) -> "DieselDbClient":
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            raise RuntimeError("DATABASE_URL must be set")
        return cls(database_url=database_url)

    def health(self) -> dict[str, str]:
        with psycopg.connect(self.database_url) as conn, conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT 'ok' AS status")
            return cur.fetchone() or {"status": "unknown"}

    def list_posts(self) -> list[dict]:
        with psycopg.connect(self.database_url) as conn, conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, title, body, published
                FROM posts
                ORDER BY id DESC
                """
            )
            return list(cur.fetchall())

    def create_post(self, title: str, body: str) -> dict:
        with psycopg.connect(self.database_url) as conn, conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO posts (title, body, published)
                VALUES (%s, %s, FALSE)
                RETURNING id, title, body, published
                """,
                (title, body),
            )
            created = cur.fetchone()
            conn.commit()
            if not created:
                raise RuntimeError("Failed to insert post")
            return created

    def introspect_schema(self, schema: str = "public") -> list[dict]:
        """Return tables/columns metadata for simple data-modeling views."""
        with psycopg.connect(self.database_url) as conn, conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT
                    cols.table_name,
                    cols.ordinal_position,
                    cols.column_name,
                    cols.data_type,
                    cols.is_nullable = 'YES' AS is_nullable,
                    cols.column_default,
                    EXISTS (
                        SELECT 1
                        FROM information_schema.table_constraints tc
                        JOIN information_schema.key_column_usage kcu
                          ON tc.constraint_name = kcu.constraint_name
                         AND tc.table_schema = kcu.table_schema
                        WHERE tc.table_schema = cols.table_schema
                          AND tc.table_name = cols.table_name
                          AND tc.constraint_type = 'PRIMARY KEY'
                          AND kcu.column_name = cols.column_name
                    ) AS is_primary_key
                FROM information_schema.columns cols
                WHERE cols.table_schema = %s
                ORDER BY cols.table_name, cols.ordinal_position
                """,
                (schema,),
            )
            return list(cur.fetchall())

    def apply_ddl(self, sql_script: str) -> None:
        """Execute generated DDL in a single transaction."""
        if not sql_script.strip():
            return
        with psycopg.connect(self.database_url) as conn, conn.cursor() as cur:
            cur.execute(sql_script)
            conn.commit()
