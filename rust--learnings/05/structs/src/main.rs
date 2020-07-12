// define a struct with associated fields
// annotation allows for non-referenced fields
#[allow(dead_code)]
struct User {
    username: String,
    email: String,
    sign_in_count: u64,
    active: bool,
}

fn main() {

    // instantiate an immutable instance of the struct
    let user1 = User {
        email: String::from("someone@example.com"),
        username: String::from("someusername123"),
        active: true,
        sign_in_count: 1,
    };
    println!("User 1 email: {}", user1.email);

    // instantiate a mutable instance of the struct
    // and then modify the email after the fact
    let mut user2 = User {
        email: String::from("someone@example.com"),
        username: String::from("someusername123"),
        active: true,
        sign_in_count: 1,
    };
    user2.email = String::from("test@test.com");
    println!("User 2 email: {}", user2.email);

    // can use shorthand notation to assign values when
    // wrapped in a function since the variables match
    // the struct variable names exactly
    let email = String::from("test2@test.com");
    let username = String::from("someuser");
    let user3 = build_user(email, username);
    println!("User 3 email: {}", user3.email);

    // re-use existing instance to create a new instance
    // known as struct update syntax, indicating the rest
    // of the unassigned fields should come over from the
    // intended copy instance
    let user4 = User {
        username: String::from("someotheruser"),
        ..user3
    };
    println!("User 4 email copied: {}", user4.email);

    // create a tuple struct
    struct Color(i32, i32, i32);
    let white = Color(255, 255, 255);
    println!("Red component of color: {}", white.0);
}

fn build_user(email: String, username: String) -> User {
    // don't need to do `email: email,` because the variable
    // matches the struct variable exactly
    User {
        email,
        username,
        active: true,
        sign_in_count: 1,
    }
}
