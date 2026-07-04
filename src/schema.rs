// @generated automatically by Diesel CLI.

pub mod analytics_analytics {
    diesel::table! {
        analytics_analytics.dim_interest (interest_id) {
            interest_id -> Int4,
            interest_name -> Nullable<Text>,
            interest_summary -> Nullable<Text>,
            created_at -> Nullable<Timestamp>,
            last_modified -> Nullable<Timestamp>,
        }
    }

    diesel::table! {
        analytics_analytics.fct_interest_monthly_performance (month_start_date, interest_id) {
            month_start_date -> Date,
            year_number -> Nullable<Int4>,
            month_number -> Nullable<Int4>,
            interest_id -> Int4,
            interest_name -> Nullable<Text>,
            interest_summary -> Nullable<Text>,
            composition -> Nullable<Numeric>,
            index_value -> Nullable<Numeric>,
            ranking -> Nullable<Int4>,
            percentile_ranking -> Nullable<Numeric>,
            ranking_bucket -> Nullable<Text>,
        }
    }

    diesel::allow_tables_to_appear_in_same_query!(dim_interest, fct_interest_monthly_performance,);
}
