// define a basic enum
enum IpAddrKind {
    V4,
    V6
}

#[allow(dead_code)]
struct IpAddr {
    kind: IpAddrKind,
    address: String,
}

// define more succinct enum that does not
// require a struct
#[derive(Debug)]
#[allow(dead_code)]
enum IpAddrAdvanced {
    V4(u8, u8, u8, u8),
    V6(String),
}

// can create method on enum
impl IpAddr {
    fn get_ping(&self) -> String {
        String::from("Ran a ping test!")
    }
}

fn main() {
    // basic use of enum
    let home = IpAddr {
        kind: IpAddrKind::V4,
        address: String::from("10.128.0.10"),
    };

    let loopback = IpAddr {
        kind: IpAddrKind::V6,
        address: String::from("::1"),
    };

    println!("Home address: {}", home.address);
    println!("Loopback address: {}", loopback.address);

    // more simplistic use of enum that does not
    // require usage of a struct to capture
    // additional fields
    let home2 = IpAddrAdvanced::V4(192, 168, 1, 15);
    println!("Home Address: {:?}", home2);

    // run the enum method
    println!("Ping test: {}", home.get_ping());

    // examples of using Option values to hold
    // number types and string types
    //  let some_number = Some(5);
    //  let some_string = Some("a string");
    //  let absent_number: Option<i32> = None;
}
