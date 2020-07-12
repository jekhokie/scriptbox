fn main() {
    // string literal - fast, stored on stack, immutable
    let a = "some string";
    println!("String a: {}", a);

    // `String` type - slower, stored in heap, mutable
    let mut s = String::from("hello");
    s.push_str(", world!");
    println!("String s: {}", s);

    // `String` type puts data on the stack:
    // 1. Pointer to heap that holds content of string
    // 2. Length (how much currently being used)
    // 3. Capacity (total memory that has been received from OS)
    // In the below case, `s1` is "moved" to `s2` (shallow copy) and
    // `s1` is invalidated - attempting to use `s1` after the move
    // would result in a compiler error
    let s1 = String::from("Shallow copy");
    let s2 = s1;
    println!("{}", s2);

    // deep copy operation - this is an expensive operation
    let x1 = String::from("Deep copy");
    let x2 = x1.clone();
    println!("x1 = {}, x2 = {}", x1, x2);

    // makes a shallow copy/loses scope of b and cannot re-use here
    let b = String::from("hello world");
    takes_ownership(b);

    // makes a copy (stack operation only)
    let q = 5;
    makes_copy(q);

    // grants ownership (out of scope from function once assigned here)
    let w = gives_ownership();
    println!("Ownership given: {}", w);

    // takes and then gives ownership back
    let e = takes_and_gives_back(w);
    println!("Value of given back: {}", e);

    // allows use but does not take ownership
    let r1 = String::from("hello");
    let (r2, len) = calculate_length(r1);
    println!("Length of r1 '{}' is {}", r2, len);

    // better way to allow using a variable without taking ownership
    // by using a reference pointer (pointer to the stack pointer of
    // the original value, which is stored in heap) - this prevents
    // the original value from going out of scope once the called
    // function exits (only the pointer to the pointer goes out of scope)
    let y1 = String::from("hello");
    let len = calculate_length_reference(&y1);
    println!("Length of y1 '{}' is {}", y1, len);

    // can use mutable references to enable manipulation of data via
    // using reference pointers - can only manipulate the var via one
    // functionality within this scope
    let mut p1 = String::from("hello");
    change_mutable(&mut p1);
    println!("Modified mutable reference: {}", p1);

    // can accommodate mutable references to same var by adding
    // curly brackets which creates separate scope
    let mut p2 = String::from("hello");
    {
        let m1 = &mut p2;
        println!("Mutable m1: {}", m1);
    }
    let m2 = &mut p2;
    println!("Mutable m2: {}", m2);
}
// at this point...`drop` is called, meaning:
// memory is freed for the `a` and `s` variables (from stack
// and heap, respectively) since they are now out of scope
// drop sequence is in reverse (LIFO) only for valid/in-scope vars

fn takes_ownership(some_string: String) {
    println!("Ownership: {}", some_string);
}

fn makes_copy(some_integer: i32) {
    println!("Copy: {}", some_integer);
}

fn gives_ownership() -> String {
    let some_string = String::from("hello");
    some_string
}

fn takes_and_gives_back(a_string: String) -> String {
    a_string
}

fn calculate_length(s: String) -> (String, usize) {
    let length = s.len();
    (s, length)
}

fn calculate_length_reference(s: &String) -> usize {
    s.len()
}

fn change_mutable(s: &mut String) {
    s.push_str(" appended");
}
