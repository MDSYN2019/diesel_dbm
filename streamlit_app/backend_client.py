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
