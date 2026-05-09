use diesel::prelude::*;

#[derive(Queryable, Selectable)]
#[diesel(table_name = crate::schema::posts)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct Post {
    pub id: i32,
    pub title: String,
    pub body: String,
    pub published: bool,
}

#[derive(Insertable)]
#[diesel(table_name = crate::schema::posts)]
pub struct NewPost<'a> {
    pub title: &'a str,
    pub body: &'a str,
    pub published: bool,
}

#[derive(Debug, Clone, Queryable, Selectable)]
#[diesel(table_name = crate::schema::interest_map)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct InterestMap {
    pub id: i32,
    pub interest_name: String,
    pub interest_summary: String,
    pub created_at: std::time::SystemTime,
    pub last_modified: std::time::SystemTime,
}

#[derive(Debug, Clone, Insertable)]
#[diesel(table_name = crate::schema::interest_map)]
pub struct NewInterestMap<'a> {
    pub id: i32,
    pub interest_name: &'a str,
    pub interest_summary: &'a str,
    pub created_at: std::time::SystemTime,
    pub last_modified: std::time::SystemTime,
}

#[derive(Debug, Clone, Queryable, Selectable)]
#[diesel(table_name = crate::schema::interest_metrics)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct InterestMetric {
    pub _month: String,
    pub _year: String,
    pub month_year: String,
    pub interest_id: String,
    pub composition: f64,
    pub index_value: f64,
    pub ranking: i32,
    pub percentile_ranking: f64,
}

#[derive(Debug, Clone, Insertable)]
#[diesel(table_name = crate::schema::interest_metrics)]
pub struct NewInterestMetric<'a> {
    pub _month: &'a str,
    pub _year: &'a str,
    pub month_year: &'a str,
    pub interest_id: &'a str,
    pub composition: f64,
    pub index_value: f64,
    pub ranking: i32,
    pub percentile_ranking: f64,
}
