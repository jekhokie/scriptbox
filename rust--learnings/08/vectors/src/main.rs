fn main() {
    // one way to initialize
    let v1 = vec![1, 2, 3];
    println!("Value at position 2: {}", v1[2]);

    // another way to initialize
    let mut v2 = Vec::new();
    v2.push(5);
    v2.push(6);
    println!("Value at position 1: {}", v2[1]);

    // ways to access the data
    let val3: &i32 = &v1[2];
    println!("The third element is {}", val3);

    match v1.get(2) {
        Some(val3) => println!("The third element is {}", val3),
        None => println!("There is no third element."),
    }

    // loop over vector read-only (immutable)
    for i in &v2 {
        println!("{}", i);
    }

    // loop over vector and update values (mutable)
    for i in &mut v2 {
        *i += 50;
    }
    for i in &v2 {
        println!("{}", i);
    }
}
