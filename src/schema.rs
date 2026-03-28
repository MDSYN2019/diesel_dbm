// @generated automatically by Diesel CLI.

diesel::table! {
    posts (id) {
        id -> Int4,
        title -> Varchar,
        body -> Text,
        published -> Bool,
    }
}

// ---

diesel::table! {
    use diesel::sql_types::*;
    use diesel::sql_types::Json;

    fresh_segments.json_data (raw_data) {
        raw_data -> Json,
    }
}

diesel::table! {
    use diesel::sql_types::*;

    fresh_segments.interest_map (id) {
        id -> Int4,
        interest_name -> Text,
        interest_summary -> Text,
        created_at -> Timestamp,
        last_modified -> Timestamp,
    }
}

diesel::table! {
    use diesel::sql_types::*;

    // Your SQL has no real PK; this is only to let Diesel declare the table.
    // Treat this as a read-mostly table unless you add a real PK later.
    fresh_segments.interest_metrics (_month, _year, month_year, interest_id, ranking) {
        _month -> Varchar,
        _year -> Varchar,
        month_year -> Varchar,
        interest_id -> Varchar,
        composition -> Float8,
        index_value -> Float8,
        ranking -> Int4,
        percentile_ranking -> Float8,
    }
}

diesel::joinable!(fresh_segments.interest_metrics -> fresh_segments.interest_map (interest_id));

diesel::allow_tables_to_appear_in_same_query!(
    fresh_segments.json_data,
    fresh_segments.interest_map,
    fresh_segments.interest_metrics,
);
