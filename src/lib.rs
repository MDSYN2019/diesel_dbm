pub mod migrations;
pub mod models;
pub mod schema;

use diesel::prelude::*;
use dotenvy::dotenv;
use std::env;

use crate::models::{NewPost, Post};

pub fn establish_connection() -> PgConnection {
    dotenv().ok();

    let database_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set");
    PgConnection::establish(&database_url)
        .unwrap_or_else(|_| panic!("Error connecting to {}", database_url))
}

pub fn list_posts(conn: &mut PgConnection) -> QueryResult<Vec<Post>> {
    use crate::schema::posts::dsl::*;

    posts
        .order(id.desc())
        .select(Post::as_select())
        .load::<Post>(conn)
}

pub fn create_post<'a>(
    conn: &mut PgConnection,
    post_title: &'a str,
    post_body: &'a str,
) -> QueryResult<Post> {
    use crate::schema::posts::dsl::*;

    let new_post = NewPost {
        title: post_title,
        body: post_body,
        published: false,
    };

    diesel::insert_into(posts)
        .values(&new_post)
        .returning(Post::as_returning())
        .get_result(conn)
}

pub fn add(left: u64, right: u64) -> u64 {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
