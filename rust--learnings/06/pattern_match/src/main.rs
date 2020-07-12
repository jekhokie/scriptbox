fn main() {
    // demonstrate the Option<T> and Some
    let five = Some(5);
    let six = plus_one(five);
    let none = plus_one(None);

    println!("Five: {:?}", five);
    println!("Six: {:?}", six);
    println!("None: {:?}", none);

    // simpler syntax if you want to do something with
    // only one value (one pattern match)
    let some_value = Some(3);
    if let Some(3) = some_value {
        println!("Found 3");
    }

    // same as if let but includes an else
    if let Some(2) = some_value {
        println!("Found 2");
    } else {
        println!("Found something different");
    }
}

fn plus_one(x: Option<i32>) -> Option<i32> {
    // if no value, return none, otherwise return
    // the addition of the value plus one
    match x {
        None => None,
        Some(i) => Some(i + 1),
    }
}
