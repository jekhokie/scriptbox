fn main() {
    // define a variable
    // must declare `mut` (mutable) in order for this to compile
    let mut x = 5;
    println!("The value of mutable variable x is: {}", x);
    x = 6;
    println!("The value of adjusted mutable variable x is: {}", x);

    // define a constant
    const MAX_POINTS: u32 = 100_000;
    println!("The value of constant MAX_POINTS is: {}", MAX_POINTS);

    // variable shadowing - should evaluate to 12
    let x = 5;
    let x = x + 1;
    let x = x * 2;
    println!("The shadowed value of x is: {}", x);
}
