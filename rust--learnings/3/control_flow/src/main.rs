fn main() {
    let x = 3;

    // simple less/greater
    if x < 5 {
        println!("condition was true - x was less than 5");
    } else {
        println!("condition was false - x was greater than 5");
    }

    // equality
    if x != 3 {
        println!("x is not equal to 3");
    } else {
        println!("x is equal to 3");
    }

    // multiple checks - mod operation
    // likely better to use a `match` here for performance/quality
    let y = 6;
    if y % 4 == 0 {
        println!("y is divisible by 4");
    } else if y % 3 == 0 {
        println!("y is divisible by 3");
    } else if y % 2 == 0 {
        println!("y is divisible by 2");
    } else {
        println!("y is not divisible by 4, 3, or 2");
    }

    // using `if` with `let`
    let condition = true;
    let z = if condition { 5 } else { 6 };
    println!("The value of z is: {}", z);
}
