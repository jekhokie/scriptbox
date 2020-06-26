fn main() {
    println!("Inside main!");

    // call another function
    another_function(5, 6);

    // create an expression
    // do *NOT* put an ending semicolon in an expression (`x+1` below)
    // otherwise it will simply be a statement and return no value
    let y = {
        let x = 3;
        x + 1
    };
    println!("Value of y after expression evaluation: {}", y);

    // call a function with a return value
    // and assign the value
    let z = plus_one(5);
    println!("Value of return from plus_one() function: {}", z);
}

// a function with parameters
fn another_function(x: i32, y: i32) {
    println!("Inside another function!");
    println!("Value of x,y: {},{}", x, y);
}

// create a function with a return value
// where we have to define the type
fn plus_one(a: i32) -> i32 {
    a + 1
}
