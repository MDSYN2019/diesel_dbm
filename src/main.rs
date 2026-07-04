mod db;

fn main() {
    let mut conn = dbn::establish_connection();
    println!("Connected to the database sucessfully");
}
