"""FastAPI control plane for the Diesel-managed Postgres schema.

Run locally:
    uvicorn streamlit_app.api:app --reload
"""

from __future__ import annotations

import re
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator

from streamlit_app.backend_client import DieselDbClient

IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
SqlType = Literal["VARCHAR(255)", "TEXT", "INTEGER", "BOOLEAN"]


class PostCreate(BaseModel):
    """Request body for creating a demo post."""

    title: str = Field(min_length=1, max_length=255)
    body: str = Field(min_length=1)


class ColumnDefinition(BaseModel):
    """Column input used to generate table DDL."""

    name: str = Field(min_length=1, max_length=63)
    data_type: SqlType
    nullable: bool = True

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return validate_identifier(value, "column name")


class TableDefinition(BaseModel):
    """Request body for generating or applying CREATE TABLE DDL."""

    table_name: str = Field(min_length=1, max_length=63)
    columns: list[ColumnDefinition] = Field(min_length=1)

    @field_validator("table_name")
    @classmethod
    def validate_table_name(cls, value: str) -> str:
        return validate_identifier(value, "table name")


class DdlRequest(BaseModel):
    """Request body for executing SQL DDL."""

    sql: str = Field(min_length=1)


class DdlResponse(BaseModel):
    """Response body that returns generated SQL."""

    sql: str


app = FastAPI(
    title="Diesel DBM API",
    summary="HTTP control plane for schema inspection, table prototyping, and posts.",
    version="0.1.0",
)


def validate_identifier(value: str, label: str) -> str:
    """Accept only simple unquoted SQL identifiers for generated DDL."""
    cleaned = value.strip()
    if not IDENTIFIER_PATTERN.fullmatch(cleaned):
        raise ValueError(f"{label} must be a simple SQL identifier")
    return cleaned


def get_client() -> DieselDbClient:
    """Build a DB client from environment for each request."""
    try:
        return DieselDbClient.from_env()
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc


def build_create_table_ddl(definition: TableDefinition) -> str:
    """Generate a small CREATE TABLE statement from validated API input."""
    column_lines = ["    id SERIAL PRIMARY KEY"]
    for column in definition.columns:
        nullability = "" if column.nullable else " NOT NULL"
        column_lines.append(f"    {column.name} {column.data_type}{nullability}")

    columns_sql = ",\n".join(column_lines)
    return f"CREATE TABLE IF NOT EXISTS {definition.table_name} (\n{columns_sql}\n);"


@app.get("/health")
def health(client: DieselDbClient = Depends(get_client)) -> dict[str, str]:
    """Check database connectivity."""
    return client.health()


@app.get("/posts")
def list_posts(client: DieselDbClient = Depends(get_client)) -> list[dict]:
    """List demo posts in reverse id order."""
    return client.list_posts()


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, client: DieselDbClient = Depends(get_client)) -> dict:
    """Create a demo post."""
    return client.create_post(title=payload.title, body=payload.body)


@app.get("/schema/{schema_name}")
def introspect_schema(schema_name: str = "public", client: DieselDbClient = Depends(get_client)) -> list[dict]:
    """Return table and column metadata for one schema."""
    try:
        schema = validate_identifier(schema_name, "schema name")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return client.introspect_schema(schema=schema)


@app.post("/ddl/generate", response_model=DdlResponse)
def generate_ddl(definition: TableDefinition) -> DdlResponse:
    """Generate CREATE TABLE SQL without applying it."""
    return DdlResponse(sql=build_create_table_ddl(definition))


@app.post("/ddl/apply", status_code=status.HTTP_204_NO_CONTENT)
def apply_ddl(payload: DdlRequest, client: DieselDbClient = Depends(get_client)) -> None:
    """Apply SQL DDL in a single database transaction."""
    client.apply_ddl(payload.sql)
