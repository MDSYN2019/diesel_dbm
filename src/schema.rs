// @generated automatically by Diesel CLI.

diesel::table! {
    posts (id) {
        id -> Int4,
        title -> Varchar,
        body -> Text,
        published -> Bool,
    }
}

diesel::table! {
    use diesel::sql_types::Json;

    json_data (raw_data) {
        raw_data -> Json,
    }
}

diesel::table! {
    interest_map (id) {
        id -> Int4,
        interest_name -> Text,
        interest_summary -> Text,
        created_at -> Timestamp,
        last_modified -> Timestamp,
    }
}

diesel::table! {
    // Composite key is used only so Diesel can map records.
    interest_metrics (_month, _year, month_year, interest_id, ranking) {
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

diesel::allow_tables_to_appear_in_same_query!(
    posts,
    json_data,
    interest_map,
    interest_metrics,
);
