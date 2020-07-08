fn main() {
    // create a new empty string
    let s = String::new();
    println!("Value of s: {}", s);

    // create a string from an existing var
    let p = "this is a test".to_string();
    println!("Value of p: {}", p);

    // create a string from another var
    let mut u = String::from("this is a test");
    println!("Value of u: {}", u);

    // append to a string
    u.push_str(", and this is also a test");
    println!("Value of new u: {}", u);

    // append a char to a String
    u.push('x');
    println!("And this is new new u: {}", u);

    // add two strings together
    // this requires using a reference based on the `add`
    // function: fn add(self, s: &str) -> String { ... }
    // and the first component of the addition is no longer
    // valid as the `add` function claimed ownership
    let s1 = String::from("Hello, ");
    let s2 = String::from("World!");
    let s3 = s1 + &s2;
    println!("Value of s3: {}", s3);

    // concatenate multiple strings (easier)
    let t1 = String::from("tic");
    let t2 = String::from("tac");
    let t3 = String::from("toe");
    let t = format!("{}-{}-{}", t1, t2, t3);
    println!("Value of t: {}", t);

    // slice string - note that this range MUST match the number
    // of bytes for a character in the UTF-8 encoded String, or
    // else Rust will complain
    let hello = "Hello";
    let v = &hello[0..1];
    println!("Value of v: {}", v);

    // iterate over a String characters
    for c in hello.chars() {
        println!("Character: {}", c);
    }

    // iterate over String bytes
    for b in hello.bytes() {
        println!("Byte: {}", b);
    }
}
